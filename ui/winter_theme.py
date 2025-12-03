"""
Winter Theme Helper
Shared visual elements for winter-themed UI screens
"""

import pygame
import random
import math


class Snowflake:
    """A single falling snowflake"""
    def __init__(self, screen_width, screen_height):
        self.x = random.randint(0, screen_width)
        self.y = random.randint(-50, screen_height)
        self.speed = random.uniform(0.5, 2.0)
        self.size = random.randint(2, 4)
        self.sway = random.uniform(-0.5, 0.5)
        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self):
        self.y += self.speed
        self.x += self.sway
        if self.y > self.screen_height:
            self.y = -10
            self.x = random.randint(0, self.screen_width)

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), self.size)


class WinterTheme:
    """Helper class for drawing winter-themed UI elements"""

    # Color palette
    BG_GRADIENT_TOP = (15, 30, 60)
    BG_GRADIENT_BOTTOM = (40, 70, 120)
    SNOW_WHITE = (255, 255, 255)
    ICE_BLUE = (180, 220, 255)
    FROST_BLUE = (200, 230, 255)
    DARK_ICE = (100, 150, 200)
    GLOW_BLUE = (150, 200, 255)
    TEXT_DARK = (20, 40, 80)

    @staticmethod
    def draw_gradient_background(screen):
        """Draw a beautiful gradient background"""
        screen_height = screen.get_height()
        screen_width = screen.get_width()

        for y in range(screen_height):
            ratio = y / screen_height
            r = int(WinterTheme.BG_GRADIENT_TOP[0] + (WinterTheme.BG_GRADIENT_BOTTOM[0] - WinterTheme.BG_GRADIENT_TOP[0]) * ratio)
            g = int(WinterTheme.BG_GRADIENT_TOP[1] + (WinterTheme.BG_GRADIENT_BOTTOM[1] - WinterTheme.BG_GRADIENT_TOP[1]) * ratio)
            b = int(WinterTheme.BG_GRADIENT_TOP[2] + (WinterTheme.BG_GRADIENT_BOTTOM[2] - WinterTheme.BG_GRADIENT_TOP[2]) * ratio)
            pygame.draw.line(screen, (r, g, b), (0, y), (screen_width, y))

    @staticmethod
    def draw_frosted_box(screen, x, y, width, height, alpha=180):
        """Draw a frosted glass effect box"""
        # Shadow
        shadow = pygame.Surface((width + 8, height + 8))
        shadow.fill((0, 0, 0))
        shadow.set_alpha(60)
        screen.blit(shadow, (x + 4, y + 4))

        # Main box
        box_surface = pygame.Surface((width, height))
        box_surface.fill(WinterTheme.FROST_BLUE)
        box_surface.set_alpha(alpha)
        screen.blit(box_surface, (x, y))

        # Border
        border_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(screen, WinterTheme.GLOW_BLUE, border_rect, 3)

        # Highlight
        pygame.draw.line(screen, (255, 255, 255), (x + 5, y + 5), (x + width - 5, y + 5), 2)
        pygame.draw.line(screen, (255, 255, 255), (x + 5, y + 5), (x + 5, y + height - 5), 2)

    @staticmethod
    def draw_snowflake_icon(screen, x, y, size, alpha=150):
        """Draw a decorative snowflake icon"""
        color = (200, 230, 255)
        alpha_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        center = (size, size)

        for angle in range(0, 360, 60):
            rad = math.radians(angle)
            end_x = center[0] + size * math.cos(rad)
            end_y = center[1] + size * math.sin(rad)
            pygame.draw.line(alpha_surface, color, center, (int(end_x), int(end_y)), 3)

            branch_size = size * 0.4
            for branch_angle in [-30, 30]:
                branch_rad = math.radians(angle + branch_angle)
                branch_start_x = center[0] + size * 0.6 * math.cos(rad)
                branch_start_y = center[1] + size * 0.6 * math.sin(rad)
                branch_end_x = branch_start_x + branch_size * math.cos(branch_rad)
                branch_end_y = branch_start_y + branch_size * math.sin(branch_rad)
                pygame.draw.line(alpha_surface, color,
                               (int(branch_start_x), int(branch_start_y)),
                               (int(branch_end_x), int(branch_end_y)), 2)

        pygame.draw.circle(alpha_surface, color, center, 4)
        alpha_surface.set_alpha(alpha)
        screen.blit(alpha_surface, (x - size, y - size))

    @staticmethod
    def draw_text_with_shadow(screen, font, text, color, x, y, center=True):
        """Draw text with a subtle shadow effect"""
        # Shadow
        shadow_surface = font.render(text, True, (0, 0, 0))
        if center:
            shadow_rect = shadow_surface.get_rect(center=(x + 3, y + 3))
        else:
            shadow_rect = (x + 3, y + 3)
        screen.blit(shadow_surface, shadow_rect)

        # Main text
        text_surface = font.render(text, True, color)
        if center:
            text_rect = text_surface.get_rect(center=(x, y))
        else:
            text_rect = (x, y)
        screen.blit(text_surface, text_rect)
