"""
Coin Counter - Analyzes level files to count total coins per level
Actually imports and runs the level build functions to get accurate counts
"""

import sys
from pathlib import Path

# Add project root to path so we can import from src
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def count_coins_in_level(level_module_path):
    """Count coins by actually running the build_level function"""
    try:
        # Import the level module
        import importlib.util
        spec = importlib.util.spec_from_file_location("level_module", level_module_path)
        level_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(level_module)

        # Call build_level with default abilities
        result = level_module.build_level()

        # Extract coins group (8th element in return tuple)
        coins_group = result[7]

        # Return the count
        return len(coins_group)
    except Exception as e:
        print(f"Error counting coins in {level_module_path}: {e}")
        return 0

def analyze_all_levels():
    """Analyze all level files and count coins"""
    levels_dir = Path(__file__).parent.parent / "src" / "levels"

    # Get all main level files (excluding editor and test levels)
    level_files = [
        ("Level 1", levels_dir / "level_1_cabin.py"),
        ("Level 2", levels_dir / "level_2_ski_lift.py"),
        ("Level 3", levels_dir / "level_3_mountain_climb.py"),
        ("Level 4", levels_dir / "level_4_northern_lights.py"),
    ]

    print("=" * 60)
    print("COIN COUNT ANALYSIS (ACTUAL EXECUTION)")
    print("=" * 60)
    print()

    total_coins = 0

    for level_name, filepath in level_files:
        if filepath.exists():
            coin_count = count_coins_in_level(filepath)
            total_coins += coin_count
            print(f"{level_name:12} : {coin_count:3} coins")
        else:
            print(f"{level_name:12} : FILE NOT FOUND")

    print()
    print("=" * 60)
    print(f"{'TOTAL':12} : {total_coins:3} coins")
    print("=" * 60)
    print()

    # Show expected vs actual
    expected = {
        1: 30,
        2: 35,
        3: 40,
        4: 45
    }

    print("COMPARISON:")
    for i, (level_name, filepath) in enumerate(level_files, 1):
        if filepath.exists():
            actual = count_coins_in_level(filepath)
            exp = expected[i]
            status = "✓" if actual == exp else "✗"
            diff = actual - exp
            diff_str = f"({diff:+d})" if diff != 0 else ""
            print(f"  {level_name}: Expected {exp}, Got {actual} {status} {diff_str}")
    print()

if __name__ == "__main__":
    analyze_all_levels()
