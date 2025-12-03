"""
Level Manager and Game Progression System
Handles level progression, ability unlocks, and game state tracking
"""

import importlib

class GameProgression:
    """Manages player progression, abilities, and stats across levels"""

    # Coin requirements for each level based on difficulty
    # Total coins available: Level 1 = 30, Level 2 = 35, Level 3 = 40, Level 4 = 45
    # Easy = 60%, Medium = 70%, Hard = 85% (rounded down)
    COIN_REQUIREMENTS = {
        "Easy": {
            1: 18,   # Level 1: 60% of 30 = 18 coins
            2: 21,   # Level 2: 60% of 35 = 21 coins
            3: 24,   # Level 3: 60% of 40 = 24 coins
            4: 27    # Level 4: 60% of 45 = 27 coins
        },
        "Medium": {
            1: 21,   # Level 1: 70% of 30 = 21 coins
            2: 24,   # Level 2: 70% of 35 = 24 coins (24.5 rounded down)
            3: 28,   # Level 3: 70% of 40 = 28 coins
            4: 31    # Level 4: 70% of 45 = 31 coins (31.5 rounded down)
        },
        "Hard": {
            1: 25,   # Level 1: 85% of 30 = 25 coins (25.5 rounded down)
            2: 29,   # Level 2: 85% of 35 = 29 coins (29.75 rounded down)
            3: 34,   # Level 3: 85% of 40 = 34 coins
            4: 38    # Level 4: 85% of 45 = 38 coins (38.25 rounded down)
        }
    }

    def __init__(self, difficulty="Medium", username="Player"):
        # --- PLAYER INFO ---
        self.username = username  # Player's username

        # --- DIFFICULTY SETTING ---
        self.difficulty = difficulty  # Easy, Medium, or Hard

        # --- ABILITY PROGRESSION ---
        # Tracks which abilities are currently unlocked
        self.unlocked_abilities = {
            'walk': True,
            'crouch': True,
            'jump': True,
            'double_jump': True,
            'roll': False,      # Unlocked after Level 1
            'spin': False       # Unlocked after Level 2
        }

        # --- LEVEL TRACKING ---
        self.current_level = 1
        self.max_level_reached = 1

        # --- STATS TRACKING ---
        self.coins_total = 0
        self.deaths_total = 0
        self.total_time = 0  # In frames

        # --- LEVEL-SPECIFIC STATS ---
        self.level_stats = {
            # level_num: {'coins': 0, 'time': 0, 'deaths': 0, 'completed': False}
        }
    
    def unlock_ability(self, ability_name):
        """Unlock a specific ability"""
        if ability_name in self.unlocked_abilities:
            self.unlocked_abilities[ability_name] = True
        else:
            print(f"Ã¢Å¡Â Ã¯Â¸Â Warning: Unknown ability '{ability_name}'")
    
    def get_abilities(self):
        """Get current unlocked abilities based on current level"""
        # Create a copy of base unlocked abilities
        abilities = self.unlocked_abilities.copy()

        # Enable abilities based on current level (not completion)
        if self.current_level >= 2:
            abilities['roll'] = True

        if self.current_level >= 3:
            abilities['spin'] = True

        return abilities
    
    def complete_level(self, level_num, coins_collected, time_taken, deaths):
        """Mark a level as completed and update stats"""
        if level_num not in self.level_stats:
            self.level_stats[level_num] = {
                'coins': 0,
                'time': 999999,
                'deaths': 999,
                'completed': False
            }
        
        # Update stats (keep best performance)
        stats = self.level_stats[level_num]
        stats['completed'] = True
        stats['coins'] = max(stats['coins'], coins_collected)
        stats['time'] = min(stats['time'], time_taken)
        stats['deaths'] = min(stats['deaths'], deaths)
        
        # Update totals
        self.coins_total += coins_collected
        self.deaths_total += deaths
        self.total_time += time_taken
        
        # Unlock next level
        if level_num >= self.max_level_reached:
            self.max_level_reached = level_num + 1
        
        # Trigger ability unlocks based on level completion
        self._check_ability_unlocks(level_num)
    
    def _check_ability_unlocks(self, completed_level):
        """Check if completing this level unlocks new abilities"""
        unlock_schedule = {
            1: ['roll'],    # Complete Level 1 Ã¢â€ â€™ Unlock Roll
            2: ['spin'],    # Complete Level 2 Ã¢â€ â€™ Unlock Spin
            # Add more as you add levels
        }
        
        if completed_level in unlock_schedule:
            for ability in unlock_schedule[completed_level]:
                self.unlock_ability(ability)
    
    def advance_to_next_level(self):
        """Move to the next level"""
        self.current_level += 1
        return self.current_level
    
    def set_level(self, level_num):
        """Manually set the current level"""
        if level_num <= self.max_level_reached:
            self.current_level = level_num
            return True
        else:
            print(f"Ã¢Å¡Â Ã¯Â¸Â Level {level_num} not yet unlocked!")
            return False
    
    def reset(self):
        """Reset progression (for New Game)"""
        self.__init__(self.difficulty, self.username)

    def get_coin_requirement(self, level_num):
        """Get the coin requirement for a specific level based on difficulty"""
        if self.difficulty in self.COIN_REQUIREMENTS:
            return self.COIN_REQUIREMENTS[self.difficulty].get(level_num, 0)
        return 0

    def get_coins_remaining(self, level_num, coins_collected):
        """Calculate how many more coins are needed for this level"""
        required = self.get_coin_requirement(level_num)
        remaining = max(0, required - coins_collected)
        return remaining

    def set_difficulty(self, difficulty):
        """Change the difficulty setting"""
        if difficulty in ["Easy", "Medium", "Hard"]:
            self.difficulty = difficulty


