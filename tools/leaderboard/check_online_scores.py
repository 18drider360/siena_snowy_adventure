#!/usr/bin/env python3
"""
Check Online Scores
Quick script to view scores from Firebase
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from dotenv import load_dotenv
load_dotenv()

from src.utils.online_leaderboard import get_online_leaderboard

def format_time(frames):
    """Convert frames to time string"""
    total_seconds = frames / 60.0
    minutes = int(total_seconds // 60)
    seconds = int(total_seconds % 60)
    milliseconds = int((total_seconds % 1) * 100)
    return f"{minutes:02d}:{seconds:02d}.{milliseconds:02d}"

print("=" * 70)
print("FIREBASE ONLINE LEADERBOARD - ALL SCORES")
print("=" * 70)

leaderboard = get_online_leaderboard()

if not leaderboard.is_available():
    print("\n❌ Online leaderboard is not available")
    print("Make sure SIENA_ONLINE_ENABLED=true in your .env file")
    exit(1)

print("\n✅ Connected to Firebase!")

# Check all 4 levels
for level in range(1, 5):
    print(f"\n{'='*70}")
    print(f"LEVEL {level} - ALL SCORES")
    print(f"{'='*70}")

    scores = leaderboard.get_leaderboard(level, difficulty='All', checkpoints_filter='All', limit=50)

    if not scores:
        print(f"  No scores yet for level {level}")
        continue

    print(f"\nTotal scores: {len(scores)}")
    print(f"\n{'Rank':<6} {'Username':<20} {'Time':<12} {'Coins':<8} {'Difficulty':<10} {'Checkpoints'}")
    print("-" * 70)

    for i, score in enumerate(scores, 1):
        time_str = format_time(score['time'])
        checkpoints = "Yes" if score['checkpoints'] else "No"
        print(f"{i:<6} {score['username']:<20} {time_str:<12} {score['coins']:<8} {score['difficulty']:<10} {checkpoints}")

# Look specifically for EpicPlayer55
print(f"\n{'='*70}")
print("SCORES BY EPICPLAYER55")
print(f"{'='*70}")

found_any = False
for level in range(1, 5):
    scores = leaderboard.get_leaderboard(level, difficulty='All', checkpoints_filter='All', limit=100)
    player_scores = [s for s in scores if s['username'] == 'EpicPlayer55']

    if player_scores:
        found_any = True
        print(f"\nLevel {level}:")
        for score in player_scores:
            time_str = format_time(score['time'])
            print(f"  Time: {time_str}, Coins: {score['coins']}, Difficulty: {score['difficulty']}, Checkpoints: {'Yes' if score['checkpoints'] else 'No'}")

if not found_any:
    print("\n  No scores found for EpicPlayer55")

print(f"\n{'='*70}")
