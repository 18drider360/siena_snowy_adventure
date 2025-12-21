"""
Checkpoint system for respawning at progress markers
"""

import pygame


class Checkpoint:
    """A checkpoint marker that players can reach and respawn at"""

    def __init__(self, x, y=360):
        """
        Initialize a checkpoint

        Args:
            x: X position of the checkpoint
            y: Y position (default 360, above ground at 400)
        """
        self.x = x
        self.y = y
        self.reached = False

        # Hitbox for detecting when player passes
        self.rect = pygame.Rect(x - 20, y, 40, 40)

    def check_player_reached(self, player):
        """
        Check if player has reached this checkpoint

        Args:
            player: Player object

        Returns:
            bool: True if player just reached this checkpoint (wasn't reached before)
        """
        if not self.reached and player.rect.centerx >= self.x:
            self.reached = True
            return True
        return False

    def draw(self, screen, camera_offset):
        """
        Draw the checkpoint flag

        Args:
            screen: Pygame surface to draw on
            camera_offset: Camera X offset for scrolling
        """
        # Calculate screen position
        screen_x = self.x - camera_offset
        screen_y = self.y

        # Don't draw if off screen
        if screen_x < -50 or screen_x > screen.get_width() + 50:
            return

        # Colors
        pole_color = (101, 67, 33)  # Brown pole
        if self.reached:
            flag_color = (0, 255, 0)  # Green flag when reached
        else:
            flag_color = (200, 200, 200)  # Gray flag when not reached

        # Draw pole (vertical line)
        pole_top = screen_y
        pole_bottom = screen_y + 40
        pygame.draw.line(screen, pole_color, (screen_x, pole_top), (screen_x, pole_bottom), 4)

        # Draw flag (triangle)
        flag_points = [
            (screen_x, pole_top),  # Top of pole
            (screen_x + 30, pole_top + 10),  # Right point of flag
            (screen_x, pole_top + 20)  # Bottom of flag attachment
        ]
        pygame.draw.polygon(screen, flag_color, flag_points)

        # Draw flag border
        pygame.draw.polygon(screen, (0, 0, 0), flag_points, 2)
