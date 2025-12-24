import pygame
import webbrowser
import threading
import platform
from src.utils import settings as S
from src.ui.winter_theme import Snowflake, WinterTheme
from src.utils.update_checker_secure import get_update_checker
from src.utils.auto_updater import UpdateDownloader, format_size, calculate_progress_percent
from src.core.game_logging import get_logger

logger = get_logger(__name__)

class TitleScreen:
    """Main title screen with Mario Bros-style presentation"""

    def __init__(self):
        # Menu options
        self.options = ["STORY MODE", "LEVEL SELECTION", "SCOREBOARD", "GUIDE"]
        self.selected_index = 0
        self.previous_selected_index = 0  # Track for hover sound

        # Settings icon state
        self.settings_hover = False
        self.previous_settings_hover = False  # Track for hover sound

        # Update checker (only on macOS - Windows auto-updates not yet implemented)
        self.update_checker = get_update_checker()
        self.update_available = None  # Will be (version, url, changelog) tuple or None
        self.update_button_hover = False

        # Only check for updates on macOS where auto-update is implemented
        if platform.system() == "Darwin":
            self.checking_update = True  # Start checking on init
            self._check_for_update()  # Check immediately
        else:
            self.checking_update = False  # Disable on Windows/other platforms

        # Auto-updater state
        self.updater = UpdateDownloader()
        self.update_state = "idle"  # States: idle, downloading, extracting, ready, error
        self.download_progress = 0  # 0-100
        self.download_current = 0  # Bytes downloaded
        self.download_total = 0  # Total bytes
        self.update_error = None  # Error message if any

        # Load select sounds (hover and click)
        self.select_sound = None
        self.select_click_sound = None
        if S.MASTER_AUDIO_ENABLED:
            try:
                self.select_sound = pygame.mixer.Sound("assets/sounds/select_fast.wav")
                self.select_sound.set_volume(0.4)
            except (FileNotFoundError, pygame.error):
                pass  # Sound optional
            try:
                self.select_click_sound = pygame.mixer.Sound("assets/sounds/select_click.wav")
                self.select_click_sound.set_volume(0.4)
            except (FileNotFoundError, pygame.error):
                pass  # Sound optional

        # Load fonts
        try:
            self.title_font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 48)
            self.menu_font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 16)  # Reduced to fit boxes
            self.small_font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 16)
        except:
            self.title_font = pygame.font.Font(None, 72)
            self.menu_font = pygame.font.Font(None, 32)  # Reduced
            self.small_font = pygame.font.Font(None, 32)

        # Animation
        self.blink_timer = 0
        self.show_cursor = True
        
        # Sign colors (Mario-style brown/tan)
        self.sign_bg = (139, 69, 19)  # Brown
        self.sign_border = (101, 67, 33)  # Dark brown
        self.sign_text = (255, 228, 196)  # Bisque
        self.sign_shadow = (80, 50, 20)  # Very dark brown

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

    def _check_for_update(self):
        """Check for updates in background"""
        def check():
            self.update_available = self.update_checker.check_for_update()
            self.checking_update = False

        if self.update_checker.is_available():
            thread = threading.Thread(target=check, daemon=True)
            thread.start()
        else:
            self.checking_update = False

    def _update_progress_callback(self, downloaded, total):
        """Callback for download progress updates"""
        self.download_current = downloaded
        self.download_total = total
        self.download_progress = calculate_progress_percent(downloaded, total)

    def _start_auto_update(self):
        """Start the auto-update process in background thread"""
        if not self.update_available:
            return

        version, url, changelog = self.update_available

        def update_thread():
            try:
                logger.info(f"Starting auto-update to version {version}")
                self.update_state = "downloading"
                self.update_error = None

                # Set progress callback
                self.updater.set_progress_callback(self._update_progress_callback)

                # Download update
                success = self.updater.download_update(url, expected_size_mb=85)
                if not success:
                    self.update_state = "error"
                    self.update_error = "Failed to download update"
                    logger.error("Download failed")
                    return

                # Extract update
                self.update_state = "extracting"
                logger.info("Extracting update...")
                success = self.updater.extract_update()
                if not success:
                    self.update_state = "error"
                    self.update_error = "Failed to extract update"
                    logger.error("Extraction failed")
                    return

                # Ready to install
                self.update_state = "ready"
                logger.info("Update ready to install")

                # Launch installer (this will quit the app)
                import time
                time.sleep(1)  # Give user a moment to see "ready" message
                success = self.updater.launch_installer()
                if success:
                    # Installer launched successfully
                    # Mark state to trigger quit from main thread
                    self.update_state = "quitting"
                    logger.info("Installer launched, will quit from main thread...")
                else:
                    self.update_state = "error"
                    self.update_error = "Cannot auto-update in dev mode"
                    logger.warning("Not running as .app bundle - cannot auto-update")

            except Exception as e:
                self.update_state = "error"
                self.update_error = f"Update error: {str(e)}"
                logger.error(f"Auto-update failed: {e}")

        # Start update in background thread
        thread = threading.Thread(target=update_thread, daemon=True)
        thread.start()

    def get_update_button_rect(self):
        """Get the rect for the update notification button"""
        button_width = 620  # Increased from 420 to fit text
        button_height = 50  # Increased from 40 for better visibility
        padding = 20
        return pygame.Rect(
            (S.WINDOW_WIDTH - button_width) // 2,
            padding,
            button_width,
            button_height
        )

    def get_settings_icon_rect(self):
        """Get the rect for the settings gear icon in top right corner"""
        icon_size = 50  # Increased from 40
        padding = 20
        return pygame.Rect(S.WINDOW_WIDTH - icon_size - padding, padding, icon_size, icon_size)

    def handle_input(self, event):
        """Handle keyboard and mouse input for menu navigation (2x2 grid)"""
        if event.type == pygame.KEYDOWN:
            # Grid navigation: 2 rows, 2 columns
            row = self.selected_index // 2
            col = self.selected_index % 2

            if event.key in (pygame.K_UP, pygame.K_w):
                # Move up one row
                row = (row - 1) % 2
                self.selected_index = (row * 2) + col
                self.play_select_sound(volume=0.08)  # Hover sound for arrow key navigation
                return "navigate"

            elif event.key in (pygame.K_DOWN, pygame.K_s):
                # Move down one row
                row = (row + 1) % 2
                self.selected_index = (row * 2) + col
                self.play_select_sound(volume=0.08)  # Hover sound for arrow key navigation
                return "navigate"

            elif event.key in (pygame.K_LEFT, pygame.K_a):
                # Move left one column
                col = (col - 1) % 2
                self.selected_index = (row * 2) + col
                self.play_select_sound(volume=0.08)  # Hover sound for arrow key navigation
                return "navigate"

            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                # Move right one column
                col = (col + 1) % 2
                self.selected_index = (row * 2) + col
                self.play_select_sound(volume=0.08)  # Hover sound for arrow key navigation
                return "navigate"

            elif event.key == pygame.K_RETURN:
                self.play_select_sound(use_click=True)
                return self.options[self.selected_index]

        elif event.type == pygame.MOUSEMOTION:
            # Update selection based on mouse position (scaled to internal coordinates)
            mouse_pos = pygame.mouse.get_pos()
            scaled_pos = (int(mouse_pos[0] / S.current_display_scale), int(mouse_pos[1] / S.current_display_scale))

            # Check update button hover
            if self.update_available:
                update_rect = self.get_update_button_rect()
                prev_hover = self.update_button_hover
                self.update_button_hover = update_rect.collidepoint(scaled_pos)
                if self.update_button_hover and not prev_hover:
                    self.play_select_sound(volume=0.08)

            # Check settings icon hover
            settings_rect = self.get_settings_icon_rect()
            self.settings_hover = settings_rect.collidepoint(scaled_pos)

            # Play sound when settings hover state changes
            if self.settings_hover and not self.previous_settings_hover:
                self.play_select_sound(volume=0.08)  # Very quiet hover sound
            self.previous_settings_hover = self.settings_hover

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
            # Click to select (scaled to internal coordinates)
            mouse_pos = pygame.mouse.get_pos()
            scaled_pos = (int(mouse_pos[0] / S.current_display_scale), int(mouse_pos[1] / S.current_display_scale))

            # Check update button click
            if self.update_available and self.update_state == "idle":
                update_rect = self.get_update_button_rect()
                if update_rect.collidepoint(scaled_pos):
                    self.play_select_sound(use_click=True)
                    # Start auto-update
                    self._start_auto_update()
                    return None

            # Check settings icon click
            settings_rect = self.get_settings_icon_rect()
            if settings_rect.collidepoint(scaled_pos):
                self.play_select_sound(use_click=True)
                return "SETTINGS"

            clicked_option = self.get_option_at_pos(scaled_pos)
            if clicked_option is not None:
                self.selected_index = clicked_option
                self.play_select_sound(use_click=True)
                return self.options[self.selected_index]

        return None

    def get_option_at_pos(self, pos):
        """Get the menu option index at the given mouse position"""
        box_width = 260
        box_height = 50
        h_spacing = 30
        v_spacing = 20
        total_width = (box_width * 2) + h_spacing
        start_x = (S.WINDOW_WIDTH - total_width) // 2
        start_y = 460

        for i in range(len(self.options)):
            row = i // 2
            col = i % 2
            x = start_x + (col * (box_width + h_spacing))
            y = start_y + (row * (box_height + v_spacing))

            box_rect = pygame.Rect(x, y, box_width, box_height)
            if box_rect.collidepoint(pos):
                return i

        return None
    
    def draw_sign(self, screen):
        """Draw the Mario-style sign with 'SUPER SIENA BROS.'"""
        # Sign dimensions
        sign_width = 700
        sign_height = 320
        sign_x = (S.WINDOW_WIDTH - sign_width) // 2
        sign_y = 120
        
        # Draw sign posts (wooden poles)
        post_width = 30
        post_height = 150
        post_color = (101, 67, 33)
        
        # Left post
        pygame.draw.rect(screen, post_color, 
                        (sign_x - 20, sign_y + sign_height - 50, post_width, post_height))
        # Right post
        pygame.draw.rect(screen, post_color, 
                        (sign_x + sign_width - 10, sign_y + sign_height - 50, post_width, post_height))
        
        # Main sign rectangle
        sign_rect = pygame.Rect(sign_x, sign_y, sign_width, sign_height)
        
        # Draw shadow (offset)
        shadow_rect = sign_rect.copy()
        shadow_rect.x += 8
        shadow_rect.y += 8
        pygame.draw.rect(screen, (0, 0, 0, 100), shadow_rect)
        
        # Draw sign background
        pygame.draw.rect(screen, self.sign_bg, sign_rect)
        
        # Draw border (thick dark brown)
        pygame.draw.rect(screen, self.sign_border, sign_rect, 12)
        
        # Draw corner screws
        screw_color = (50, 50, 50)
        screw_radius = 8
        screws = [
            (sign_x + 30, sign_y + 30),
            (sign_x + sign_width - 30, sign_y + 30),
            (sign_x + 30, sign_y + sign_height - 30),
            (sign_x + sign_width - 30, sign_y + sign_height - 30)
        ]
        for screw_pos in screws:
            pygame.draw.circle(screen, screw_color, screw_pos, screw_radius)
            pygame.draw.circle(screen, (80, 80, 80), screw_pos, screw_radius - 3)
        
        # Draw text with shadow effect
        # Line 1: "SUPER"
        super_text = self.title_font.render("SUPER", True, self.sign_shadow)
        super_rect = super_text.get_rect(center=(S.WINDOW_WIDTH // 2, sign_y + 100))
        screen.blit(super_text, (super_rect.x + 4, super_rect.y + 4))
        
        super_text = self.title_font.render("SUPER", True, self.sign_text)
        screen.blit(super_text, super_rect)
        
        # Line 2: "SIENA BROS."
        siena_text = self.title_font.render("SIENA BROS.", True, self.sign_shadow)
        siena_rect = siena_text.get_rect(center=(S.WINDOW_WIDTH // 2, sign_y + 180))
        screen.blit(siena_text, (siena_rect.x + 4, siena_rect.y + 4))
        
        siena_text = self.title_font.render("SIENA BROS.", True, self.sign_text)
        screen.blit(siena_text, siena_rect)
        
        # Subtitle
        subtitle = self.small_font.render("A Winter Adventure", True, (200, 200, 255))
        subtitle_rect = subtitle.get_rect(center=(S.WINDOW_WIDTH // 2, sign_y + 250))
        screen.blit(subtitle, subtitle_rect)
    
    def draw_menu(self, screen):
        """Draw menu options in 2x2 grid"""
        # Grid layout: 2 rows, 2 columns
        box_width = 260
        box_height = 50
        h_spacing = 30
        v_spacing = 20

        # Calculate grid positioning
        total_width = (box_width * 2) + h_spacing
        total_height = (box_height * 2) + v_spacing
        start_x = (S.WINDOW_WIDTH - total_width) // 2
        start_y = 460

        for i, option in enumerate(self.options):
            # Calculate grid position (0,1 = row 0, 2,3 = row 1)
            row = i // 2
            col = i % 2

            x = start_x + (col * (box_width + h_spacing))
            y = start_y + (row * (box_height + v_spacing))

            # Draw box
            box_rect = pygame.Rect(x, y, box_width, box_height)

            if i == self.selected_index:
                # Draw glow effect behind selected option
                glow_padding = 8
                glow_rect = box_rect.inflate(glow_padding * 2, glow_padding * 2)
                glow_surface = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
                glow_surface.fill((255, 200, 0, 100))  # Golden glow with alpha
                screen.blit(glow_surface, glow_rect.topleft)

                # Selected: orange fill
                pygame.draw.rect(screen, (255, 140, 0), box_rect)
                pygame.draw.rect(screen, (255, 200, 100), box_rect, 4)
                text_color = (255, 255, 255)
            else:
                # Not selected: dark fill
                pygame.draw.rect(screen, (101, 67, 33), box_rect)
                pygame.draw.rect(screen, (139, 89, 49), box_rect, 3)
                text_color = (200, 200, 200)

            # Draw menu option text
            text = self.menu_font.render(option, True, text_color)
            text_rect = text.get_rect(center=(x + box_width // 2, y + box_height // 2))
            screen.blit(text, text_rect)
    
    def draw_staging_indicator(self, screen):
        """Draw staging mode indicator banner at top of screen"""
        if self.update_checker.is_available() and self.update_checker.get_update_channel() == 'staging':
            # Draw orange/yellow warning banner at top
            banner_height = 30
            banner_rect = pygame.Rect(0, 0, S.WINDOW_WIDTH, banner_height)
            pygame.draw.rect(screen, (255, 165, 0), banner_rect)  # Orange
            pygame.draw.rect(screen, (200, 130, 0), banner_rect, 2)  # Border

            # Draw text
            try:
                font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 10)
            except:
                font = pygame.font.Font(None, 16)

            text = font.render("STAGING MODE - Testing Updates", True, (255, 255, 255))
            text_rect = text.get_rect(center=(S.WINDOW_WIDTH // 2, banner_height // 2))
            screen.blit(text, text_rect)

    def draw_footer(self, screen):
        """Draw footer with version number and staging indicator"""
        # Display version number in bottom left
        version_font = pygame.font.Font(None, 24)

        # Build version text with staging indicator if applicable
        version_text_str = f"v{S.CURRENT_VERSION}"
        if self.update_checker.is_available() and self.update_checker.get_update_channel() == 'staging':
            version_text_str += " [STAGING]"

        version_text = version_font.render(version_text_str, True, (100, 100, 100))
        screen.blit(version_text, (10, S.WINDOW_HEIGHT - 30))
    
    def update(self):
        """Update animations"""
        self.blink_timer += 1
        if self.blink_timer >= 30:  # Blink every 0.5 seconds
            self.blink_timer = 0
            self.show_cursor = not self.show_cursor

    def draw_settings_icon(self, screen):
        """Draw a gear/settings icon in the top right corner"""
        import math
        rect = self.get_settings_icon_rect()
        center_x = rect.centerx
        center_y = rect.centery

        # Darker grey color for settings icon
        if self.settings_hover:
            gear_color = (40, 40, 40)  # Very dark grey when hovered
        else:
            gear_color = (70, 70, 70)  # Dark grey normally

        # Draw gear icon (simplified gear with teeth) - scaled up
        outer_radius = 20  # Increased from 16
        inner_radius = 13  # Increased from 10
        center_hole_radius = 6  # Increased from 5
        num_teeth = 8

        # Draw gear teeth as a polygon
        points = []
        for i in range(num_teeth * 2):
            angle = (i * math.pi / num_teeth) - math.pi / 2
            if i % 2 == 0:
                radius = outer_radius
            else:
                radius = inner_radius
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            points.append((int(x), int(y)))

        pygame.draw.polygon(screen, gear_color, points)

        # Draw center hole
        pygame.draw.circle(screen, (200, 220, 255), (center_x, center_y), center_hole_radius)  # Sky blue background
        pygame.draw.circle(screen, gear_color, (center_x, center_y), center_hole_radius, 2)

        # Draw "SETTINGS" text in grey to the left of the gear
        grey = (120, 120, 120)
        settings_text = self.small_font.render("SETTINGS", True, grey)
        text_rect = settings_text.get_rect()
        text_rect.right = rect.left - 10  # Position to the left of gear with 10px spacing
        text_rect.centery = center_y
        screen.blit(settings_text, text_rect)

    def draw_update_notification(self, screen):
        """Draw update notification banner at top of screen with progress"""
        if not self.update_available:
            return

        version, url, changelog = self.update_available
        rect = self.get_update_button_rect()

        # Determine colors and text based on update state
        if self.update_state == "error":
            bg_color = (200, 50, 50)  # Red for error
            border_color = (150, 30, 30)
            text = f"UPDATE ERROR: {self.update_error or 'Unknown error'}"
        elif self.update_state == "quitting":
            bg_color = (50, 200, 50)  # Green for quitting
            border_color = (30, 150, 30)
            text = "Update installed! Restarting game..."
        elif self.update_state == "ready":
            bg_color = (50, 200, 50)  # Green for ready
            border_color = (30, 150, 30)
            text = "Update ready! Installing..."
        elif self.update_state == "extracting":
            bg_color = (255, 165, 0)  # Orange for extracting
            border_color = (200, 130, 0)
            text = "Extracting update..."
        elif self.update_state == "downloading":
            bg_color = (255, 165, 0)  # Orange for downloading
            border_color = (200, 130, 0)
            text = f"Downloading: {self.download_progress}% ({format_size(self.download_current)} / {format_size(self.download_total)})"
        else:  # idle
            if self.update_button_hover:
                bg_color = (30, 144, 255)  # Brighter blue when hovering
                border_color = (0, 100, 200)
            else:
                bg_color = (70, 130, 220)  # Royal blue
                border_color = (40, 80, 150)
            text = f"UPDATE AVAILABLE: v{version} - Click to Update"

        # Draw banner background
        pygame.draw.rect(screen, bg_color, rect, border_radius=8)
        pygame.draw.rect(screen, border_color, rect, 3, border_radius=8)

        # Draw warning triangles on both sides
        triangle_size = 30
        triangle_padding = 50  # Moved closer to center

        # Left triangle
        left_triangle_x = rect.x + triangle_padding
        left_triangle_y = rect.centery
        left_points = [
            (left_triangle_x, left_triangle_y - triangle_size // 2),  # Top
            (left_triangle_x - triangle_size // 2, left_triangle_y + triangle_size // 2),  # Bottom left
            (left_triangle_x + triangle_size // 2, left_triangle_y + triangle_size // 2)   # Bottom right
        ]
        pygame.draw.polygon(screen, (255, 220, 0), left_points)  # Yellow triangle
        pygame.draw.polygon(screen, (200, 160, 0), left_points, 2)  # Dark outline

        # Right triangle
        right_triangle_x = rect.right - triangle_padding
        right_triangle_y = rect.centery
        right_points = [
            (right_triangle_x, right_triangle_y - triangle_size // 2),  # Top
            (right_triangle_x - triangle_size // 2, right_triangle_y + triangle_size // 2),  # Bottom left
            (right_triangle_x + triangle_size // 2, right_triangle_y + triangle_size // 2)   # Bottom right
        ]
        pygame.draw.polygon(screen, (255, 220, 0), right_points)  # Yellow triangle
        pygame.draw.polygon(screen, (200, 160, 0), right_points, 2)  # Dark outline

        # Draw exclamation points in triangles
        try:
            exclamation_font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 14)
        except:
            exclamation_font = pygame.font.Font(None, 20)

        exclamation = exclamation_font.render("!", True, (0, 0, 0))

        # Left exclamation
        left_exclamation_rect = exclamation.get_rect(center=(left_triangle_x, left_triangle_y + 2))
        screen.blit(exclamation, left_exclamation_rect)

        # Right exclamation
        right_exclamation_rect = exclamation.get_rect(center=(right_triangle_x, right_triangle_y + 2))
        screen.blit(exclamation, right_exclamation_rect)

        # Draw progress bar if downloading
        if self.update_state == "downloading" and self.download_progress > 0:
            progress_rect = pygame.Rect(
                rect.x + 5,
                rect.y + rect.height - 8,
                int((rect.width - 10) * (self.download_progress / 100)),
                4
            )
            pygame.draw.rect(screen, (100, 255, 100), progress_rect, border_radius=2)

        # Draw text
        try:
            small_font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 10)
        except:
            small_font = pygame.font.Font(None, 16)

        text_surface = small_font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(rect.centerx, rect.centery - 2))
        screen.blit(text_surface, text_rect)

    def draw(self, screen):
        """Draw the complete title screen"""
        # Winter sky background (lighter blue/white)
        screen.fill((200, 220, 255))

        # Draw staging indicator FIRST (so it's at the top)
        self.draw_staging_indicator(screen)

        # Draw falling snow
        self.draw_snow(screen)
        
        # Draw clouds (winter style)
        self.draw_clouds(screen)
        
        # Draw snowy ground
        self.draw_ground(screen)
        
        # Draw the sign FIRST
        self.draw_sign(screen)
        
        # Draw penguin IN FRONT of sign
        self.draw_penguin(screen)
        
        # Draw menu
        self.draw_menu(screen)

        # Draw footer
        self.draw_footer(screen)

        # Draw settings icon
        self.draw_settings_icon(screen)

        # Draw update notification (drawn last so it's on top)
        self.draw_update_notification(screen)
    
    def draw_snow(self, screen):
        """Draw falling snowflakes"""
        import random
        random.seed(42)  # Consistent snow pattern
        
        for i in range(50):
            x = random.randint(0, S.WINDOW_WIDTH)
            y = random.randint(0, S.WINDOW_HEIGHT)
            size = random.randint(2, 4)
            
            # Snowflake
            pygame.draw.circle(screen, (255, 255, 255), (x, y), size)
    
    def draw_penguin(self, screen):
        """Draw a simple cute penguin below and to the left of sign"""
        penguin_x = 180  # Adjusted for wider screen
        penguin_y = 460  # Below sign, moved up a bit
        
        # Scale down - make penguin smaller (0.7x size)
        scale = 0.7
        body_width = int(60 * scale)
        body_height = int(80 * scale)
        head_radius = int(25 * scale)
        
        # Body (black oval)
        pygame.draw.ellipse(screen, (40, 40, 40), 
                          (penguin_x, penguin_y, body_width, body_height))
        
        # Belly (white)
        pygame.draw.ellipse(screen, (255, 255, 255), 
                          (penguin_x + int(10 * scale), penguin_y + int(15 * scale), 
                           int(40 * scale), int(50 * scale)))
        
        # Head (black circle)
        pygame.draw.circle(screen, (40, 40, 40), 
                         (penguin_x + body_width // 2, penguin_y - int(10 * scale)), 
                         head_radius)
        
        # Eyes (white)
        pygame.draw.circle(screen, (255, 255, 255), 
                         (penguin_x + int(22 * scale), penguin_y - int(12 * scale)), 
                         int(6 * scale))
        pygame.draw.circle(screen, (255, 255, 255), 
                         (penguin_x + int(38 * scale), penguin_y - int(12 * scale)), 
                         int(6 * scale))
        
        # Pupils (black)
        pygame.draw.circle(screen, (0, 0, 0), 
                         (penguin_x + int(24 * scale), penguin_y - int(10 * scale)), 
                         int(3 * scale))
        pygame.draw.circle(screen, (0, 0, 0), 
                         (penguin_x + int(40 * scale), penguin_y - int(10 * scale)), 
                         int(3 * scale))
        
        # Beak (orange)
        beak_points = [
            (penguin_x + int(30 * scale), penguin_y - int(5 * scale)),
            (penguin_x + int(35 * scale), penguin_y),
            (penguin_x + int(30 * scale), penguin_y + int(2 * scale))
        ]
        pygame.draw.polygon(screen, (255, 140, 0), beak_points)
        
        # Feet (orange)
        pygame.draw.ellipse(screen, (255, 140, 0), 
                          (penguin_x + int(8 * scale), penguin_y + int(75 * scale), 
                           int(20 * scale), int(10 * scale)))
        pygame.draw.ellipse(screen, (255, 140, 0), 
                          (penguin_x + int(32 * scale), penguin_y + int(75 * scale), 
                           int(20 * scale), int(10 * scale)))
    
    def draw_clouds(self, screen):
        """Draw winter clouds (more white and fluffy)"""
        cloud_color = (255, 255, 255)
        
        # Cloud 1
        pygame.draw.ellipse(screen, cloud_color, (80, 60, 140, 70))
        pygame.draw.ellipse(screen, cloud_color, (170, 50, 110, 70))
        pygame.draw.ellipse(screen, cloud_color, (120, 75, 90, 60))
        
        # Cloud 2
        pygame.draw.ellipse(screen, cloud_color, (680, 130, 160, 80))
        pygame.draw.ellipse(screen, cloud_color, (780, 120, 120, 80))
        pygame.draw.ellipse(screen, cloud_color, (730, 150, 100, 70))
        
        # Cloud 3
        pygame.draw.ellipse(screen, cloud_color, (380, 80, 120, 60))
        pygame.draw.ellipse(screen, cloud_color, (460, 75, 90, 60))
        
        # Cloud 4 (additional)
        pygame.draw.ellipse(screen, cloud_color, (550, 110, 100, 50))
        pygame.draw.ellipse(screen, cloud_color, (610, 105, 80, 55))
    
    def draw_ground(self, screen):
        """Draw snowy ground at bottom"""
        ground_y = S.WINDOW_HEIGHT - 120
        
        # White snow
        pygame.draw.rect(screen, (255, 255, 255), (0, ground_y, S.WINDOW_WIDTH, 120))
        
        # Snow drifts (light blue shadows for depth)
        drift_color = (230, 240, 255)
        pygame.draw.ellipse(screen, drift_color, (50, ground_y - 20, 200, 80))
        pygame.draw.ellipse(screen, drift_color, (600, ground_y - 30, 250, 100))
        pygame.draw.ellipse(screen, drift_color, (300, ground_y - 15, 180, 70))


class LevelSelectScreen:
    """Level selection screen with winter theme"""

    def __init__(self, max_level=1):
        self.max_level = max_level
        self.selected_level = 1
        self.previous_selected_level = 1  # Track for hover sound

        try:
            self.title_font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 36)
            self.level_font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 32)
            self.small_font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 14)
        except:
            self.title_font = pygame.font.Font(None, 56)
            self.level_font = pygame.font.Font(None, 48)
            self.small_font = pygame.font.Font(None, 24)

        # Snowflakes
        self.snowflakes = [Snowflake(S.WINDOW_WIDTH, S.WINDOW_HEIGHT) for _ in range(60)]

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
        """Handle level selection input (keyboard and mouse)"""
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_a):
                if self.selected_level > 1:
                    self.selected_level -= 1
                    self.play_select_sound(volume=0.08)  # Hover sound for arrow key navigation
                return "navigate"

            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                if self.selected_level < self.max_level:
                    self.selected_level += 1
                    self.play_select_sound(volume=0.08)  # Hover sound for arrow key navigation
                return "navigate"

            elif event.key == pygame.K_RETURN:
                self.play_select_sound(use_click=True)
                return f"LEVEL_{self.selected_level}"

            elif event.key == pygame.K_ESCAPE:
                self.play_select_sound(use_click=True)
                return "BACK"

        elif event.type == pygame.MOUSEMOTION:
            # Update selection on hover (scaled to internal coordinates)
            mouse_pos = pygame.mouse.get_pos()
            scaled_pos = (int(mouse_pos[0] / S.current_display_scale), int(mouse_pos[1] / S.current_display_scale))
            level = self.get_level_at_pos(scaled_pos)
            if level is not None:
                # Play sound when hovering over a new level
                if level != self.previous_selected_level:
                    self.play_select_sound(volume=0.08)  # Very quiet hover sound
                self.selected_level = level
                self.previous_selected_level = level
            else:
                # Reset tracking when not hovering over any level
                self.previous_selected_level = -1

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Click to select level (scaled to internal coordinates)
            mouse_pos = pygame.mouse.get_pos()
            scaled_pos = (int(mouse_pos[0] / S.current_display_scale), int(mouse_pos[1] / S.current_display_scale))
            level = self.get_level_at_pos(scaled_pos)
            if level is not None:
                self.selected_level = level
                self.play_select_sound(use_click=True)
                return f"LEVEL_{self.selected_level}"

        return None

    def get_level_at_pos(self, pos):
        """Get the level number at the given mouse position"""
        box_width = 130
        box_height = 130
        box_spacing = 30
        total_width = (self.max_level * box_width) + ((self.max_level - 1) * box_spacing)
        start_x = (S.WINDOW_WIDTH - total_width) // 2

        for i in range(1, self.max_level + 1):
            x = start_x + ((i - 1) * (box_width + box_spacing))
            y = 250

            box_rect = pygame.Rect(x, y, box_width, box_height)
            if box_rect.collidepoint(pos):
                return i

        return None

    def draw(self, screen):
        """Draw level selection screen with winter theme"""
        # Update snowflakes
        for snowflake in self.snowflakes:
            snowflake.update()

        # Draw gradient background
        WinterTheme.draw_gradient_background(screen)

        # Draw snowflakes
        for snowflake in self.snowflakes:
            snowflake.draw(screen)

        # Draw decorative snowflakes
        WinterTheme.draw_snowflake_icon(screen, 100, 80, 25)
        WinterTheme.draw_snowflake_icon(screen, S.WINDOW_WIDTH - 100, 80, 25)

        # Title with shadow
        WinterTheme.draw_text_with_shadow(screen, self.title_font, "LEVEL SELECT",
                                         WinterTheme.SNOW_WHITE, S.WINDOW_WIDTH // 2, 60)

        # Level boxes
        box_width = 130
        box_height = 130
        box_spacing = 30
        total_width = (self.max_level * box_width) + ((self.max_level - 1) * box_spacing)
        start_x = (S.WINDOW_WIDTH - total_width) // 2

        for i in range(1, self.max_level + 1):
            x = start_x + ((i - 1) * (box_width + box_spacing))
            y = 250

            # Draw frosted box with different alpha for selected
            alpha = 200 if i == self.selected_level else 160
            WinterTheme.draw_frosted_box(screen, x, y, box_width, box_height, alpha)

            # Selected indicator
            if i == self.selected_level:
                # Draw glow effect behind selected level
                glow_padding = 12
                glow_rect = pygame.Rect(x - glow_padding, y - glow_padding,
                                       box_width + glow_padding * 2, box_height + glow_padding * 2)
                glow_surface = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
                glow_surface.fill((255, 215, 0, 80))  # Golden glow with alpha
                screen.blit(glow_surface, glow_rect.topleft)

                # Draw glowing border
                border_rect = pygame.Rect(x - 5, y - 5, box_width + 10, box_height + 10)
                pygame.draw.rect(screen, (255, 215, 0), border_rect, 5)

                # Draw snowflake above
                WinterTheme.draw_snowflake_icon(screen, x + box_width // 2, y - 30, 15, 200)

            # Level number
            level_text = self.level_font.render(f"{i}", True, WinterTheme.TEXT_DARK)
            level_rect = level_text.get_rect(center=(x + box_width // 2, y + box_height // 2))
            screen.blit(level_text, level_rect)

        # Instructions
        hint_text = "< / > : SELECT     ENTER : PLAY     ESC : BACK"
        hint = self.small_font.render(hint_text, True, WinterTheme.ICE_BLUE)
        hint_rect = hint.get_rect(center=(S.WINDOW_WIDTH // 2, S.WINDOW_HEIGHT - 60))
        screen.blit(hint, hint_rect)


class GuideScreen:
    """Comprehensive guide screen with game information, controls, and tips"""

    def __init__(self):
        try:
            self.title_font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 36)
            self.header_font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 18)
            self.text_font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 14)
            self.small_font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 12)
        except:
            self.title_font = pygame.font.Font(None, 56)
            self.header_font = pygame.font.Font(None, 28)
            self.text_font = pygame.font.Font(None, 22)
            self.small_font = pygame.font.Font(None, 18)

        # Snowflakes
        self.snowflakes = [Snowflake(S.WINDOW_WIDTH, S.WINDOW_HEIGHT) for _ in range(60)]

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

        # Scrolling state
        self.scroll_offset = 0  # Always resets to 0 when opened
        self.content_height = 1500  # Adjusted for optimized spacing
        self.visible_height = 500  # Increased box height
        self.max_scroll = max(0, self.content_height - self.visible_height)

        # Tab navigation
        self.active_tab = 0  # Currently selected tab (0-4)
        self.tab_hover = None  # Track mouse hover over tabs
        self.previous_tab_hover = None  # Track for hover sound

        # Section offsets (where each section starts in the scrollable content)
        # Optimized spacing between sections
        self.section_offsets = [0, 280, 520, 820, 1120]
        self.section_labels = ["Modes", "Board", "Diff", "Check", "Ctrl"]

        # Back button state
        self.back_hover = False
        self.previous_back_hover = False  # Track for hover sound

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
        """Handle guide screen input with scrolling and tab navigation"""
        # Tab selection via number keys (1-5)
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_1, pygame.K_KP1):
                self.jump_to_section(0)
                return "navigate"
            elif event.key in (pygame.K_2, pygame.K_KP2):
                self.jump_to_section(1)
                return "navigate"
            elif event.key in (pygame.K_3, pygame.K_KP3):
                self.jump_to_section(2)
                return "navigate"
            elif event.key in (pygame.K_4, pygame.K_KP4):
                self.jump_to_section(3)
                return "navigate"
            elif event.key in (pygame.K_5, pygame.K_KP5):
                self.jump_to_section(4)
                return "navigate"
            elif event.key in (pygame.K_UP, pygame.K_w):
                self.scroll_offset -= 30
                self.scroll_offset = max(0, self.scroll_offset)
                return "scroll"
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.scroll_offset += 30
                self.scroll_offset = min(self.scroll_offset, self.max_scroll)
                return "scroll"
            elif event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                self.play_select_sound(use_click=True)
                return "BACK"

        # Mouse wheel scrolling
        elif event.type == pygame.MOUSEWHEEL:
            self.scroll_offset -= event.y * 30
            self.scroll_offset = max(0, min(self.scroll_offset, self.max_scroll))
            return "scroll"

        # Mouse hover over tabs and back button
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            scaled_pos = (int(mouse_pos[0] / S.current_display_scale),
                          int(mouse_pos[1] / S.current_display_scale))

            # Track tab hover and play sound on change
            self.tab_hover = self.get_tab_at_pos(scaled_pos)
            if self.tab_hover is not None and self.tab_hover != self.previous_tab_hover:
                self.play_select_sound(volume=0.08)  # Very quiet hover sound
            self.previous_tab_hover = self.tab_hover

            # Track back button hover and play sound on change
            self.back_hover = self.is_back_button_hovered(scaled_pos)
            if self.back_hover and not self.previous_back_hover:
                self.play_select_sound(volume=0.08)  # Very quiet hover sound
            self.previous_back_hover = self.back_hover

        # Mouse click on tabs or back button
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            scaled_pos = (int(mouse_pos[0] / S.current_display_scale),
                          int(mouse_pos[1] / S.current_display_scale))

            # Check back button first
            if self.is_back_button_hovered(scaled_pos):
                self.play_select_sound(use_click=True)
                return "BACK"

            # Then check tabs
            tab_index = self.get_tab_at_pos(scaled_pos)
            if tab_index is not None:
                self.play_select_sound(use_click=True)
                self.jump_to_section(tab_index)
                return "navigate"

        return None

    def jump_to_section(self, tab_index):
        """Jump scroll position to show the selected section"""
        self.active_tab = tab_index
        self.scroll_offset = self.section_offsets[tab_index]
        self.scroll_offset = max(0, min(self.scroll_offset, self.max_scroll))

    def get_tab_at_pos(self, pos):
        """Get the tab index at the given mouse position, or None"""
        tab_width = 120
        tab_height = 35
        tab_spacing = 10
        total_width = (tab_width * 5) + (tab_spacing * 4)
        start_x = (S.WINDOW_WIDTH - total_width) // 2
        tab_y = 95

        for i in range(5):
            x = start_x + (i * (tab_width + tab_spacing))
            tab_rect = pygame.Rect(x, tab_y, tab_width, tab_height)
            if tab_rect.collidepoint(pos):
                return i

        return None

    def is_back_button_hovered(self, pos):
        """Check if the back button is hovered"""
        back_rect = pygame.Rect(20, 20, 100, 40)
        return back_rect.collidepoint(pos)

    def draw_trophy_icon(self, screen, x, y, size=15):
        """Draw a simple trophy icon"""
        # Golden circle
        pygame.draw.circle(screen, (255, 215, 0), (x, y), size)
        # Inner detail
        pygame.draw.circle(screen, (255, 255, 255), (x, y), size - 3)
        # "1" text
        font = pygame.font.Font(None, size * 2)
        text = font.render("1", True, (255, 215, 0))
        text_rect = text.get_rect(center=(x, y))
        screen.blit(text, text_rect)

    def draw_bars_icon(self, screen, x, y, size=15):
        """Draw three stacked bars (difficulty levels)"""
        bar_colors = [(100, 255, 100), (255, 255, 100), (255, 100, 100)]
        bar_height = size // 4
        for i, color in enumerate(bar_colors):
            bar_y = y - size//2 + i * (bar_height + 2)
            bar_width = size - (i * 3)  # Decreasing width
            pygame.draw.rect(screen, color,
                            (x - bar_width//2, bar_y, bar_width, bar_height))

    def draw_flag_icon(self, screen, x, y, size=15):
        """Draw a checkpoint flag icon"""
        # Pole (brown)
        pygame.draw.rect(screen, (101, 67, 33), (x - 1, y - size, 2, size))
        # Flag (green)
        flag_points = [
            (x, y - size),
            (x + size, y - size + 5),
            (x, y - size + 10)
        ]
        pygame.draw.polygon(screen, (100, 255, 100), flag_points)

    def draw_controller_icon(self, screen, x, y, size=15):
        """Draw directional arrows for controls"""
        arrow_color = (200, 200, 200)
        # Up arrow
        pygame.draw.polygon(screen, arrow_color,
                           [(x, y - size//2), (x - 5, y), (x + 5, y)])
        # Down arrow
        pygame.draw.polygon(screen, arrow_color,
                           [(x, y + size//2), (x - 5, y), (x + 5, y)])

    def draw_multiline_text(self, screen, font, text_lines, color, x, y, line_spacing=18):
        """Draw multiple lines of text with proper spacing"""
        current_y = y
        for line in text_lines:
            text_surface = font.render(line, True, color)
            screen.blit(text_surface, (x, current_y))
            current_y += line_spacing
        return current_y

    def draw(self, screen):
        """Draw comprehensive guide screen with winter theme"""
        # Update snowflakes
        for snowflake in self.snowflakes:
            snowflake.update()

        # Draw gradient background
        WinterTheme.draw_gradient_background(screen)

        # Draw snowflakes
        for snowflake in self.snowflakes:
            snowflake.draw(screen)

        # Draw decorative snowflakes
        WinterTheme.draw_snowflake_icon(screen, 100, 80, 25)
        WinterTheme.draw_snowflake_icon(screen, S.WINDOW_WIDTH - 100, 80, 25)

        # Draw back button in top left
        self.draw_back_button(screen)

        # Title with shadow
        WinterTheme.draw_text_with_shadow(screen, self.title_font, "GUIDE",
                                         WinterTheme.SNOW_WHITE, S.WINDOW_WIDTH // 2, 60)

        # Draw tabs
        self.draw_tabs(screen)

        # Draw main content box (increased height now that bottom text is removed)
        box_width = 900
        box_height = 500  # Increased from 460
        box_x = (S.WINDOW_WIDTH - box_width) // 2
        box_y = 140  # Below tabs

        WinterTheme.draw_frosted_box(screen, box_x, box_y, box_width, box_height, 170)

        # Set up clipping to draw only within the box
        clip_rect = pygame.Rect(box_x, box_y, box_width, box_height)
        screen.set_clip(clip_rect)

        # Calculate base Y with scroll offset
        content_y = box_y + 20 - self.scroll_offset

        # Draw all sections with proper spacing
        self.draw_game_modes_section(screen, box_x, content_y + self.section_offsets[0])
        self.draw_scoreboard_section(screen, box_x, content_y + self.section_offsets[1])
        self.draw_difficulty_section(screen, box_x, content_y + self.section_offsets[2])
        self.draw_checkpoints_section(screen, box_x, content_y + self.section_offsets[3])
        self.draw_controls_section(screen, box_x, content_y + self.section_offsets[4])

        # Clear clip
        screen.set_clip(None)

        # Draw scrollbar if needed
        if self.max_scroll > 0:
            self.draw_scrollbar(screen, box_x + box_width + 5, box_y, box_height)

    def draw_tabs(self, screen):
        """Draw navigation tabs at top of guide"""
        tab_width = 120
        tab_height = 35
        tab_spacing = 10
        total_width = (tab_width * 5) + (tab_spacing * 4)
        start_x = (S.WINDOW_WIDTH - total_width) // 2
        tab_y = 95

        # Tab icons (simple indicators)
        for i in range(5):
            x = start_x + (i * (tab_width + tab_spacing))

            # Determine if tab is active or hovered
            is_active = (i == self.active_tab)
            is_hovered = (i == self.tab_hover)

            # Draw tab box
            tab_rect = pygame.Rect(x, tab_y, tab_width, tab_height)
            if is_active:
                color = (255, 140, 0)  # Orange for active
                border_color = (255, 200, 100)
            elif is_hovered:
                color = (150, 100, 50)  # Lighter brown for hover
                border_color = (180, 140, 80)
            else:
                color = (101, 67, 33)  # Dark brown
                border_color = (139, 89, 49)

            pygame.draw.rect(screen, color, tab_rect)
            pygame.draw.rect(screen, border_color, tab_rect, 3)

            # Draw tab label
            label_text = f"{i+1}. {self.section_labels[i]}"
            text_color = (255, 255, 255) if is_active else (200, 200, 200)
            label_surface = self.small_font.render(label_text, True, text_color)
            label_rect = label_surface.get_rect(center=(x + tab_width//2, tab_y + tab_height//2))
            screen.blit(label_surface, label_rect)

    def draw_scrollbar(self, screen, x, y, height):
        """Draw scrollbar to indicate scroll position"""
        # Background track
        pygame.draw.rect(screen, (80, 80, 80), (x, y, 8, height))

        # Calculate thumb position and size
        if self.max_scroll > 0:
            thumb_height = max(20, int(height * (self.visible_height / self.content_height)))
            thumb_y = y + int((self.scroll_offset / self.max_scroll) * (height - thumb_height))

            # Thumb
            pygame.draw.rect(screen, (200, 200, 200), (x, thumb_y, 8, thumb_height))
            pygame.draw.rect(screen, (255, 255, 255), (x, thumb_y, 8, thumb_height), 1)

    def draw_back_button(self, screen):
        """Draw back button with arrow in top left"""
        button_x = 20
        button_y = 20
        button_width = 100
        button_height = 40

        # Button background color (darker if hovered)
        if self.back_hover:
            color = (150, 100, 50)
            border_color = (180, 140, 80)
        else:
            color = (101, 67, 33)
            border_color = (139, 89, 49)

        # Draw button box
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        pygame.draw.rect(screen, color, button_rect)
        pygame.draw.rect(screen, border_color, button_rect, 3)

        # Draw left arrow
        arrow_x = button_x + 15
        arrow_y = button_y + button_height // 2
        arrow_points = [
            (arrow_x + 10, arrow_y - 8),
            (arrow_x, arrow_y),
            (arrow_x + 10, arrow_y + 8)
        ]
        pygame.draw.polygon(screen, (255, 255, 255), arrow_points)

        # Draw "Back" text
        back_text = self.small_font.render("Back", True, (255, 255, 255))
        text_rect = back_text.get_rect(center=(button_x + 65, button_y + button_height // 2))
        screen.blit(back_text, text_rect)

    def draw_game_modes_section(self, screen, box_x, y):
        """Draw Game Modes section"""
        # Section header with icon
        WinterTheme.draw_snowflake_icon(screen, box_x + 30, y + 10, 12)
        header = self.header_font.render("GAME MODES", True, (255, 200, 100))
        screen.blit(header, (box_x + 50, y))

        y += 30

        # Story Mode
        subsection = self.text_font.render("Story Mode", True, (180, 220, 255))
        screen.blit(subsection, (box_x + 30, y))
        y += 22

        lines = [
            "Main narrative experience with progressive",
            "ability unlocks. Start with basic movement,",
            "unlock Roll after Level 1, and Spin Attack",
            "before Level 3. Follow Siena's journey to",
            "reunite with family in Antarctica."
        ]
        y = self.draw_multiline_text(screen, self.small_font, lines, WinterTheme.TEXT_DARK, box_x + 30, y, 16)

        y += 10

        # Level Selection
        subsection = self.text_font.render("Level Selection", True, (180, 220, 255))
        screen.blit(subsection, (box_x + 30, y))
        y += 22

        lines = [
            "Practice individual levels after unlocking",
            "in Story Mode. Try different difficulties",
            "or checkpoint settings. Improve scores!"
        ]
        self.draw_multiline_text(screen, self.small_font, lines, WinterTheme.TEXT_DARK, box_x + 30, y, 16)

    def draw_scoreboard_section(self, screen, box_x, y):
        """Draw Scoreboard section"""
        # Section header with trophy icon
        self.draw_trophy_icon(screen, box_x + 30, y + 8, 12)
        header = self.header_font.render("SCOREBOARD", True, (255, 200, 100))
        screen.blit(header, (box_x + 50, y))

        y += 30

        lines = [
            "View top 100 scores per level.",
            "Filter by difficulty: Easy/Medium/Hard",
            "Filter by checkpoint usage: On/Off",
            "Scores show: Rank, Name, Time, Coins,",
            "Difficulty, Checkpoints",
            "Top 3 players get special highlighting!"
        ]
        self.draw_multiline_text(screen, self.small_font, lines, WinterTheme.TEXT_DARK, box_x + 30, y, 16)

    def draw_difficulty_section(self, screen, box_x, y):
        """Draw Difficulty section"""
        # Section header with bars icon
        self.draw_bars_icon(screen, box_x + 30, y + 8, 12)
        header = self.header_font.render("DIFFICULTY", True, (255, 200, 100))
        screen.blit(header, (box_x + 50, y))

        y += 30

        # Easy
        easy = self.text_font.render("Easy Mode", True, (100, 255, 100))
        screen.blit(easy, (box_x + 30, y))
        y += 20
        lines = [
            "Collect 50-56% of coins to complete.",
            "Forgiving - perfect for first playthrough."
        ]
        y = self.draw_multiline_text(screen, self.small_font, lines, WinterTheme.TEXT_DARK, box_x + 30, y, 16)

        y += 10

        # Medium
        medium = self.text_font.render("Medium Mode (Default)", True, (255, 255, 100))
        screen.blit(medium, (box_x + 30, y))
        y += 20
        lines = [
            "Collect 69-75% of coins to complete.",
            "Balanced challenge for most players."
        ]
        y = self.draw_multiline_text(screen, self.small_font, lines, WinterTheme.TEXT_DARK, box_x + 30, y, 16)

        y += 10

        # Hard
        hard = self.text_font.render("Hard Mode", True, (255, 100, 100))
        screen.blit(hard, (box_x + 30, y))
        y += 20
        lines = [
            "Collect 89-93% of coins to complete.",
            "Nearly all coins needed!"
        ]
        y = self.draw_multiline_text(screen, self.small_font, lines, WinterTheme.TEXT_DARK, box_x + 30, y, 16)

        y += 5
        note = self.small_font.render("Change in Settings (gear icon, top-right)", True, (180, 220, 255))
        screen.blit(note, (box_x + 30, y))

    def draw_checkpoints_section(self, screen, box_x, y):
        """Draw Checkpoints section"""
        # Section header with flag icon
        self.draw_flag_icon(screen, box_x + 30, y + 8, 12)
        header = self.header_font.render("CHECKPOINTS", True, (255, 200, 100))
        screen.blit(header, (box_x + 50, y))

        y += 30

        # What
        what = self.text_font.render("What Are They?", True, (180, 220, 255))
        screen.blit(what, (box_x + 30, y))
        y += 20
        lines = [
            "Progress markers throughout levels.",
            "Green flag markers show locations.",
            "Respawn at last checkpoint if you die."
        ]
        y = self.draw_multiline_text(screen, self.small_font, lines, WinterTheme.TEXT_DARK, box_x + 30, y, 16)

        y += 10

        # How
        how = self.text_font.render("How to Enable:", True, (180, 220, 255))
        screen.blit(how, (box_x + 30, y))
        y += 20
        lines = [
            "Toggle in Settings (gear icon, top-right)",
            "OFF by default - must opt-in.",
            "Setting persists across sessions."
        ]
        y = self.draw_multiline_text(screen, self.small_font, lines, WinterTheme.TEXT_DARK, box_x + 30, y, 16)

        y += 10

        # Impact
        impact = self.text_font.render("Scoreboard Impact:", True, (255, 100, 100))
        screen.blit(impact, (box_x + 30, y))
        y += 20
        lines = [
            "Checkpoint usage IS displayed!",
            "Allows fair comparison between players."
        ]
        self.draw_multiline_text(screen, self.small_font, lines, WinterTheme.TEXT_DARK, box_x + 30, y, 16)

    def draw_controls_section(self, screen, box_x, y):
        """Draw Controls section (adapted from original)"""
        # Section header with controller icon
        self.draw_controller_icon(screen, box_x + 30, y + 8, 12)
        header = self.header_font.render("CONTROLS", True, (255, 200, 100))
        screen.blit(header, (box_x + 50, y))

        y += 35

        # Controls list
        controls = [
            ("MOVE", "Arrow Keys / A-D"),
            ("JUMP", "Space / W / Up"),
            ("CROUCH", "Down / S"),
            ("ROLL", "Down + Left/Right"),
            ("SPIN ATTACK", "E (in air)"),
            ("RESTART", "Shift + Enter"),
        ]

        for action, keys in controls:
            # Action name (left side)
            action_text = self.text_font.render(action, True, (255, 200, 100))
            action_rect = action_text.get_rect(right=box_x + 400, centery=y)
            screen.blit(action_text, action_rect)

            # Divider
            pygame.draw.circle(screen, WinterTheme.GLOW_BLUE, (box_x + 420, y), 4)

            # Keys (right side)
            keys_text = self.text_font.render(keys, True, WinterTheme.TEXT_DARK)
            keys_rect = keys_text.get_rect(left=box_x + 440, centery=y)
            screen.blit(keys_text, keys_rect)

            y += 28