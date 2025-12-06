"""
Platform Collision Analyzer
Checks for platforms that are touching or overlapping each other
"""

import pygame
import importlib.util
from pathlib import Path

def analyze_platform_collisions(level_path, level_name):
    """Analyze a level for platform-platform collisions"""
    try:
        # Import the level module
        spec = importlib.util.spec_from_file_location("level_module", level_path)
        level_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(level_module)

        # Build the level
        result = level_module.build_level()
        platforms = result[1]

        print(f"\n{'='*70}")
        print(f"LEVEL: {level_name}")
        print(f"{'='*70}")
        print(f"Total platforms: {len(platforms)}")
        print()

        overlapping = []  # Platforms overlapping with other platforms
        touching = []  # Platforms that are exactly touching (within 1 pixel)

        # Check each platform against every other platform
        for i, platform1 in enumerate(platforms):
            for j, platform2 in enumerate(platforms):
                if i >= j:  # Skip self-comparison and duplicate pairs
                    continue

                if platform1.colliderect(platform2):
                    overlapping.append((i, platform1, j, platform2))
                else:
                    # Check if platforms are within 1 pixel of each other (touching but not overlapping)
                    # Check all 4 sides
                    touching_detected = False
                    touch_description = ""

                    # Platform1 bottom touching platform2 top
                    if abs(platform1.bottom - platform2.top) <= 1:
                        # Check if horizontally aligned
                        if platform1.right > platform2.left and platform1.left < platform2.right:
                            touching_detected = True
                            touch_description = f"Platform {i} bottom touching Platform {j} top"

                    # Platform1 top touching platform2 bottom
                    if abs(platform1.top - platform2.bottom) <= 1:
                        # Check if horizontally aligned
                        if platform1.right > platform2.left and platform1.left < platform2.right:
                            touching_detected = True
                            touch_description = f"Platform {i} top touching Platform {j} bottom"

                    # Platform1 right touching platform2 left
                    if abs(platform1.right - platform2.left) <= 1:
                        # Check if vertically aligned
                        if platform1.bottom > platform2.top and platform1.top < platform2.bottom:
                            touching_detected = True
                            touch_description = f"Platform {i} right touching Platform {j} left"

                    # Platform1 left touching platform2 right
                    if abs(platform1.left - platform2.right) <= 1:
                        # Check if vertically aligned
                        if platform1.bottom > platform2.top and platform1.top < platform2.bottom:
                            touching_detected = True
                            touch_description = f"Platform {i} left touching Platform {j} right"

                    if touching_detected:
                        touching.append((i, platform1, j, platform2, touch_description))

        # Report overlapping platforms
        if overlapping:
            print(f"⚠️  OVERLAPPING PLATFORMS FOUND: {len(overlapping)}")
            print("-" * 70)
            for plat1_idx, platform1, plat2_idx, platform2 in overlapping:
                print(f"  Platform {plat1_idx} at (x={platform1.x}, y={platform1.y}, w={platform1.width}, h={platform1.height})")
                print(f"    → OVERLAPPING with Platform {plat2_idx}")
                print(f"    → Platform {plat2_idx}: x={platform2.x}, y={platform2.y}, w={platform2.width}, h={platform2.height}")

                # Calculate overlap amount
                overlap_x = min(platform1.right, platform2.right) - max(platform1.left, platform2.left)
                overlap_y = min(platform1.bottom, platform2.bottom) - max(platform1.top, platform2.top)
                print(f"    → Overlap: {overlap_x}px horizontal, {overlap_y}px vertical")
                print()
        else:
            print("✓ No overlapping platforms found")

        # Report touching platforms
        if touching:
            print(f"\n⚠️  PLATFORMS TOUCHING (within 1px): {len(touching)}")
            print("-" * 70)
            for plat1_idx, platform1, plat2_idx, platform2, description in touching:
                print(f"  {description}")
                print(f"    → Platform {plat1_idx}: x={platform1.x}, y={platform1.y}, w={platform1.width}, h={platform1.height}")
                print(f"    → Platform {plat2_idx}: x={platform2.x}, y={platform2.y}, w={platform2.width}, h={platform2.height}")
                print()
        else:
            print("\n✓ No platforms touching (all have >1px clearance)")

        print(f"\nSUMMARY: {len(overlapping)} overlapping, {len(touching)} touching")

        return len(overlapping) + len(touching)

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
            issues = analyze_platform_collisions(filepath, level_name)
            total_issues += issues
        else:
            print(f"\n{level_name}: FILE NOT FOUND")

    print(f"\n{'='*70}")
    print(f"TOTAL PLATFORM COLLISION ISSUES ACROSS ALL LEVELS: {total_issues}")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    main()
