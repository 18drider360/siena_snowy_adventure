# Installing Siena's Snowy Adventure on Mac

## Quick Install (3 Steps)

### Step 1: Download & Extract
1. Download `SienaSnowyAdventure-Mac.zip`
2. Double-click to extract it
3. You'll see `SienaSnowyAdventure.app`

### Step 2: Remove Security Block
Open **Terminal** (search for "Terminal" in Spotlight) and paste this command:

```bash
xattr -cr ~/Downloads/SienaSnowyAdventure.app
```

Press Enter. This removes the quarantine flag that prevents the app from opening.

### Step 3: Open the Game
Double-click `SienaSnowyAdventure.app` - it should now launch!

---

## Alternative Method (Without Terminal)

If you're not comfortable with Terminal:

### Method 1: Right-Click Open
1. **Right-click** on `SienaSnowyAdventure.app`
2. Select **"Open"**
3. Click **"Open"** in the dialog
4. If it still doesn't work, try Method 2

### Method 2: System Settings
1. Go to **System Settings** → **Privacy & Security**
2. Scroll down to Security section
3. You'll see: "SienaSnowyAdventure was blocked"
4. Click **"Open Anyway"**
5. Try opening the app again
6. If a dialog appears, click **"Open"**

### Method 3: Remove Quarantine (No Terminal)
1. Select `SienaSnowyAdventure.app`
2. Press **Command+I** (Get Info)
3. At the bottom, look for "Where from:" and click **"Allow"** if present
4. Close the window
5. Try opening the app again

---

## Why This Happens

macOS blocks apps downloaded from the internet unless they're:
1. From the App Store, or
2. Code-signed by a registered developer ($99/year)

This game isn't code-signed (it's free!), so macOS blocks it. The `xattr -cr` command tells macOS "I trust this app."

---

## Still Not Working?

### Check if it's running:
- Look for the app in Activity Monitor (search in Spotlight)
- If you see "SienaSnowyAdventure" running, force quit it and try again

### Try running from Terminal:
```bash
cd ~/Downloads/SienaSnowyAdventure.app/Contents/MacOS
./SienaSnowyAdventure
```

This will show any error messages.

### Common Issues:

**"Operation not permitted"**
- You need to give Terminal permission in System Settings → Privacy & Security → Full Disk Access

**Black screen then closes**
- Your Mac might not support the required graphics
- Try updating macOS to the latest version

**"Damaged and can't be opened"**
- The download might be corrupted
- Delete and redownload the zip file

---

## Easy Install Script

Create a file called `install.sh` next to the app:

```bash
#!/bin/bash
echo "Removing security quarantine from Siena's Snowy Adventure..."
xattr -cr SienaSnowyAdventure.app
echo "Done! You can now open the app by double-clicking it."
echo "Press Enter to close this window."
read
```

Save it, then in Terminal:
```bash
cd ~/Downloads
chmod +x install.sh
./install.sh
```

---

## Uninstalling

To remove the game:
1. Drag `SienaSnowyAdventure.app` to Trash
2. Delete saved games: `~/Library/Application Support/.siena_snowy_adventure/`
3. Empty Trash

---

## Need Help?

If none of these work, text me with:
- Your macOS version (System Settings → General → About)
- What error message you see (if any)
- Screenshot of what happens when you try to open it
