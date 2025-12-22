#!/usr/bin/env python3
"""
Debug script to test online connectivity
Run this from terminal to diagnose online leaderboard issues
"""

import sys
import os

print("=" * 60)
print("Siena's Snowy Adventure - Online Debug")
print("=" * 60)

# Check if we're in a PyInstaller bundle
if hasattr(sys, '_MEIPASS'):
    print(f"\n✓ Running from bundled app")
    print(f"  Bundle path: {sys._MEIPASS}")
else:
    print(f"\n✓ Running from source")

# Check Python version
print(f"\nPython: {sys.version}")

# Test imports
print("\n1. Testing imports...")
try:
    import pygame
    print("  ✓ pygame imported")
except Exception as e:
    print(f"  ✗ pygame import failed: {e}")

try:
    from src.utils.secure_leaderboard import get_secure_leaderboard, ONLINE_ENABLED
    print("  ✓ secure_leaderboard imported")
except Exception as e:
    print(f"  ✗ secure_leaderboard import failed: {e}")
    sys.exit(1)

# Check environment
print(f"\n2. Environment:")
print(f"  SIENA_ONLINE_ENABLED: {os.environ.get('SIENA_ONLINE_ENABLED', 'NOT SET (will use default: true)')}")
print(f"  FIREBASE_URL: {os.environ.get('FIREBASE_URL', 'NOT SET (will use hardcoded default)')}")
print(f"  ONLINE_ENABLED constant: {ONLINE_ENABLED}")

# Initialize leaderboard
print(f"\n3. Initializing leaderboard...")
try:
    lb = get_secure_leaderboard()
    print(f"  ✓ Leaderboard created")
    print(f"  Initialized: {lb.initialized}")
    print(f"  Base URL: {lb.base_url}")
    print(f"  Available: {lb.is_available()}")
except Exception as e:
    print(f"  ✗ Leaderboard initialization failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

if not lb.is_available():
    print("\n✗ Leaderboard not available - online features disabled")
    sys.exit(1)

# Test READ
print(f"\n4. Testing READ access...")
try:
    scores = lb.get_leaderboard(level=1, limit=3)
    print(f"  ✓ Read {len(scores)} scores from Firebase")
    if scores:
        print(f"  Top 3 scores:")
        for i, score in enumerate(scores[:3], 1):
            print(f"    {i}. {score['username']}: {score['time']/60:.1f}s, {score['coins']} coins")
    else:
        print(f"  (No scores in database yet)")
except Exception as e:
    print(f"  ✗ READ failed: {e}")
    import traceback
    traceback.print_exc()

# Test WRITE
print(f"\n5. Testing WRITE access...")
try:
    test_username = f"DiagTest"
    success = lb.submit_score(
        level=1,
        username=test_username,
        time=3000,  # 50 seconds
        coins=18,
        difficulty='Medium',
        checkpoints=False
    )

    if success:
        print(f"  ✓ Score submitted successfully")

        # Verify it appears
        import time
        time.sleep(1)
        scores = lb.get_leaderboard(level=1, limit=50)
        found = any('Diag' in s['username'] for s in scores)
        if found:
            print(f"  ✓ Score verified in Firebase")
        else:
            print(f"  ⚠ Score submitted but not found in Firebase (may take a moment)")
    else:
        print(f"  ✗ Score submission failed")
except Exception as e:
    print(f"  ✗ WRITE failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("CONCLUSION:")
if lb.is_available():
    print("✓ Online features should be working")
    print("  If the game still can't connect, there may be a network firewall issue")
else:
    print("✗ Online features NOT working")
    print("  Check the errors above for details")
print("=" * 60)

input("\nPress Enter to exit...")
