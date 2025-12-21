"""
Screen shake effect for impactful game feel.

Used for:
- Enemy stomps
- Taking damage
- Enemy defeats
- Large explosions
"""

import random


class ScreenShake:
    """Manages screen shake effects with intensity and duration."""

    def __init__(self):
        self.duration = 0
        self.intensity = 0
        self.offset_x = 0
        self.offset_y = 0

    def start(self, intensity, duration):
        """
        Start a screen shake effect.

        Args:
            intensity: Pixel offset magnitude (2-6 typical)
            duration: Number of frames (3-15 typical)
        """
        # If already shaking, use the stronger intensity
        self.intensity = max(self.intensity, intensity)
        self.duration = max(self.duration, duration)

    def update(self):
        """Update shake effect each frame."""
        if self.duration > 0:
            self.duration -= 1

            # Generate random offset based on intensity
            self.offset_x = random.randint(-self.intensity, self.intensity)
            self.offset_y = random.randint(-self.intensity, self.intensity)

            # Reduce intensity over time for smoother end
            if self.duration < 5:
                self.intensity = max(1, self.intensity - 1)
        else:
            # No shake active
            self.intensity = 0
            self.offset_x = 0
            self.offset_y = 0

    def get_offset(self):
        """Get current screen offset as (x, y) tuple."""
        return (self.offset_x, self.offset_y)

    def is_active(self):
        """Check if shake is currently active."""
        return self.duration > 0

    def clear(self):
        """Immediately stop shaking."""
        self.duration = 0
        self.intensity = 0
        self.offset_x = 0
        self.offset_y = 0


# Preset shake effects for common events
SHAKE_PRESETS = {
    'land_soft': (2, 4),       # Player lands from small height
    'land_hard': (4, 6),       # Player lands from big jump
    'stomp_enemy': (3, 6),     # Player stomps enemy
    'take_damage': (5, 8),     # Player takes damage
    'enemy_defeat': (4, 8),    # Enemy defeated
    'spin_attack': (2, 3),     # Spin attack connects
    'boss_hit': (6, 12),       # Boss takes damage
    'explosion': (8, 15),      # Big explosion
}


def apply_preset(screen_shake, preset_name):
    """Apply a preset shake effect."""
    if preset_name in SHAKE_PRESETS:
        intensity, duration = SHAKE_PRESETS[preset_name]
        screen_shake.start(intensity, duration)
