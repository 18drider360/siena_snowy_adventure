"""
Save System for Game Progression
Handles saving and loading player progress to/from disk
"""

import json
import os
from pathlib import Path


class SaveSystem:
    """Manages saving and loading game progression data"""

    # Save file location (in user's home directory)
    SAVE_DIR = Path.home() / ".siena_snowy_adventure"
    SAVE_FILE = SAVE_DIR / "save_data.json"
    SCOREBOARD_FILE = SAVE_DIR / "scoreboard.json"

    @staticmethod
    def ensure_save_directory():
        """Create save directory if it doesn't exist"""
        SaveSystem.SAVE_DIR.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def save_progress(progression, username="Player"):
        """
        Save current game progression to disk

        Args:
            progression: GameProgression instance to save
            username: Player's username (default "Player")

        Returns:
            bool: True if save succeeded, False otherwise
        """
        try:
            SaveSystem.ensure_save_directory()

            # Convert progression data to dictionary
            save_data = {
                'version': 1,  # For future compatibility
                'username': username,
                'unlocked_abilities': progression.unlocked_abilities,
                'current_level': progression.current_level,
                'max_level_reached': progression.max_level_reached,
                'coins_total': progression.coins_total,
                'deaths_total': progression.deaths_total,
                'total_time': progression.total_time,
                'level_stats': progression.level_stats
            }

            # Write to file
            with open(SaveSystem.SAVE_FILE, 'w') as f:
                json.dump(save_data, f, indent=2)

            return True

        except Exception as e:
            print(f"⚠️ Failed to save progress: {e}")
            return False

    @staticmethod
    def load_progress(progression):
        """
        Load saved game progression from disk

        Args:
            progression: GameProgression instance to populate with saved data

        Returns:
            tuple: (success: bool, username: str) - Success status and username
        """
        try:
            # Check if save file exists
            if not SaveSystem.SAVE_FILE.exists():
                print("ℹ️ No save file found. Starting new game.")
                return (False, None)

            # Read save file
            with open(SaveSystem.SAVE_FILE, 'r') as f:
                save_data = json.load(f)

            # Validate version (for future compatibility)
            version = save_data.get('version', 1)
            if version > 1:
                print(f"⚠️ Save file version {version} is newer than supported. Using defaults.")
                return (False, None)

            # Load data into progression object
            username = save_data.get('username', 'Player')
            progression.unlocked_abilities = save_data.get('unlocked_abilities', progression.unlocked_abilities)
            progression.current_level = save_data.get('current_level', 1)
            progression.max_level_reached = save_data.get('max_level_reached', 1)
            progression.coins_total = save_data.get('coins_total', 0)
            progression.deaths_total = save_data.get('deaths_total', 0)
            progression.total_time = save_data.get('total_time', 0)
            progression.level_stats = save_data.get('level_stats', {})

            print(f"✅ Progress loaded! Level {progression.current_level}, Max Level: {progression.max_level_reached}")
            return (True, username)

        except json.JSONDecodeError as e:
            print(f"⚠️ Save file corrupted: {e}. Starting new game.")
            return (False, None)
        except Exception as e:
            print(f"⚠️ Failed to load progress: {e}")
            return (False, None)

    @staticmethod
    def delete_save():
        """
        Delete the save file (for New Game)

        Returns:
            bool: True if deletion succeeded or file didn't exist
        """
        try:
            if SaveSystem.SAVE_FILE.exists():
                SaveSystem.SAVE_FILE.unlink()
                print("🗑️ Save file deleted.")
            return True
        except Exception as e:
            print(f"⚠️ Failed to delete save file: {e}")
            return False

    @staticmethod
    def save_exists():
        """
        Check if a save file exists

        Returns:
            bool: True if save file exists
        """
        return SaveSystem.SAVE_FILE.exists()

    @staticmethod
    def get_save_info():
        """
        Get information about the save file without loading it

        Returns:
            dict or None: Save file info (level, stats) or None if no save
        """
        try:
            if not SaveSystem.SAVE_FILE.exists():
                return None

            with open(SaveSystem.SAVE_FILE, 'r') as f:
                save_data = json.load(f)

            return {
                'current_level': save_data.get('current_level', 1),
                'max_level_reached': save_data.get('max_level_reached', 1),
                'coins_total': save_data.get('coins_total', 0),
                'deaths_total': save_data.get('deaths_total', 0),
                'total_time': save_data.get('total_time', 0)
            }
        except:
            return None

    @staticmethod
    def submit_score(username, level_num, time_taken, coins_collected, difficulty="Medium"):
        """
        Submit a score to the scoreboard

        Args:
            username: Player's username
            level_num: Level number
            time_taken: Time taken in frames
            coins_collected: Number of coins collected
            difficulty: Difficulty level (Easy/Medium/Hard, defaults to Medium)

        Returns:
            bool: True if score was submitted successfully
        """
        try:
            SaveSystem.ensure_save_directory()

            # Load existing scoreboard or create new one
            scoreboard = SaveSystem._load_scoreboard()

            # Ensure level exists in scoreboard
            level_key = str(level_num)
            if level_key not in scoreboard:
                scoreboard[level_key] = []

            # Create score entry
            score_entry = {
                'username': username,
                'time': time_taken,
                'coins': coins_collected,
                'difficulty': difficulty,
                'timestamp': __import__('time').time()
            }

            # Add to scoreboard
            scoreboard[level_key].append(score_entry)

            # Sort by time (fastest first), then by coins (most first)
            scoreboard[level_key].sort(key=lambda x: (x['time'], -x['coins']))

            # Keep only top 100 scores per level (allows scrolling through more scores)
            scoreboard[level_key] = scoreboard[level_key][:100]

            # Save scoreboard
            with open(SaveSystem.SCOREBOARD_FILE, 'w') as f:
                json.dump(scoreboard, f, indent=2)

            return True

        except Exception as e:
            print(f"⚠️ Failed to submit score: {e}")
            return False

    @staticmethod
    def get_leaderboard(level_num):
        """
        Get leaderboard for a specific level

        Args:
            level_num: Level number

        Returns:
            list: List of score entries (dicts with username, time, coins)
        """
        try:
            scoreboard = SaveSystem._load_scoreboard()
            level_key = str(level_num)
            return scoreboard.get(level_key, [])
        except Exception as e:
            print(f"⚠️ Failed to load leaderboard: {e}")
            return []

    @staticmethod
    def get_all_leaderboards():
        """
        Get all leaderboards for all levels

        Returns:
            dict: Dictionary mapping level_num (str) to list of score entries
        """
        try:
            return SaveSystem._load_scoreboard()
        except Exception as e:
            print(f"⚠️ Failed to load leaderboards: {e}")
            return {}

    @staticmethod
    def _load_scoreboard():
        """
        Internal method to load scoreboard from disk

        Returns:
            dict: Scoreboard data
        """
        if not SaveSystem.SCOREBOARD_FILE.exists():
            return {}

        try:
            with open(SaveSystem.SCOREBOARD_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("⚠️ Scoreboard file corrupted. Creating new one.")
            return {}
        except Exception as e:
            print(f"⚠️ Failed to load scoreboard: {e}")
            return {}


# Example usage
if __name__ == "__main__":
    from utils.progression import GameProgression

    # Create progression
    progression = GameProgression()

    # Try to load saved progress
    if SaveSystem.load_progress(progression):
        print(f"Loaded: Level {progression.current_level}")
    else:
        print("Starting new game")

    # Simulate playing
    progression.complete_level(1, coins_collected=50, time_taken=3600, deaths=2)
    progression.advance_to_next_level()

    # Save progress
    if SaveSystem.save_progress(progression):
        print(f"✅ Progress saved!")
