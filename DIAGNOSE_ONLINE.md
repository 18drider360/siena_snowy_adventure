# Diagnosing Online Leaderboard Issues

If you can't see or upload online scores on your laptop, follow these steps:

## Step 1: Test Firebase Access from Browser

1. Open your web browser
2. Go to: `https://siena-snowy-adventure-default-rtdb.firebaseio.com/leaderboards/level_1.json`
3. **Expected result:** You should see JSON data with scores
4. **If you see an error:** Your network/firewall is blocking Firebase

## Step 2: Run the Game from Terminal

Don't double-click the app - run it from Terminal to see error messages:

```bash
/Applications/SienaSnowyAdventure.app/Contents/MacOS/SienaSnowyAdventure
```

Or if you haven't moved it to Applications yet:

```bash
./SienaSnowyAdventure.app/Contents/MacOS/SienaSnowyAdventure
```

## Step 3: Look for These Messages

When you complete a level, you should see ONE of these messages:

- ✅ **"🌐 Score submitted to online leaderboard!"** - Everything works!
- ⚠️ **"Online score submission failed (check network connection)"** - Validation or network issue
- ℹ️ **"Online leaderboard not available (offline mode)"** - Firebase disabled
- ⚠️ **"Online leaderboard error: [details]"** - An exception occurred

## Step 4: Check Scoreboard

After completing a level:
1. Go to SCOREBOARD from the main menu
2. Look at the top of the scoreboard
3. You should see **"🌐 ONLINE LEADERBOARD"** or **"LOCAL SCORES"**

## Common Issues

### Issue: "Online leaderboard not available (offline mode)"
**Cause:** Firebase URL not set correctly
**Fix:** The app should have hardcoded defaults - this shouldn't happen in v1.0.7+

### Issue: "Online score submission failed"
**Cause:** Score validation failed (too fast, too many coins, etc.)
**Fix:** Check the terminal output for validation error details

### Issue: HTTP 401 Unauthorized
**Cause:** Firebase security rules not allowing access
**Fix:** Verify Firebase rules have `.read: true` and `.write: true`

### Issue: HTTP 400 Bad Request
**Cause:** Invalid query parameters or missing index
**Fix:** Verify Firebase has `.indexOn: ["time", "coins"]` in rules

### Issue: Network timeout
**Cause:** Firewall blocking Firebase
**Fix:** Check your firewall settings or try a different network

## Still Not Working?

If none of the above helps, there are a few possibilities:

1. **Old version cached:** Make sure you deleted the old app before installing v1.0.7
2. **Firewall issue:** Your network may be blocking `firebaseio.com` domains
3. **macOS security:** You may need to allow the app in System Settings → Security & Privacy

## Testing Firebase Directly

You can test if your network can reach Firebase by running this in Terminal:

```bash
curl "https://siena-snowy-adventure-default-rtdb.firebaseio.com/leaderboards/level_1.json?limitToFirst=3"
```

If this returns JSON data, your network can reach Firebase. If it fails, there's a network/firewall issue.

## Contact

If you're still having issues, check the Firebase Console for error logs or connection statistics.
