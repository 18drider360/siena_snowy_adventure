"""
Game Controller Module
Handles all input processing and game state management
"""

import pygame


class GameController:
    """Manages game input and state transitions"""

    def __init__(self):
        """Initialize the game controller"""
        self.keys_pressed = {}
        self.events = []
        self.quit_requested = False

    def update(self):
        """Update input state - call this once per frame"""
        self.events = pygame.event.get()
        self.keys_pressed = pygame.key.get_pressed()
        self.quit_requested = False

        # Check for quit events
        for event in self.events:
            if event.type == pygame.QUIT:
                self.quit_requested = True

    def is_key_pressed(self, key):
        """Check if a key is currently held down"""
        return self.keys_pressed.get(key, False)

    def was_key_pressed_this_frame(self, key):
        """Check if a key was pressed this frame (not held)"""
        for event in self.events:
            if event.type == pygame.KEYDOWN and event.key == key:
                return True
        return False

    def get_movement_input(self):
        """
        Get horizontal movement input

        Returns:
            int: -1 for left, 1 for right, 0 for no movement
        """
        left = self.is_key_pressed(pygame.K_LEFT) or self.is_key_pressed(pygame.K_a)
        right = self.is_key_pressed(pygame.K_RIGHT) or self.is_key_pressed(pygame.K_d)

        if left and not right:
            return -1
        elif right and not left:
            return 1
        else:
            return 0

    def is_jump_pressed(self):
        """Check if jump button was pressed this frame"""
        return (self.was_key_pressed_this_frame(pygame.K_SPACE) or
                self.was_key_pressed_this_frame(pygame.K_UP) or
                self.was_key_pressed_this_frame(pygame.K_w))

    def is_crouch_held(self):
        """Check if crouch button is held"""
        return (self.is_key_pressed(pygame.K_DOWN) or
                self.is_key_pressed(pygame.K_s))

    def is_roll_pressed(self):
        """Check if roll button was pressed this frame"""
        return self.was_key_pressed_this_frame(pygame.K_LSHIFT) or self.was_key_pressed_this_frame(pygame.K_RSHIFT)

    def is_spin_attack_pressed(self):
        """Check if spin attack button was pressed this frame"""
        return self.was_key_pressed_this_frame(pygame.K_e)

    def is_pause_pressed(self):
        """Check if pause button was pressed this frame"""
        return self.was_key_pressed_this_frame(pygame.K_ESCAPE)

    def is_confirm_pressed(self):
        """Check if confirm/select button was pressed (Enter or Space)"""
        return (self.was_key_pressed_this_frame(pygame.K_RETURN) or
                self.was_key_pressed_this_frame(pygame.K_SPACE))

    def is_restart_combo_pressed(self):
        """Check if restart combination (Shift+Enter) was pressed"""
        if self.was_key_pressed_this_frame(pygame.K_RETURN):
            return (self.is_key_pressed(pygame.K_LSHIFT) or
                    self.is_key_pressed(pygame.K_RSHIFT))
        return False


