"""
Configuration Loader
Loads game configuration from config.yaml and provides easy access to settings
"""

import yaml
import os


class GameConfig:
    """Loads and provides access to game configuration"""

    def __init__(self, config_file='config.yaml'):
        """
        Load configuration from YAML file

        Args:
            config_file: Path to the config file
        """
        self.config_file = config_file
        self.config = self._load_config()

    def _load_config(self):
        """Load configuration from YAML file"""
        try:
            with open(self.config_file, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print(f"Warning: Config file '{self.config_file}' not found. Using defaults.")
            return self._get_default_config()
        except yaml.YAMLError as e:
            print(f"Error parsing config file: {e}. Using defaults.")
            return self._get_default_config()

    def _get_default_config(self):
        """Return default configuration if file is not found"""
        return {
            'display': {'fps': 60, 'window_width': 1000, 'window_height': 600},
            'audio': {'master_enabled': True},
            'player': {'speed': 4, 'gravity': 0.6, 'jump_strength': -13},
            'enemies': {'global': {'gravity': 0.6}},
            'debug': {'show_hitboxes': False}
        }

    def get(self, path, default=None):
        """
        Get a configuration value using dot notation

        Args:
            path: Dot-separated path (e.g., 'player.speed', 'enemies.snowy.health')
            default: Default value if path not found

        Returns:
            Configuration value or default
        """
        keys = path.split('.')
        value = self.config

        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default

        return value

    def reload(self):
        """Reload configuration from file"""
        self.config = self._load_config()

    def save(self, config_file=None):
        """
        Save current configuration to YAML file

        Args:
            config_file: Optional path to save to (defaults to current config_file)
        """
        if config_file is None:
            config_file = self.config_file

        with open(config_file, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False, sort_keys=False)

    # === Convenience properties for common settings ===

    @property
    def fps(self):
        """Get FPS setting"""
        return self.get('display.fps', 60)

    @property
    def player_speed(self):
        """Get player speed"""
        return self.get('player.speed', 4)

    @property
    def player_jump_strength(self):
        """Get player jump strength"""
        return self.get('player.jump_strength', -13)

    @property
    def player_max_health(self):
        """Get player max health"""
        return self.get('player.max_health', 6)

    @property
    def master_audio_enabled(self):
        """Get master audio setting"""
        return self.get('audio.master_enabled', True)

    @property
    def show_hitboxes(self):
        """Get hitbox debug setting"""
        return self.get('debug.show_hitboxes', False)

    def __repr__(self):
        """String representation"""
        return f"GameConfig(file='{self.config_file}', loaded={len(self.config)} sections)"


# Global config instance
_config = None


def get_config():
    """Get the global configuration instance"""
    global _config
    if _config is None:
        _config = GameConfig()
    return _config


def reload_config():
    """Reload the global configuration"""
    global _config
    if _config is not None:
        _config.reload()
    else:
        _config = GameConfig()


# Example usage
if __name__ == '__main__':
    config = GameConfig()
    print(f"Player speed: {config.get('player.speed')}")
    print(f"Player jump: {config.get('player.jump_strength')}")
    print(f"Snowy health: {config.get('enemies.snowy.health')}")
    print(f"FPS: {config.fps}")
    print(f"Debug hitboxes: {config.show_hitboxes}")
