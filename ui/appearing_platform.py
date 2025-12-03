import pygame

class AppearingPlatform:
    """Platform that appears and disappears on a timer cycle"""
    def __init__(self, x, y, width, height, appear_time=60, disappear_time=60, start_visible=True):
        """
        Args:
            x, y: Position
            width, height: Dimensions
            appear_time: Frames the platform is visible (default 60 = 1 second at 60fps)
            disappear_time: Frames the platform is invisible (default 60 = 1 second at 60fps)
            start_visible: Whether platform starts visible or invisible
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.original_x = x
        self.original_y = y

        # Timing
        self.appear_time = appear_time
        self.disappear_time = disappear_time
        self.timer = 0
        self.visible = start_visible

        # Visual properties
        self.alpha = 255 if start_visible else 0

    def update(self):
        """Update platform visibility based on timer"""
        self.timer += 1

        if self.visible:
            # Platform is currently visible
            if self.timer >= self.appear_time:
                # Time to disappear
                self.visible = False
                self.timer = 0
                # Move rect off-screen when invisible
                self.rect = pygame.Rect(-1000, -1000, 0, 0)
                self.x = -1000
                self.y = -1000
            else:
                # Calculate fade effect when about to disappear
                time_remaining = self.appear_time - self.timer
                if time_remaining <= 15:  # Start fading in last 0.25 seconds
                    fade_progress = time_remaining / 15
                    self.alpha = int(255 * fade_progress)
                else:
                    self.alpha = 255
        else:
            # Platform is currently invisible
            if self.timer >= self.disappear_time:
                # Time to appear
                self.visible = True
                self.timer = 0
                # Restore rect position when visible
                self.rect = pygame.Rect(self.original_x, self.original_y, self.width, self.height)
                self.x = self.original_x
                self.y = self.original_y
            else:
                # Calculate fade in effect when about to appear
                time_remaining = self.disappear_time - self.timer
                if time_remaining <= 15:  # Start fading in 0.25 seconds before appearing
                    fade_progress = 1 - (time_remaining / 15)
                    self.alpha = int(255 * fade_progress * 0.5)  # Fade in to 50% opacity as preview
                else:
                    self.alpha = 0

    def get_alpha(self):
        """Get current transparency level"""
        return self.alpha

    def is_solid(self):
        """Returns True if platform is solid (fully visible only)"""
        # Only solid when visible AND not in the fading out phase
        if not self.visible:
            return False
        # Check if we're in the fade-out phase (last 15 frames before disappearing)
        time_remaining = self.appear_time - self.timer
        return time_remaining > 15  # Only solid when more than 15 frames (0.25s) remain

    def should_pulse(self):
        """Returns True if platform should pulse (warning about state change)"""
        if self.visible:
            # Pulse when about to disappear
            return self.timer >= self.appear_time - 20
        else:
            # Pulse when about to appear
            return self.timer >= self.disappear_time - 20