class GameState:
    """Manages game state (playing, paused, game over, etc.)"""

    # State constants
    PLAYING = 'playing'
    PAUSED = 'paused'
    GAME_OVER = 'game_over'
    LEVEL_COMPLETE = 'level_complete'
    CUTSCENE = 'cutscene'
    DEATH_SCREEN = 'death_screen'

    def __init__(self):
        """Initialize game state"""
        self.current_state = self.PLAYING
        self.previous_state = None

        # State flags
        self.game_over = False
        self.level_complete = False
        self.cutscene_active = False
        self.paused = False
        self.show_death_screen = False

        # Death animation
        self.death_fade_alpha = 0
        self.death_fade_speed = 5
        self.death_animation_timer = 0
        self.death_animation_delay = 90

    def set_state(self, new_state):
        """Change to a new state"""
        self.previous_state = self.current_state
        self.current_state = new_state

        # Update flags based on state
        self.paused = (new_state == self.PAUSED)
        self.game_over = (new_state == self.GAME_OVER)
        self.level_complete = (new_state == self.LEVEL_COMPLETE)
        self.cutscene_active = (new_state == self.CUTSCENE)
        self.show_death_screen = (new_state == self.DEATH_SCREEN)

    def toggle_pause(self):
        """Toggle between playing and paused states"""
        if self.current_state == self.PLAYING:
            self.set_state(self.PAUSED)
        elif self.current_state == self.PAUSED:
            self.set_state(self.PLAYING)

    def is_playing(self):
        """Check if game is in playing state"""
        return self.current_state == self.PLAYING

    def is_paused(self):
        """Check if game is paused"""
        return self.current_state == self.PAUSED

    def is_game_over(self):
        """Check if game is over"""
        return self.current_state == self.GAME_OVER or self.current_state == self.DEATH_SCREEN

    def can_update_game(self):
        """Check if game entities should be updated"""
        return not (self.game_over or self.cutscene_active or self.paused)

    def trigger_death(self):
        """Trigger death state"""
        self.game_over = True
        self.death_fade_alpha = 0
        self.death_animation_timer = 0
        self.show_death_screen = False
        self.set_state(self.GAME_OVER)

    def update_death_animation(self):
        """Update death animation state"""
        if self.game_over and not self.show_death_screen:
            self.death_animation_timer += 1
            if self.death_animation_timer >= self.death_animation_delay:
                self.show_death_screen = True
                self.set_state(self.DEATH_SCREEN)

    def trigger_level_complete(self):
        """Trigger level complete state"""
        self.level_complete = True
        self.cutscene_active = True
        self.set_state(self.LEVEL_COMPLETE)


class InputMapper:
    """Maps raw input to game actions"""

    def __init__(self):
        """Initialize input mapper with default key bindings"""
        self.key_bindings = {
            'move_left': [pygame.K_LEFT, pygame.K_a],
            'move_right': [pygame.K_RIGHT, pygame.K_d],
            'jump': [pygame.K_SPACE, pygame.K_UP, pygame.K_w],
            'crouch': [pygame.K_DOWN, pygame.K_s],
            'roll': [pygame.K_LSHIFT, pygame.K_RSHIFT],
            'spin_attack': [pygame.K_e],
            'pause': [pygame.K_ESCAPE],
            'confirm': [pygame.K_RETURN, pygame.K_SPACE],
        }

    def rebind_key(self, action, new_key):
        """
        Rebind an action to a new key

        Args:
            action: Action name (e.g., 'jump')
            new_key: New pygame key constant
        """
        if action in self.key_bindings:
            if new_key not in self.key_bindings[action]:
                self.key_bindings[action].append(new_key)

    def get_keys_for_action(self, action):
        """Get all keys bound to an action"""
        return self.key_bindings.get(action, [])

    def is_action_pressed(self, action, keys_pressed):
        """Check if any key for an action is pressed"""
        action_keys = self.get_keys_for_action(action)
        return any(keys_pressed.get(key, False) for key in action_keys)


# Example usage
if __name__ == '__main__':
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    # Create controller and state
    controller = GameController()
    game_state = GameState()

    print("Game Controller Demo - Press keys to see output, ESC to quit")

    running = True
    while running:
        controller.update()

        if controller.quit_requested or controller.is_pause_pressed():
            running = False

        # Test movement
        movement = controller.get_movement_input()
        if movement != 0:
            direction = "left" if movement < 0 else "right"
            print(f"Moving {direction}")

        # Test jump
        if controller.is_jump_pressed():
            print("Jump!")

        # Test actions
        if controller.is_crouch_held():
            print("Crouching...")

        if controller.is_roll_pressed():
            print("Roll!")

        if controller.is_spin_attack_pressed():
            print("Spin Attack!")

        clock.tick(60)

    pygame.quit()
    print("Demo ended")
