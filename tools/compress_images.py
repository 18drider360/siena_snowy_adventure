#!/usr/bin/env python3
"""
Image Compression Tool - Optimizes PNG files
"""

import os
from pathlib import Path
from PIL import Image

def optimize_images(directory, max_width=1920):
    """Optimize PNG images in a directory"""
    print(f"\n🖼️  Optimizing images in {directory}...")

    total_before = 0
    total_after = 0
    count = 0

    image_files = list(Path(directory).glob('**/*.png'))

    for filepath in image_files:
        # Get original size
        original_size = filepath.stat().st_size
        total_before += original_size

        try:
            # Open and optimize image
            img = Image.open(filepath)

            # Resize if too large (dialogue images are probably huge)
            width, height = img.size
            if width > max_width:
                ratio = max_width / width
                new_height = int(height * ratio)
                img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
                print(f"  Resized: {filepath.name} ({width}x{height} → {max_width}x{new_height})")

            # Save optimized PNG
            img.save(filepath, 'PNG', optimize=True, compress_level=9)

            # Get new size
            new_size = filepath.stat().st_size
            total_after += new_size
            count += 1

            savings = original_size - new_size
            if savings > 10240:  # Only show if saved more than 10KB
                print(f"  ✓ {filepath.name}: {original_size//1024}KB → {new_size//1024}KB (saved {savings//1024}KB)")

        except Exception as e:
            print(f"  ✗ Error optimizing {filepath.name}: {e}")
            total_after += original_size  # Count as no change

    print(f"\n  Total: {count} images")
    print(f"  Before: {total_before / 1024 / 1024:.1f} MB")
    print(f"  After:  {total_after / 1024 / 1024:.1f} MB")
    print(f"  Saved:  {(total_before - total_after) / 1024 / 1024:.1f} MB ({100 * (total_before - total_after) / total_before:.1f}%)")

    return total_before, total_after

def main():
    project_root = Path(__file__).parent.parent

    print("=" * 60)
    print("Image Compression Tool")
    print("=" * 60)

    # Optimize dialogue images (biggest impact)
    dialogue_dir = project_root / "assets" / "images" / "dialogue"
    if dialogue_dir.exists():
        optimize_images(dialogue_dir, max_width=1920)

    print("\n" + "=" * 60)
    print("✓ Complete! Test the game to ensure images look good.")
    print("=" * 60)

if __name__ == '__main__':
    main()
