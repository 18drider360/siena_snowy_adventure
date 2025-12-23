# 🎮 Quick Install - Siena's Snowy Adventure (Windows)

## Download & Install (Recommended)

**[📥 Download Latest Windows Version](https://github.com/18drider360/siena_snowy_adventure/releases/latest)**

### Installation Steps:
1. Click the download link above
2. Download the file ending in `-Windows-vX.X.X.zip`
3. Extract the ZIP file (right-click → "Extract All...")
4. Open the extracted folder
5. Double-click `SienaSnowyAdventure.exe` to play!

### First Launch:
If you see "Windows protected your PC":
1. Click "More info"
2. Click "Run anyway"
3. This is normal for new applications - the game is safe!

---

## Automatic Install (Easiest!)

### Option 1: PowerShell One-Liner (Recommended)
Open PowerShell and run:
```powershell
iwr -useb https://raw.githubusercontent.com/18drider360/siena_snowy_adventure/main/install_windows.ps1 | iex
```

**How to open PowerShell:**
1. Press `Windows Key + X`
2. Click "Windows PowerShell" or "Terminal"
3. Paste the command above and press Enter
4. The game will download and launch automatically!

### Option 2: Download Installer Script
**[📥 Download install_windows.bat](https://raw.githubusercontent.com/18drider360/siena_snowy_adventure/main/install_windows.bat)** (right-click → Save As)
- Double-click to run
- Game downloads and launches automatically!

### Option 3: Manual One-Line Command
```powershell
$url = "https://github.com/18drider360/siena_snowy_adventure/releases/download/v1.2.7/SienaSnowyAdventure-Windows-v1.2.7.zip"; $dest = "$env:USERPROFILE\Downloads\SienaSnowyAdventure.zip"; $extract = "$env:USERPROFILE\Downloads\SienaSnowyAdventure"; Invoke-WebRequest -Uri $url -OutFile $dest; Expand-Archive -Path $dest -DestinationPath $extract -Force; Start-Process "$extract\SienaSnowyAdventure\SienaSnowyAdventure.exe"
```

---

## System Requirements

- **OS**: Windows 10 or Windows 11 (64-bit)
- **RAM**: 2 GB minimum
- **Graphics**: Any modern graphics card with OpenGL 2.0
- **Storage**: 100 MB free space

---

## Troubleshooting

### Antivirus Warning
Some antivirus software may flag the game. This is a false positive. Add an exception for `SienaSnowyAdventure.exe`.

### Missing DLL Error
Install Visual C++ Redistributable:
**[Download VC++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe)**

### Game Won't Start
- Update your graphics drivers
- Try running as Administrator (right-click → "Run as administrator")

---

## Game Location

After installation, the game will be in:
```
%USERPROFILE%\Downloads\SienaSnowyAdventure\
```

Your save files are stored in:
```
%USERPROFILE%\.siena_snowy_adventure\
```

---

## Updating

Windows version doesn't have automatic updates yet. To update:
1. Visit the [Releases Page](https://github.com/18drider360/siena_snowy_adventure/releases)
2. Download the latest Windows version
3. Extract and replace your old game folder
4. Your saves will be preserved!

---

## Support

Having issues? Report them here:
**[GitHub Issues](https://github.com/18drider360/siena_snowy_adventure/issues)**

---

**Enjoy the adventure!** ❄️🎮
