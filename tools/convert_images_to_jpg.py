#!/usr/bin/env python3
"""
Convert PNG images to high-quality JPEG to reduce file size
"""

import os
import shutil
from pathlib import Path
from PIL import Image

def convert_png_to_jpg(directory, quality=92, backup=True):
    """Convert PNG images to JPEG"""
    print(f"\n🖼️  Converting PNG to JPEG in {directory}...")

    if backup:
        backup_dir = Path(directory).parent / f"{Path(directory).name}_backup"
        if not backup_dir.exists():
            print(f"  Creating backup at {backup_dir}")
            shutil.copytree(directory, backup_dir)

    total_before = 0
    total_after = 0
    count = 0

    image_files = list(Path(directory).glob('*.png'))

    for filepath in image_files:
        # Get original size
        original_size = filepath.stat().st_size
        total_before += original_size

        try:
            # Open image
            img = Image.open(filepath)

            # Convert RGBA to RGB if needed (JPEG doesn't support transparency)
            if img.mode in ('RGBA', 'LA', 'P'):
                # Create white background
                rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                rgb_img.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                img = rgb_img

            # Save as JPEG
            jpg_path = filepath.with_suffix('.jpg')
            img.save(jpg_path, 'JPEG', quality=quality, optimize=True)

            # Get new size
            new_size = jpg_path.stat().st_size
            total_after += new_size
            count += 1

            savings = original_size - new_size
            print(f"  ✓ {filepath.name}: {original_size//1024}KB → {new_size//1024}KB (saved {savings//1024}KB)")

            # Remove old PNG
            filepath.unlink()

        except Exception as e:
            print(f"  ✗ Error converting {filepath.name}: {e}")
            total_after += original_size  # Count as no change

    print(f"\n  Total: {count} images converted")
    print(f"  Before: {total_before / 1024 / 1024:.1f} MB")
    print(f"  After:  {total_after / 1024 / 1024:.1f} MB")
    print(f"  Saved:  {(total_before - total_after) / 1024 / 1024:.1f} MB ({100 * (total_before - total_after) / total_before:.1f}%)")

    return total_before, total_after

def main():
    project_root = Path(__file__).parent.parent

    print("=" * 60)
    print("PNG to JPEG Converter")
    print("=" * 60)
    print("\nThis will convert dialogue images from PNG to high-quality JPEG.")
    print("A backup will be created at assets/images/dialogue_backup/")

    response = input("\nContinue? (y/n): ")
    if response.lower() != 'y':
        print("Cancelled.")
        return

    # Convert dialogue images
    dialogue_dir = project_root / "assets" / "images" / "dialogue"
    if dialogue_dir.exists():
        convert_png_to_jpg(dialogue_dir, quality=92, backup=True)

    print("\n" + "=" * 60)
    print("✓ Complete! Test the game to ensure images look good.")
    print("  If images look bad, restore from: assets/images/dialogue_backup/")
    print("=" * 60)

if __name__ == '__main__':
    main()
