# How to Install Siena's Snowy Adventure on Mac

**IMPORTANT: This is NOT malware or a virus!**

This game is completely safe - it's a winter platformer game I made. The complicated installation steps below are required because:

1. **Apple requires apps to be "code-signed"** - This costs $99/year for a developer certificate
2. **I haven't paid for code-signing** - Since this is a free game for friends/family
3. **macOS blocks unsigned apps by default** - This is Apple's security feature

These steps bypass Apple's security check **that you choose to bypass**. You're telling your Mac "I trust this app." Big commercial apps (like Steam games) go through the same process if downloaded outside official stores.

**The game does NOT:**
- ❌ Access your files or personal data
- ❌ Connect to anything except the game's Firebase leaderboard
- ❌ Install anything permanently (you can delete it anytime)
- ❌ Run in the background or use resources when closed

**The game DOES:**
- ✅ Play music and sound effects
- ✅ Save your progress locally
- ✅ Upload your high scores to an online leaderboard (if you want)
- ✅ Use keyboard controls to play

---

## Installation Steps (10-15 minutes)

### Step 1: Open the Google Drive Folder
You should already be here if you're reading this!

### Step 2: Download the Game
1. Click on **`SienaSnowyAdventure-Mac.zip`**
2. Click the **Download** button (top-right corner)
3. Google will show a warning: *"Google Drive can't scan this file for viruses"*
4. Click **"Download anyway"**
   - *(This warning appears because the file is large, not because it's dangerous)*

### Step 3: Wait for Download
The file is about 225MB, so it may take 2-5 minutes depending on your internet speed.

### Step 4: Locate the Downloaded File
1. Open **Finder**
2. Go to your **Downloads** folder
3. You should see `SienaSnowyAdventure-Mac.zip`

### Step 5: Extract the Zip File
1. **Double-click** `SienaSnowyAdventure-Mac.zip`
2. macOS will automatically extract it
3. A folder or files will appear:
   - `SienaSnowyAdventure.app` (the game)
   - `INSTALL.command` (installer helper)
   - `README.txt` (instructions)

### Step 6: Run the Installer
1. **Double-click** `INSTALL.command`
2. A Terminal window will open
3. You might see another security warning
4. If you do, continue to Step 7
5. If the installer runs successfully, you'll see:
   ```
   ✅ Success! The game is ready to play.
   Press Enter to close this window...
   ```
6. Press **Enter** and skip to Step 12

---

## If the Installer Gets Blocked (Steps 7-11)

### Step 7: Open System Settings
1. Click the  menu (top-left of screen)
2. Select **System Settings** (or **System Preferences** on older macOS)

### Step 8: Go to Privacy & Security
1. Click **Privacy & Security** in the left sidebar
2. If you don't see it, use the search box at the top

### Step 9: Scroll to the Security Section
1. Scroll down past all the privacy options
2. Look for the **Security** section (near the bottom)
3. You should see a message like:
   ```
   "INSTALL.command" was blocked from use because it is not from an identified developer.
   ```

### Step 10: Click "Open Anyway"
1. Click the **"Open Anyway"** button next to the message
2. You may need to enter your Mac password or use Touch ID
3. A dialog will appear asking if you're sure
4. Click **"Open"**

### Step 11: Run Installer Again
1. Go back to your Downloads folder (or wherever you extracted the game)
2. **Double-click** `INSTALL.command` again
3. The Terminal window will open and show:
   ```
   ✅ Success! The game is ready to play.
   Press Enter to close this window...
   ```
4. Press **Enter** to close the Terminal window

---

### Step 12: Launch the Game!
1. **Double-click** `SienaSnowyAdventure.app`
2. If you get ANOTHER security warning about the game itself:
   - **Right-click** (or Control-click) on `SienaSnowyAdventure.app`
   - Select **"Open"**
   - Click **"Open"** in the confirmation dialog
3. The game should launch! 🎮

### Step 13: Play!
- Use **Arrow Keys** or **WASD** to move
- Press **Space** to jump
- Press **Shift** while moving to roll
- Press **ESC** to pause

Your scores will automatically sync to the online leaderboard so you can compete with friends!

---

## Troubleshooting

### "The game won't open at all"
1. Make sure you extracted the .zip file (don't run it from inside the zip)
2. Try moving the game to your Applications folder
3. Run the `INSTALL.command` script again

### "I see a white/black screen then it closes"
1. Make sure you have macOS 10.13 or newer
2. Try restarting your Mac
3. Check that you have at least 500MB of free disk space

### "No sound is playing"
1. Check your Mac's volume (top-right corner)
2. Check System Settings → Sound → make sure the game isn't muted
3. The game has music and sound effects that should play automatically

### "Online leaderboard shows 'OFFLINE'"
1. Check your internet connection
2. Try going to Local/Online toggle and back to Online
3. The game works fine offline - you just won't see other players' scores

### "I want to uninstall the game"
1. Drag `SienaSnowyAdventure.app` to the Trash
2. Empty the Trash
3. Optional: Delete saved games at:
   `~/Library/Application Support/.siena_snowy_adventure/`

---

## Still Having Issues?

Contact me directly and I'll help you out! Include:
- Your macOS version (go to  → About This Mac)
- What step you're stuck on
- Any error messages you see
- A screenshot if possible

Enjoy the game! ❄️⛄🎮
