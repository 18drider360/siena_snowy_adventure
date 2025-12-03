"""
Scoreboard Display Screen
Shows high scores for each level with beautiful winter theme
"""

import pygame
import random
from utils.save_system import SaveSystem
from utils.progression import LevelManager


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


class ScoreboardScreen:
    """Displays high scores for all levels with winter theme"""

    def __init__(self, screen):
        self.screen = screen
        self.current_level = 1
        self.max_levels = len(LevelManager.LEVELS)

        # Wintery color palette
        self.bg_gradient_top = (15, 30, 60)
        self.bg_gradient_bottom = (40, 70, 120)
        self.snow_white = (255, 255, 255)
        self.ice_blue = (180, 220, 255)
        self.frost_blue = (200, 230, 255)
        self.glow_blue = (150, 200, 255)
        self.gold_color = (255, 215, 0)
        self.silver_color = (192, 192, 192)
        self.bronze_color = (205, 127, 50)

        # Fonts
        try:
            self.title_font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 36)
            self.level_font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 20)  # Reduced from 24
            self.header_font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 14)  # Reduced from 16
            self.score_font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 12)  # Reduced from 14
            self.hint_font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 12)
        except:
            self.title_font = pygame.font.Font(None, 54)
            self.level_font = pygame.font.Font(None, 32)
            self.header_font = pygame.font.Font(None, 22)
            self.score_font = pygame.font.Font(None, 18)
            self.hint_font = pygame.font.Font(None, 18)

        # Create snowflakes
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        self.snowflakes = [Snowflake(screen_width, screen_height) for _ in range(80)]

    def get_arrow_at_pos(self, pos):
        """Get which arrow (if any) is at the given mouse position"""
        screen_width = self.screen.get_width()
        level_box_width = 600
        level_box_height = 50
        level_box_x = (screen_width - level_box_width) // 2
        level_box_y = 90

        # Create clickable regions for arrows (larger than visual arrows for easier clicking)
        arrow_size = 40

        # Left arrow region
        if self.current_level > 1:
            left_arrow_rect = pygame.Rect(
                level_box_x + 10,
                level_box_y + (level_box_height - arrow_size) // 2,
                arrow_size,
                arrow_size
            )
            if left_arrow_rect.collidepoint(pos):
                return "LEFT"

        # Right arrow region
        if self.current_level < self.max_levels:
            right_arrow_rect = pygame.Rect(
                level_box_x + level_box_width - 50,
                level_box_y + (level_box_height - arrow_size) // 2,
                arrow_size,
                arrow_size
            )
            if right_arrow_rect.collidepoint(pos):
                return "RIGHT"

        return None

    def handle_event(self, event):
        """Handle keyboard and mouse input"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                return True
            elif event.key == pygame.K_LEFT:
                self.current_level = max(1, self.current_level - 1)
            elif event.key == pygame.K_RIGHT:
                self.current_level = min(self.max_levels, self.current_level + 1)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            arrow = self.get_arrow_at_pos(mouse_pos)
            if arrow == "LEFT":
                self.current_level = max(1, self.current_level - 1)
            elif arrow == "RIGHT":
                self.current_level = min(self.max_levels, self.current_level + 1)
            else:
                # Click anywhere else to go back
                return True
        return False

    def format_time(self, frames):
        """Convert frame count to time string"""
        total_seconds = frames / 60.0
        minutes = int(total_seconds // 60)
        seconds = int(total_seconds % 60)
        milliseconds = int((total_seconds % 1) * 100)
        return f"{minutes:02d}:{seconds:02d}.{milliseconds:02d}"

    def draw_gradient_background(self):
        """Draw a beautiful gradient background"""
        screen_height = self.screen.get_height()
        for y in range(screen_height):
            ratio = y / screen_height
            r = int(self.bg_gradient_top[0] + (self.bg_gradient_bottom[0] - self.bg_gradient_top[0]) * ratio)
            g = int(self.bg_gradient_top[1] + (self.bg_gradient_bottom[1] - self.bg_gradient_top[1]) * ratio)
            b = int(self.bg_gradient_top[2] + (self.bg_gradient_bottom[2] - self.bg_gradient_top[2]) * ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (self.screen.get_width(), y))

    def draw_frosted_box(self, x, y, width, height, alpha=180):
        """Draw a frosted glass effect box"""
        # Shadow
        shadow = pygame.Surface((width + 8, height + 8))
        shadow.fill((0, 0, 0))
        shadow.set_alpha(60)
        self.screen.blit(shadow, (x + 4, y + 4))

        # Main box
        box_surface = pygame.Surface((width, height))
        box_surface.fill(self.frost_blue)
        box_surface.set_alpha(alpha)
        self.screen.blit(box_surface, (x, y))

        # Border
        border_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, self.glow_blue, border_rect, 3)

        # Highlight
        pygame.draw.line(self.screen, (255, 255, 255), (x + 5, y + 5), (x + width - 5, y + 5), 2)
        pygame.draw.line(self.screen, (255, 255, 255), (x + 5, y + 5), (x + 5, y + height - 5), 2)

    def draw_snowflake_icon(self, x, y, size):
        """Draw a decorative snowflake icon"""
        import math
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
        alpha_surface.set_alpha(150)
        self.screen.blit(alpha_surface, (x - size, y - size))

    def draw(self):
        """Draw the scoreboard screen with winter theme"""
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        # Update and draw snowflakes
        for snowflake in self.snowflakes:
            snowflake.update()

        # Draw gradient background
        self.draw_gradient_background()

        # Draw snowflakes
        for snowflake in self.snowflakes:
            snowflake.draw(self.screen)

        # Draw decorative snowflakes
        for pos in [(80, 80), (screen_width - 80, 80)]:
            self.draw_snowflake_icon(pos[0], pos[1], 25)

        # Draw title with shadow
        title_text = "SCOREBOARD"
        title_shadow = self.title_font.render(title_text, True, (0, 0, 0))
        shadow_rect = title_shadow.get_rect(center=(screen_width // 2 + 3, 43))
        self.screen.blit(title_shadow, shadow_rect)

        title_surface = self.title_font.render(title_text, True, self.snow_white)
        title_rect = title_surface.get_rect(center=(screen_width // 2, 40))
        self.screen.blit(title_surface, title_rect)

        # Draw level selector in frosted box
        level_box_width = 600
        level_box_height = 50
        level_box_x = (screen_width - level_box_width) // 2
        level_box_y = 90

        self.draw_frosted_box(level_box_x, level_box_y, level_box_width, level_box_height, 160)

        # Level name - just show the world identifier (e.g., "1-4 Northern Lights")
        level_name = LevelManager.get_level_name(self.current_level)
        world_id = LevelManager.get_level_world(self.current_level)
        level_text = f"{world_id} {level_name.upper()}"
        level_surface = self.level_font.render(level_text, True, (20, 40, 80))
        level_rect = level_surface.get_rect(center=(screen_width // 2, level_box_y + level_box_height // 2))
        self.screen.blit(level_surface, level_rect)

        # Navigation arrows
        if self.current_level > 1:
            left_arrow = self.header_font.render("<", True, (20, 40, 80))
            left_rect = left_arrow.get_rect(midright=(level_box_x + 30, level_box_y + level_box_height // 2))
            self.screen.blit(left_arrow, left_rect)

        if self.current_level < self.max_levels:
            right_arrow = self.header_font.render(">", True, (20, 40, 80))
            right_rect = right_arrow.get_rect(midleft=(level_box_x + level_box_width - 30, level_box_y + level_box_height // 2))
            self.screen.blit(right_arrow, right_rect)

        # Get leaderboard
        leaderboard = SaveSystem.get_leaderboard(self.current_level)

        # Draw scores in frosted box
        scores_box_width = 650
        scores_box_height = 380
        scores_box_x = (screen_width - scores_box_width) // 2
        scores_box_y = 160

        self.draw_frosted_box(scores_box_x, scores_box_y, scores_box_width, scores_box_height, 170)

        # Column headers
        header_y = scores_box_y + 20
        headers = [
            ("RANK", 50),
            ("NAME", 140),
            ("TIME", 370),
            ("COINS", 520)
        ]

        for text, x_offset in headers:
            header_surface = self.header_font.render(text, True, (20, 40, 80))
            self.screen.blit(header_surface, (scores_box_x + x_offset, header_y))

        # Separator line
        pygame.draw.line(self.screen, self.glow_blue,
                        (scores_box_x + 20, header_y + 30),
                        (scores_box_x + scores_box_width - 20, header_y + 30), 2)

        # Draw scores or empty message
        start_y = header_y + 50
        row_height = 32

        if not leaderboard:
            no_scores = self.score_font.render("NO SCORES YET! BE THE FIRST!", True, self.snow_white)
            no_scores_rect = no_scores.get_rect(center=(screen_width // 2, start_y + 100))
            self.screen.blit(no_scores, no_scores_rect)
        else:
            for i, score in enumerate(leaderboard[:10]):
                y = start_y + (i * row_height)

                # Rank color
                if i == 0:
                    rank_color = self.gold_color
                elif i == 1:
                    rank_color = self.silver_color
                elif i == 2:
                    rank_color = self.bronze_color
                else:
                    rank_color = (20, 40, 80)

                # Draw rank
                rank_text = self.score_font.render(f"#{i+1}", True, rank_color)
                self.screen.blit(rank_text, (scores_box_x + 50, y))

                # Draw username
                username_text = self.score_font.render(score['username'][:15], True, (20, 40, 80))
                self.screen.blit(username_text, (scores_box_x + 140, y))

                # Draw time
                time_str = self.format_time(score['time'])
                time_text = self.score_font.render(time_str, True, (20, 40, 80))
                self.screen.blit(time_text, (scores_box_x + 370, y))

                # Draw coins
                coins_text = self.score_font.render(str(score['coins']), True, (20, 40, 80))
                self.screen.blit(coins_text, (scores_box_x + 520, y))

        # Draw hints at bottom
        hint_y = screen_height - 40
        hints = [
            "< / > : CHANGE LEVEL     ESC / ENTER : BACK"
        ]

        for hint in hints:
            hint_surface = self.hint_font.render(hint, True, self.ice_blue)
            hint_rect = hint_surface.get_rect(center=(screen_width // 2, hint_y))
            self.screen.blit(hint_surface, hint_rect)


def show_scoreboard(screen):
    """Show the scoreboard screen"""
    scoreboard = ScoreboardScreen(screen)
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if scoreboard.handle_event(event):
                return

        scoreboard.draw()
        pygame.display.flip()
        clock.tick(60)
