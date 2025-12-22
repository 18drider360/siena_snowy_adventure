#!/usr/bin/env python3
"""
Asset Optimization Tool
Compresses images and audio files to reduce distribution size
"""

import os
import sys
from pathlib import Path
from PIL import Image
import subprocess

def optimize_images(directory, quality=85, max_width=1920):
    """
    Optimize PNG images in a directory

    Args:
        directory: Directory containing images
        quality: JPEG quality (not used for PNG, but affects conversion decisions)
        max_width: Maximum width to resize images to
    """
    print(f"\n🖼️  Optimizing images in {directory}...")

    total_before = 0
    total_after = 0
    count = 0

    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.lower().endswith('.png'):
                filepath = os.path.join(root, filename)

                # Get original size
                original_size = os.path.getsize(filepath)
                total_before += original_size

                try:
                    # Open and optimize image
                    img = Image.open(filepath)

                    # Resize if too large
                    if img.width > max_width:
                        ratio = max_width / img.width
                        new_height = int(img.height * ratio)
                        img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
                        print(f"  Resized: {filename} ({img.width}x{img.height})")

                    # Save optimized PNG
                    img.save(filepath, 'PNG', optimize=True, compress_level=9)

                    # Get new size
                    new_size = os.path.getsize(filepath)
                    total_after += new_size
                    count += 1

                    savings = original_size - new_size
                    if savings > 1024:  # Only show if saved more than 1KB
                        print(f"  ✓ {filename}: {original_size//1024}KB → {new_size//1024}KB (saved {savings//1024}KB)")

                except Exception as e:
                    print(f"  ✗ Error optimizing {filename}: {e}")
                    total_after += original_size  # Count as no change

    if count > 0:
        print(f"\n  Total: {count} images")
        print(f"  Before: {total_before / 1024 / 1024:.1f} MB")
        print(f"  After:  {total_after / 1024 / 1024:.1f} MB")
        print(f"  Saved:  {(total_before - total_after) / 1024 / 1024:.1f} MB ({100 * (total_before - total_after) / total_before:.1f}%)")

    return total_before, total_after

def convert_wav_to_ogg(wav_file, quality=5):
    """
    Convert WAV file to OGG format using ffmpeg

    Args:
        wav_file: Path to WAV file
        quality: OGG quality (0-10, where 10 is highest)
    """
    print(f"\n🎵 Converting {wav_file} to OGG...")

    if not os.path.exists(wav_file):
        print(f"  ✗ File not found: {wav_file}")
        return False

    # Check for ffmpeg
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("  ✗ ffmpeg not found. Installing via homebrew...")
        try:
            subprocess.run(['brew', 'install', 'ffmpeg'], check=True)
        except:
            print("  ✗ Could not install ffmpeg. Please install manually:")
            print("     brew install ffmpeg")
            return False

    ogg_file = wav_file.replace('.wav', '.ogg')
    original_size = os.path.getsize(wav_file)

    try:
        # Convert to OGG
        subprocess.run([
            'ffmpeg', '-i', wav_file,
            '-codec:a', 'libvorbis',
            '-qscale:a', str(quality),
            '-y',  # Overwrite output file
            ogg_file
        ], check=True, capture_output=True)

        new_size = os.path.getsize(ogg_file)

        print(f"  ✓ Converted: {original_size / 1024 / 1024:.1f} MB → {new_size / 1024 / 1024:.1f} MB")
        print(f"  Saved: {(original_size - new_size) / 1024 / 1024:.1f} MB ({100 * (original_size - new_size) / original_size:.1f}%)")
        print(f"  Output: {ogg_file}")

        # Ask user if they want to delete the original
        response = input(f"\n  Delete original {os.path.basename(wav_file)}? (y/n): ")
        if response.lower() == 'y':
            os.remove(wav_file)
            print(f"  ✓ Deleted {wav_file}")

        return True

    except subprocess.CalledProcessError as e:
        print(f"  ✗ Conversion failed: {e}")
        return False

def main():
    # Get project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent

    print("=" * 60)
    print("Asset Optimization Tool")
    print("=" * 60)

    total_saved = 0

    # 1. Optimize dialogue images (biggest impact)
    dialogue_dir = project_root / "assets" / "images" / "dialogue"
    if dialogue_dir.exists():
        before, after = optimize_images(dialogue_dir, quality=85, max_width=1920)
        total_saved += (before - after)

    # 2. Optimize other images
    images_dir = project_root / "assets" / "images"
    if images_dir.exists():
        # Skip dialogue directory since we already did it
        for subdir in ['backgrounds', 'characters', 'ui', 'tiles']:
            subdir_path = images_dir / subdir
            if subdir_path.exists():
                before, after = optimize_images(subdir_path, quality=90, max_width=1920)
                total_saved += (before - after)

    # 3. Convert dialogue.wav to OGG
    dialogue_wav = project_root / "assets" / "music" / "dialogue.wav"
    if dialogue_wav.exists():
        convert_wav_to_ogg(str(dialogue_wav), quality=6)

    print("\n" + "=" * 60)
    print(f"Total space saved: {total_saved / 1024 / 1024:.1f} MB")
    print("=" * 60)

    print("\n⚠️  IMPORTANT: Test the game to make sure everything still works!")
    print("   Run: python main.py")

if __name__ == '__main__':
    main()
