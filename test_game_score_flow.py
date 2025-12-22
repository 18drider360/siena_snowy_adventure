"""Test the exact flow the game uses when submitting scores"""
import os
from dotenv import load_dotenv
import logging

# Load environment
load_dotenv()

# Enable detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

print("=" * 60)
print("Testing Game Score Submission Flow")
print("=" * 60)

print("\n1. Environment:")
print(f"   SIENA_ONLINE_ENABLED: {os.environ.get('SIENA_ONLINE_ENABLED', 'NOT SET')}")
print(f"   FIREBASE_URL: {os.environ.get('FIREBASE_URL', 'NOT SET')}")

# Import save system (like the game does)
print("\n2. Importing SaveSystem...")
from src.utils.save_system import SaveSystem

# Submit score using SaveSystem (exactly like the game does)
print("\n3. Submitting score via SaveSystem.submit_score()...")
print("   (This is what the game calls after completing a level)")

success = SaveSystem.submit_score(
    username="GameFlowTest",
    level_num=1,
    time_taken=4800,  # 80 seconds
    coins_collected=23,
    difficulty="Medium",
    checkpoints_enabled=False
)

print(f"\n4. SaveSystem.submit_score() returned: {success}")

if success:
    print("\n5. Score saved locally. Checking online...")

    # Wait a moment for Firebase
    import time
    time.sleep(2)

    # Check online leaderboard
    from src.utils.secure_leaderboard import get_secure_leaderboard
    lb = get_secure_leaderboard()

    if lb.is_available():
        scores = lb.get_leaderboard(level=1, limit=20)
        print(f"   Total online scores: {len(scores)}")

        flow_scores = [s for s in scores if 'Flow' in s['username']]
        if flow_scores:
            print(f"   ✅ GameFlowTest found in online leaderboard!")
            for score in flow_scores:
                print(f"      {score['username']}: {score['time']/60:.1f}s, {score['coins']} coins")
        else:
            print(f"   ❌ GameFlowTest NOT in online leaderboard")
            print(f"   This means the game is NOT submitting online")
    else:
        print(f"   ❌ Online leaderboard not available")
else:
    print("\n5. SaveSystem.submit_score() failed")

print("\n" + "=" * 60)
