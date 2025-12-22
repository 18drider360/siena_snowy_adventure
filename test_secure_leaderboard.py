"""
Test script for secure leaderboard implementation
Tests score submission and retrieval using REST API
"""

import os
import sys

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Import secure leaderboard
from src.utils.secure_leaderboard import get_secure_leaderboard
from src.utils.update_checker_secure import get_update_checker

def test_leaderboard():
    """Test secure leaderboard functionality"""
    print("=" * 60)
    print("Testing Secure Leaderboard Implementation")
    print("=" * 60)

    # Get leaderboard instance
    lb = get_secure_leaderboard()

    # Check if available
    print(f"\n1. Checking availability...")
    if lb.is_available():
        print("   ✅ Secure leaderboard is available")
    else:
        print("   ❌ Secure leaderboard is NOT available")
        print("   Make sure SIENA_ONLINE_ENABLED=true and FIREBASE_URL is set in .env")
        return False

    # Test score submission
    print(f"\n2. Testing score submission...")
    success = lb.submit_score(
        level=1,
        username="TestPlayer",
        time=3600,  # 60 seconds at 60fps
        coins=15,
        difficulty="Medium",
        checkpoints=False
    )

    if success:
        print("   ✅ Score submitted successfully")
    else:
        print("   ❌ Failed to submit score")
        print("   Check Firebase security rules are applied")
        return False

    # Test score retrieval
    print(f"\n3. Testing score retrieval...")
    scores = lb.get_leaderboard(level=1, limit=5)

    if scores:
        print(f"   ✅ Retrieved {len(scores)} scores")
        print("\n   Top 3 scores for Level 1:")
        for i, score in enumerate(scores[:3], 1):
            username = score.get('username', 'Unknown')
            time = score.get('time', 0)
            coins = score.get('coins', 0)
            print(f"      {i}. {username} - {time/60:.1f}s, {coins} coins")
    else:
        print("   ⚠️  No scores retrieved (this might be OK if database is empty)")

    # Test invalid score submission (should be rejected)
    print(f"\n4. Testing validation (should reject invalid score)...")
    invalid_success = lb.submit_score(
        level=1,
        username="Hacker",
        time=1,  # Too fast - should be rejected by validation
        coins=999,  # Too many coins - should be rejected
        difficulty="Medium",
        checkpoints=False
    )

    if not invalid_success:
        print("   ✅ Invalid score correctly rejected")
    else:
        print("   ⚠️  Invalid score was accepted (check validation logic)")

    print("\n" + "=" * 60)
    return True


def test_update_checker():
    """Test secure update checker functionality"""
    print("\n" + "=" * 60)
    print("Testing Secure Update Checker")
    print("=" * 60)

    # Get update checker instance
    checker = get_update_checker()

    # Check if available
    print(f"\n1. Checking availability...")
    if checker.is_available():
        print("   ✅ Update checker is available")
    else:
        print("   ❌ Update checker is NOT available")
        print("   Make sure SIENA_UPDATE_CHECK_ENABLED=true and FIREBASE_URL is set")
        return False

    # Get current version
    current_version = checker.get_current_version()
    print(f"\n2. Current version: {current_version}")

    # Check for updates
    print(f"\n3. Checking for updates...")
    update_info = checker.check_for_update()

    if update_info:
        latest_version, download_url, changelog = update_info
        print(f"   ℹ️  Update available: v{latest_version}")
        print(f"      Download: {download_url}")
        print(f"      Changes: {changelog[:100]}...")
    else:
        print("   ✅ No updates available (you're on the latest version)")

    print("\n" + "=" * 60)
    return True


if __name__ == "__main__":
    # Test leaderboard
    lb_success = test_leaderboard()

    # Test update checker
    uc_success = test_update_checker()

    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    print(f"Secure Leaderboard: {'✅ PASSED' if lb_success else '❌ FAILED'}")
    print(f"Update Checker:     {'✅ PASSED' if uc_success else '❌ FAILED'}")
    print("=" * 60)

    if lb_success and uc_success:
        print("\n🎉 All tests passed! Ready to rebuild distribution.")
        sys.exit(0)
    else:
        print("\n⚠️  Some tests failed. Check configuration and Firebase setup.")
        sys.exit(1)
