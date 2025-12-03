"""
Username Input Screen
Allows player to enter their username or generate a random one
Winter-themed with falling snow animation
"""

import pygame
import random
from utils import settings as S


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


class UsernameInput:
    """Handles username input from the player with winter theme"""

    # Lists for random username generation
    ADJECTIVES = [
        "Tiny", "Little", "Swift", "Brave", "Mighty", "Cool", "Frosty", "Snowy",
        "Icy", "Chill", "Arctic", "Winter", "Frozen", "Bold", "Quick", "Happy",
        "Lucky", "Smart", "Clever", "Wild", "Bright", "Shiny", "Silent", "Stealth",
        "Epic", "Super", "Mega", "Ultra", "Turbo", "Hyper"
    ]

    NOUNS = [
        "Gamer", "Player", "Hero", "Ninja", "Wizard", "Knight", "Dragon", "Tiger",
        "Wolf", "Bear", "Fox", "Hawk", "Eagle", "Lion", "Panda", "Penguin",
        "Racoon", "Otter", "Yeti", "Snowman", "Warrior", "Champion", "Legend",
        "Master", "Pro", "Star", "Comet", "Storm", "Blaze", "Thunder"
    ]

    def __init__(self, screen):
        self.screen = screen
        self.username = ""
        self.max_length = 12
        self.cursor_visible = True
        self.cursor_timer = 0
        self.cursor_blink_rate = 30
        self.selected_button = None  # Track which button is selected with keyboard
        self.button_hover = None  # Track which button is being hovered with mouse

        # Wintery color palette
        self.bg_gradient_top = (15, 30, 60)
        self.bg_gradient_bottom = (40, 70, 120)
        self.snow_white = (255, 255, 255)
        self.ice_blue = (180, 220, 255)
        self.frost_blue = (200, 230, 255)
        self.dark_ice = (100, 150, 200)
        self.glow_blue = (150, 200, 255)

        # Fonts
        try:
            self.title_font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 32)
            self.input_font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 20)
            self.button_font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 12)
            self.hint_font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 12)
        except:
            self.title_font = pygame.font.Font(None, 48)
            self.input_font = pygame.font.Font(None, 32)
            self.button_font = pygame.font.Font(None, 18)
            self.hint_font = pygame.font.Font(None, 18)

        # Create snowflakes
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        self.snowflakes = [Snowflake(screen_width, screen_height) for _ in range(100)]

    def generate_random_username(self):
        """Generate a random username: Adjective + Noun + 2-digit number"""
        adjective = random.choice(self.ADJECTIVES)
        noun = random.choice(self.NOUNS)
        number = random.randint(10, 99)
        return f"{adjective}{noun}{number}"

    def get_button_rect(self, button_name):
        """Get the rect for a specific button"""
        screen_width = self.screen.get_width()

        if button_name == "generate":
            # To the right of the input box - moved further right
            # Input box ends at screen_width // 2 + 170, so start button at +190
            return pygame.Rect(screen_width // 2 + 190, 230, 240, 50)
        elif button_name == "confirm":
            # Below the input box, centered
            return pygame.Rect(screen_width // 2 - 100, 360, 200, 50)

        return None

    def handle_event(self, event):
        """Handle keyboard and mouse input"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # If a button is selected, activate it
                if self.selected_button == "generate":
                    self.username = self.generate_random_username()
                    return False
                elif self.selected_button == "confirm":
                    # Only confirm if username has at least 1 character
                    if self.username.strip():
                        return True
                    # If empty, ignore the Enter key
                else:
                    # No button selected - just confirm username
                    # Only confirm if username has at least 1 character
                    if self.username.strip():
                        return True
                    # If empty, ignore the Enter key

            elif event.key == pygame.K_ESCAPE:
                # Use default
                self.username = "Player"
                return True

            elif event.key == pygame.K_BACKSPACE:
                self.username = self.username[:-1]
                # If username becomes empty and confirm button is selected, deselect it
                if not self.username.strip() and self.selected_button == "confirm":
                    self.selected_button = None

            elif event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN):
                # Arrow navigation between buttons
                # Don't allow selecting confirm button if username is empty
                if self.selected_button is None:
                    self.selected_button = "generate"
                elif self.selected_button == "generate":
                    # Only allow switching to confirm if username has text
                    if self.username.strip():
                        self.selected_button = "confirm"
                else:
                    self.selected_button = "generate"

            elif event.key == pygame.K_SPACE and self.selected_button:
                # Activate selected button with spacebar
                if self.selected_button == "generate":
                    self.username = self.generate_random_username()
                elif self.selected_button == "confirm":
                    # Only confirm if username has at least 1 character
                    if self.username.strip():
                        return True
                    # If empty, ignore the spacebar

            else:
                # Regular typing
                if len(self.username) < self.max_length:
                    char = event.unicode
                    if char.isalnum() or char in " -_":
                        self.username += char
                        self.selected_button = None  # Deselect button when typing

        elif event.type == pygame.MOUSEMOTION:
            # Check button hover (no scaling needed - already in display coordinates)
            mouse_pos = pygame.mouse.get_pos()

            self.button_hover = None
            for button in ["generate", "confirm"]:
                # Don't allow hover on confirm button if username is empty
                if button == "confirm" and not self.username.strip():
                    continue

                rect = self.get_button_rect(button)
                if rect and rect.collidepoint(mouse_pos):
                    self.button_hover = button
                    break

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Handle button clicks (no scaling needed - already in display coordinates)
            mouse_pos = pygame.mouse.get_pos()

            # Generate button
            generate_rect = self.get_button_rect("generate")
            if generate_rect.collidepoint(mouse_pos):
                self.username = self.generate_random_username()
                return False

            # Confirm button - only clickable if username has at least 1 character
            confirm_rect = self.get_button_rect("confirm")
            if confirm_rect.collidepoint(mouse_pos):
                if self.username.strip():
                    return True
                # If empty, don't do anything (ignore click)

        return False

    def update(self):
        """Update animations"""
        self.cursor_timer += 1
        if self.cursor_timer >= self.cursor_blink_rate:
            self.cursor_timer = 0
            self.cursor_visible = not self.cursor_visible

        # Update snowflakes
        for snowflake in self.snowflakes:
            snowflake.update()

    def draw_gradient_background(self):
        """Draw a beautiful gradient background"""
        screen_height = self.screen.get_height()
        for y in range(screen_height):
            ratio = y / screen_height
            r = int(self.bg_gradient_top[0] + (self.bg_gradient_bottom[0] - self.bg_gradient_top[0]) * ratio)
            g = int(self.bg_gradient_top[1] + (self.bg_gradient_bottom[1] - self.bg_gradient_top[1]) * ratio)
            b = int(self.bg_gradient_top[2] + (self.bg_gradient_bottom[2] - self.bg_gradient_top[2]) * ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (self.screen.get_width(), y))

    def draw_frosted_box(self, x, y, width, height):
        """Draw a frosted glass effect box"""
        # Shadow
        shadow = pygame.Surface((width + 8, height + 8))
        shadow.fill((0, 0, 0))
        shadow.set_alpha(60)
        self.screen.blit(shadow, (x + 4, y + 4))

        # Main box with transparency
        box_surface = pygame.Surface((width, height))
        box_surface.fill(self.frost_blue)
        box_surface.set_alpha(180)
        self.screen.blit(box_surface, (x, y))

        # Border with glow effect
        border_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, self.glow_blue, border_rect, 3)

        # Inner highlight (top-left)
        pygame.draw.line(self.screen, (255, 255, 255), (x + 5, y + 5), (x + width - 5, y + 5), 2)
        pygame.draw.line(self.screen, (255, 255, 255), (x + 5, y + 5), (x + 5, y + height - 5), 2)

    def draw_button(self, text, rect, button_name, is_selected=False):
        """Draw a button with hover effect"""
        # Check if button should be disabled (confirm button with empty username)
        is_disabled = (button_name == "confirm" and not self.username.strip())

        is_hovered = (self.button_hover == button_name) and not is_disabled

        # Draw glow if hovered or selected (but not if disabled)
        if (is_hovered or is_selected) and not is_disabled:
            glow_rect = rect.inflate(8, 8)
            glow_surface = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
            glow_surface.fill((255, 200, 0, 80))
            self.screen.blit(glow_surface, glow_rect.topleft)

        # Draw button background
        if is_disabled:
            button_color = (60, 60, 80)  # Dark grey for disabled
            text_color = (100, 100, 120)  # Muted text
            border_color = (80, 80, 100)
        elif is_hovered:
            button_color = (120, 160, 220)  # Lighter when hovered
            text_color = (255, 255, 255)
            border_color = self.glow_blue
        elif is_selected:
            button_color = (100, 180, 255)  # Bright blue for keyboard-selected
            text_color = (255, 255, 255)
            border_color = self.glow_blue
        else:
            button_color = (80, 120, 180)  # Dark blue
            text_color = (200, 220, 255)
            border_color = self.glow_blue

        pygame.draw.rect(self.screen, button_color, rect)
        pygame.draw.rect(self.screen, border_color, rect, 3)

        # Draw button text
        button_text = self.button_font.render(text, True, text_color)
        button_text_rect = button_text.get_rect(center=rect.center)
        self.screen.blit(button_text, button_text_rect)

    def draw(self):
        """Draw the username input screen with winter theme"""
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()

        # Draw gradient background
        self.draw_gradient_background()

        # Draw snowflakes
        for snowflake in self.snowflakes:
            snowflake.draw(self.screen)

        # Draw decorative snowflake icons
        snowflake_positions = [
            (100, 80), (screen_width - 100, 80)
        ]
        for pos in snowflake_positions:
            self.draw_snowflake_icon(pos[0], pos[1], 25)

        # Draw title "USERNAME"
        title_text = "USERNAME"
        title_shadow = self.title_font.render(title_text, True, (0, 0, 0))
        shadow_rect = title_shadow.get_rect(center=(screen_width // 2 + 3, 103))
        self.screen.blit(title_shadow, shadow_rect)

        title_surface = self.title_font.render(title_text, True, self.snow_white)
        title_rect = title_surface.get_rect(center=(screen_width // 2, 100))
        self.screen.blit(title_surface, title_rect)

        # Draw input box (left side)
        input_box_width = 420
        input_box_height = 70
        input_box_x = screen_width // 2 - 250
        input_box_y = 220

        self.draw_frosted_box(input_box_x, input_box_y, input_box_width, input_box_height)

        # Show the username being typed
        display_text = self.username if self.username else ""
        text_surface = self.input_font.render(display_text, True, (20, 40, 80))
        text_rect = text_surface.get_rect(midleft=(input_box_x + 20, input_box_y + input_box_height // 2))
        self.screen.blit(text_surface, text_rect)

        # Draw cursor
        if self.cursor_visible and self.selected_button is None:
            cursor_x = text_rect.right + 8 if display_text else input_box_x + 20
            cursor_y = input_box_y + 15
            glow_surface = pygame.Surface((6, input_box_height - 30))
            glow_surface.fill(self.glow_blue)
            glow_surface.set_alpha(150)
            self.screen.blit(glow_surface, (cursor_x - 1, cursor_y))
            pygame.draw.rect(self.screen, (20, 40, 80), (cursor_x, cursor_y, 4, input_box_height - 30))

        # Draw "Generate Random Username" button (right of input box)
        generate_rect = self.get_button_rect("generate")
        self.draw_button("GENERATE RANDOM", generate_rect, "generate", self.selected_button == "generate")

        # Draw "Confirm" button (below, centered)
        confirm_rect = self.get_button_rect("confirm")
        self.draw_button("CONFIRM", confirm_rect, "confirm", self.selected_button == "confirm")

        # Draw hint text
        hint_text = "PRESS ENTER TO CONFIRM"
        hint_surface = self.hint_font.render(hint_text, True, self.ice_blue)
        hint_rect = hint_surface.get_rect(center=(screen_width // 2, 430))
        self.screen.blit(hint_surface, hint_rect)

        # Additional hint about max characters
        char_hint = f"MAX {self.max_length} CHARACTERS"
        char_surface = self.hint_font.render(char_hint, True, (180, 200, 220))
        char_rect = char_surface.get_rect(center=(screen_width // 2, 460))
        self.screen.blit(char_surface, char_rect)

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


class PlayerProfileScreen:
    """Player profile screen for viewing username and changing difficulty"""

    def __init__(self, screen, current_username, current_difficulty="Medium"):
        self.screen = screen
        self.username = current_username
        self.difficulty = current_difficulty

        # Selection tracking
        self.button_hover = None

        # Difficulty options
        self.difficulties = ["Easy", "Medium", "Hard"]

        # Winter color palette
        self.bg_gradient_top = (15, 30, 60)
        self.bg_gradient_bottom = (40, 70, 120)
        self.snow_white = (255, 255, 255)
        self.ice_blue = (180, 220, 255)
        self.frost_blue = (200, 230, 255)
        self.glow_blue = (150, 200, 255)

        # Fonts
        try:
            self.title_font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 28)
            self.label_font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 16)
            self.input_font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 18)
            self.button_font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 14)
            self.note_font = pygame.font.Font("assets/fonts/PressStart2P-Regular.ttf", 10)
        except:
            self.title_font = pygame.font.Font(None, 42)
            self.label_font = pygame.font.Font(None, 24)
            self.input_font = pygame.font.Font(None, 28)
            self.button_font = pygame.font.Font(None, 20)
            self.note_font = pygame.font.Font(None, 16)

        # Create snowflakes
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        self.snowflakes = [Snowflake(screen_width, screen_height) for _ in range(50)]

    def get_username_box_rect(self):
        """Get rect for username input box"""
        screen_width = self.screen.get_width()
        return pygame.Rect(screen_width // 2 - 200, 180, 400, 50)

    def get_difficulty_button_rect(self, difficulty):
        """Get rect for a difficulty button"""
        screen_width = self.screen.get_width()
        index = self.difficulties.index(difficulty)
        x = screen_width // 2 - 300 + (index * 200)
        return pygame.Rect(x, 320, 180, 50)

    def get_back_button_rect(self):
        """Get rect for back button"""
        screen_width = self.screen.get_width()
        return pygame.Rect(screen_width // 2 - 100, 500, 200, 50)

    def handle_event(self, event):
        """Handle input events"""
        from utils import settings as S

        if event.type == pygame.KEYDOWN:
            # Handle navigation with arrow keys
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                return "BACK"

            elif event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                # Navigate between difficulty options
                current_index = self.difficulties.index(self.difficulty)
                if event.key == pygame.K_LEFT:
                    current_index = (current_index - 1) % len(self.difficulties)
                else:  # RIGHT
                    current_index = (current_index + 1) % len(self.difficulties)
                self.difficulty = self.difficulties[current_index]

        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            # Scale mouse position to internal coordinates
            scaled_pos = (int(mouse_pos[0] / S.DISPLAY_SCALE), int(mouse_pos[1] / S.DISPLAY_SCALE))

            # Check button hovers
            self.button_hover = None

            # Check difficulty buttons
            for difficulty in self.difficulties:
                rect = self.get_difficulty_button_rect(difficulty)
                if rect.collidepoint(scaled_pos):
                    self.button_hover = difficulty
                    break

            # Check back button
            if not self.button_hover:
                back_rect = self.get_back_button_rect()
                if back_rect.collidepoint(scaled_pos):
                    self.button_hover = "BACK"

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            # Scale mouse position to internal coordinates
            scaled_pos = (int(mouse_pos[0] / S.DISPLAY_SCALE), int(mouse_pos[1] / S.DISPLAY_SCALE))

            # Check difficulty buttons
            for difficulty in self.difficulties:
                rect = self.get_difficulty_button_rect(difficulty)
                if rect.collidepoint(scaled_pos):
                    self.difficulty = difficulty
                    return None

            # Check back button
            back_rect = self.get_back_button_rect()
            if back_rect.collidepoint(scaled_pos):
                return "BACK"

        return None

    def update(self):
        """Update animations"""
        # Update snowflakes
        for snowflake in self.snowflakes:
            snowflake.update()

    def draw_gradient_background(self):
        """Draw gradient background"""
        screen_height = self.screen.get_height()
        for y in range(screen_height):
            ratio = y / screen_height
            r = int(self.bg_gradient_top[0] + (self.bg_gradient_bottom[0] - self.bg_gradient_top[0]) * ratio)
            g = int(self.bg_gradient_top[1] + (self.bg_gradient_bottom[1] - self.bg_gradient_top[1]) * ratio)
            b = int(self.bg_gradient_top[2] + (self.bg_gradient_bottom[2] - self.bg_gradient_top[2]) * ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (self.screen.get_width(), y))

    def draw_frosted_box(self, x, y, width, height):
        """Draw a frosted glass effect box"""
        # Shadow
        shadow = pygame.Surface((width + 8, height + 8))
        shadow.fill((0, 0, 0))
        shadow.set_alpha(60)
        self.screen.blit(shadow, (x + 4, y + 4))

        # Main box with transparency
        box_surface = pygame.Surface((width, height))
        box_surface.fill(self.frost_blue)
        box_surface.set_alpha(180)
        self.screen.blit(box_surface, (x, y))

        # Border with glow effect
        border_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, self.glow_blue, border_rect, 3)

        # Inner highlight
        pygame.draw.line(self.screen, (255, 255, 255), (x + 5, y + 5), (x + width - 5, y + 5), 2)
        pygame.draw.line(self.screen, (255, 255, 255), (x + 5, y + 5), (x + 5, y + height - 5), 2)

    def draw_button(self, text, rect, button_name, is_selected=False):
        """Draw a button with hover effect"""
        is_hovered = (self.button_hover == button_name)

        # Draw glow if hovered or selected
        if is_hovered or is_selected:
            glow_rect = rect.inflate(8, 8)
            glow_surface = pygame.Surface((glow_rect.width, glow_rect.height), pygame.SRCALPHA)
            glow_surface.fill((255, 200, 0, 80))
            self.screen.blit(glow_surface, glow_rect.topleft)

        # Button color
        if is_selected:
            button_color = (100, 180, 255)  # Bright blue for selected difficulty
            text_color = (255, 255, 255)
        elif is_hovered:
            button_color = (120, 160, 220)
            text_color = (255, 255, 255)
        else:
            button_color = (80, 120, 180)
            text_color = (200, 220, 255)

        pygame.draw.rect(self.screen, button_color, rect)
        pygame.draw.rect(self.screen, self.glow_blue, rect, 3)

        # Draw text
        button_text = self.button_font.render(text, True, text_color)
        button_text_rect = button_text.get_rect(center=rect.center)
        self.screen.blit(button_text, button_text_rect)

    def draw(self):
        """Draw the player profile screen"""
        screen_width = self.screen.get_width()

        # Draw gradient background
        self.draw_gradient_background()

        # Draw snowflakes
        for snowflake in self.snowflakes:
            snowflake.draw(self.screen)

        # Draw title
        title_text = "PLAYER PROFILE"
        title_shadow = self.title_font.render(title_text, True, (0, 0, 0))
        shadow_rect = title_shadow.get_rect(center=(screen_width // 2 + 3, 63))
        self.screen.blit(title_shadow, shadow_rect)

        title_surface = self.title_font.render(title_text, True, self.snow_white)
        title_rect = title_surface.get_rect(center=(screen_width // 2, 60))
        self.screen.blit(title_surface, title_rect)

        # Username section
        label_text = "USERNAME"
        label_surface = self.label_font.render(label_text, True, self.ice_blue)
        label_rect = label_surface.get_rect(center=(screen_width // 2, 140))
        self.screen.blit(label_surface, label_rect)

        # Username input box
        username_rect = self.get_username_box_rect()
        self.draw_frosted_box(username_rect.x, username_rect.y, username_rect.width, username_rect.height)

        # Username text (read-only display)
        display_text = self.username if self.username else ""
        text_surface = self.input_font.render(display_text, True, (20, 40, 80))
        text_rect = text_surface.get_rect(center=(username_rect.centerx, username_rect.centery))
        self.screen.blit(text_surface, text_rect)

        # Difficulty section
        difficulty_label = "DIFFICULTY"
        difficulty_label_surface = self.label_font.render(difficulty_label, True, self.ice_blue)
        difficulty_label_rect = difficulty_label_surface.get_rect(center=(screen_width // 2, 270))
        self.screen.blit(difficulty_label_surface, difficulty_label_rect)

        # Difficulty buttons
        for difficulty in self.difficulties:
            rect = self.get_difficulty_button_rect(difficulty)
            is_selected = (difficulty == self.difficulty)
            self.draw_button(difficulty.upper(), rect, difficulty, is_selected)

        # Difficulty explanation note
        note_lines = [
            "Difficulty only affects coin requirements",
            "to pass each level, not the level itself"
        ]
        y_offset = 400
        for line in note_lines:
            note_surface = self.note_font.render(line, True, (180, 200, 220))
            note_rect = note_surface.get_rect(center=(screen_width // 2, y_offset))
            self.screen.blit(note_surface, note_rect)
            y_offset += 20

        # Back button
        back_rect = self.get_back_button_rect()
        self.draw_button("BACK", back_rect, "BACK")

        # Navigation hint
        hint_text = "Use LEFT/RIGHT arrows to change difficulty  |  ENTER or ESC to go back"
        hint_surface = self.note_font.render(hint_text, True, (150, 170, 200))
        hint_rect = hint_surface.get_rect(center=(screen_width // 2, 565))
        self.screen.blit(hint_surface, hint_rect)


def show_username_input(screen):
    """Show username input screen and get username"""
    username_input = UsernameInput(screen)
    clock = pygame.time.Clock()

    # Enable key repeat for holding down keys (delay, interval in milliseconds)
    pygame.key.set_repeat(500, 50)  # 500ms delay, then 50ms between repeats

    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None

                if username_input.handle_event(event):
                    username = username_input.username.strip()
                    return username if username else "Player"

            username_input.update()
            username_input.draw()
            pygame.display.flip()
            clock.tick(60)
    finally:
        # Disable key repeat when leaving username input
        pygame.key.set_repeat()
