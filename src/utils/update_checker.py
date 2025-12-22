"""
Update Checker Module
Checks for game updates by comparing local version with Firebase
"""

import os
from typing import Optional, Tuple
from src.core.game_logging import get_logger

logger = get_logger(__name__)

# Flag to enable/disable update checks
UPDATE_CHECK_ENABLED = os.environ.get('SIENA_UPDATE_CHECK_ENABLED', 'true').lower() == 'true'


class UpdateChecker:
    """Checks for game updates against Firebase"""

    def __init__(self):
        """Initialize update checker"""
        self.initialized = False
        self.db_ref = None
        self.current_version = self._load_current_version()

        if not UPDATE_CHECK_ENABLED:
            logger.info("Update checking disabled (SIENA_UPDATE_CHECK_ENABLED not set)")
            return

        try:
            import firebase_admin
            from firebase_admin import db

            # Check if Firebase is already initialized
            try:
                firebase_admin.get_app()
                self.initialized = True
                logger.info("Firebase already initialized for update checker")
            except ValueError:
                # Firebase not initialized - update checker will be unavailable
                logger.warning("Firebase not initialized - update checking unavailable")
                return

            # Get reference to version node
            self.db_ref = db.reference('version')
            self.initialized = True
            logger.info(f"Update checker initialized (current version: {self.current_version})")

        except ImportError:
            logger.warning("firebase-admin not installed. Update checking disabled.")
        except Exception as e:
            logger.error(f"Failed to initialize update checker: {e}")

    def _load_current_version(self) -> str:
        """Load current version from VERSION file"""
        try:
            # Handle PyInstaller bundled apps
            import sys
            if hasattr(sys, '_MEIPASS'):
                version_path = os.path.join(sys._MEIPASS, 'VERSION')
            else:
                version_path = 'VERSION'

            if os.path.exists(version_path):
                with open(version_path, 'r') as f:
                    version = f.read().strip()
                    logger.info(f"Loaded version from file: {version}")
                    return version
            else:
                logger.warning(f"VERSION file not found at {version_path}")
                return "1.0.0"
        except Exception as e:
            logger.error(f"Failed to load version: {e}")
            return "1.0.0"

    def is_available(self) -> bool:
        """Check if update checker is available"""
        return self.initialized and self.db_ref is not None

    def check_for_update(self) -> Optional[Tuple[str, str]]:
        """
        Check if a new version is available

        Returns:
            Tuple of (latest_version, download_url) if update available, None otherwise
        """
        if not self.is_available():
            logger.debug("Update checker not available")
            return None

        try:
            # Fetch version info from Firebase
            version_data = self.db_ref.get()

            if not version_data:
                logger.warning("No version data in Firebase")
                return None

            latest_version = version_data.get('latest', self.current_version)
            download_url = version_data.get('download_url', '')
            changelog = version_data.get('changelog', '')

            logger.info(f"Latest version: {latest_version}, Current version: {self.current_version}")

            # Compare versions
            if self._is_newer_version(latest_version, self.current_version):
                logger.info(f"Update available: {latest_version}")
                return (latest_version, download_url, changelog)
            else:
                logger.debug("No update available")
                return None

        except Exception as e:
            logger.error(f"Failed to check for update: {e}")
            return None

    def _is_newer_version(self, latest: str, current: str) -> bool:
        """
        Compare semantic versions (e.g., "1.2.3")

        Args:
            latest: Latest version string
            current: Current version string

        Returns:
            True if latest is newer than current
        """
        try:
            # Parse semantic versions
            latest_parts = [int(x) for x in latest.split('.')]
            current_parts = [int(x) for x in current.split('.')]

            # Pad shorter version with zeros
            while len(latest_parts) < 3:
                latest_parts.append(0)
            while len(current_parts) < 3:
                current_parts.append(0)

            # Compare major, minor, patch
            for l, c in zip(latest_parts, current_parts):
                if l > c:
                    return True
                elif l < c:
                    return False

            return False  # Versions are equal

        except Exception as e:
            logger.error(f"Failed to compare versions: {e}")
            return False

    def get_current_version(self) -> str:
        """Get the current game version"""
        return self.current_version


# Singleton instance
_update_checker = None

def get_update_checker() -> UpdateChecker:
    """Get the singleton UpdateChecker instance"""
    global _update_checker
    if _update_checker is None:
        _update_checker = UpdateChecker()
    return _update_checker
