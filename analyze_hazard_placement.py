"""
Hazard Placement Analyzer
Checks that all hazards are properly supported by platforms/ground
and not overlapping with platforms
"""

import pygame
import importlib.util
from pathlib import Path

def analyze_hazard_placement(level_path, level_name):
    """Analyze a level for hazard placement issues"""
    try:
        # Import the level module
        spec = importlib.util.spec_from_file_location("level_module", level_path)
        level_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(level_module)

        # Build the level
        result = level_module.build_level()
        platforms = result[1]
        hazards = result[2]

        print(f"\n{'='*70}")
        print(f"LEVEL: {level_name}")
        print(f"{'='*70}")
        print(f"Total platforms: {len(platforms)}")
        print(f"Total hazards: {len(hazards)}")
        print()

        unsupported = []  # Hazards with nothing underneath
        overlapping = []  # Hazards overlapping with platforms
        floating = []  # Hazards with gap between them and platform below
        overhanging = []  # Hazards extending beyond platform edges

        for i, hazard in enumerate(hazards):
            # Check if hazard overlaps with any platform
            overlaps = []
            for j, platform in enumerate(platforms):
                if hazard.colliderect(platform):
                    overlaps.append((j, platform))

            if overlaps:
                overlapping.append((i, hazard, overlaps))
                continue  # Skip support check if overlapping

            # Check if hazard has support underneath AND if it's overhanging
            # A hazard is supported if there's a platform directly below it (within 2 pixels)
            hazard_bottom = hazard.bottom
            supported = False
            closest_platform_below = None
            min_gap = float('inf')
            supporting_platform = None

            for j, platform in enumerate(platforms):
                # Check if platform is below hazard and horizontally aligned
                if platform.top >= hazard_bottom:
                    # Check horizontal overlap
                    if platform.right > hazard.left and platform.left < hazard.right:
                        gap = platform.top - hazard_bottom
                        if gap < min_gap:
                            min_gap = gap
                            closest_platform_below = (j, platform)

                        # Consider supported if within 2 pixels
                        if gap <= 2:
                            supported = True
                            supporting_platform = platform
                            break

            # Check for overhanging (hazard extends beyond platform edges)
            # Check ALL platforms that the hazard is near (within 50px vertically)
            for j, platform in enumerate(platforms):
                # Check if platform is near the hazard vertically (within 50px)
                vertical_distance = abs(hazard.centery - platform.centery)
                if vertical_distance <= 50:
                    # Check if there's horizontal overlap
                    if hazard.right > platform.left and hazard.left < platform.right:
                        # Check if hazard extends beyond platform edges
                        hazard_left_overhang = max(0, platform.left - hazard.left)
                        hazard_right_overhang = max(0, hazard.right - platform.right)

                        if hazard_left_overhang > 0 or hazard_right_overhang > 0:
                            overhanging.append((i, hazard, j, platform,
                                              hazard_left_overhang, hazard_right_overhang))

            if not supported:
                if closest_platform_below:
                    floating.append((i, hazard, min_gap, closest_platform_below))
                else:
                    unsupported.append((i, hazard))

        # Report overlapping hazards
        if overlapping:
            print(f"⚠️  HAZARDS OVERLAPPING WITH PLATFORMS: {len(overlapping)}")
            print("-" * 70)
            for haz_idx, hazard, overlaps in overlapping:
                print(f"  Hazard {haz_idx} at (x={hazard.x}, y={hazard.y}, w={hazard.width}, h={hazard.height})")
                print(f"    → Overlapping with {len(overlaps)} platform(s):")
                for plat_idx, platform in overlaps:
                    print(f"      - Platform {plat_idx}: x={platform.x}, y={platform.y}, w={platform.width}, h={platform.height}")
                    print(f"        Hazard bottom: {hazard.bottom}, Platform top: {platform.y}")
                    print(f"        Overlap: {hazard.bottom - platform.y} pixels")
                print()
        else:
            print("✓ No hazards overlapping with platforms")

        # Report floating hazards
        if floating:
            print(f"\n⚠️  HAZARDS FLOATING (gap > 2px from platform below): {len(floating)}")
            print("-" * 70)
            for haz_idx, hazard, gap, (plat_idx, platform) in floating:
                print(f"  Hazard {haz_idx} at (x={hazard.x}, y={hazard.y}, w={hazard.width}, h={hazard.height})")
                print(f"    → Floating {gap} pixels above Platform {plat_idx}")
                print(f"    → Platform: x={platform.x}, y={platform.y}, w={platform.width}, h={platform.height}")
                print(f"    → Hazard bottom: {hazard.bottom}, Platform top: {platform.y}")
                print()
        else:
            print("\n✓ No floating hazards (all within 2px of support)")

        # Report completely unsupported hazards
        if unsupported:
            print(f"\n⚠️  HAZARDS WITH NO SUPPORT BELOW: {len(unsupported)}")
            print("-" * 70)
            for haz_idx, hazard in unsupported:
                print(f"  Hazard {haz_idx} at (x={hazard.x}, y={hazard.y}, w={hazard.width}, h={hazard.height})")
                print(f"    → No platform found below this hazard!")
                print()
        else:
            print("\n✓ All hazards have platforms below them")

        # Report overhanging hazards
        if overhanging:
            print(f"\n⚠️  HAZARDS OVERHANGING PLATFORM EDGES: {len(overhanging)}")
            print("-" * 70)
            for haz_idx, hazard, plat_idx, platform, left_overhang, right_overhang in overhanging:
                print(f"  Hazard {haz_idx} at (x={hazard.x}, y={hazard.y}, w={hazard.width}, h={hazard.height})")
                print(f"    → Supported by Platform {plat_idx}: x={platform.x}, y={platform.y}, w={platform.width}")
                if left_overhang > 0:
                    print(f"    → LEFT OVERHANG: {left_overhang}px (hazard left={hazard.left}, platform left={platform.left})")
                if right_overhang > 0:
                    print(f"    → RIGHT OVERHANG: {right_overhang}px (hazard right={hazard.right}, platform right={platform.right})")
                print()
        else:
            print("\n✓ No hazards overhanging platform edges")

        print(f"\nSUMMARY: {len(overlapping)} overlapping, {len(floating)} floating, {len(unsupported)} unsupported, {len(overhanging)} overhanging")

        return len(overlapping) + len(floating) + len(unsupported) + len(overhanging)

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
            issues = analyze_hazard_placement(filepath, level_name)
            total_issues += issues
        else:
            print(f"\n{level_name}: FILE NOT FOUND")

    print(f"\n{'='*70}")
    print(f"TOTAL HAZARD ISSUES ACROSS ALL LEVELS: {total_issues}")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    main()
