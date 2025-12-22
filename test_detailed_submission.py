"""Test with very detailed logging to see what's happening"""
import os
import sys
from dotenv import load_dotenv
import logging

# Load environment
load_dotenv()

# Enable DEBUG level logging to see everything
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

print("=" * 60)
print("Detailed Score Submission Debug Test")
print("=" * 60)

print("\n1. Environment:")
print(f"   SIENA_ONLINE_ENABLED: {os.environ.get('SIENA_ONLINE_ENABLED', 'NOT SET')}")
print(f"   FIREBASE_URL: {os.environ.get('FIREBASE_URL', 'NOT SET')}")

print("\n2. Importing secure_leaderboard...")
from src.utils.secure_leaderboard import get_secure_leaderboard

print("\n3. Getting leaderboard instance...")
lb = get_secure_leaderboard()
print(f"   Is available: {lb.is_available()}")
print(f"   Base URL: {lb.base_url}")

print("\n4. Submitting score with detailed logging...")
print("   This will show HTTP request details")

success = lb.submit_score(
    level=1,
    username="DetailedTest",
    time=4500,  # 75 seconds
    coins=22,
    difficulty="Medium",
    checkpoints=False
)

print(f"\n5. Submission result: {success}")

if success:
    print("\n6. Waiting 2 seconds for Firebase to process...")
    import time
    time.sleep(2)

    print("\n7. Checking if score appears...")
    scores = lb.get_leaderboard(level=1, limit=20)
    print(f"   Total scores: {len(scores)}")

    detailed_scores = [s for s in scores if 'Detailed' in s['username']]
    if detailed_scores:
        print(f"   ✅ Found DetailedTest score!")
        for score in detailed_scores:
            print(f"      {score['username']}: {score['time']/60:.1f}s, {score['coins']} coins")
    else:
        print(f"   ❌ DetailedTest NOT in Firebase")
        print(f"\n   Top 5 scores for reference:")
        for i, s in enumerate(scores[:5], 1):
            print(f"      {i}. {s['username']}: {s['time']/60:.1f}s, {s['coins']} coins")
else:
    print("\n6. Submission failed - check logs above for error details")

print("\n" + "=" * 60)
