"""
Secure Online Leaderboard Module
Uses Firebase REST API without exposing admin credentials
"""

import os
import json
import urllib.request
import urllib.error
import ssl
from typing import List, Dict, Optional
from src.core.game_logging import get_logger

logger = get_logger(__name__)

def _make_request(req, timeout=10):
    """
    Make an HTTP request with SSL fallback support.

    Tries with verified SSL first, falls back to unverified if certificate issues occur.
    """
    # Try with verified SSL first (most secure)
    try:
        ssl_context = ssl.create_default_context()
        return urllib.request.urlopen(req, timeout=timeout, context=ssl_context)
    except ssl.SSLError as e:
        # SSL certificate verification failed, try with unverified context
        logger.warning(f"SSL verification failed ({e}), retrying with unverified context")
        ssl_context = ssl._create_unverified_context()
        return urllib.request.urlopen(req, timeout=timeout, context=ssl_context)
    except urllib.error.URLError as e:
        # Check if the URLError was caused by an SSL error
        if isinstance(e.reason, ssl.SSLError):
            logger.warning(f"SSL verification failed ({e.reason}), retrying with unverified context")
            ssl_context = ssl._create_unverified_context()
            return urllib.request.urlopen(req, timeout=timeout, context=ssl_context)
        else:
            raise

# Flag to enable/disable online features (default to enabled)
ONLINE_ENABLED = os.environ.get('SIENA_ONLINE_ENABLED', 'true').lower() == 'true'


class SecureLeaderboard:
    """Manages online leaderboard using Firebase REST API (no admin SDK)"""

    def __init__(self):
        """Initialize Firebase REST API connection"""
        self.initialized = False
        self.base_url = None

        if not ONLINE_ENABLED:
            logger.info("Online leaderboards disabled (SIENA_ONLINE_ENABLED not set)")
            return

        # Get Firebase database URL from environment or use default
        # Default URL is safe to expose (security is enforced by Firebase rules)
        firebase_url = os.environ.get(
            'FIREBASE_URL',
            'https://siena-snowy-adventure-default-rtdb.firebaseio.com'
        )

        # Remove trailing slash if present
        self.base_url = firebase_url.rstrip('/')
        self.initialized = True
        logger.info(f"Secure leaderboard initialized with database: {self.base_url}")

    def is_available(self) -> bool:
        """Check if online leaderboard is available"""
        return self.initialized and self.base_url is not None

    def submit_score(self, level: int, username: str, time: int, coins: int,
                    difficulty: str, checkpoints: bool) -> bool:
        """
        Submit a score to the online leaderboard using REST API

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

        # Basic client-side validation (server will also validate)
        if not self._validate_score(level, username, time, coins, difficulty):
            logger.warning("Score validation failed")
            return False

        try:
            import time as time_module

            score_data = {
                'username': username,
                'time': time,
                'coins': coins,
                'difficulty': difficulty,
                'checkpoints': checkpoints,
                'timestamp': int(time_module.time() * 1000)
            }

            # Submit to Firebase using REST API
            url = f"{self.base_url}/leaderboards/level_{level}.json"

            data = json.dumps(score_data).encode('utf-8')
            req = urllib.request.Request(url, data=data, method='POST')
            req.add_header('Content-Type', 'application/json')

            with _make_request(req, timeout=10) as response:
                if response.status == 200:
                    logger.info(f"Score submitted for {username} on level {level}")
                    return True
                else:
                    logger.error(f"Failed to submit score: HTTP {response.status}")
                    return False

        except urllib.error.HTTPError as e:
            logger.error(f"HTTP error submitting score: {e.code} - {e.reason}")
            return False
        except urllib.error.URLError as e:
            logger.error(f"Network error submitting score: {e.reason}")
            return False
        except Exception as e:
            logger.error(f"Failed to submit score: {e}")
            return False

    def get_leaderboard(self, level: int, difficulty: str = 'All',
                       checkpoints_filter: str = 'All', limit: int = 100) -> List[Dict]:
        """
        Fetch leaderboard for a specific level using REST API

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
            # Fetch scores using REST API
            url = f"{self.base_url}/leaderboards/level_{level}.json?orderBy=\"time\"&limitToFirst={limit * 2}"

            req = urllib.request.Request(url, method='GET')

            with _make_request(req, timeout=10) as response:
                data = response.read().decode('utf-8')
                scores_snapshot = json.loads(data)

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

        except urllib.error.HTTPError as e:
            logger.error(f"HTTP error fetching leaderboard: {e.code} - {e.reason}")
            return []
        except urllib.error.URLError as e:
            logger.error(f"Network error fetching leaderboard: {e.reason}")
            return []
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

    def _validate_score(self, level: int, username: str, time: int, coins: int, difficulty: str) -> bool:
        """
        Client-side validation (server should also validate)

        Args:
            level: Level number
            username: Player username
            time: Completion time in frames
            coins: Coins collected
            difficulty: Difficulty level

        Returns:
            True if score passes basic validation
        """
        # Level must be 1-4
        if not (1 <= level <= 4):
            logger.warning(f"Score validation failed: Invalid level {level} (must be 1-4)")
            return False

        # Username must be 1-20 characters
        if not (1 <= len(username) <= 20):
            logger.warning(f"Score validation failed: Invalid username length {len(username)} (must be 1-20)")
            return False

        # Time must be reasonable (at least 15 seconds = 900 frames at 60fps)
        # Maximum 1 hour = 216000 frames
        if not (900 <= time <= 216000):
            time_seconds = time / 60
            logger.warning(f"Score validation failed: Time {time} frames ({time_seconds:.1f}s) out of range (must be 15-3600 seconds)")
            return False

        # Coins must be reasonable (max ~50 per level)
        if not (0 <= coins <= 100):
            logger.warning(f"Score validation failed: Coins {coins} out of range (must be 0-100)")
            return False

        # Difficulty must be valid
        if difficulty not in ['Easy', 'Medium', 'Hard']:
            logger.warning(f"Score validation failed: Invalid difficulty '{difficulty}' (must be Easy/Medium/Hard)")
            return False

        return True


# Singleton instance
_secure_leaderboard = None

def get_secure_leaderboard() -> SecureLeaderboard:
    """Get the singleton SecureLeaderboard instance"""
    global _secure_leaderboard
    if _secure_leaderboard is None:
        _secure_leaderboard = SecureLeaderboard()
    return _secure_leaderboard
