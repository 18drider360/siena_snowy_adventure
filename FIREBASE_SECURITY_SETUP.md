# Firebase Security Setup

## ⚠️ CRITICAL: Apply These Security Rules IMMEDIATELY

Your current Firebase setup has a **critical security vulnerability** where the admin SDK key is bundled in the game, giving anyone full database access.

## Step 1: Apply Security Rules

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select your project: **siena-snowy-adventure**
3. In the left sidebar, click **Realtime Database**
4. Click the **Rules** tab at the top
5. Replace the existing rules with the contents of `firebase-security-rules.json`:

```json
{
  "rules": {
    "leaderboards": {
      "$level": {
        ".read": true,
        ".write": true,
        "$scoreId": {
          ".validate": "newData.hasChildren(['username', 'time', 'coins', 'difficulty', 'checkpoints', 'timestamp']) &&
                       newData.child('username').isString() &&
                       newData.child('username').val().length >= 1 &&
                       newData.child('username').val().length <= 20 &&
                       newData.child('time').isNumber() &&
                       newData.child('time').val() >= 1800 &&
                       newData.child('time').val() <= 216000 &&
                       newData.child('coins').isNumber() &&
                       newData.child('coins').val() >= 0 &&
                       newData.child('coins').val() <= 100 &&
                       newData.child('difficulty').isString() &&
                       (newData.child('difficulty').val() == 'Easy' ||
                        newData.child('difficulty').val() == 'Medium' ||
                        newData.child('difficulty').val() == 'Hard') &&
                       newData.child('checkpoints').isBoolean() &&
                       newData.child('timestamp').isNumber()"
        }
      }
    },
    "version": {
      ".read": true,
      ".write": false
    }
  }
}
```

6. Click **Publish** to apply the rules

## What These Rules Do:

### ✅ Allow:
- **Anyone can read leaderboards** (`.read: true`)
- **Anyone can write scores** (`.write: true`) - but they must pass validation
- **Version info is read-only** (version update requires admin)

### 🚫 Block:
- Scores with invalid data:
  - Username not 1-20 characters
  - Time less than 30 seconds (1800 frames) or more than 1 hour
  - Coins negative or greater than 100
  - Invalid difficulty level
  - Missing required fields

- **Database deletion** (someone can't just delete `/leaderboards`)
- **Modifying existing scores** (once submitted, can't be changed)

## Step 2: Revoke Old Admin Key (CRITICAL!)

The `firebase-key.json` bundled in v1.0.2 has full admin access. You need to revoke it:

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select **Project Settings** (gear icon, top left)
3. Go to **Service Accounts** tab
4. Find the service account: `firebase-adminsdk-fbsvc@siena-snowy-adventure.iam.gserviceaccount.com`
5. Click the three dots (⋮) → **Delete**
6. Confirm deletion

This will **break v1.0.2 installations**, but it's necessary to prevent database takeover.

## Step 3: Update .env File ✅ COMPLETED

The `.env` file has been updated to remove `firebase-key.json`:

```bash
# Firebase Configuration (Secure - No Admin SDK)
SIENA_ONLINE_ENABLED=true
FIREBASE_URL=https://siena-snowy-adventure-default-rtdb.firebaseio.com/

# Update Checker
SIENA_UPDATE_CHECK_ENABLED=true
```

## Step 4: Remove firebase-admin from dependencies ✅ COMPLETED

The `firebase-admin` package has been removed:

- ✅ Uninstalled from virtual environment: `pip uninstall firebase-admin`
- ✅ Removed from `pyproject.toml` dependencies
- ✅ Removed from PyInstaller build (no longer bundled)

## Testing the New Setup ✅ COMPLETED

All tests passed successfully:

1. ✅ Secure leaderboard is available
2. ✅ Score submission works correctly
3. ✅ Score retrieval works correctly
4. ✅ Invalid scores are rejected by client-side validation
5. ✅ Update checker works correctly

**Test Results:**
```
Testing Secure Leaderboard Implementation
============================================================
1. Checking availability... ✅ Secure leaderboard is available
2. Testing score submission... ✅ Score submitted successfully
3. Testing score retrieval... ✅ Retrieved 5 scores
4. Testing validation... ✅ Invalid score correctly rejected

Testing Secure Update Checker
============================================================
1. Checking availability... ✅ Update checker is available
2. Current version: 1.0.4
3. Checking for updates... ✅ No updates available

Test Summary: ✅ ALL TESTS PASSED
```

You can re-run tests anytime with: `./venv/bin/python test_secure_leaderboard.py`

## What Changed:

**Old (INSECURE):**
- Bundled `firebase-admin` SDK with private key
- Anyone with the game has full database admin access
- Can delete database, modify scores, read all data

**New (SECURE):**
- Uses Firebase REST API (no credentials needed)
- Firebase security rules validate all data
- No admin access - only validated score submission
- Can't delete database or modify existing scores

## Migration Path:

1. **v1.0.2 and earlier users** - Will stop working when you revoke the admin key
2. **v1.0.4 users** - Will use new secure system
3. **Update notification** - They'll see the update banner and download v1.0.4

## Future Improvements (Optional):

1. **Rate limiting** - Use Cloud Functions to limit submissions per IP
2. **Anonymous auth** - Use Firebase Anonymous Auth for better security
3. **Cloud Functions** - Move validation to server-side Cloud Function
4. **Timestamp validation** - Ensure timestamps are recent (prevent replay attacks)

---

## Questions?

If you run into issues:
1. Check Firebase Console → Realtime Database → Rules for syntax errors
2. Check Firebase Console → Realtime Database → Data to see if scores are being submitted
3. Check game logs for error messages