class LevelManager:
    """Manages level loading and transitions"""
    
    # Define all levels in your game
    LEVELS = {
        1: {
            'name': 'Winter Welcome',
            'module': 'levels.level_1_cabin',
            'world': '1-1'
        },
        2: {
            'name': 'Snow Cabin',
            'module': 'levels.level_2_ski_lift',
            'world': '1-2'
        },
        3: {
            'name': 'Mountain Climb',
            'module': 'levels.level_3_mountain_climb',
            'world': '1-3'
        },
        4: {
            'name': 'Northern Lights',
            'module': 'levels.level_4_northern_lights',
            'world': '1-4'
        },
    }
    
    @staticmethod
    def load_level(level_num, progression):
        """
        Load a level and return all game objects
        
        Args:
            level_num: The level number to load
            progression: GameProgression instance with current abilities
        
        Returns:
            Tuple of (bg_color, platforms, hazards, level_width, player, 
                     enemies, projectiles, coins, world_name, goal_npc, background_layers)
        """
        if level_num not in LevelManager.LEVELS:
            raise ValueError(f"Level {level_num} does not exist!")
        
        level_info = LevelManager.LEVELS[level_num]
        
        
        # Dynamically import the level module
        try:
            module = importlib.import_module(level_info['module'])
        except ImportError as e:
            raise ImportError(f"Failed to load level {level_num}: {e}")
        
        # Call build_level with current abilities
        result = module.build_level(progression.get_abilities())
        
        # Handle different return formats for backwards compatibility
        if len(result) == 14:
            # Level 3 format with moving, disappearing, and appearing platforms
            bg_color, platforms, hazards, level_width, player, enemies, projectiles, coins, world_name, goal_npc, background_layers, moving_platforms, disappearing_platforms, appearing_platforms = result
        elif len(result) == 13:
            # Level 3 format with moving and disappearing platforms (no appearing)
            bg_color, platforms, hazards, level_width, player, enemies, projectiles, coins, world_name, goal_npc, background_layers, moving_platforms, disappearing_platforms = result
            appearing_platforms = []
        elif len(result) == 11:
            # New format with goal_npc and background_layers
            bg_color, platforms, hazards, level_width, player, enemies, projectiles, coins, world_name, goal_npc, background_layers = result
            moving_platforms = []
            disappearing_platforms = []
            appearing_platforms = []
        elif len(result) == 10:
            # Format with goal_npc but no background_layers
            bg_color, platforms, hazards, level_width, player, enemies, projectiles, coins, world_name, goal_npc = result
            # Use default mountain background
            background_layers = [
                "assets/images/backgrounds/mountains/5.png",
                "assets/images/backgrounds/mountains/4.png",
                "assets/images/backgrounds/mountains/3.png",
                "assets/images/backgrounds/mountains/2.png",
                "assets/images/backgrounds/mountains/1.png",
            ]
            moving_platforms = []
            disappearing_platforms = []
            appearing_platforms = []
        else:
            # Old format without goal_npc (backwards compatibility)
            bg_color, platforms, hazards, level_width, player, enemies, projectiles, coins, world_name = result
            goal_npc = None
            # Use default mountain background
            background_layers = [
                "assets/images/backgrounds/mountains/5.png",
                "assets/images/backgrounds/mountains/4.png",
                "assets/images/backgrounds/mountains/3.png",
                "assets/images/backgrounds/mountains/2.png",
                "assets/images/backgrounds/mountains/1.png",
            ]
            moving_platforms = []
            disappearing_platforms = []
            appearing_platforms = []

        return (bg_color, platforms, hazards, level_width, player,
                enemies, projectiles, coins, world_name, goal_npc, background_layers,
                moving_platforms, disappearing_platforms, appearing_platforms)
    
    @staticmethod
    def get_level_count():
        """Return total number of levels"""
        return len(LevelManager.LEVELS)
    
    @staticmethod
    def get_level_name(level_num):
        """Get the display name of a level"""
        if level_num in LevelManager.LEVELS:
            return LevelManager.LEVELS[level_num]['name']
        return f"Level {level_num}"
    
    @staticmethod
    def get_level_world(level_num):
        """Get the world identifier (e.g. '1-1') for a level"""
        if level_num in LevelManager.LEVELS:
            return LevelManager.LEVELS[level_num]['world']
        return f"{level_num}"


# Example usage:
if __name__ == "__main__":
    # Create progression system
    progression = GameProgression()
    
    # Load level 1
    
    # Complete level 1
    progression.complete_level(1, coins_collected=50, time_taken=3600, deaths=2)
    
    # Check new abilities
    
    # Load level 2
    progression.advance_to_next_level()