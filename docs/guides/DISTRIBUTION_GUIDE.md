# Distribution Guide

This guide explains how to build and distribute Siena's Snowy Adventure.

## Quick Distribution Checklist

Before building a distribution, ensure:

- [ ] All tests pass: `./venv/bin/pytest`
- [ ] Game runs correctly locally: `python main.py`
- [ ] Firebase credentials are in place (`.env` and `firebase-key.json`)
- [ ] Version number updated in `VERSION` file
- [ ] `CHANGELOG.md` updated with changes
- [ ] Git commit created with version tag

---

## Building Distributions

### Mac (.app)

**Requirements:**
- macOS machine
- Python 3.10+
- PyInstaller installed: `pip install pyinstaller`

**Build Steps:**

1. **Clean previous builds:**
   ```bash
   rm -rf build/ dist/
   ```

2. **Build the app:**
   ```bash
   ./venv/bin/pyinstaller siena_snowy_adventure.spec --clean --noconfirm
   ```

3. **Create zip file:**
   ```bash
   cd dist
   zip -r SienaSnowyAdventure-Mac-v1.0.0.zip SienaSnowyAdventure.app
   cd ..
   ```

4. **Test the distribution:**
   - Open `dist/SienaSnowyAdventure.app`
   - Play through at least one level
   - Verify online leaderboard works
   - Submit a test score

**File size:** ~190-230MB

---

### Windows (.exe)

**Requirements:**
- Windows machine (or Windows VM)
- Python 3.10+
- PyInstaller installed: `pip install pyinstaller`

**Build Steps:**

1. **Transfer project to Windows machine:**
   - Copy entire project directory
   - Ensure `.env` and `firebase-key.json` are included

2. **Install dependencies:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   pip install pyinstaller
   ```

3. **Clean previous builds:**
   ```bash
   rmdir /s /q build dist
   ```

4. **Build the exe:**
   ```bash
   pyinstaller siena_snowy_adventure_windows.spec --clean --noconfirm
   ```

5. **Create zip file:**
   ```bash
   cd dist
   powershell Compress-Archive -Path SienaSnowyAdventure -DestinationPath SienaSnowyAdventure-Windows-v1.0.0.zip
   cd ..
   ```

6. **Test the distribution:**
   - Run `dist\SienaSnowyAdventure\SienaSnowyAdventure.exe`
   - Play through at least one level
   - Verify online leaderboard works

**File size:** ~150-200MB

---

## Distributing Updates

### Option 1: Manual Distribution (Current Method)

**Pros:** Simple, full control, no infrastructure needed
**Cons:** Users must manually download and replace

**Process:**

1. **Update version number:**
   ```bash
   echo "1.1.0" > VERSION
   ```

2. **Update CHANGELOG.md** with new features/fixes

3. **Build new distributions** (Mac and Windows)

4. **Upload to cloud storage:**
   - Google Drive / Dropbox / iCloud
   - Use version numbers in filenames: `SienaSnowyAdventure-Mac-v1.1.0.zip`

5. **Notify users:**
   - Send new download link
   - Include changelog in message

**User Update Process:**
- Download new zip file
- Delete old .app/.exe
- Extract and run new version
- Scores/saves are preserved (stored separately)

---

### Option 2: GitHub Releases (Recommended)

**Pros:** Version history, automatic downloads, professional
**Cons:** Requires GitHub account, public repository (or paid private)

**Setup:**

1. **Create GitHub repository:**
   ```bash
   git remote add origin https://github.com/yourusername/siena-snowy-adventure.git
   git push -u origin main
   ```

2. **Create a release:**
   - Go to GitHub repository
   - Click "Releases" → "Create a new release"
   - Tag: `v1.0.0`
   - Title: "Version 1.0.0 - Initial Release"
   - Description: Copy from CHANGELOG.md
   - Attach: `SienaSnowyAdventure-Mac-v1.0.0.zip`
   - Attach: `SienaSnowyAdventure-Windows-v1.0.0.zip`
   - Publish release

3. **Share release link:**
   - `https://github.com/yourusername/siena-snowy-adventure/releases/latest`
   - Always points to latest version

