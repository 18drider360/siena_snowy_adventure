# Firebase Online Leaderboard Setup

This guide will help you set up online leaderboards for Siena's Snowy Adventure using Firebase Realtime Database.

## Step 1: Create a Firebase Project

1. Go to https://console.firebase.google.com
2. Click "Add project"
3. Enter project name (e.g., "siena-snowy-adventure")
4. Disable Google Analytics (optional)
5. Click "Create project"

## Step 2: Enable Realtime Database

1. In the Firebase console, click "Realtime Database" in the left sidebar
2. Click "Create Database"
3. Choose a location (e.g., "us-central1")
4. Start in **test mode** (for development)
5. Click "Enable"

## Step 3: Configure Security Rules

1. In the Realtime Database, click on the "Rules" tab
2. Replace the default rules with:

```json
{
  "rules": {
    "leaderboards": {
      "$level": {
        ".read": true,
        ".write": true,
        ".indexOn": ["time"],
        "$score_id": {
          ".validate": "newData.hasChildren(['username', 'time', 'coins', 'difficulty', 'checkpoints', 'timestamp'])"
        }
      }
    }
  }
}
```

3. Click "Publish"

**Important**: The `.indexOn": ["time"]` line is required for fast leaderboard queries!

**Note**: These rules allow anyone to read and write. For production, you should add authentication and stricter validation.

## Step 4: Get Service Account Key

1. In Firebase console, click the gear icon (⚙️) next to "Project Overview"
2. Click "Project settings"
3. Go to the "Service accounts" tab
4. Click "Generate new private key"
5. Click "Generate key" (this downloads a JSON file)
6. **IMPORTANT**: Rename the file to `firebase-key.json`
7. Move it to the root of your game directory (same level as `main.py`)
8. **NEVER commit this file to git!** (already in `.gitignore`)

## Step 5: Get Database URL

1. In the Realtime Database page, copy the database URL
   - It looks like: `https://siena-snowy-adventure-default-rtdb.firebaseio.com/`
2. Keep this URL for the next step

## Step 6: Configure Environment Variables

### Option A: Using a `.env` file (recommended for development)

1. Create a file named `.env` in the root directory:

```bash
# Firebase Configuration
SIENA_ONLINE_ENABLED=true
FIREBASE_URL=https://your-project-id-default-rtdb.firebaseio.com/
FIREBASE_KEY_PATH=firebase-key.json
```

2. Install python-dotenv:
```bash
./venv/bin/pip install python-dotenv
```

3. Add this to the top of `main.py`:
```python
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env
```

### Option B: Using system environment variables

**macOS/Linux:**
```bash
export SIENA_ONLINE_ENABLED=true
export FIREBASE_URL=https://your-project-id-default-rtdb.firebaseio.com/
export FIREBASE_KEY_PATH=firebase-key.json
```

**Windows (Command Prompt):**
```cmd
set SIENA_ONLINE_ENABLED=true
set FIREBASE_URL=https://your-project-id-default-rtdb.firebaseio.com/
set FIREBASE_KEY_PATH=firebase-key.json
```

**Windows (PowerShell):**
```powershell
$env:SIENA_ONLINE_ENABLED="true"
$env:FIREBASE_URL="https://your-project-id-default-rtdb.firebaseio.com/"
$env:FIREBASE_KEY_PATH="firebase-key.json"
```

## Step 7: Test the Connection

Run the game:
```bash
python main.py
```

Check the console output for:
- `Firebase initialized with database: [your-url]` ✅
- Or `Online leaderboards disabled` (if env vars not set)
- Or error messages if something went wrong

## Security Best Practices

### For Production:

1. **Add Firebase Authentication**:
```json
{
  "rules": {
    "leaderboards": {
      "$level": {
        ".read": true,
        ".write": "auth != null",
        "$score_id": {
          ".validate": "newData.child('username').val() === auth.uid"
        }
      }
    }
  }
}
```

2. **Implement Rate Limiting**:
   - Limit submissions to 1 per minute per user
   - Use server-side validation

3. **Add Anti-Cheat Validation**:
   - Validate completion times are physically possible
   - Check coin counts match level maximums
   - Hash scores on client and verify on server

## Troubleshooting

### "Firebase key file not found"
- Ensure `firebase-key.json` is in the root directory
- Check the `FIREBASE_KEY_PATH` environment variable

### "FIREBASE_URL not set in environment"
- Add the `FIREBASE_URL` to your `.env` file or environment variables
- Make sure to include the full URL with `https://`

### "Permission denied"
- Check your Firebase security rules
- Ensure you're using test mode for development

### "Module 'firebase_admin' not found"
- Install Firebase: `./venv/bin/pip install firebase-admin`

## Disabling Online Features

To disable online leaderboards (e.g., for offline play):

1. Set `SIENA_ONLINE_ENABLED=false` (or remove the variable)
2. Or delete/rename `firebase-key.json`

The game will automatically fall back to local leaderboards only.

## Database Structure

Your Firebase database will have this structure:

```
leaderboards/
  level_1/
    -RandomKey1: {username: "Player1", time: 1234, coins: 30, ...}
    -RandomKey2: {username: "Player2", time: 1456, coins: 28, ...}
  level_2/
    -RandomKey3: {username: "Player1", time: 2345, coins: 35, ...}
  level_3/
    ...
  level_4/
    ...
```

## Free Tier Limits

Firebase free tier includes:
- 1 GB stored data
- 10 GB/month downloaded
- 100 simultaneous connections

This should be sufficient for thousands of players!
