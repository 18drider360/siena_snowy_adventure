# Temporary file with the section methods - will be copied into title_screen.py

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