**User Update Process:**
- Visit releases page
- Download latest version for their platform
- Extract and run

---

### Option 3: Auto-Update System (Advanced)

**Pros:** Users get updates automatically, professional
**Cons:** Complex implementation, requires server/hosting

**How it works:**

1. Game checks for updates on launch (via Firebase or API)
2. If new version available, shows "Update Available" dialog
3. Downloads new version in background
4. Installs update and restarts

**Implementation overview:**

1. **Version check endpoint:**
   - Store current version in Firebase: `{"version": "1.1.0", "download_url": "..."}`
   - Game fetches on startup, compares with local `VERSION` file

2. **Download and replace:**
   - Download new zip file
   - Extract to temp directory
   - Replace current executable
   - Restart game

3. **Code changes needed:**
   - Add `src/utils/updater.py` module
   - Modify `main.py` to check for updates
   - Add "Check for Updates" to main menu

**Note:** This is complex and optional. Manual updates work fine for small projects.

---

## Version Tagging with Git

After building each release, tag it in git:

```bash
# Update version
echo "1.1.0" > VERSION

# Commit changes
git add VERSION CHANGELOG.md
git commit -m "Release v1.1.0"

# Create tag
git tag -a v1.1.0 -m "Version 1.1.0 - New Level 5"

# Push to remote (if using GitHub)
git push origin main --tags
```

---

## Security Considerations

### Firebase Credentials in Distribution

**Current approach:** Credentials are bundled in the app

**Security implications:**
- ✅ Users don't need to configure anything
- ❌ Credentials can be extracted from the app bundle
- ✅ Firebase security rules protect against abuse
- ✅ Username filter prevents inappropriate content

**Firebase security rules should include:**
```json
{
  "rules": {
    "leaderboard": {
      ".read": true,
      ".write": "auth == null &&
                 newData.child('username').val().length <= 20 &&
                 newData.child('username').val().length >= 2"
    }
  }
}
```

**Alternative (more secure but complex):**
- Set up backend API server
- App talks to your API
- API talks to Firebase with secure credentials
- Requires hosting (AWS, Heroku, etc.)

For a small game with content filtering, bundled credentials are acceptable.

---

## File Size Optimization

Current distributions are large (~200MB) due to Python + Pygame + dependencies.

**To reduce size:**

1. **Use UPX compression** (already enabled in spec files)

2. **Exclude unused modules:**
   ```python
   # In .spec file
   excludes=['tkinter', 'matplotlib', 'scipy', 'numpy'],
   ```

3. **One-file vs one-folder:**
   - Current: One folder with many files (~200MB)
   - Alternative: Single .exe with everything embedded (~250MB but simpler)
   - Trade-off: Slower startup time vs easier distribution

**To create single-file .exe:**
```python
# Modify exe = EXE(...) in spec file
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,  # Add this
    a.zipfiles,  # Add this
    a.datas,     # Add this
    [],
    exclude_binaries=False,  # Change to False
    name='SienaSnowyAdventure',
    # ... rest stays the same
)

# Remove COLLECT and BUNDLE sections
```

---

## Testing Distributions

Before sharing distributions, test thoroughly:

### Mac Testing:
- [ ] App launches without errors
- [ ] All 4 levels playable
- [ ] Online leaderboard loads and submits scores
- [ ] Local leaderboard shows scores
- [ ] Sound effects and music work
- [ ] Username filter works correctly
- [ ] Save system preserves progress
- [ ] No console window appears
- [ ] App works on fresh Mac (not just development machine)

### Windows Testing:
- [ ] Same as Mac testing
- [ ] Test on Windows 10 and Windows 11
- [ ] Test with antivirus enabled (may flag as suspicious)

### Common Issues:

**"App can't be opened" (Mac):**
- Solution documented in user guide
- Right-click → Open → Open

**"Windows protected your PC" (Windows):**
- Click "More info" → "Run anyway"
- This happens because app isn't code-signed ($$$)

**Firebase doesn't connect:**
- Check `.env` file is included in bundle
- Check `firebase-key.json` is included
- Check internet connection

---

## Distribution Platforms

