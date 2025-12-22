"""Test live score submission with debug logging"""
import os
import sys
from dotenv import load_dotenv

# Load environment
load_dotenv()

print("=" * 60)
print("Live Score Submission Test")
print("=" * 60)

print("\n1. Environment check:")
print(f"   SIENA_ONLINE_ENABLED: {os.environ.get('SIENA_ONLINE_ENABLED', 'NOT SET')}")
print(f"   FIREBASE_URL: {os.environ.get('FIREBASE_URL', 'NOT SET')}")

print("\n2. Importing save system...")
from src.utils.save_system import SaveSystem

print("\n3. Submitting test score...")
print("   This simulates what happens when you beat Level 1")

# Enable extra logging
import logging
logging.basicConfig(level=logging.DEBUG)

success = SaveSystem.submit_score(
    username="TerminalTest",
    level_num=1,
    time_taken=4200,  # 70 seconds
    coins_collected=20,
    difficulty="Medium",
    checkpoints_enabled=False
)

print(f"\n4. Result: {'✅ SUCCESS' if success else '❌ FAILED'}")

if success:
    print("\n5. Checking if score appears in Firebase...")
    from src.utils.secure_leaderboard import get_secure_leaderboard
    lb = get_secure_leaderboard()
    scores = lb.get_leaderboard(level=1, limit=10)

    terminal_scores = [s for s in scores if 'Terminal' in s['username']]
    if terminal_scores:
        print(f"   ✅ Found {len(terminal_scores)} TerminalTest score(s)")
        for score in terminal_scores:
            print(f"      {score['username']}: {score['time']/60:.1f}s, {score['coins']} coins")
    else:
        print("   ❌ TerminalTest NOT found in Firebase")
else:
    print("\n5. Score submission failed - check errors above")

print("\n" + "=" * 60)
