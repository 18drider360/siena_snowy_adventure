import pygame
from utils import settings as S
from ui.winter_theme import Snowflake, WinterTheme

class TitleScreen:
    """Main title screen with Mario Bros-style presentation"""
    
    def __init__(self):
        # Menu options
        self.options = ["START GAME", "LEVEL SELECTION", "SCOREBOARD", "CONTROLS"]
        self.selected_index = 0

        # Settings icon state
        self.settings_hover = False

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
                return "navigate"

            elif event.key in (pygame.K_DOWN, pygame.K_s):
                # Move down one row
                row = (row + 1) % 2
                self.selected_index = (row * 2) + col
                return "navigate"

            elif event.key in (pygame.K_LEFT, pygame.K_a):
                # Move left one column
                col = (col - 1) % 2
                self.selected_index = (row * 2) + col
                return "navigate"

            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                # Move right one column
                col = (col + 1) % 2
                self.selected_index = (row * 2) + col
                return "navigate"

            elif event.key == pygame.K_RETURN:
                return self.options[self.selected_index]

        elif event.type == pygame.MOUSEMOTION:
            # Update selection based on mouse position (scaled to internal coordinates)
            mouse_pos = pygame.mouse.get_pos()
            scaled_pos = (int(mouse_pos[0] / S.DISPLAY_SCALE), int(mouse_pos[1] / S.DISPLAY_SCALE))

            # Check settings icon hover
            settings_rect = self.get_settings_icon_rect()
            self.settings_hover = settings_rect.collidepoint(scaled_pos)

            clicked_option = self.get_option_at_pos(scaled_pos)
            if clicked_option is not None:
                self.selected_index = clicked_option

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Click to select (scaled to internal coordinates)
            mouse_pos = pygame.mouse.get_pos()
            scaled_pos = (int(mouse_pos[0] / S.DISPLAY_SCALE), int(mouse_pos[1] / S.DISPLAY_SCALE))

            # Check settings icon click
            settings_rect = self.get_settings_icon_rect()
            if settings_rect.collidepoint(scaled_pos):
                return "SETTINGS"

            clicked_option = self.get_option_at_pos(scaled_pos)
            if clicked_option is not None:
                self.selected_index = clicked_option
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
    
    def draw_footer(self, screen):
        """Draw footer - removed navigation hints"""
        pass  # No footer text needed
    
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

    def draw(self, screen):
        """Draw the complete title screen"""
        # Winter sky background (lighter blue/white)
        screen.fill((200, 220, 255))
        
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

    def handle_input(self, event):
        """Handle level selection input (keyboard and mouse)"""
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_a):
                if self.selected_level > 1:
                    self.selected_level -= 1
                return "navigate"

            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                if self.selected_level < self.max_level:
                    self.selected_level += 1
                return "navigate"

            elif event.key == pygame.K_RETURN:
                return f"LEVEL_{self.selected_level}"

            elif event.key == pygame.K_ESCAPE:
                return "BACK"

        elif event.type == pygame.MOUSEMOTION:
            # Update selection on hover (scaled to internal coordinates)
            mouse_pos = pygame.mouse.get_pos()
            scaled_pos = (int(mouse_pos[0] / S.DISPLAY_SCALE), int(mouse_pos[1] / S.DISPLAY_SCALE))
            level = self.get_level_at_pos(scaled_pos)
            if level is not None:
                self.selected_level = level

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Click to select level (scaled to internal coordinates)
            mouse_pos = pygame.mouse.get_pos()
            scaled_pos = (int(mouse_pos[0] / S.DISPLAY_SCALE), int(mouse_pos[1] / S.DISPLAY_SCALE))
            level = self.get_level_at_pos(scaled_pos)
            if level is not None:
                self.selected_level = level
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


class ControlsScreen:
    """Controls/instructions screen with winter theme"""

    def __init__(self):
        try:
            self.title_font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 36)
            self.text_font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 16)
            self.small_font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 14)
        except:
            self.title_font = pygame.font.Font(None, 56)
            self.text_font = pygame.font.Font(None, 28)
            self.small_font = pygame.font.Font(None, 24)

        # Snowflakes
        self.snowflakes = [Snowflake(S.WINDOW_WIDTH, S.WINDOW_HEIGHT) for _ in range(60)]

    def handle_input(self, event):
        """Handle controls screen input"""
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                return "BACK"
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Click anywhere to go back
            return "BACK"
        return None

    def draw(self, screen):
        """Draw controls screen with winter theme"""
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
        WinterTheme.draw_text_with_shadow(screen, self.title_font, "CONTROLS",
                                         WinterTheme.SNOW_WHITE, S.WINDOW_WIDTH // 2, 60)

        # Draw control box
        box_width = 650
        box_height = 420
        box_x = (S.WINDOW_WIDTH - box_width) // 2
        box_y = 120

        WinterTheme.draw_frosted_box(screen, box_x, box_y, box_width, box_height, 170)

        # Controls list
        controls = [
            ("MOVE", "Arrow Keys / A-D"),
            ("JUMP", "Space / W / Up"),
            ("CROUCH", "Down / S"),
            ("ROLL", "Down + Left/Right"),
            ("SPIN ATTACK", "E (in air)"),
            ("RESTART", "Shift + Enter"),
        ]

        y_start = box_y + 60
        y_spacing = 55

        for i, (action, keys) in enumerate(controls):
            y = y_start + (i * y_spacing)

            # Action name (left side)
            action_text = self.text_font.render(action, True, (255, 200, 100))
            action_rect = action_text.get_rect(right=S.WINDOW_WIDTH // 2 - 30, centery=y)
            screen.blit(action_text, action_rect)

            # Divider
            pygame.draw.circle(screen, WinterTheme.GLOW_BLUE, (S.WINDOW_WIDTH // 2, y), 5)

            # Keys (right side)
            keys_text = self.text_font.render(keys, True, WinterTheme.TEXT_DARK)
            keys_rect = keys_text.get_rect(left=S.WINDOW_WIDTH // 2 + 30, centery=y)
            screen.blit(keys_text, keys_rect)

        # Back instruction
        back_text = self.small_font.render("ESC / ENTER : BACK", True, WinterTheme.ICE_BLUE)
        back_rect = back_text.get_rect(center=(S.WINDOW_WIDTH // 2, S.WINDOW_HEIGHT - 40))
        screen.blit(back_text, back_rect)