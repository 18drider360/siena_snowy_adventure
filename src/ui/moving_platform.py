import pygame

class MovingPlatform:
    """Platform that moves horizontally or vertically"""
    def __init__(self, x, y, width, height, move_range, speed, direction='horizontal'):
        self.rect = pygame.Rect(x, y, width, height)
        self.start_x = x
        self.start_y = y
        self.move_range = move_range  # How far it moves in pixels
        self.speed = speed  # Pixels per frame
        self.direction = direction  # 'horizontal' or 'vertical'
        self.moving_forward = True

        # For collision detection
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def update(self):
        """Move the platform back and forth"""
        if self.direction == 'horizontal':
            if self.moving_forward:
                self.rect.x += self.speed
                if self.rect.x >= self.start_x + self.move_range:
                    self.moving_forward = False
            else:
                self.rect.x -= self.speed
                if self.rect.x <= self.start_x:
                    self.moving_forward = True
        else:  # vertical
            if self.moving_forward:
                self.rect.y += self.speed
                if self.rect.y >= self.start_y + self.move_range:
                    self.moving_forward = False
            else:
                self.rect.y -= self.speed
                if self.rect.y <= self.start_y:
                    self.moving_forward = True

        # Update coordinate properties
        self.x = self.rect.x
        self.y = self.rect.y


class DisappearingPlatform:
    """Platform that disappears after player stands on it"""
    def __init__(self, x, y, width, height, disappear_time=120):
        self.rect = pygame.Rect(x, y, width, height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.disappear_time = disappear_time  # Frames until disappearance
        self.timer = 0
        self.player_on_platform = False
        self.disappeared = False
        self.respawn_timer = 0
        self.respawn_time = 180  # Frames until respawn
        self.original_x = x
        self.original_y = y

    def update(self, player_on_platform):
        """Update platform state"""
        if self.disappeared:
            self.respawn_timer += 1
            if self.respawn_timer >= self.respawn_time:
                # Respawn platform
                self.disappeared = False
                self.timer = 0
                self.respawn_timer = 0
                self.rect = pygame.Rect(self.original_x, self.original_y, self.width, self.height)
                self.x = self.original_x
                self.y = self.original_y
            return

        if player_on_platform:
            self.timer += 1
            if self.timer >= self.disappear_time:
                # Disappear
                self.disappeared = True
                self.rect = pygame.Rect(-1000, -1000, 0, 0)  # Move off screen
                self.x = -1000
                self.y = -1000
        else:
            # Reset timer if player steps off
            if self.timer > 0:
                self.timer = max(0, self.timer - 2)  # Slowly reset

    def get_alpha(self):
        """Get transparency based on timer for visual indicator"""
        if self.disappeared:
            return 0
        if self.timer == 0:
            return 255
        # Fade out as timer progresses
        progress = self.timer / self.disappear_time
        return int(255 * (1 - progress * 0.7))  # Fade to 30% opacity

    def should_shake(self):
        """Return True if platform should shake (warning indicator)"""
        if self.disappeared:
            return False
        return self.timer > self.disappear_time * 0.5  # Shake when more than 50% through timer
