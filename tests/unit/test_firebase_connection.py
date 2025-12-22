#!/usr/bin/env python3
"""
Test Firebase Connection
Quick script to verify Firebase online leaderboard is working
"""

from dotenv import load_dotenv
load_dotenv()

import os
import sys

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

print("=" * 60)
print("FIREBASE CONNECTION TEST")
print("=" * 60)

# Check environment variables
print("\n1. Checking environment variables...")
online_enabled = os.environ.get('SIENA_ONLINE_ENABLED', 'false')
firebase_url = os.environ.get('FIREBASE_URL')
firebase_key = os.environ.get('FIREBASE_KEY_PATH', 'firebase-key.json')

print(f"   SIENA_ONLINE_ENABLED: {online_enabled}")
print(f"   FIREBASE_URL: {firebase_url or '❌ NOT SET'}")
print(f"   FIREBASE_KEY_PATH: {firebase_key}")

if online_enabled.lower() != 'true':
    print("\n❌ Online leaderboards are DISABLED")
    print("   Set SIENA_ONLINE_ENABLED=true in .env to enable")
    sys.exit(1)

if not firebase_url:
    print("\n❌ FIREBASE_URL not set in .env")
    sys.exit(1)

# Check Firebase key file
print("\n2. Checking Firebase key file...")
if not os.path.exists(firebase_key):
    print(f"   ❌ Firebase key file not found: {firebase_key}")
    print("   Download from: Firebase Console > Project Settings > Service Accounts")
    sys.exit(1)
else:
    print(f"   ✅ Firebase key file found: {firebase_key}")

# Test Firebase initialization
print("\n3. Testing Firebase initialization...")
try:
    from src.utils.online_leaderboard import get_online_leaderboard

    leaderboard = get_online_leaderboard()

    if leaderboard.is_available():
        print("   ✅ Firebase initialized successfully!")
    else:
        print("   ❌ Firebase failed to initialize")
        print("   Check logs above for error details")
        sys.exit(1)

except Exception as e:
    print(f"   ❌ Error initializing Firebase: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test submitting a score
print("\n4. Testing score submission...")
try:
    success = leaderboard.submit_score(
        level=1,
        username="TestPlayer",
        time=6000,  # 100 seconds
        coins=30,
        difficulty="Medium",
        checkpoints=False
    )

    if success:
        print("   ✅ Score submitted successfully!")
    else:
        print("   ❌ Score submission failed")
        sys.exit(1)

except Exception as e:
    print(f"   ❌ Error submitting score: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test fetching leaderboard
print("\n5. Testing leaderboard fetch...")
try:
    scores = leaderboard.get_leaderboard(level=1, difficulty='All', limit=10)

    if scores:
        print(f"   ✅ Fetched {len(scores)} scores from leaderboard")
        print(f"\n   Top 3 scores:")
        for i, score in enumerate(scores[:3], 1):
            time_sec = score['time'] / 60.0
            print(f"   {i}. {score['username']}: {time_sec:.2f}s, {score['coins']} coins")
    else:
        print("   ✅ Leaderboard fetch succeeded (no scores yet)")

except Exception as e:
    print(f"   ❌ Error fetching leaderboard: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ ALL TESTS PASSED! Firebase online leaderboard is working!")
print("=" * 60)
print("\nYou can now run the game and your scores will be synced online.")
print("Other players will see your scores on the leaderboard!")
