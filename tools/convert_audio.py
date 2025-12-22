#!/usr/bin/env python3
"""
Convert WAV audio to OGG format using pygame
"""

import os
import subprocess
from pathlib import Path

def convert_wav_to_ogg_ffmpeg(wav_file, quality=6):
    """Convert WAV to OGG using ffmpeg if available"""
    ogg_file = wav_file.replace('.wav', '.ogg')
    original_size = os.path.getsize(wav_file)

    # Try different ffmpeg locations
    ffmpeg_paths = [
        '/usr/local/bin/ffmpeg',
        '/opt/homebrew/bin/ffmpeg',
        'ffmpeg'  # Try PATH
    ]

    ffmpeg_cmd = None
    for path in ffmpeg_paths:
        try:
            subprocess.run([path, '-version'], capture_output=True, check=True, timeout=5)
            ffmpeg_cmd = path
            break
        except:
            continue

    if not ffmpeg_cmd:
        print("❌ ffmpeg not found. Please install it:")
        print("   brew install ffmpeg")
        return False

    print(f"🎵 Converting {wav_file} to OGG...")
    print(f"   Original size: {original_size / 1024 / 1024:.1f} MB")

    try:
        # Convert to OGG
        result = subprocess.run([
            ffmpeg_cmd, '-i', wav_file,
            '-codec:a', 'libvorbis',
            '-qscale:a', str(quality),
            '-y',  # Overwrite
            ogg_file
        ], capture_output=True, text=True, timeout=60)

        if result.returncode != 0:
            print(f"❌ Conversion failed: {result.stderr}")
            return False

        new_size = os.path.getsize(ogg_file)
        savings = original_size - new_size

        print(f"   ✅ Converted successfully!")
        print(f"   New size: {new_size / 1024 / 1024:.1f} MB")
        print(f"   Saved: {savings / 1024 / 1024:.1f} MB ({100 * savings / original_size:.1f}%)")
        print(f"   Output: {ogg_file}")

        return True

    except Exception as e:
        print(f"❌ Conversion failed: {e}")
        return False

def update_audio_references(project_root):
    """Update code to use .ogg instead of .wav"""
    print("\n📝 Updating audio references in code...")

    # Find files that might reference dialogue.wav
    import subprocess
    result = subprocess.run(
        ['grep', '-r', 'dialogue.wav', str(project_root / 'src')],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print(f"   Found references in:")
        for line in result.stdout.split('\n'):
            if line:
                print(f"   {line}")

        # Update references
        subprocess.run([
            'find', str(project_root / 'src'), '-type', 'f', '-name', '*.py',
            '-exec', 'sed', '-i', '', 's/dialogue\\.wav/dialogue.ogg/g', '{}', ';'
        ])
        print("   ✅ Updated references to use .ogg")
    else:
        print("   No references to dialogue.wav found in src/")

def main():
    project_root = Path(__file__).parent.parent

    print("=" * 60)
    print("Audio Conversion Tool")
    print("=" * 60)

    dialogue_wav = project_root / "assets" / "music" / "dialogue.wav"

    if not dialogue_wav.exists():
        print(f"❌ File not found: {dialogue_wav}")
        return

    # Convert WAV to OGG
    success = convert_wav_to_ogg_ffmpeg(str(dialogue_wav), quality=6)

    if success:
        # Update code references
        update_audio_references(project_root)

        print("\n" + "=" * 60)
        print("✅ Complete! Test the game to ensure audio works.")
        print("=" * 60)

        response = input("\nDelete original dialogue.wav? (y/n): ")
        if response.lower() == 'y':
            dialogue_wav.unlink()
            print(f"✅ Deleted {dialogue_wav}")

if __name__ == '__main__':
    main()
