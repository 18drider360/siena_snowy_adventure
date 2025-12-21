"""
Game State Manager
Manages all game state flags and transitions
"""

from enum import Enum
from src.core.game_logging import get_logger

logger = get_logger(__name__)


class GameState(Enum):
    """Enumeration of possible game states"""
    PLAYING = "playing"
    PAUSED = "paused"
    GAME_OVER = "game_over"
    CUTSCENE = "cutscene"
    LEVEL_COMPLETE = "level_complete"
    DEATH_SCREEN = "death_screen"


class GameStateManager:
    """
    Manages game state and state transitions

    This class centralizes all game state management to prevent
    scattered state flags throughout the code.
    """

    def __init__(self):
        """Initialize the game state manager"""
        self.state = GameState.PLAYING
        self.previous_state = None

        # Game flags
        self.paused = False
        self.game_over = False
        self.cutscene_active = False
        self.level_complete = False
        self.show_death_screen = False

        # Death animation state
        self.death_animation_timer = 0
        self.death_animation_delay = 90  # frames
        self.death_fade_alpha = 0
        self.death_fade_speed = 5

        # Cutscene state
        self.cutscene_selected_button = "continue"

        logger.debug("GameStateManager initialized")

    def pause(self):
        """Pause the game"""
        if not self.game_over and not self.cutscene_active:
            self.paused = True
            self.previous_state = self.state
            self.state = GameState.PAUSED
            logger.info("Game paused")

    def unpause(self):
        """Unpause the game"""
        if self.paused:
            self.paused = False
            self.state = self.previous_state if self.previous_state else GameState.PLAYING
            logger.info("Game unpaused")

    def toggle_pause(self):
        """Toggle pause state"""
        if self.paused:
            self.unpause()
        else:
            self.pause()

    def trigger_death(self):
        """Trigger player death"""
        if not self.game_over:
            self.game_over = True
            self.death_animation_timer = 0
            self.death_fade_alpha = 0
            self.show_death_screen = False
            self.state = GameState.GAME_OVER
            logger.info("Player died")

    def update_death_animation(self):
        """Update death animation state"""
        if self.game_over and not self.show_death_screen:
            self.death_animation_timer += 1
            if self.death_animation_timer >= self.death_animation_delay:
                self.show_death_screen = True
                self.state = GameState.DEATH_SCREEN
                logger.debug("Death screen shown")

    def trigger_level_complete(self):
        """Trigger level completion"""
        if not self.level_complete:
            self.level_complete = True
            self.cutscene_active = True
            self.state = GameState.LEVEL_COMPLETE
            logger.info("Level complete")

    def start_cutscene(self):
        """Start a cutscene"""
        self.cutscene_active = True
        self.previous_state = self.state
        self.state = GameState.CUTSCENE
        logger.debug("Cutscene started")

    def end_cutscene(self):
        """End a cutscene"""
        self.cutscene_active = False
        self.state = self.previous_state if self.previous_state else GameState.PLAYING
        logger.debug("Cutscene ended")

    def reset_for_new_level(self):
        """Reset state for a new level"""
        self.state = GameState.PLAYING
        self.previous_state = None
        self.paused = False
        self.game_over = False
        self.cutscene_active = False
        self.level_complete = False
        self.show_death_screen = False
        self.death_animation_timer = 0
        self.death_fade_alpha = 0
        logger.info("State reset for new level")

    # Convenience properties for backward compatibility

    @property
    def is_playing(self):
        """Check if game is in active playing state"""
        return not self.game_over and not self.cutscene_active and not self.paused

    @property
    def can_handle_input(self):
        """Check if game can handle player input"""
        return not self.cutscene_active

    @property
    def can_update_game_logic(self):
        """Check if game logic should be updated"""
        return self.is_playing

    def __repr__(self):
        """String representation for debugging"""
        return (f"GameStateManager(state={self.state.value}, "
                f"paused={self.paused}, game_over={self.game_over}, "
                f"level_complete={self.level_complete})")
