"""
Input Handler
Centralized input processing for the game
"""

import pygame
from src.core.game_logging import get_logger

logger = get_logger(__name__)


class InputHandler:
    """
    Handles all keyboard and mouse input for the game

    This class centralizes input processing to prevent scattered
    event handling throughout the code.
    """

    def __init__(self):
        """Initialize the input handler"""
        self.quit_requested = False
        logger.debug("InputHandler initialized")

    def handle_events(self, game_state, player, pause_menu, death_menu, audio_manager):
        """
        Process all pygame events

        Args:
            game_state: GameStateManager instance
            player: Player instance
            pause_menu: PauseMenu instance
            death_menu: DeathMenu instance
            audio_manager: AudioManager instance

        Returns:
            str or None: Command string ("RESTART", "MAIN_MENU", etc.) or None
        """
        command = None

        if not game_state.cutscene_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_requested = True
                    return "QUIT"

                # Handle keyboard events
                if event.type == pygame.KEYDOWN:
                    result = self._handle_keydown(
                        event, game_state, player, pause_menu, death_menu, audio_manager
                    )
                    if result:
                        command = result

                # Handle mouse events
                elif event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN):
                    result = self._handle_mouse(
                        event, game_state, pause_menu, death_menu, audio_manager
                    )
                    if result:
                        command = result

        return command

    def _handle_keydown(self, event, game_state, player, pause_menu, death_menu, audio_manager):
        """
        Handle keyboard events

        Returns:
            str or None: Command string or None
        """
        # ESC key - Pause toggle
        if event.key == pygame.K_ESCAPE:
            return self._handle_escape(game_state, audio_manager)

        # Handle pause menu input
        if game_state.paused:
            return self._handle_pause_menu_input(event, pause_menu, game_state, audio_manager)

        # Handle death menu input
        if game_state.show_death_screen:
            return self._handle_death_menu_input(event, death_menu, audio_manager)

        # Gameplay input (only if actively playing)
        if game_state.is_playing:
            return self._handle_gameplay_input(event, player, audio_manager)

        return None

    def _handle_escape(self, game_state, audio_manager):
        """Handle ESC key press"""
        # Play click sound for Escape key
        audio_manager.play_sound('select_click', volume=0.3)

        if not game_state.game_over and not game_state.cutscene_active:
            game_state.toggle_pause()
            if game_state.paused:
                audio_manager.pause_music()
            else:
                audio_manager.unpause_music()
        elif game_state.paused:
            game_state.unpause()
            audio_manager.unpause_music()
        return None

    def _handle_pause_menu_input(self, event, pause_menu, game_state, audio_manager):
        """Handle input when pause menu is active"""
        result = pause_menu.handle_input(event)

        if result == "CONTINUE":
            game_state.unpause()
            audio_manager.unpause_music()
            return None

        elif result == "RESTART":
            audio_manager.stop_music()
            return "RESTART"

        elif result == "MAIN MENU":
            audio_manager.stop_music()
            return "MAIN_MENU"

        return None

    def _handle_death_menu_input(self, event, death_menu, audio_manager):
        """Handle input when death menu is active"""
        result = death_menu.handle_input(event)

        if result == "RESTART":
            audio_manager.stop_music()
            return "RESTART"

        elif result == "CHECKPOINT":
            # Don't stop music for checkpoint respawn
            return "CHECKPOINT"

        elif result == "MAIN MENU":
            audio_manager.stop_music()
            return "MAIN_MENU"

        return None

    def _handle_gameplay_input(self, event, player, audio_manager):
        """Handle gameplay input (jumps, attacks, etc.)"""
        # Jump
        if event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
            player.jump(
                audio_manager.get_sound('jump'),
                audio_manager.get_sound('double_jump')
            )

        # Spin attack
        elif event.key == pygame.K_e:
            player.spin_attack(audio_manager.get_sound('spin_attack'))

        # Quick restart (Shift+Enter)
        elif event.key == pygame.K_RETURN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
                return "RESTART"

        return None

    def _handle_mouse(self, event, game_state, pause_menu, death_menu, audio_manager):
        """
        Handle mouse events

        Returns:
            str or None: Command string or None
        """
        # Handle pause menu mouse input
        if game_state.paused:
            result = pause_menu.handle_input(event)

            if result == "CONTINUE":
                game_state.unpause()
                audio_manager.unpause_music()
                return None

            elif result == "RESTART":
                audio_manager.stop_music()
                return "RESTART"

            elif result == "MAIN MENU":
                audio_manager.stop_music()
                return "MAIN_MENU"

        # Handle death menu mouse input
        elif game_state.show_death_screen:
            result = death_menu.handle_input(event)

            if result == "RESTART":
                audio_manager.stop_music()
                return "RESTART"

            elif result == "CHECKPOINT":
                # Don't stop music for checkpoint respawn
                return "CHECKPOINT"

            elif result == "MAIN MENU":
                audio_manager.stop_music()
                return "MAIN_MENU"

        return None

    def get_pressed_keys(self):
        """
        Get currently pressed keys

        Returns:
            pygame.key.ScancodeWrapper: Currently pressed keys
        """
        return pygame.key.get_pressed()