### Free Options:
- **Google Drive** (15GB free) ✅ Current method
- **Dropbox** (2GB free)
- **GitHub Releases** (Unlimited for public repos)
- **itch.io** (Game distribution platform, supports pay-what-you-want)

### Paid Options:
- **Steam** ($100 one-time fee, 30% cut)
- **Epic Games Store** (12% cut, curated)
- **GOG** (Curated, DRM-free focus)

For sharing with friends/family, Google Drive or GitHub Releases are perfect.

---

## Updating the Game

### Workflow for updates:

1. **Make changes** to code
2. **Test locally**: `python main.py`
3. **Run tests**: `./venv/bin/pytest`
4. **Update version**: Increment `VERSION` file
5. **Update changelog**: Add changes to `CHANGELOG.md`
6. **Commit to git**: `git commit -am "Add new feature"`
7. **Build distributions**: Run PyInstaller on Mac and Windows
8. **Test distributions**: Run and verify on both platforms
9. **Upload to storage**: Google Drive / GitHub Releases
10. **Notify users**: Share download links with changelog

### Example update workflow:

```bash
# 1. Make changes (e.g., add Level 5)
# 2. Test
python main.py

# 3. Run tests
./venv/bin/pytest

# 4. Update version
echo "1.1.0" > VERSION

# 5. Update changelog
# Edit CHANGELOG.md manually

# 6. Commit
git add .
git commit -m "Add Level 5 - Ice Cave"
git tag -a v1.1.0 -m "Version 1.1.0"

# 7. Build Mac distribution
rm -rf build/ dist/
./venv/bin/pyinstaller siena_snowy_adventure.spec --clean --noconfirm
cd dist
zip -r ../SienaSnowyAdventure-Mac-v1.1.0.zip SienaSnowyAdventure.app
cd ..

# 8. Transfer to Windows, build there
# (or use CI/CD - see Advanced section below)

# 9. Upload to Google Drive / GitHub Releases

# 10. Share link with users
```

---

## Advanced: CI/CD with GitHub Actions

For automatic builds on every release:

1. **Create `.github/workflows/build.yml`:**
   ```yaml
   name: Build Distributions

   on:
     push:
       tags:
         - 'v*'

   jobs:
     build-mac:
       runs-on: macos-latest
       steps:
         - uses: actions/checkout@v3
         - uses: actions/setup-python@v4
           with:
             python-version: '3.11'
         - run: pip install -r requirements.txt pyinstaller
         - run: pyinstaller siena_snowy_adventure.spec --clean --noconfirm
         - run: cd dist && zip -r SienaSnowyAdventure-Mac.zip SienaSnowyAdventure.app
         - uses: actions/upload-artifact@v3
           with:
             name: mac-build
             path: dist/SienaSnowyAdventure-Mac.zip

     build-windows:
       runs-on: windows-latest
       steps:
         - uses: actions/checkout@v3
         - uses: actions/setup-python@v4
           with:
             python-version: '3.11'
         - run: pip install -r requirements.txt pyinstaller
         - run: pyinstaller siena_snowy_adventure_windows.spec --clean --noconfirm
         - run: Compress-Archive -Path dist/SienaSnowyAdventure -DestinationPath dist/SienaSnowyAdventure-Windows.zip
         - uses: actions/upload-artifact@v3
           with:
             name: windows-build
             path: dist/SienaSnowyAdventure-Windows.zip
   ```

2. **Push a tag:**
   ```bash
   git tag v1.1.0
   git push origin v1.1.0
   ```

3. **Builds run automatically** on GitHub servers

4. **Download artifacts** from Actions tab

**Note:** This requires setting up secrets for Firebase credentials in GitHub.

---

## Summary

**For now (simple approach):**
1. Build distributions manually on Mac (and Windows if available)
2. Upload to Google Drive with version numbers in filenames
3. Share links with users when updates are released
4. Users manually download and replace old version

**For the future (if game grows):**
- Set up GitHub Releases for version history
- Consider auto-update system
- Look into itch.io for wider distribution
- Implement CI/CD for automatic builds

The manual approach works great for sharing with friends/family and small audiences!
