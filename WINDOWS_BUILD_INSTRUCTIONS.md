# Windows Build Instructions

This guide explains how to build and release the Windows version of Siena's Snowy Adventure.

## Prerequisites

You need access to a Windows 10 or Windows 11 machine with:
- Python 3.10 or higher installed
- Git installed
- Internet connection

## Step 1: Setup Windows Build Environment

1. **Clone the repository on Windows:**
   ```cmd
   git clone https://github.com/18drider360/siena_snowy_adventure.git
   cd siena_snowy_adventure
   ```

2. **Create virtual environment:**
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```cmd
   pip install -r requirements.txt
   ```

4. **Verify files are present:**
   - Check that `assets/icon.ico` exists
   - Check that `siena_snowy_adventure_windows.spec` exists
   - Check that `build_windows.bat` exists

## Step 2: Build the Windows Executable

1. **Run the build script:**
   ```cmd
   build_windows.bat
   ```

2. **Wait for build to complete** (may take 2-5 minutes)

3. **Verify the build:**
   - Check that `dist\SienaSnowyAdventure\SienaSnowyAdventure.exe` exists
   - Check that `dist\SienaSnowyAdventure-Windows-v1.2.7.zip` exists

## Step 3: Test the Build

1. **Test the executable:**
   ```cmd
   dist\SienaSnowyAdventure\SienaSnowyAdventure.exe
   ```

2. **Verify game functionality:**
   - [ ] Game launches without console window
   - [ ] Title screen displays correctly
   - [ ] Can navigate menus with keyboard
   - [ ] Can start and play level 1
   - [ ] Audio works (music and sound effects)
   - [ ] No "Check for Updates" button (disabled on Windows)
   - [ ] Game saves progress
   - [ ] Game exits cleanly

3. **Test on clean Windows VM** (if possible):
   - Extract ZIP on a Windows machine without Python
   - Verify no missing DLL errors
   - Check that game runs without admin rights

## Step 4: Create GitHub Release

### Option A: Using GitHub CLI (gh)

1. **Ensure you're on the main branch with latest changes:**
   ```cmd
   git checkout main
   git pull origin main
   ```

2. **Create the release:**
   ```cmd
   gh release create v1.2.7 ^
     dist\SienaSnowyAdventure-Windows-v1.2.7.zip ^
     --title "v1.2.7 - Windows Release" ^
     --notes "Windows version of Siena's Snowy Adventure.

   ## What's New
   - Initial Windows release
   - Full gameplay support
   - Local and online scoreboards
   - Manual updates (auto-updates coming later)

   ## Installation
   See QUICK_INSTALL_WINDOWS.md for installation instructions.

   ## Known Issues
   - Auto-updates not yet implemented (manual updates only)
   - Windows Defender may show protection warning (click 'More info' → 'Run anyway')

   ## System Requirements
   - Windows 10/11 (64-bit)
   - 2 GB RAM
   - OpenGL 2.0 compatible graphics"
   ```

### Option B: Using GitHub Web Interface

1. **Navigate to:** https://github.com/18drider360/siena_snowy_adventure/releases/new

2. **Fill in the form:**
   - **Tag:** `v1.2.7`
   - **Title:** `v1.2.7 - Windows Release`
   - **Description:** (copy from Option A above)
   - **Attach files:** Upload `dist\SienaSnowyAdventure-Windows-v1.2.7.zip`

3. **Click "Publish release"**

## Step 5: Update Existing Mac Release (Optional)

If you want to combine Mac and Windows in the same release:

1. **Edit the existing v1.2.7 release**

2. **Upload the Windows ZIP** as an additional asset

3. **Update release notes** to mention both platforms:
   ```markdown
   # v1.2.7 - Multi-Platform Release

   ## Downloads
   - **Mac:** SienaSnowyAdventure-Mac-v1.2.7.zip
   - **Windows:** SienaSnowyAdventure-Windows-v1.2.7.zip

   ## Installation
   - Mac: See QUICK_INSTALL.md
   - Windows: See QUICK_INSTALL_WINDOWS.md
   ```

## Step 6: Verify Installation Scripts Work

After creating the release, test the installation scripts:

1. **Test PowerShell one-liner** (on Windows):
   ```powershell
   iwr -useb https://raw.githubusercontent.com/18drider360/siena_snowy_adventure/main/install_windows.ps1 | iex
   ```

2. **Test batch installer:**
   - Download `install_windows.bat`
   - Double-click to run
   - Verify it downloads and launches the game

3. **Test manual download link:**
   - Visit https://github.com/18drider360/siena_snowy_adventure/releases/latest
   - Verify Windows ZIP is available
   - Download and test

## Troubleshooting Build Issues

### PyInstaller not found
```cmd
pip install pyinstaller
```

### Missing icon.ico
```cmd
REM The icon should exist. If not, you may need to pull latest changes:
git pull origin main
```

### Build fails with import errors
```cmd
REM Ensure all dependencies are installed:
pip install -r requirements.txt --upgrade
```

### Antivirus blocks PyInstaller
- Add exception for Python, PyInstaller, and the project directory
- Temporarily disable real-time protection during build

### ZIP creation fails
```cmd
REM Create ZIP manually:
cd dist
powershell Compress-Archive -Path SienaSnowyAdventure -DestinationPath SienaSnowyAdventure-Windows-v1.2.7.zip -Force
```

## File Checklist

Before releasing, ensure these files are committed:
- [x] `assets/icon.ico` - Windows application icon
- [x] `siena_snowy_adventure_windows.spec` - PyInstaller config
- [x] `build_windows.bat` - Build script
- [x] `install_windows.bat` - User installer (batch)
- [x] `install_windows.ps1` - User installer (PowerShell)
- [x] `QUICK_INSTALL_WINDOWS.md` - User installation guide
- [x] `WINDOWS_README.txt` - User documentation
- [x] `src/rendering/screens/title_screen.py` - Platform detection

## After Release

1. **Announce the release:**
   - Update main README.md if needed
   - Share download links with testers
   - Monitor GitHub Issues for Windows-specific bugs

2. **Update version for next release:**
   - Update `VERSION` file if needed
   - Update version in installer scripts

3. **Collect feedback:**
   - Ask Windows users to test
   - Document any Windows-specific issues
   - Consider implementing auto-updates if demand is high

## Notes

- Windows builds take longer than Mac builds (3-5 minutes vs 1-2 minutes)
- The executable is larger due to bundled Python runtime
- First-time Windows Defender warnings are normal for unsigned applications
- Consider code signing certificate for future releases ($200-400/year)

---

**Build completed successfully?** Proceed to create the GitHub release! 🚀
