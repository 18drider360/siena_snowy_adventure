"""
Level Manager and Game Progression System
Handles level progression, ability unlocks, and game state tracking
"""

import importlib

class GameProgression:
    """Manages player progression, abilities, and stats across levels"""
    
    def __init__(self):
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
            print(f"⚠️ Warning: Unknown ability '{ability_name}'")
    
    def get_abilities(self):
        """Get current unlocked abilities"""
        return self.unlocked_abilities.copy()
    
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
            1: ['roll'],    # Complete Level 1 → Unlock Roll
            2: ['spin'],    # Complete Level 2 → Unlock Spin
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
            print(f"⚠️ Level {level_num} not yet unlocked!")
            return False
    
    def reset(self):
        """Reset progression (for New Game)"""
        self.__init__()


class LevelManager:
    """Manages level loading and transitions"""
    
    # Define all levels in your game
    LEVELS = {
        1: {
            'name': '1-1 Cabin Base',
            'module': 'levels.level_1_cabin',
            'world': '1-1'
        },
        # Add more levels as you create them:
        # 2: {
        #     'name': '1-2 Ski Lift',
        #     'module': 'levels.level_2_ski_lift',
        #     'world': '1-2'
        # },
        # 3: {
        #     'name': '2-1 Mountain Climb',
        #     'module': 'levels.level_3_mountain',
        #     'world': '2-1'
        # },
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
                     enemies, projectiles, coins, world_name, goal_npc)
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
        
        # Handle different return formats (with or without goal_npc)
        if len(result) == 10:
            # New format with goal_npc
            bg_color, platforms, hazards, level_width, player, enemies, projectiles, coins, world_name, goal_npc = result
        else:
            # Old format without goal_npc (backwards compatibility)
            bg_color, platforms, hazards, level_width, player, enemies, projectiles, coins, world_name = result
            goal_npc = None
        
        return (bg_color, platforms, hazards, level_width, player, 
                enemies, projectiles, coins, world_name, goal_npc)
    
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
