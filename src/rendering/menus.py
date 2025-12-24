import pygame
from src.utils import settings as S

class PauseMenu:
    """Pause menu overlay during gameplay"""

    def __init__(self):
        # Menu options
        self.options = ["CONTINUE", "RESTART", "MAIN MENU"]
        self.selected_index = 0
        self.previous_selected_index = 0  # Track for hover sound

        # Load fonts
        try:
            self.title_font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 32)
            self.menu_font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 20)
        except:
            self.title_font = pygame.font.Font(None, 56)
            self.menu_font = pygame.font.Font(None, 40)

        # Load select sounds (hover and click)
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

        # Animation
        self.blink_timer = 0
        self.show_cursor = True

    def get_option_at_pos(self, pos):
        """Get the menu option index at the given mouse position"""
        box_width = 500
        box_height = 400
        box_x = (S.WINDOW_WIDTH - box_width) // 2
        box_y = (S.WINDOW_HEIGHT - box_height) // 2

        menu_y_start = box_y + 180
        menu_spacing = 60

        for i, option in enumerate(self.options):
            y_pos = menu_y_start + (i * menu_spacing)

            # Create clickable rect for each option
            text = self.menu_font.render(option, True, (255, 255, 255))
            text_rect = text.get_rect(center=(S.WINDOW_WIDTH // 2, y_pos))

            # Expand clickable area
            click_rect = text_rect.inflate(40, 20)
            if click_rect.collidepoint(pos):
                return i

        return None

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

    def handle_input(self, event):
        """Handle keyboard and mouse input for menu navigation"""
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.selected_index = (self.selected_index - 1) % len(self.options)
                self.play_select_sound(volume=0.08)  # Hover sound for arrow key navigation
                return "navigate"

            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected_index = (self.selected_index + 1) % len(self.options)
                self.play_select_sound(volume=0.08)  # Hover sound for arrow key navigation
                return "navigate"

            elif event.key == pygame.K_RETURN:
                self.play_select_sound(use_click=True)
                return self.options[self.selected_index]

            # ESC handling removed - now handled in main.py

        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            # Scale mouse position to internal coordinates
            scaled_pos = (int(mouse_pos[0] / S.current_display_scale), int(mouse_pos[1] / S.current_display_scale))
            clicked_option = self.get_option_at_pos(scaled_pos)
            if clicked_option is not None:
                # Play sound when hovering over a new option
                if clicked_option != self.previous_selected_index:
                    self.play_select_sound(volume=0.08)  # Very quiet hover sound
                self.selected_index = clicked_option
                self.previous_selected_index = clicked_option
            else:
                # Reset tracking when not hovering over any option
                self.previous_selected_index = -1

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            # Scale mouse position to internal coordinates
            scaled_pos = (int(mouse_pos[0] / S.current_display_scale), int(mouse_pos[1] / S.current_display_scale))
            clicked_option = self.get_option_at_pos(scaled_pos)
            if clicked_option is not None:
                self.selected_index = clicked_option
                self.play_select_sound(use_click=True)
                return self.options[self.selected_index]

        return None

    def update(self):
        """Update animations"""
        self.blink_timer += 1
        if self.blink_timer >= 30:
            self.blink_timer = 0
            self.show_cursor = not self.show_cursor
    
    def draw(self, screen):
        """Draw pause menu overlay"""
        # Semi-transparent dark overlay
        overlay = pygame.Surface((S.WINDOW_WIDTH, S.WINDOW_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(180)
        screen.blit(overlay, (0, 0))
        
        # Draw pause box
        box_width = 500
        box_height = 400
        box_x = (S.WINDOW_WIDTH - box_width) // 2
        box_y = (S.WINDOW_HEIGHT - box_height) // 2
        
        box_rect = pygame.Rect(box_x, box_y, box_width, box_height)
        
        # Box shadow
        shadow_rect = box_rect.copy()
        shadow_rect.x += 6
        shadow_rect.y += 6
        pygame.draw.rect(screen, (0, 0, 0), shadow_rect)
        
        # Main box
        pygame.draw.rect(screen, (100, 120, 150), box_rect)
        pygame.draw.rect(screen, (255, 255, 255), box_rect, 4)
        
        # Title
        title = self.title_font.render("PAUSED", True, (255, 255, 255))
        title_rect = title.get_rect(center=(S.WINDOW_WIDTH // 2, box_y + 80))
        screen.blit(title, title_rect)
        
        # Menu options
        menu_y_start = box_y + 180
        menu_spacing = 60
        
        for i, option in enumerate(self.options):
            y_pos = menu_y_start + (i * menu_spacing)

            # Draw glow effect for selected option
            if i == self.selected_index:
                # Create a glowing background rectangle
                glow_width = 300
                glow_height = 50
                glow_rect = pygame.Rect(
                    S.WINDOW_WIDTH // 2 - glow_width // 2,
                    y_pos - glow_height // 2,
                    glow_width,
                    glow_height
                )

                # Draw glow (semi-transparent yellow)
                glow_surface = pygame.Surface((glow_width, glow_height), pygame.SRCALPHA)
                glow_surface.fill((255, 200, 0, 80))  # Yellow with alpha
                screen.blit(glow_surface, glow_rect.topleft)

                # Draw border around selection
                pygame.draw.rect(screen, (255, 200, 0), glow_rect, 2)

            # Selection indicator
            if i == self.selected_index and self.show_cursor:
                indicator = self.menu_font.render(">", True, (255, 200, 0))
                indicator_rect = indicator.get_rect(right=S.WINDOW_WIDTH // 2 - 100, centery=y_pos)
                screen.blit(indicator, indicator_rect)

            # Menu option
            if i == self.selected_index:
                color = (255, 200, 0)  # Yellow when selected
            else:
                color = (255, 255, 255)  # White when not selected

            text = self.menu_font.render(option, True, color)
            text_rect = text.get_rect(center=(S.WINDOW_WIDTH // 2, y_pos))
            screen.blit(text, text_rect)


class DeathMenu:
    """Death screen menu with restart/main menu/checkpoint options"""

    def __init__(self):
        # Menu options (default: no checkpoint)
        self.options = ["RESTART", "MAIN MENU"]
        self.selected_index = 0
        self.previous_selected_index = 0  # Track for hover sound
        self.has_checkpoint = False

        # Load fonts
        try:
            self.title_font = pygame.font.Font("assets/fonts/Fixedsys500c.ttf", 48)
            self.menu_font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 20)
        except:
            self.title_font = pygame.font.Font(None, 72)
            self.menu_font = pygame.font.Font(None, 40)

        # Load select sounds (hover and click)
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

        # Animation
        self.blink_timer = 0
        self.show_cursor = True

    def set_checkpoint_available(self, has_checkpoint):
        """Enable or disable the checkpoint option"""
        self.has_checkpoint = has_checkpoint
        if has_checkpoint:
            self.options = ["RESTART", "CHECKPOINT", "MAIN MENU"]
        else:
            self.options = ["RESTART", "MAIN MENU"]
        # Reset selection if out of bounds
        self.selected_index = min(self.selected_index, len(self.options) - 1)

    def get_option_at_pos(self, pos):
        """Get the menu option index at the given mouse position"""
        menu_y_start = S.WINDOW_HEIGHT // 2 + 20
        menu_spacing = 60

        for i, option in enumerate(self.options):
            y_pos = menu_y_start + (i * menu_spacing)

            # Create clickable rect for each option
            text = self.menu_font.render(option, True, (255, 255, 255))
            text_rect = text.get_rect(center=(S.WINDOW_WIDTH // 2, y_pos))

            # Expand clickable area
            click_rect = text_rect.inflate(40, 20)
            if click_rect.collidepoint(pos):
                return i

        return None

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

    def handle_input(self, event):
        """Handle keyboard and mouse input for menu navigation"""
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.selected_index = (self.selected_index - 1) % len(self.options)
                self.play_select_sound(volume=0.08)  # Hover sound for arrow key navigation
                return "navigate"

            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected_index = (self.selected_index + 1) % len(self.options)
                self.play_select_sound(volume=0.08)  # Hover sound for arrow key navigation
                return "navigate"

            elif event.key == pygame.K_RETURN:
                self.play_select_sound(use_click=True)
                return self.options[self.selected_index]

        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            # Scale mouse position to internal coordinates
            scaled_pos = (int(mouse_pos[0] / S.current_display_scale), int(mouse_pos[1] / S.current_display_scale))
            clicked_option = self.get_option_at_pos(scaled_pos)
            if clicked_option is not None:
                # Play sound when hovering over a new option
                if clicked_option != self.previous_selected_index:
                    self.play_select_sound(volume=0.08)  # Very quiet hover sound
                self.selected_index = clicked_option
                self.previous_selected_index = clicked_option
            else:
                # Reset tracking when not hovering over any option
                self.previous_selected_index = -1

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            # Scale mouse position to internal coordinates
            scaled_pos = (int(mouse_pos[0] / S.current_display_scale), int(mouse_pos[1] / S.current_display_scale))
            clicked_option = self.get_option_at_pos(scaled_pos)
            if clicked_option is not None:
                self.selected_index = clicked_option
                self.play_select_sound(use_click=True)
                return self.options[self.selected_index]

        return None

    def update(self):
        """Update animations"""
        self.blink_timer += 1
        if self.blink_timer >= 30:
            self.blink_timer = 0
            self.show_cursor = not self.show_cursor

    def draw(self, screen):
        """Draw death screen with menu options"""
        # Semi-transparent black overlay
        overlay = pygame.Surface((S.WINDOW_WIDTH, S.WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))  # RGBA - 140 alpha for better visibility
        screen.blit(overlay, (0, 0))
        
        # Death message
        text1 = self.title_font.render("Oh no! You died.", True, (255, 255, 255))
        text1_rect = text1.get_rect(center=(S.WINDOW_WIDTH // 2, S.WINDOW_HEIGHT // 2 - 100))
        screen.blit(text1, text1_rect)
        
        # Menu options
        menu_y_start = S.WINDOW_HEIGHT // 2 + 20
        menu_spacing = 60
        
        for i, option in enumerate(self.options):
            y_pos = menu_y_start + (i * menu_spacing)

            # Draw glow effect for selected option
            if i == self.selected_index:
                # Create a glowing background rectangle
                glow_width = 280
                glow_height = 50
                glow_rect = pygame.Rect(
                    S.WINDOW_WIDTH // 2 - glow_width // 2,
                    y_pos - glow_height // 2,
                    glow_width,
                    glow_height
                )

                # Draw glow (semi-transparent yellow)
                glow_surface = pygame.Surface((glow_width, glow_height), pygame.SRCALPHA)
                glow_surface.fill((255, 200, 0, 80))  # Yellow with alpha
                screen.blit(glow_surface, glow_rect.topleft)

                # Draw border around selection
                pygame.draw.rect(screen, (255, 200, 0), glow_rect, 2)

            # Selection indicator - moved further left
            if i == self.selected_index and self.show_cursor:
                indicator = self.menu_font.render(">", True, (255, 200, 0))
                indicator_rect = indicator.get_rect(right=S.WINDOW_WIDTH // 2 - 120, centery=y_pos)
                screen.blit(indicator, indicator_rect)

            # Menu option
            if i == self.selected_index:
                color = (255, 200, 0)  # Yellow when selected
            else:
                color = (200, 200, 200)  # Gray when not selected

            text = self.menu_font.render(option, True, color)
            text_rect = text.get_rect(center=(S.WINDOW_WIDTH // 2, y_pos))
            screen.blit(text, text_rect)