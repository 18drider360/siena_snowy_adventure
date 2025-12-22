"""
Scoreboard Display Screen
Shows high scores for each level with beautiful winter theme
"""

import pygame
import random
import threading
from src.utils.save_system import SaveSystem
from src.utils.progression import LevelManager
from src.utils.secure_leaderboard import get_secure_leaderboard


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
        self.difficulties = ["All", "Easy", "Medium", "Hard"]
        self.current_difficulty = 0  # Index into difficulties list (0 = "All")
        self.checkpoints_filter = ["All", "Off", "On"]
        self.current_checkpoints = 0  # Index into checkpoints_filter list (0 = "All")
        self.scroll_offset = 0  # Track scroll position for viewing more than 10 scores

        # Online leaderboard integration (using secure REST API)
        self.online_leaderboard = get_secure_leaderboard()
        self.is_online_available = self.online_leaderboard.is_available()
        # Default to online if available, otherwise local
        self.view_mode = "online" if self.is_online_available else "local"
        self.online_scores = []
        self.loading_online = False
        self.loading_spinner_angle = 0

        # Load online scores immediately if starting in online mode
        if self.view_mode == "online":
            self.load_online_scores()

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

        # Load select sounds (hover and click)
        from src.utils import settings as S
        self.select_sound = None
        self.select_click_sound = None
        if S.MASTER_AUDIO_ENABLED:
            try:
                self.select_sound = pygame.mixer.Sound("assets/sounds/select_fast.wav")
                self.select_sound.set_volume(0.4)
            except (FileNotFoundError, pygame.error):
                pass
            try:
                self.select_click_sound = pygame.mixer.Sound("assets/sounds/select_click.wav")
                self.select_click_sound.set_volume(0.4)
            except (FileNotFoundError, pygame.error):
                pass

    def play_select_sound(self, volume=0.3, use_click=False):
        """Play the select sound effect with specified volume

        Args:
            volume: Volume level (0.0 to 1.0)
            use_click: If True, use higher-pitched click sound; if False, use hover sound
        """
        sound = self.select_click_sound if use_click else self.select_sound
        if sound:
            try:
                sound.set_volume(volume)
                sound.play()
            except pygame.error:
                pass

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

    def get_difficulty_arrow_at_pos(self, pos):
        """Get which difficulty arrow (if any) is at the given mouse position"""
        screen_width = self.screen.get_width()
        diff_box_width = 300
        diff_box_height = 50
        diff_box_x = screen_width - diff_box_width - 40
        diff_box_y = 90

        arrow_size = 30

        # Up arrow region
        up_arrow_rect = pygame.Rect(
            diff_box_x + (diff_box_width - arrow_size) // 2,
            diff_box_y - arrow_size - 5,
            arrow_size,
            arrow_size
        )
        if up_arrow_rect.collidepoint(pos):
            return "UP"

        # Down arrow region
        down_arrow_rect = pygame.Rect(
            diff_box_x + (diff_box_width - arrow_size) // 2,
            diff_box_y + diff_box_height + 5,
            arrow_size,
            arrow_size
        )
        if down_arrow_rect.collidepoint(pos):
            return "DOWN"

        # Check if clicking inside the difficulty box itself (cycle through on click)
        diff_box_rect = pygame.Rect(diff_box_x, diff_box_y, diff_box_width, diff_box_height)
        if diff_box_rect.collidepoint(pos):
            return "CYCLE"

        return None

    def get_checkpoints_box_at_pos(self, pos):
        """Check if the given position is inside the checkpoints box"""
        screen_width = self.screen.get_width()
        diff_box_width = 300
        diff_box_height = 50
        diff_box_x = screen_width - diff_box_width - 40
        diff_box_y = 90

        chkpt_box_width = 220
        chkpt_box_height = 60
        chkpt_box_x = screen_width - chkpt_box_width - 40
        chkpt_box_y = diff_box_y + diff_box_height + 50

        chkpt_box_rect = pygame.Rect(chkpt_box_x, chkpt_box_y, chkpt_box_width, chkpt_box_height)
        if chkpt_box_rect.collidepoint(pos):
            return True
        return False

    def get_view_mode_box_at_pos(self, pos):
        """Check if the given position is inside the view mode toggle box"""
        box_width = 180
        box_height = 50
        box_x = 40
        box_y = 90
        box_rect = pygame.Rect(box_x, box_y, box_width, box_height)
        return box_rect.collidepoint(pos)

    def toggle_view_mode(self):
        """Toggle between local and online view modes"""
        if not self.is_online_available:
            return  # Can't switch to online if not available

        if self.view_mode == "local":
            self.view_mode = "online"
            self.scroll_offset = 0
            self.load_online_scores()
        else:
            self.view_mode = "local"
            self.scroll_offset = 0

    def load_online_scores(self):
        """Load scores from online leaderboard in a background thread"""
        if self.loading_online:
            return  # Already loading

        self.loading_online = True
        self.online_scores = []

        def fetch_scores():
            try:
                difficulty = self.difficulties[self.current_difficulty]
                checkpoints = self.checkpoints_filter[self.current_checkpoints]
                scores = self.online_leaderboard.get_leaderboard(
                    self.current_level,
                    difficulty=difficulty,
                    checkpoints_filter=checkpoints,
                    limit=100
                )
                self.online_scores = scores
            except Exception as e:
                print(f"Failed to load online scores: {e}")
                self.online_scores = []
            finally:
                self.loading_online = False

        thread = threading.Thread(target=fetch_scores, daemon=True)
        thread.start()

    def handle_event(self, event):
        """Handle keyboard and mouse input"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                self.play_select_sound(use_click=True)  # Click sound for exiting
                return True
            elif event.key == pygame.K_t:
                # Toggle between local and online view modes
                if self.is_online_available:
                    self.toggle_view_mode()
                    self.play_select_sound(use_click=True)
            elif event.key == pygame.K_LEFT:
                self.current_level = max(1, self.current_level - 1)
                self.scroll_offset = 0  # Reset scroll when changing levels
                if self.view_mode == "online":
                    self.load_online_scores()
                self.play_select_sound(volume=0.08)  # Hover sound for navigation
            elif event.key == pygame.K_RIGHT:
                self.current_level = min(self.max_levels, self.current_level + 1)
                self.scroll_offset = 0  # Reset scroll when changing levels
                if self.view_mode == "online":
                    self.load_online_scores()
                self.play_select_sound(volume=0.08)  # Hover sound for navigation
            elif event.key in (pygame.K_UP, pygame.K_w):
                self.current_difficulty = (self.current_difficulty - 1) % len(self.difficulties)
                self.scroll_offset = 0  # Reset scroll when changing difficulty
                if self.view_mode == "online":
                    self.load_online_scores()
                self.play_select_sound(volume=0.08)  # Hover sound for navigation
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.current_difficulty = (self.current_difficulty + 1) % len(self.difficulties)
                self.scroll_offset = 0  # Reset scroll when changing difficulty
                if self.view_mode == "online":
                    self.load_online_scores()
                self.play_select_sound(volume=0.08)  # Hover sound for navigation
            elif event.key in (pygame.K_q,):
                self.current_checkpoints = (self.current_checkpoints - 1) % len(self.checkpoints_filter)
                self.scroll_offset = 0  # Reset scroll when changing checkpoint filter
                if self.view_mode == "online":
                    self.load_online_scores()
                self.play_select_sound(volume=0.08)  # Hover sound for navigation
            elif event.key in (pygame.K_e,):
                self.current_checkpoints = (self.current_checkpoints + 1) % len(self.checkpoints_filter)
                self.scroll_offset = 0  # Reset scroll when changing checkpoint filter
                if self.view_mode == "online":
                    self.load_online_scores()
                self.play_select_sound(volume=0.08)  # Hover sound for navigation
        elif event.type == pygame.MOUSEWHEEL:
            # Handle trackpad/mouse wheel scrolling (Mac/modern mice)
            mouse_pos = pygame.mouse.get_pos()
            is_hovering = self.is_hovering_scoreboard(mouse_pos)
            if is_hovering:
                # event.y > 0 is scroll up, event.y < 0 is scroll down
                if event.y > 0:  # Scroll up
                    self.scroll_offset = max(0, self.scroll_offset - 1)
                elif event.y < 0:  # Scroll down
                    self.scroll_offset += 1
                return False  # Don't exit to main menu
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # Handle old-style mouse wheel scrolling (Linux/older mice)
            if event.button == 4:  # Scroll up
                if self.is_hovering_scoreboard(mouse_pos):
                    self.scroll_offset = max(0, self.scroll_offset - 1)
                    return False  # Don't exit to main menu
            elif event.button == 5:  # Scroll down
                if self.is_hovering_scoreboard(mouse_pos):
                    self.scroll_offset += 1
                    return False  # Don't exit to main menu

            # Check if clicking on view mode toggle box
            if self.get_view_mode_box_at_pos(mouse_pos):
                if self.is_online_available:
                    self.toggle_view_mode()
                    self.play_select_sound(use_click=True)
            else:
                arrow = self.get_arrow_at_pos(mouse_pos)
                if arrow == "LEFT":
                    self.current_level = max(1, self.current_level - 1)
                    self.scroll_offset = 0  # Reset scroll when changing levels
                    if self.view_mode == "online":
                        self.load_online_scores()
                    self.play_select_sound(volume=0.08)  # Hover sound for arrow navigation
                elif arrow == "RIGHT":
                    self.current_level = min(self.max_levels, self.current_level + 1)
                    self.scroll_offset = 0  # Reset scroll when changing levels
                    if self.view_mode == "online":
                        self.load_online_scores()
                    self.play_select_sound(volume=0.08)  # Hover sound for arrow navigation
                else:
                    # Check if clicking on difficulty filter
                    diff_arrow = self.get_difficulty_arrow_at_pos(mouse_pos)
                    if diff_arrow == "UP":
                        self.current_difficulty = (self.current_difficulty - 1) % len(self.difficulties)
                        self.scroll_offset = 0  # Reset scroll when changing difficulty
                        if self.view_mode == "online":
                            self.load_online_scores()
                        self.play_select_sound(volume=0.08)  # Hover sound for navigation
                    elif diff_arrow == "DOWN":
                        self.current_difficulty = (self.current_difficulty + 1) % len(self.difficulties)
                        self.scroll_offset = 0  # Reset scroll when changing difficulty
                        if self.view_mode == "online":
                            self.load_online_scores()
                        self.play_select_sound(volume=0.08)  # Hover sound for navigation
                    elif diff_arrow == "CYCLE":
                        # Clicking the box itself cycles through difficulties
                        self.current_difficulty = (self.current_difficulty + 1) % len(self.difficulties)
                        self.scroll_offset = 0  # Reset scroll when changing difficulty
                        if self.view_mode == "online":
                            self.load_online_scores()
                        self.play_select_sound(volume=0.08)  # Hover sound for navigation
                    else:
                        # Check if clicking on checkpoints filter box
                        if self.get_checkpoints_box_at_pos(mouse_pos):
                            # Cycle through checkpoint filters
                            self.current_checkpoints = (self.current_checkpoints + 1) % len(self.checkpoints_filter)
                            self.scroll_offset = 0  # Reset scroll when changing checkpoints
                            if self.view_mode == "online":
                                self.load_online_scores()
                            self.play_select_sound(volume=0.08)  # Hover sound for navigation
                        else:
                            # Click anywhere else to go back (but not if scrolling over scoreboard)
                            if not self.is_hovering_scoreboard(mouse_pos):
                                self.play_select_sound(use_click=True)  # Click sound for exit
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

    def is_hovering_view_mode_box(self, pos):
        """Check if mouse is hovering over the view mode toggle box"""
        box_width = 180
        box_height = 50
        box_x = 40
        box_y = 90
        box_rect = pygame.Rect(box_x, box_y, box_width, box_height)
        return box_rect.collidepoint(pos)

    def is_hovering_difficulty_box(self, pos):
        """Check if mouse is hovering over the difficulty box"""
        screen_width = self.screen.get_width()
        diff_box_width = 300
        diff_box_height = 50
        diff_box_x = screen_width - diff_box_width - 40
        diff_box_y = 90
        diff_box_rect = pygame.Rect(diff_box_x, diff_box_y, diff_box_width, diff_box_height)
        return diff_box_rect.collidepoint(pos)

    def is_hovering_checkpoints_box(self, pos):
        """Check if mouse is hovering over the checkpoints box"""
        screen_width = self.screen.get_width()
        diff_box_width = 300
        diff_box_height = 50
        diff_box_x = screen_width - diff_box_width - 40
        diff_box_y = 90

        chkpt_box_width = 220
        chkpt_box_height = 60
        chkpt_box_x = screen_width - chkpt_box_width - 40
        chkpt_box_y = diff_box_y + diff_box_height + 50
        chkpt_box_rect = pygame.Rect(chkpt_box_x, chkpt_box_y, chkpt_box_width, chkpt_box_height)
        return chkpt_box_rect.collidepoint(pos)

    def is_hovering_scoreboard(self, pos):
        """Check if mouse is hovering over the scoreboard area"""
        # Mouse position is in display coordinates, need to convert to render coordinates
        from src.utils import settings as S
        scaled_x = int(pos[0] / S.DISPLAY_SCALE) if hasattr(S, 'DISPLAY_SCALE') else pos[0]
        scaled_y = int(pos[1] / S.DISPLAY_SCALE) if hasattr(S, 'DISPLAY_SCALE') else pos[1]
        scaled_pos = (scaled_x, scaled_y)

        screen_width = self.screen.get_width()
        scores_box_width = 650
        scores_box_height = 380
        scores_box_x = (screen_width - scores_box_width) // 2
        scores_box_y = 160
        scores_box_rect = pygame.Rect(scores_box_x, scores_box_y, scores_box_width, scores_box_height)
        return scores_box_rect.collidepoint(scaled_pos)

    def draw_loading_spinner(self, x, y, radius=20):
        """Draw an animated loading spinner"""
        import math
        self.loading_spinner_angle = (self.loading_spinner_angle + 8) % 360

        # Draw multiple arcs to create a spinner effect
        for i in range(8):
            angle = (self.loading_spinner_angle + i * 45) % 360
            alpha = 255 - (i * 30)  # Fade out the trailing segments
            color = (150, 200, 255, alpha)

            # Calculate arc endpoints
            start_angle = math.radians(angle)
            end_angle = math.radians(angle + 30)

            # Draw arc segment
            points = [(x, y)]
            for a in range(int(angle), int(angle + 30), 5):
                rad = math.radians(a)
                px = x + radius * math.cos(rad)
                py = y + radius * math.sin(rad)
                points.append((int(px), int(py)))

            if len(points) > 2:
                try:
                    pygame.draw.polygon(self.screen, color[:3], points)
                except:
                    pass

        # Draw center circle
        pygame.draw.circle(self.screen, (200, 230, 255), (x, y), radius // 3)

    def draw(self):
        """Draw the scoreboard screen with winter theme"""
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        # Check if hovering over difficulty box or checkpoints box
        mouse_pos = pygame.mouse.get_pos()
        is_hovering = self.is_hovering_difficulty_box(mouse_pos)
        is_hovering_checkpoints = self.is_hovering_checkpoints_box(mouse_pos)
        is_hovering_view_mode = self.is_hovering_view_mode_box(mouse_pos)

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

        # Draw view mode toggle box (top left)
        view_box_width = 180
        view_box_height = 50
        view_box_x = 40
        view_box_y = 90

        # Determine if clickable (only if online is available)
        view_box_alpha = 200 if (is_hovering_view_mode and self.is_online_available) else 160
        if not self.is_online_available:
            view_box_alpha = 100  # Dimmed if offline

        self.draw_frosted_box(view_box_x, view_box_y, view_box_width, view_box_height, view_box_alpha)

        # View mode label
        mode_text = "LOCAL" if self.view_mode == "local" else "ONLINE"
        mode_color = (10, 30, 70) if self.is_online_available else (100, 100, 100)
        mode_surface = self.level_font.render(mode_text, True, mode_color)
        mode_rect = mode_surface.get_rect(center=(view_box_x + view_box_width // 2, view_box_y + view_box_height // 2))
        self.screen.blit(mode_surface, mode_rect)

        # Connection status indicator (small text below)
        status_y = view_box_y + view_box_height + 8
        if self.is_online_available:
            status_text = "Online ✓"
            status_color = (50, 150, 50)
        else:
            status_text = "Offline"
            status_color = (150, 50, 50)
        status_surface = self.score_font.render(status_text, True, status_color)
        status_rect = status_surface.get_rect(center=(view_box_x + view_box_width // 2, status_y))
        self.screen.blit(status_surface, status_rect)

        # Add click hint when hovering and online is available
        if is_hovering_view_mode and self.is_online_available:
            hint_text = self.score_font.render("(click to toggle)", True, (80, 120, 160))
            hint_rect = hint_text.get_rect(center=(view_box_x + view_box_width // 2, status_y + 20))
            self.screen.blit(hint_text, hint_rect)

        # Draw difficulty filter box (top right)
        diff_box_width = 300
        diff_box_height = 50
        diff_box_x = screen_width - diff_box_width - 40
        diff_box_y = 90

        # Use brighter alpha if hovering to indicate clickability
        box_alpha = 200 if is_hovering else 160
        self.draw_frosted_box(diff_box_x, diff_box_y, diff_box_width, diff_box_height, box_alpha)

        # Difficulty filter text
        label_color = (10, 30, 70) if is_hovering else (20, 40, 80)
        diff_label = self.score_font.render("DIFFICULTY:", True, label_color)
        diff_label_rect = diff_label.get_rect(center=(diff_box_x + diff_box_width // 2, diff_box_y + 18))
        self.screen.blit(diff_label, diff_label_rect)

        value_color = (10, 30, 70) if is_hovering else (20, 40, 80)
        current_diff_text = self.difficulties[self.current_difficulty]
        diff_value = self.level_font.render(current_diff_text, True, value_color)
        diff_value_rect = diff_value.get_rect(center=(diff_box_x + diff_box_width // 2, diff_box_y + 35))
        self.screen.blit(diff_value, diff_value_rect)

        # Add click hint when hovering
        if is_hovering:
            hint_text = self.score_font.render("(click to cycle)", True, (80, 120, 160))
            hint_rect = hint_text.get_rect(center=(diff_box_x + diff_box_width // 2, diff_box_y + diff_box_height + 35))
            self.screen.blit(hint_text, hint_rect)

        # Up/Down arrows for difficulty
        arrow_color = (20, 40, 80)
        arrow_size = 15
        center_x = diff_box_x + diff_box_width // 2

        # Up arrow
        up_arrow_y = diff_box_y - arrow_size - 10
        up_arrow_points = [
            (center_x, up_arrow_y),
            (center_x - arrow_size, up_arrow_y + arrow_size),
            (center_x + arrow_size, up_arrow_y + arrow_size)
        ]
        pygame.draw.polygon(self.screen, arrow_color, up_arrow_points)

        # Down arrow
        down_arrow_y = diff_box_y + diff_box_height + 10
        down_arrow_points = [
            (center_x, down_arrow_y + arrow_size),
            (center_x - arrow_size, down_arrow_y),
            (center_x + arrow_size, down_arrow_y)
        ]
        pygame.draw.polygon(self.screen, arrow_color, down_arrow_points)

        # Draw checkpoints filter box (below difficulty)
        chkpt_box_width = 220
        chkpt_box_height = 60
        chkpt_box_x = screen_width - chkpt_box_width - 40
        chkpt_box_y = diff_box_y + diff_box_height + 50  # Below difficulty box

        # Use brighter alpha if hovering to indicate clickability
        chkpt_box_alpha = 200 if is_hovering_checkpoints else 160
        self.draw_frosted_box(chkpt_box_x, chkpt_box_y, chkpt_box_width, chkpt_box_height, chkpt_box_alpha)

        # Checkpoints filter text
        chkpt_label_color = (10, 30, 70) if is_hovering_checkpoints else (20, 40, 80)
        chkpt_label = self.score_font.render("CHECKPOINTS:", True, chkpt_label_color)
        chkpt_label_rect = chkpt_label.get_rect(center=(chkpt_box_x + chkpt_box_width // 2, chkpt_box_y + 18))
        self.screen.blit(chkpt_label, chkpt_label_rect)

        chkpt_value_color = (10, 30, 70) if is_hovering_checkpoints else (20, 40, 80)
        current_chkpt_text = self.checkpoints_filter[self.current_checkpoints]
        chkpt_value = self.level_font.render(current_chkpt_text, True, chkpt_value_color)
        chkpt_value_rect = chkpt_value.get_rect(center=(chkpt_box_x + chkpt_box_width // 2, chkpt_box_y + 38))
        self.screen.blit(chkpt_value, chkpt_value_rect)

        # Add click hint when hovering
        if is_hovering_checkpoints:
            hint_text = self.score_font.render("(click to cycle)", True, (80, 120, 160))
            hint_rect = hint_text.get_rect(center=(chkpt_box_x + chkpt_box_width // 2, chkpt_box_y + chkpt_box_height + 35))
            self.screen.blit(hint_text, hint_rect)

        # Get leaderboard based on view mode
        if self.view_mode == "online":
            # Use online scores
            leaderboard = self.online_scores
        else:
            # Use local scores
            leaderboard = SaveSystem.get_leaderboard(self.current_level)

            # Filter scores by difficulty if not "All"
            if self.current_difficulty > 0:  # 0 is "All"
                selected_difficulty = self.difficulties[self.current_difficulty]
                leaderboard = [score for score in leaderboard if score.get('difficulty', 'Medium') == selected_difficulty]

            # Filter scores by checkpoints if not "All"
            if self.current_checkpoints > 0:  # 0 is "All"
                checkpoints_enabled = (self.current_checkpoints == 2)  # 1="Off", 2="On"
                leaderboard = [score for score in leaderboard if score.get('checkpoints', False) == checkpoints_enabled]

        # Draw scores in frosted box (widened for checkpoints column)
        scores_box_width = 780
        scores_box_height = 380
        scores_box_x = (screen_width - scores_box_width) // 2
        scores_box_y = 160

        self.draw_frosted_box(scores_box_x, scores_box_y, scores_box_width, scores_box_height, 170)

        # Column headers (adjusted for wider username column)
        header_y = scores_box_y + 20
        headers = [
            ("RANK", 30),
            ("NAME", 100),
            ("TIME", 340),
            ("COINS", 470),
            ("DIFF", 580),
            ("CHKPT", 690)
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
        max_visible_rows = 10

        # Show loading spinner if loading online scores
        if self.loading_online:
            spinner_x = screen_width // 2
            spinner_y = start_y + 100
            self.draw_loading_spinner(spinner_x, spinner_y, 25)

            loading_text = self.score_font.render("Loading online scores...", True, self.ice_blue)
            loading_rect = loading_text.get_rect(center=(screen_width // 2, spinner_y + 50))
            self.screen.blit(loading_text, loading_rect)
        elif not leaderboard:
            no_scores = self.score_font.render("NO SCORES YET! BE THE FIRST!", True, self.snow_white)
            no_scores_rect = no_scores.get_rect(center=(screen_width // 2, start_y + 100))
            self.screen.blit(no_scores, no_scores_rect)
        else:
            # Clamp scroll offset to valid range
            max_scroll = max(0, len(leaderboard) - max_visible_rows)
            self.scroll_offset = max(0, min(self.scroll_offset, max_scroll))

            # Determine which scores to show based on scroll offset
            visible_scores = leaderboard[self.scroll_offset:self.scroll_offset + max_visible_rows]

            for display_index, score in enumerate(visible_scores):
                actual_rank = self.scroll_offset + display_index  # Actual rank in full leaderboard
                y = start_y + (display_index * row_height)

                # Rank color based on actual rank
                if actual_rank == 0:
                    rank_color = self.gold_color
                elif actual_rank == 1:
                    rank_color = self.silver_color
                elif actual_rank == 2:
                    rank_color = self.bronze_color
                else:
                    rank_color = (20, 40, 80)

                # Draw rank (using actual rank, not display index)
                rank_text = self.score_font.render(f"#{actual_rank + 1}", True, rank_color)
                self.screen.blit(rank_text, (scores_box_x + 30, y))

                # Draw username (up to 20 characters)
                username_text = self.score_font.render(score['username'][:20], True, (20, 40, 80))
                self.screen.blit(username_text, (scores_box_x + 100, y))

                # Draw time (moved right to accommodate longer usernames)
                time_str = self.format_time(score['time'])
                time_text = self.score_font.render(time_str, True, (20, 40, 80))
                self.screen.blit(time_text, (scores_box_x + 340, y))

                # Draw coins (moved right to match)
                coins_text = self.score_font.render(str(score['coins']), True, (20, 40, 80))
                self.screen.blit(coins_text, (scores_box_x + 470, y))

                # Draw difficulty (default to "Medium" for old scores)
                difficulty = score.get('difficulty', 'Medium')
                # Shorten difficulty names for display
                diff_short = difficulty[0]  # E, M, or H
                diff_text = self.score_font.render(diff_short, True, (20, 40, 80))
                self.screen.blit(diff_text, (scores_box_x + 580, y))

                # Draw checkpoints (default to False for old scores)
                checkpoints = score.get('checkpoints', False)
                checkpoint_text = "On" if checkpoints else "Off"
                chkpt_text = self.score_font.render(checkpoint_text, True, (20, 40, 80))
                self.screen.blit(chkpt_text, (scores_box_x + 690, y))

            # Draw scroll indicator below the scoreboard box if there are more scores
            if len(leaderboard) > max_visible_rows:
                indicator_y = scores_box_y + scores_box_height + 25  # 25 pixels below the box
                indicator_text = f"Showing {self.scroll_offset + 1}-{min(self.scroll_offset + max_visible_rows, len(leaderboard))} of {len(leaderboard)}"
                indicator_surface = self.score_font.render(indicator_text, True, (80, 120, 160))
                indicator_rect = indicator_surface.get_rect(center=(screen_width // 2, indicator_y))
                self.screen.blit(indicator_surface, indicator_rect)

        # Draw hints at bottom
        hint_y = screen_height - 40
        if self.is_online_available:
            hints = [
                "< / > : LEVEL     UP / DOWN : DIFFICULTY     Q / E : CHECKPOINTS     T : TOGGLE VIEW     ESC : BACK"
            ]
        else:
            hints = [
                "< / > : LEVEL     UP / DOWN : DIFFICULTY     Q / E : CHECKPOINTS     ESC / ENTER : BACK"
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
