"""
Auto-Update Module
Handles downloading and installing game updates from GitHub Releases
"""

import urllib.request
import urllib.error
import ssl
import zipfile
import tempfile
import os
import sys
import subprocess
import shutil
from pathlib import Path
from src.core.game_logging import get_logger

logger = get_logger(__name__)


def _make_request_with_ssl_fallback(url, timeout=30):
    """
    Make an HTTP request with SSL fallback support.
    Tries with verified SSL first, falls back to unverified if certificate issues occur.
    """
    req = urllib.request.Request(url, method='GET')

    # Try with verified SSL first (most secure)
    try:
        ssl_context = ssl.create_default_context()
        return urllib.request.urlopen(req, timeout=timeout, context=ssl_context)
    except ssl.SSLError as e:
        # SSL certificate verification failed, try with unverified context
        logger.warning(f"SSL verification failed ({e}), retrying with unverified context")
        ssl_context = ssl._create_unverified_context()
        return urllib.request.urlopen(req, timeout=timeout, context=ssl_context)
    except urllib.error.URLError as e:
        # Check if the URLError was caused by an SSL error
        if isinstance(e.reason, ssl.SSLError):
            logger.warning(f"SSL verification failed ({e.reason}), retrying with unverified context")
            ssl_context = ssl._create_unverified_context()
            return urllib.request.urlopen(req, timeout=timeout, context=ssl_context)
        else:
            raise


