"""
Audio Manager Module
Handles all audio loading, playback, and control for the game
"""

import pygame
from utils import settings as S


class AudioManager:
    """Manages all game audio including music and sound effects"""

    def __init__(self, enable_music=True, enable_sound=True):
        """
        Initialize the audio manager

        Args:
            enable_music: Whether to enable background music
            enable_sound: Whether to enable sound effects
        """
        self.audio_enabled = S.MASTER_AUDIO_ENABLED
        self.enable_music = enable_music and self.audio_enabled
        self.enable_sound = enable_sound and self.audio_enabled

        # Disable pygame mixer if audio is disabled
        if not self.audio_enabled:
            try:
                pygame.mixer.quit()
            except:
                pass

        # Sound effect storage
        self.sounds = {}

        # Load all sounds
        self._load_music()
        self._load_sound_effects()

    def _load_music(self):
        """Load and configure background music"""
        if not self.enable_music:
            return

        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.load("assets/music/main_theme.ogg")
            pygame.mixer.music.set_volume(0.6)
        except Exception as e:
            print(f"Could not load music: {e}")

    def _load_sound_effects(self):
        """Load all sound effects with appropriate volumes"""
        if not self.enable_sound:
            # Set all sounds to None
            sound_names = [
                'death', 'stage_clear', 'jump', 'double_jump',
                'coin', 'bump', 'land_enemy', 'land_slime',
                'enemy_projectile', 'spin_attack'
            ]
            for name in sound_names:
                self.sounds[name] = None
            return

        # Sound definitions: (paths to try, volume)
        sound_config = {
            'death': (["assets/sounds/death.wav", "assets/music/death.wav"], 0.6),
            'stage_clear': (["assets/sounds/stage_clear.wav", "assets/music/stage_clear.wav"], 0.7),
            'jump': (["assets/sounds/jump.ogg"], 0.4),
            'double_jump': (["assets/sounds/double_jump.ogg"], 0.4),
            'coin': (["assets/sounds/coin.ogg"], 0.2),
            'bump': (["assets/sounds/bump.ogg"], 0.2),
            'land_enemy': (["assets/sounds/land_enemy.ogg"], 0.3),
            'land_slime': (["assets/sounds/land_slime.ogg"], 0.3),
            'enemy_projectile': (["assets/sounds/enemy_projectile.ogg"], 0.2),
            'spin_attack': (["assets/sounds/spin_attack.ogg"], 0.3),
        }

        # Load each sound
        for name, (paths, volume) in sound_config.items():
            self.sounds[name] = self._load_sound(paths, volume)

    def _load_sound(self, paths, volume):
        """
        Load a sound effect from one of multiple possible paths

        Args:
            paths: List of file paths to try
            volume: Volume level for the sound (0.0 to 1.0)

        Returns:
            pygame.mixer.Sound or None if loading failed
        """
        for path in paths:
            try:
                sound = pygame.mixer.Sound(path)
                sound.set_volume(volume)
                return sound
            except:
                continue

        # If all paths failed
        print(f"Could not load sound from any of: {paths}")
        return None

    def play_music(self, loop=True):
        """
        Start playing background music

        Args:
            loop: Whether to loop the music (-1 for infinite loop, 0 for once)
        """
        if self.enable_music:
            try:
                loops = -1 if loop else 0
                pygame.mixer.music.play(loops)
            except Exception as e:
                print(f"Could not play music: {e}")

    def stop_music(self):
        """Stop background music"""
        if self.enable_music:
            try:
                pygame.mixer.music.stop()
            except Exception as e:
                print(f"Could not stop music: {e}")

    def pause_music(self):
        """Pause background music"""
        if self.enable_music:
            try:
                pygame.mixer.music.pause()
            except Exception as e:
                print(f"Could not pause music: {e}")

    def unpause_music(self):
        """Unpause background music"""
        if self.enable_music:
            try:
                pygame.mixer.music.unpause()
            except Exception as e:
                print(f"Could not unpause music: {e}")

    def play_sound(self, sound_name):
        """
        Play a sound effect by name

        Args:
            sound_name: Name of the sound to play (e.g., 'jump', 'coin', 'death')

        Returns:
            bool: True if sound played successfully, False otherwise
        """
        if not self.enable_sound:
            return False

        sound = self.sounds.get(sound_name)
        if sound:
            try:
                sound.play()
                return True
            except Exception as e:
                print(f"Could not play sound '{sound_name}': {e}")
                return False
        return False

    def get_sound(self, sound_name):
        """
        Get a sound object by name (for passing to other objects like player)

        Args:
            sound_name: Name of the sound

        Returns:
            pygame.mixer.Sound or None
        """
        return self.sounds.get(sound_name)

    def set_music_volume(self, volume):
        """
        Set music volume

        Args:
            volume: Volume level (0.0 to 1.0)
        """
        if self.enable_music:
            try:
                pygame.mixer.music.set_volume(volume)
            except Exception as e:
                print(f"Could not set music volume: {e}")

    def set_sound_volume(self, sound_name, volume):
        """
        Set volume for a specific sound effect

        Args:
            sound_name: Name of the sound
            volume: Volume level (0.0 to 1.0)
        """
        sound = self.sounds.get(sound_name)
        if sound:
            try:
                sound.set_volume(volume)
            except Exception as e:
                print(f"Could not set volume for sound '{sound_name}': {e}")

    def load_and_play_music(self, music_path, volume=0.6, loop=True):
        """
        Load and play a specific music file

        Args:
            music_path: Path to the music file
            volume: Volume level (0.0 to 1.0)
            loop: Whether to loop the music
        """
        if not self.enable_music:
            return

        try:
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(volume)
            loops = -1 if loop else 0
            pygame.mixer.music.play(loops)
        except Exception as e:
            print(f"Could not load/play music '{music_path}': {e}")

    def is_music_playing(self):
        """
        Check if music is currently playing

        Returns:
            bool: True if music is playing, False otherwise
        """
        if not self.enable_music:
            return False

        try:
            return pygame.mixer.music.get_busy()
        except:
            return False
