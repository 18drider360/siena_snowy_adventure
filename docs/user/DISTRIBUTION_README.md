# Siena's Snowy Adventure - Distribution Guide

## 📦 Files for Distribution

The game is packaged and ready to share! Here's what you have:

### For Mac Users (Your Friends)
**File**: `SienaSnowyAdventure-Mac.zip` (189MB)
**Location**: Root of project directory

**How to Share**:
1. Upload `SienaSnowyAdventure-Mac.zip` to:
   - Google Drive / Dropbox / iCloud
   - WeTransfer (wetransfer.com)
   - File.io or similar file sharing service
2. Send the download link to your friends

**Installation Instructions for Friends**:
1. Download `SienaSnowyAdventure-Mac.zip`
2. Double-click to extract it
3. Drag `SienaSnowyAdventure.app` to Applications folder
4. **First Launch**: Right-click app → Select "Open" → Click "Open" (bypasses security)
5. Future launches: Just double-click normally!

## 🎮 What's Included

- Complete game with 4 levels
- All story cutscenes and dialogue
- Full audio (music + sound effects)
- Save system (auto-saves progress)
- Difficulty settings (Easy/Medium/Hard)
- Optional checkpoint system
- Scoreboard tracking
- Player profiles

## 🔧 Technical Details

### System Requirements
- **OS**: macOS 10.13 (High Sierra) or higher
- **Architecture**: Apple Silicon (M1/M2/M3) optimized
- **RAM**: 512MB minimum
- **Storage**: 200MB free space
- **Display**: 1000x600 minimum resolution

### What's Bundled
- Python 3.11 interpreter
- Pygame 2.6.1
- PyYAML configuration system
- All game assets (70MB of images, music, sounds)
- Complete source code

### File Structure
```
SienaSnowyAdventure.app/
├── Contents/
│   ├── MacOS/
│   │   └── SienaSnowyAdventure (executable)
│   └── Resources/
│       ├── assets/ (game assets)
│       ├── src/ (game code)
│       ├── config.yaml
│       └── [Python + Pygame libraries]
```

## 🌐 Alternative Distribution Methods

### Option 1: GitHub Releases (Recommended)
1. Go to your repo: https://github.com/18drider360/siena_snowy_adventure
2. Click "Releases" → "Create a new release"
3. Tag: `v1.0.0`
4. Title: `Siena's Snowy Adventure v1.0.0 - Mac Release`
5. Upload `SienaSnowyAdventure-Mac.zip`
6. Publish release
7. Share the release URL with friends

**Advantages**:
- Professional distribution
- Version tracking
- Direct download links
- Automatic changelog
- Free hosting

### Option 2: itch.io (Game Platform)
1. Create account at itch.io
2. Create new project
3. Upload `SienaSnowyAdventure-Mac.zip`
4. Set as "Mac" platform
5. Price: Free
6. Publish
7. Share itch.io page URL

**Advantages**:
- Game-focused platform
- Built-in analytics
- Player comments/feedback
- Easy updates
- Free hosting

### Option 3: Direct File Sharing
**Services**:
- **Google Drive**: Easy if friends have Google accounts
- **Dropbox**: Good for larger files
- **WeTransfer**: No account needed, 2GB free transfers
- **File.io**: Anonymous, temporary links

## 🐛 Troubleshooting for Users

### "App is damaged and can't be opened"
**Solution**: User needs to run in Terminal:
```bash
xattr -cr /Applications/SienaSnowyAdventure.app
```

### "App from unidentified developer"
**Solution**: Right-click → Open → Click "Open" (first time only)

### Game won't start / Crashes immediately
**Solutions**:
1. Check macOS version (must be 10.13+)
2. Try moving app to Applications folder
3. Check Console.app for error messages
4. Verify app wasn't corrupted during download (re-download)

### No sound / Audio issues
**Solutions**:
1. Check system sound settings
2. Check game is not muted in System Preferences
3. Try restarting the app
4. Check if other apps have sound

### Save data not loading
**Check**: `~/.siena_snowy_adventure/` folder exists
**Solution**: Game creates this automatically on first run

## 📊 Analytics & Feedback

### What to Ask Friends
- Did the installation work smoothly?
- Are there any bugs or crashes?
- Is the difficulty balanced?
- Which levels did they enjoy most?
- Any suggestions for improvements?

### Collecting Feedback
- Create a Google Form
- Use GitHub Issues
- Discord/Slack channel
- Direct messages

## 🔄 Updates & Patches

If you need to release an update:

1. Make code changes
2. Rebuild app: `pyinstaller siena_snowy_adventure.spec --clean`
3. Create new ZIP: `cd dist && zip -r ../SienaSnowyAdventure-Mac-v1.1.zip SienaSnowyAdventure.app`
4. Upload to same distribution channel
5. Notify users of update
6. Consider adding auto-update check in future version

## 📝 Version History

### v1.0.0 (Current)
- Initial release
- 4 complete levels
- Full story implementation
- Particle effects & screen shake
- Sound effects (select, roll, bump)
- Checkpoint system
- Save/load system
- Scoreboard tracking

## 🎉 Success Checklist

Before sharing with friends:

- [x] Game builds successfully
- [x] App launches on your Mac
- [x] All levels playable
- [x] Sound works
- [x] Save system works
- [ ] Test on friend's Mac (different from yours)
- [ ] Create distribution (GitHub Release / itch.io / file sharing)
- [ ] Write installation instructions
- [ ] Share link with friends!

## 💡 Tips for Success

1. **Test First**: Have one friend test before sharing widely
2. **Clear Instructions**: Include USER_GUIDE.md with download
3. **Be Available**: Help troubleshoot in first few days
4. **Gather Feedback**: Ask for honest opinions
5. **Iterate**: Use feedback for future updates

## 📧 Support

If friends have issues, they can:
1. Check this README for troubleshooting
2. Check USER_GUIDE.md for gameplay help
3. Contact you directly
4. Open GitHub issue (if public)

---

**You did it!** 🎮✨

Your game is packaged and ready to share. Your friends on Mac can now enjoy Siena's Snowy Adventure!

---

*Built with Python, Pygame, and lots of ❤️*