class UpdateDownloader:
    """Handles downloading and extracting game updates"""

    def __init__(self):
        self.download_url = None
        self.temp_dir = None
        self.zip_path = None
        self.extracted_path = None
        self.progress_callback = None

    def set_progress_callback(self, callback):
        """
        Set a callback function to receive progress updates

        Args:
            callback: Function that takes (bytes_downloaded, total_bytes) as parameters
        """
        self.progress_callback = callback

    def download_update(self, download_url, expected_size_mb=None, max_retries=3):
        """
        Download update ZIP file from GitHub Releases with retry logic

        Args:
            download_url: Direct URL to the .zip file
            expected_size_mb: Expected file size in MB (for validation)
            max_retries: Maximum number of retry attempts (default: 3)

        Returns:
            bool: True if download successful, False otherwise
        """
        self.download_url = download_url

        # Create temporary directory for download
        self.temp_dir = tempfile.mkdtemp(prefix="siena_update_")
        self.zip_path = os.path.join(self.temp_dir, "update.zip")

        logger.info(f"Starting download from: {download_url}")
        logger.info(f"Temp directory: {self.temp_dir}")

        # Try downloading with retries
        for attempt in range(max_retries):
            try:
                # Download with progress tracking
                def reporthook(block_num, block_size, total_size):
                    if self.progress_callback and total_size > 0:
                        downloaded = block_num * block_size
                        self.progress_callback(downloaded, total_size)

                if attempt > 0:
                    wait_seconds = 2 ** attempt  # Exponential backoff: 2, 4, 8 seconds
                    logger.info(f"Retry attempt {attempt + 1}/{max_retries} after {wait_seconds}s delay...")
                    import time
                    time.sleep(wait_seconds)

                # Download using SSL fallback support
                with _make_request_with_ssl_fallback(download_url) as response:
                    total_size = int(response.headers.get('content-length', 0))
                    downloaded = 0
                    block_size = 8192

                    with open(self.zip_path, 'wb') as f:
                        while True:
                            buffer = response.read(block_size)
                            if not buffer:
                                break
                            f.write(buffer)
                            downloaded += len(buffer)
                            if self.progress_callback and total_size > 0:
                                self.progress_callback(downloaded, total_size)

                # Verify download
                if not os.path.exists(self.zip_path):
                    logger.error("Downloaded file does not exist")
                    if attempt < max_retries - 1:
                        continue  # Retry
                    return False

                file_size_mb = os.path.getsize(self.zip_path) / (1024 * 1024)
                logger.info(f"Download complete: {file_size_mb:.1f} MB")

                # Basic size validation
                if expected_size_mb and abs(file_size_mb - expected_size_mb) > 10:
                    logger.warning(f"File size {file_size_mb:.1f}MB differs from expected {expected_size_mb}MB")

                return True

            except ssl.SSLError as e:
                logger.error(f"SSL error during download (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    continue  # Retry
                return False
            except urllib.error.URLError as e:
                logger.error(f"Network error during download (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    continue  # Retry
                return False
            except Exception as e:
                logger.error(f"Unexpected error during download (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    continue  # Retry
                return False

        return False

    def extract_update(self):
        """
        Extract the downloaded ZIP file

        Returns:
            bool: True if extraction successful, False otherwise
        """
        if not self.zip_path or not os.path.exists(self.zip_path):
            logger.error("No ZIP file to extract")
            return False

        try:
            logger.info("Extracting update...")

            # Create extraction directory
            extract_dir = os.path.join(self.temp_dir, "extracted")
            os.makedirs(extract_dir, exist_ok=True)

            # Extract ZIP
            with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)

            # Find the .app bundle
            app_name = "SienaSnowyAdventure.app"
            app_path = os.path.join(extract_dir, app_name)

            if not os.path.exists(app_path):
                logger.error(f"Could not find {app_name} in extracted files")
                return False

            self.extracted_path = app_path
            logger.info(f"Extraction complete: {app_path}")
            return True

        except zipfile.BadZipFile as e:
            logger.error(f"Corrupted ZIP file: {e}")
            return False
        except Exception as e:
            logger.error(f"Error during extraction: {e}")
            return False

    def get_current_app_path(self):
        """
        Get the path to the currently running .app bundle

        Returns:
            str: Path to current .app bundle, or None if not running as app
        """
        if getattr(sys, 'frozen', False):
            # Running as PyInstaller bundle
            bundle_dir = sys._MEIPASS
            # Navigate up to find .app bundle
            # Path is typically: MyApp.app/Contents/MacOS/
            current = Path(bundle_dir)
            while current.parent != current:
                if current.suffix == '.app':
                    return str(current)
                current = current.parent

        # Not running as a bundle (development mode)
        return None

    def launch_installer(self):
        """
        Launch the update installer script and quit the current app

        Returns:
            bool: True if installer launched successfully
        """
        if not self.extracted_path:
            logger.error("No extracted update to install")
            return False

        current_app = self.get_current_app_path()
        if not current_app:
            logger.error("Not running as a .app bundle - cannot auto-update")
            logger.info("In development mode, manual update required")
            return False

        try:
            # Create update installer script
            installer_script = self._create_installer_script(
                old_app=current_app,
                new_app=self.extracted_path
            )

            if not installer_script:
                return False

            logger.info(f"Launching installer: {installer_script}")

            # Launch installer in detached process with nohup for better Finder compatibility
            # Redirect stdin/stdout/stderr to avoid blocking
            subprocess.Popen([
                '/usr/bin/nohup',
                '/bin/bash',
                installer_script
            ],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
            cwd=os.path.expanduser('~'))

            logger.info("Installer launched, quitting application...")
            return True

        except Exception as e:
            logger.error(f"Error launching installer: {e}")
            return False

    def _create_installer_script(self, old_app, new_app):
        """
        Create a shell script to replace the old app with the new one

        Args:
            old_app: Path to current .app bundle
            new_app: Path to new .app bundle

        Returns:
            str: Path to installer script, or None if creation failed
        """
        try:
            script_path = os.path.join(self.temp_dir, "install_update.sh")

            script_content = f'''#!/bin/bash
# Auto-generated update installer for Siena's Snowy Adventure

OLD_APP="{old_app}"
NEW_APP="{new_app}"
TARGET_DIR="$(dirname "$OLD_APP")"
TARGET_NAME="$(basename "$OLD_APP")"

# Wait for main app to quit
echo "Waiting for application to quit..."
sleep 3

# Wait for the process to actually terminate (check for up to 10 seconds)
APP_NAME="SienaSnowyAdventure"
for i in {{1..10}}; do
    if ! pgrep -x "$APP_NAME" > /dev/null; then
        echo "Application has quit"
        break
    fi
    echo "Waiting for $APP_NAME to quit... ($i/10)"
    sleep 1
done

# Force kill if still running
if pgrep -x "$APP_NAME" > /dev/null; then
    echo "Forcing application to quit..."
    pkill -9 "$APP_NAME"
    sleep 1
fi

# Verify old app exists
if [ ! -d "$OLD_APP" ]; then
    echo "ERROR: Old app not found at $OLD_APP"
    exit 1
fi

# Verify new app exists
if [ ! -d "$NEW_APP" ]; then
    echo "ERROR: New app not found at $NEW_APP"
    exit 1
fi

# Remove old app
echo "Removing old version..."
rm -rf "$OLD_APP"

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to remove old app"
    exit 1
fi

# If the target name has " 2" or similar, also try to remove the base name
# This handles cases where macOS renamed the file
BASE_NAME="SienaSnowyAdventure.app"
if [ "$TARGET_NAME" != "$BASE_NAME" ]; then
    BASE_PATH="$TARGET_DIR/$BASE_NAME"
    if [ -d "$BASE_PATH" ]; then
        echo "Removing existing $BASE_NAME..."
        rm -rf "$BASE_PATH"
    fi
fi

# Copy new app to target location using rsync to preserve permissions
echo "Installing new version..."
rsync -a "$NEW_APP" "$TARGET_DIR/"

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install new app"
    exit 1
fi

# The installed app will always have the base name (rsync copies the source name)
INSTALLED_APP="$TARGET_DIR/$BASE_NAME"

# Ensure the main executable has execute permission
echo "Setting executable permissions..."
chmod +x "$INSTALLED_APP/Contents/MacOS/"*

# Verify installation
if [ ! -d "$INSTALLED_APP" ]; then
    echo "ERROR: New app not found after installation at $INSTALLED_APP"
    exit 1
fi

echo ""
echo "✅ Update installed successfully!"
echo ""

# Clear macOS Launch Services cache to ensure new version is recognized
echo "Clearing Launch Services cache..."
/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister -kill -r -domain local -domain system -domain user

# Wait a moment for cache to clear
sleep 2

# Launch new version using macOS 'open' command (more reliable than direct exec)
echo "Launching new version..."
open "$INSTALLED_APP"

# Clean up temp directory (after a delay)
sleep 2
TEMP_DIR="{self.temp_dir}"
if [ -d "$TEMP_DIR" ]; then
    rm -rf "$TEMP_DIR"
    echo "Cleaned up temporary files"
fi

echo "Update complete!"
'''

            # Write script to file
            with open(script_path, 'w') as f:
                f.write(script_content)

            # Make script executable
            os.chmod(script_path, 0o755)

            logger.info(f"Created installer script: {script_path}")
            return script_path

        except Exception as e:
            logger.error(f"Error creating installer script: {e}")
            return None

    def cleanup(self):
        """Clean up temporary files"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            try:
                shutil.rmtree(self.temp_dir)
                logger.info("Cleaned up temporary files")
            except Exception as e:
                logger.warning(f"Could not clean up temp directory: {e}")

    def cancel_download(self):
        """Cancel an in-progress download"""
        # Note: urllib.request.urlretrieve doesn't support cancellation
        # This is a limitation we'll document
        logger.info("Download cancellation requested")
        self.cleanup()


def format_size(bytes_size):
    """
    Format bytes as human-readable size

    Args:
        bytes_size: Size in bytes

    Returns:
        str: Formatted size (e.g., "15.3 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.1f} TB"


def calculate_progress_percent(downloaded, total):
    """
    Calculate download progress percentage

    Args:
        downloaded: Bytes downloaded
        total: Total bytes

    Returns:
        int: Progress percentage (0-100)
    """
    if total <= 0:
        return 0
    return min(100, int((downloaded / total) * 100))
