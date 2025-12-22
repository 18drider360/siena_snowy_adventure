"""Debug online score submission"""
import os
from dotenv import load_dotenv
load_dotenv()

print("=" * 60)
print("Testing Score Submission (Like Game Does)")
print("=" * 60)

# Test environment
print("\n1. Checking environment...")
print(f"   SIENA_ONLINE_ENABLED: {os.environ.get('SIENA_ONLINE_ENABLED')}")
print(f"   FIREBASE_URL: {os.environ.get('FIREBASE_URL')}")

# Import save system
from src.utils.save_system import SaveSystem

# Test submission (like game does after completing level)
print("\n2. Testing score submission...")
print("   Submitting score for 'BraveStorm77' on Level 1...")

success = SaveSystem.submit_score(
    username="BraveStorm77",
    level_num=1,
    time_taken=3000,  # 50 seconds
    coins_collected=25,
    difficulty="Medium",
    checkpoints_enabled=False
)

if success:
    print("   ✅ Score submitted successfully")
else:
    print("   ❌ Score submission failed")

# Check if it appears in online leaderboard
print("\n3. Checking online leaderboard...")
from src.utils.secure_leaderboard import get_secure_leaderboard

lb = get_secure_leaderboard()
if lb.is_available():
    scores = lb.get_leaderboard(level=1, limit=10)
    print(f"   Found {len(scores)} scores")

    # Look for BraveStorm77
    brave_scores = [s for s in scores if 'BraveStorm' in s['username']]
    if brave_scores:
        print(f"   ✅ Found BraveStorm77 in leaderboard!")
        for score in brave_scores:
            print(f"      - {score['username']}: {score['time']/60:.1f}s, {score['coins']} coins")
    else:
        print(f"   ❌ BraveStorm77 NOT in leaderboard")
        print(f"   Top 3 scores:")
        for i, s in enumerate(scores[:3], 1):
            print(f"      {i}. {s['username']}: {s['time']/60:.1f}s, {s['coins']} coins")
else:
    print("   ❌ Online leaderboard not available")

print("\n" + "=" * 60)
