# Version Management Guide

This guide explains how to manage versions and push updates to players.

## Overview

The game includes an automatic update checker that:
- Checks Firebase for the latest version on game launch
- Displays a notification banner if an update is available
- Opens the download link when players click the notification

## How to Push an Update

When you make changes to the game and want to distribute them to players, follow these steps:

### 1. Update the VERSION File

Edit the `VERSION` file in the root directory:

```bash
# Before (old version)
1.0.1

# After (new version)
1.0.2
```

Use [Semantic Versioning](https://semver.org/):
- **MAJOR.MINOR.PATCH** (e.g., 1.0.2)
  - **MAJOR**: Breaking changes or complete rewrites (e.g., 2.0.0)
  - **MINOR**: New features, new levels (e.g., 1.1.0)
  - **PATCH**: Bug fixes, small tweaks (e.g., 1.0.2)

### 2. Update the CHANGELOG

Add your changes to `CHANGELOG.md`:

```markdown
## [1.0.2] - 2025-12-21

### Added
- New Level 5 with ice physics

### Fixed
- Fixed jump bug on slopes
- Improved collision detection

### Changed
- Increased coin spawn rate in Level 2
```

Categories:
- **Added**: New features
- **Changed**: Changes to existing features
- **Fixed**: Bug fixes
- **Removed**: Removed features

### 3. Rebuild the Distribution

#### For Mac:

```bash
./venv/bin/pyinstaller siena_snowy_adventure.spec

# Create installer package
cd dist
zip -r SienaSnowyAdventure-Mac.zip SienaSnowyAdventure.app INSTALL.command README.txt
```

#### For Windows (requires Windows machine):

```bash
pyinstaller siena_snowy_adventure_windows.spec

# Create installer package
cd dist
# Zip the folder or create installer
```

### 4. Upload to Google Drive

1. Upload the new `.zip` file to your Google Drive folder
2. Right-click the file → Share → Copy link
3. Make sure the link is set to "Anyone with the link can view"
4. Copy the shareable link (you'll need this for step 5)

### 5. Update Firebase Version Info

You need to update the Firebase Realtime Database with the new version info:

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select your project
3. Go to **Realtime Database** in the left sidebar
4. Find or create the `version` node
5. Set the following values:

```json
{
  "version": {
    "latest": "1.0.2",
    "download_url": "https://drive.google.com/file/d/YOUR_FILE_ID/view?usp=sharing",
    "changelog": "Added Level 5, fixed jump bug, improved collision"
  }
}
```

**Important**: Make sure the `download_url` is the shareable Google Drive link from step 4.

### 6. Test the Update

1. Install the OLD version on a test machine
2. Launch the game
3. You should see the update notification banner at the top
4. Click the banner to verify it opens the download link correctly

## Firebase Database Structure

Your Firebase Realtime Database should have this structure:

```
siena_snowy_adventure/
├── leaderboards/
│   ├── level_1/
│   ├── level_2/
│   ├── level_3/
│   └── level_4/
└── version/
    ├── latest: "1.0.2"
    ├── download_url: "https://drive.google.com/..."
    └── changelog: "Bug fixes and improvements"
```

## How the Update System Works

### On Game Launch:

1. Game reads `VERSION` file from bundle (e.g., "1.0.1")
2. Game connects to Firebase and reads `/version/latest`
3. If Firebase version > local version:
   - Show blue notification banner at top of title screen
   - Banner text: "UPDATE AVAILABLE: v1.0.2 - Click to Download"
4. When player clicks banner:
   - Opens `download_url` in their default browser
   - Player downloads new version manually

### Version Comparison:

The system uses semantic version comparison:
```
1.0.1 < 1.0.2  ✓ Shows update
1.0.2 < 1.1.0  ✓ Shows update
1.1.0 < 2.0.0  ✓ Shows update
1.0.2 = 1.0.2  ✗ No update
1.0.3 > 1.0.2  ✗ No update (player has newer version)
```

## Disabling Update Checks

If you need to disable update checking (for testing or offline use), set this environment variable:

```bash
# In .env file
SIENA_UPDATE_CHECK_ENABLED=false
```

Or temporarily for a single run:

```bash
export SIENA_UPDATE_CHECK_ENABLED=false
python main.py
```

## Troubleshooting

### Update banner doesn't appear

1. **Check Firebase connection**: Verify the game shows "ONLINE" status
2. **Check Firebase database**: Verify `/version/latest` exists and has correct value
3. **Check version format**: Must be semantic version (e.g., "1.0.2", not "v1.0.2")
4. **Check logs**: Look in game logs for "Update available" messages

### Update banner shows but link doesn't work

1. **Check download_url**: Verify it's a valid shareable Google Drive link
2. **Check permissions**: Make sure link is set to "Anyone with the link"
3. **Test link manually**: Open the link in a browser to verify it works

### Players report not seeing updates

1. **Old version cached**: They might be running an old cached version
   - Mac: Delete app and re-extract from zip
   - Windows: Delete app and reinstall
2. **Firewall blocking Firebase**: Check if their firewall blocks Firebase
3. **Offline mode**: If they're offline, update check won't work

## Quick Reference

### Creating a New Update

```bash
# 1. Update version
echo "1.0.2" > VERSION

# 2. Update changelog
# Edit CHANGELOG.md manually

# 3. Rebuild
./venv/bin/pyinstaller siena_snowy_adventure.spec
cd dist
zip -r SienaSnowyAdventure-Mac.zip SienaSnowyAdventure.app INSTALL.command

# 4. Upload to Google Drive
# (Manual step)

# 5. Update Firebase
# Go to Firebase Console → Realtime Database → version node
# Set: latest="1.0.2", download_url="...", changelog="..."

# 6. Test
# Run old version, verify update banner appears
```

## Example Update Workflow

Let's say you fixed a bug and want to release v1.0.2:

1. **Make your code changes**
   ```bash
   # Fix the bug in your code
   # Test thoroughly
   ```

2. **Update version files**
   ```bash
   # VERSION
   echo "1.0.2" > VERSION

   # CHANGELOG.md - add at the top:
   ## [1.0.2] - 2025-12-22
   ### Fixed
   - Fixed player getting stuck in walls
   ```

3. **Rebuild and package**
   ```bash
   ./venv/bin/pyinstaller siena_snowy_adventure.spec
   cd dist
   zip -r SienaSnowyAdventure-Mac-v1.0.2.zip SienaSnowyAdventure.app INSTALL.command
   ```

4. **Upload to Google Drive**
   - Upload `SienaSnowyAdventure-Mac-v1.0.2.zip`
   - Get shareable link: `https://drive.google.com/file/d/ABC123/view?usp=sharing`

5. **Update Firebase**
   - Go to Firebase Console
   - Update `/version` node:
     ```json
     {
       "latest": "1.0.2",
       "download_url": "https://drive.google.com/file/d/ABC123/view?usp=sharing",
       "changelog": "Fixed player getting stuck in walls"
     }
     ```

6. **Notify players**
   - Send a message: "New update available! Relaunch the game to see the update notification."
   - They'll see the banner when they next launch

Done! Players will automatically see the update notification next time they launch the game.
