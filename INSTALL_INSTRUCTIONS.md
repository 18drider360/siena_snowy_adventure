# 🎮 How to Install Siena's Snowy Adventure (Mac)

Welcome! This guide will help you install the game on your Mac. Choose the method that works best for you.

---

## ⚡ Method 1: Terminal Install (Fastest & Easiest)

This method uses a simple command that does everything automatically.

### **Step-by-Step Instructions:**

#### **Step 1: Open Terminal**
Terminal is a built-in app on your Mac that lets you type commands.

1. Press `Command (⌘) + Spacebar` on your keyboard
2. Type: `terminal`
3. Press `Enter`

A window with white or black text will open - this is Terminal!

#### **Step 2: Copy and Paste the Install Command**

Copy this entire line (click the copy button or select all and press `Command + C`):

```bash
curl -fsSL https://raw.githubusercontent.com/18drider360/siena_snowy_adventure/main/install.sh | bash
```

Then:
1. Click inside the Terminal window
2. Press `Command (⌘) + V` to paste
3. Press `Enter`

#### **Step 3: Wait for Installation**

The installer will:
- ✅ Download the game (this takes about 1-2 minutes)
- ✅ Extract the files
- ✅ Install it to your Applications folder
- ✅ Set up security permissions
- ✅ Ask if you want to launch it immediately

That's it! The game is now installed!

#### **Troubleshooting Terminal Install:**
- If you see "command not found", make sure you copied the entire line
- If it asks for your password, type your Mac password (it won't show while typing - this is normal!)
- If you see any security warnings, the installer will guide you through them

---

## 📥 Method 2: Manual Download (Click & Drag)

Prefer clicking buttons? No problem! This method doesn't require Terminal at all.

### **Step-by-Step Instructions:**

#### **Step 1: Download the Game**

Click this link to download (no sign-up required):

**[📥 Download Siena's Snowy Adventure v1.2.7](https://github.com/18drider360/siena_snowy_adventure/releases/download/v1.2.7/SienaSnowyAdventure-Mac-v1.2.7.zip)**

The file will download to your `Downloads` folder (usually at the bottom of your screen or in Finder).

#### **Step 2: Find the Downloaded File**

1. Open `Finder` (the smiling face icon in your dock)
2. Click `Downloads` in the left sidebar
3. Look for a file named `SienaSnowyAdventure-Mac-v1.2.7.zip`

#### **Step 3: Unzip the File**

1. Double-click the `SienaSnowyAdventure-Mac-v1.2.7.zip` file
2. It will create a new file called `SienaSnowyAdventure.app`
3. You can delete the `.zip` file now if you want

#### **Step 4: Move to Applications** *(Recommended but optional)*

1. Keep your `Downloads` folder open
2. Open a new Finder window (`Command + N`)
3. Click `Applications` in the left sidebar
4. Drag `SienaSnowyAdventure.app` from Downloads to Applications

#### **Step 5: Open the Game (First Time Only)**

The first time you open the game, macOS will try to protect you from unknown apps. Here's how to allow it:

1. Find `SienaSnowyAdventure.app` (in Applications or Downloads)
2. **Right-click** (or hold `Control` and click) on the app
3. Select **"Open"** from the menu
4. A warning will appear - click **"Open"** again

**Important:** You only need to do this the first time! After that, you can open it normally by double-clicking.

#### **Step 6: Play!**

The game will now open and you can start playing! 🎉

---

## 🔄 Updates

Good news! Once installed, the game automatically checks for updates when you launch it. You'll never need to reinstall manually - just let the game update itself!

---

## ❓ Troubleshooting

### **"The app is damaged and can't be opened"**
This is a macOS security feature. Try this:
1. Open Terminal (press `Command + Spacebar`, type `terminal`, press Enter)
2. Copy and paste this command:
   ```bash
   xattr -d com.apple.quarantine /Applications/SienaSnowyAdventure.app
   ```
3. Press Enter
4. Try opening the game again

### **"I don't see the app in Applications"**
- Check your Downloads folder - you may have skipped Step 4
- The app works from anywhere, Applications is just the recommended location

### **The download is slow**
- The file is about 110 MB, so it may take 1-5 minutes depending on your internet speed
- Make sure you have a stable internet connection

### **Terminal method asks for password**
- This is normal! Type your Mac login password
- The cursor won't move while typing - this is a security feature
- Just type your password and press Enter

### **Still having issues?**
Open an issue on GitHub or contact support with:
- Which method you tried (Terminal or Manual)
- What error message you see (take a screenshot if possible)
- Your macOS version (click Apple menu  > About This Mac)

---

## 🎮 System Requirements

- macOS 10.13 (High Sierra) or newer
- ~200 MB of free disk space
- Internet connection (for initial download and updates)

---

## 🙋 Need Help?

If you're stuck or confused at any step:
1. Read the troubleshooting section above
2. Ask a tech-savvy friend for help
3. Contact us at [your support email/link]

**Remember:** There's no "wrong" way to install it - choose whichever method feels more comfortable to you! Both methods result in the exact same game.

---

**Happy gaming! ⛷️ 🎿 ❄️**
