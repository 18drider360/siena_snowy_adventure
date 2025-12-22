"""
Coin-Platform Collision Analyzer
Scans level files to detect coins that are touching or overlapping platforms
"""

import pygame
import importlib.util
from pathlib import Path

def analyze_level_collisions(level_path, level_name):
    """Analyze a level for coin-platform collisions"""
    try:
        # Import the level module
        spec = importlib.util.spec_from_file_location("level_module", level_path)
        level_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(level_module)

        # Build the level
        result = level_module.build_level()
        platforms = result[1]
        coins_group = result[7]

        print(f"\n{'='*70}")
        print(f"LEVEL: {level_name}")
        print(f"{'='*70}")
        print(f"Total platforms: {len(platforms)}")
        print(f"Total coins: {len(coins_group)}")
        print()

        # Convert coins group to list of rects
        coins = []
        for coin in coins_group:
            # Coin has rect attribute (40x40 image) and hitbox attribute (30x30)
            # Use hitbox for collision detection (more accurate)
            coin_x = coin.rect.centerx
            coin_y = coin.rect.centery
            # Hitbox is 30x30 centered on rect
            hitbox = coin.hitbox
            coins.append((coin_x, coin_y, hitbox))

        # Check each coin against each platform
        collisions = []
        touching = []  # Coins that are exactly touching (within 1 pixel)

        for coin_x, coin_y, hitbox in coins:
            for i, platform in enumerate(platforms):
                if hitbox.colliderect(platform):
                    overlap_type = "OVERLAPPING"
                    collisions.append((coin_x, coin_y, hitbox, i, platform, overlap_type))
                else:
                    # Check if coin is within 2 pixels of platform (touching but not overlapping)
                    # Coin bottom touching platform top
                    coin_bottom = hitbox.bottom
                    platform_top = platform.y

                    # Check if horizontally aligned
                    if hitbox.right > platform.left and hitbox.left < platform.right:
                        # Check vertical proximity
                        if abs(coin_bottom - platform_top) <= 2:
                            touching.append((coin_x, coin_y, hitbox, i, platform, "TOUCHING_TOP"))
                        elif abs(hitbox.top - platform.bottom) <= 2:
                            touching.append((coin_x, coin_y, hitbox, i, platform, "TOUCHING_BOTTOM"))

        # Report overlapping collisions
        if collisions:
            print(f"⚠️  OVERLAPPING COLLISIONS FOUND: {len(collisions)}")
            print("-" * 70)
            for coin_x, coin_y, hitbox, plat_idx, platform, overlap_type in collisions:
                print(f"  Coin at center ({coin_x}, {coin_y})")
                print(f"    → {overlap_type} with Platform {plat_idx}")
                print(f"    → Platform: x={platform.x}, y={platform.y}, w={platform.width}, h={platform.height}")
                print(f"    → Coin hitbox: x={hitbox.x}, y={hitbox.y}, w={hitbox.width}, h={hitbox.height}")
                print(f"    → Coin bottom: {hitbox.bottom}")
                print(f"    → Platform top: {platform.y}")
                print(f"    → Clearance: {platform.y - hitbox.bottom} pixels")
                print()
        else:
            print("✓ No overlapping collisions found")

        # Report touching (within 2 pixels)
        if touching:
            print(f"\n⚠️  COINS TOUCHING PLATFORMS (within 2px): {len(touching)}")
            print("-" * 70)
            for coin_x, coin_y, hitbox, plat_idx, platform, touch_type in touching:
                print(f"  Coin at center ({coin_x}, {coin_y})")
                print(f"    → {touch_type} Platform {plat_idx}")
                print(f"    → Platform: x={platform.x}, y={platform.y}, w={platform.width}, h={platform.height}")
                print(f"    → Coin hitbox: x={hitbox.x}, y={hitbox.y}, w={hitbox.width}, h={hitbox.height}")
                if touch_type == "TOUCHING_TOP":
                    print(f"    → Clearance: {platform.y - hitbox.bottom} pixels (coin bottom to platform top)")
                else:
                    print(f"    → Clearance: {hitbox.top - platform.bottom} pixels (platform bottom to coin top)")
                print()
        else:
            print("\n✓ No coins touching platforms (all have >2px clearance)")

        print(f"\nSUMMARY: {len(collisions)} overlapping, {len(touching)} touching")

        return len(collisions) + len(touching)

    except Exception as e:
        print(f"Error analyzing {level_name}: {e}")
        import traceback
        traceback.print_exc()
        return 0

def main():
    """Analyze all levels"""
    levels_dir = Path(__file__).parent / "levels"

    level_files = [
        ("Level 1 - Cabin", levels_dir / "level_1_cabin.py"),
        ("Level 2 - Ski Lift", levels_dir / "level_2_ski_lift.py"),
        ("Level 3 - Mountain Climb", levels_dir / "level_3_mountain_climb.py"),
        ("Level 4 - Northern Lights", levels_dir / "level_4_northern_lights.py"),
    ]

    pygame.init()

    total_issues = 0

    for level_name, filepath in level_files:
        if filepath.exists():
            issues = analyze_level_collisions(filepath, level_name)
            total_issues += issues
        else:
            print(f"\n{level_name}: FILE NOT FOUND")

    print(f"\n{'='*70}")
    print(f"TOTAL ISSUES ACROSS ALL LEVELS: {total_issues}")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    main()
