"""
Online Leaderboard Module
Handles synchronization with Firebase Realtime Database for global leaderboards
"""

import os
import json
from typing import List, Dict, Optional
from src.core.game_logging import get_logger

logger = get_logger(__name__)

# Flag to enable/disable online features
ONLINE_ENABLED = os.environ.get('SIENA_ONLINE_ENABLED', 'false').lower() == 'true'


class OnlineLeaderboard:
    """Manages online leaderboard synchronization with Firebase"""

    def __init__(self):
        """Initialize Firebase connection"""
        self.initialized = False
        self.db_ref = None

        if not ONLINE_ENABLED:
            logger.info("Online leaderboards disabled (SIENA_ONLINE_ENABLED not set)")
            return

        try:
            import firebase_admin
            from firebase_admin import credentials, db

            # Check if Firebase is already initialized
            try:
                firebase_admin.get_app()
                self.initialized = True
                logger.info("Firebase already initialized")
            except ValueError:
                # Not initialized yet, so initialize it
                firebase_key_path = os.environ.get('FIREBASE_KEY_PATH', 'firebase-key.json')
                firebase_url = os.environ.get('FIREBASE_URL')

                if not firebase_url:
                    logger.warning("FIREBASE_URL not set in environment")
                    return

                # Handle PyInstaller bundled apps - look in _MEIPASS directory
                if not os.path.exists(firebase_key_path):
                    if hasattr(os.sys, '_MEIPASS'):
                        # PyInstaller bundles files in _MEIPASS temporary directory
                        bundle_dir = os.sys._MEIPASS
                        firebase_key_path = os.path.join(bundle_dir, firebase_key_path)
                        logger.info(f"Looking for Firebase key in bundle: {firebase_key_path}")

                if not os.path.exists(firebase_key_path):
                    logger.warning(f"Firebase key file not found: {firebase_key_path}")
                    return

                cred = credentials.Certificate(firebase_key_path)
                firebase_admin.initialize_app(cred, {
                    'databaseURL': firebase_url
                })
                self.initialized = True
                logger.info(f"Firebase initialized with database: {firebase_url}")

            # Get reference to leaderboards node
            self.db_ref = db.reference('leaderboards')

        except ImportError:
            logger.warning("firebase-admin not installed. Online features disabled.")
        except Exception as e:
            logger.error(f"Failed to initialize Firebase: {e}")

    def is_available(self) -> bool:
        """Check if online leaderboard is available"""
        return self.initialized and self.db_ref is not None

    def submit_score(self, level: int, username: str, time: int, coins: int,
                    difficulty: str, checkpoints: bool) -> bool:
        """
        Submit a score to the online leaderboard

        Args:
            level: Level number (1-4)
            username: Player username
            time: Completion time in frames
            coins: Coins collected
            difficulty: Difficulty level (Easy/Medium/Hard)
            checkpoints: Whether checkpoints were enabled

        Returns:
            True if submission successful, False otherwise
        """
        if not self.is_available():
            logger.debug("Online leaderboard not available")
            return False

        try:
            import time as time_module

            score_data = {
                'username': username,
                'time': time,
                'coins': coins,
                'difficulty': difficulty,
                'checkpoints': checkpoints,
                'timestamp': int(time_module.time() * 1000)  # Unix timestamp in milliseconds
            }

            # Submit to Firebase
            self.db_ref.child(f'level_{level}').push(score_data)
            logger.info(f"Score submitted for {username} on level {level}")
            return True

        except Exception as e:
            logger.error(f"Failed to submit score: {e}")
            return False

    def get_leaderboard(self, level: int, difficulty: str = 'All',
                       checkpoints_filter: str = 'All', limit: int = 100) -> List[Dict]:
        """
        Fetch leaderboard for a specific level

        Args:
            level: Level number (1-4)
            difficulty: Filter by difficulty (Easy/Medium/Hard/All)
            checkpoints_filter: Filter by checkpoint usage (On/Off/All)
            limit: Maximum number of scores to return

        Returns:
            List of score dictionaries sorted by time
        """
        if not self.is_available():
            logger.debug("Online leaderboard not available")
            return []

        try:
            # Fetch all scores for this level
            scores_ref = self.db_ref.child(f'level_{level}')
            scores_snapshot = scores_ref.order_by_child('time').limit_to_first(limit * 2).get()

            if not scores_snapshot:
                return []

            # Convert to list format
            scores = []
            for key, value in scores_snapshot.items():
                score_dict = {
                    'id': key,
                    'username': value.get('username', 'Unknown'),
                    'time': value.get('time', 999999),
                    'coins': value.get('coins', 0),
                    'difficulty': value.get('difficulty', 'Medium'),
                    'checkpoints': value.get('checkpoints', False),
                    'timestamp': value.get('timestamp', 0)
                }
                scores.append(score_dict)

            # Apply filters
            if difficulty != 'All':
                scores = [s for s in scores if s['difficulty'] == difficulty]

            if checkpoints_filter == 'On':
                scores = [s for s in scores if s['checkpoints'] is True]
            elif checkpoints_filter == 'Off':
                scores = [s for s in scores if s['checkpoints'] is False]

            # Sort by time and limit
            scores.sort(key=lambda x: x['time'])
            scores = scores[:limit]

            logger.debug(f"Fetched {len(scores)} scores for level {level}")
            return scores

        except Exception as e:
            logger.error(f"Failed to fetch leaderboard: {e}")
            return []

    def get_user_rank(self, level: int, username: str, time: int,
                     difficulty: str, checkpoints: bool) -> Optional[int]:
        """
        Get a user's rank on the leaderboard

        Args:
            level: Level number
            username: Player username
            time: Player's time
            difficulty: Player's difficulty
            checkpoints: Whether checkpoints were used

        Returns:
            Rank (1-indexed) or None if not found
        """
        if not self.is_available():
            return None

        try:
            # Get all scores better than this time
            leaderboard = self.get_leaderboard(level, difficulty,
                                               'On' if checkpoints else 'Off',
                                               limit=1000)

            # Count how many scores are better
            better_scores = sum(1 for score in leaderboard if score['time'] < time)

            return better_scores + 1  # Rank is 1-indexed

        except Exception as e:
            logger.error(f"Failed to get rank: {e}")
            return None


# Singleton instance
_online_leaderboard = None

def get_online_leaderboard() -> OnlineLeaderboard:
    """Get the singleton OnlineLeaderboard instance"""
    global _online_leaderboard
    if _online_leaderboard is None:
        _online_leaderboard = OnlineLeaderboard()
    return _online_leaderboard
