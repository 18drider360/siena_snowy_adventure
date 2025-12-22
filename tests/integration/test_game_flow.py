#!/usr/bin/env python3
"""
Integration tests for game flow
Tests end-to-end gameplay scenarios
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import pytest
import pygame
from src.utils.save_system import SaveSystem
from src.utils.progression import LevelManager
from src.utils.username_filter import validate_username


class TestGameFlow:
    """Test complete game flow scenarios"""
    
    def setup_method(self):
        """Set up test environment"""
        pygame.init()
        # Initialize with headless display for testing
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        self.screen = pygame.display.set_mode((800, 600))
        
    def teardown_method(self):
        """Clean up after tests"""
        pygame.quit()
    
    def test_level_completion_saves_score(self):
        """Test that completing a level saves the score"""
        # Arrange
        level = 1
        time = 1800  # 30 seconds at 60 FPS
        coins = 10
        username = "TestPlayer"
        difficulty = "Medium"
        
        # Act
        SaveSystem.add_score(level, time, coins, username, difficulty, checkpoints=False)
        leaderboard = SaveSystem.get_leaderboard(level)
        
        # Assert
        assert len(leaderboard) > 0
        assert leaderboard[0]['username'] == username
        assert leaderboard[0]['time'] == time
        assert leaderboard[0]['coins'] == coins
    
    def test_level_unlock_progression(self):
        """Test level unlocking progression"""
        # Arrange
        SaveSystem.save_completion(level=1, time=1800, coins=10, 
                                  username="TestPlayer", difficulty="Medium")
        
        # Act
        is_unlocked = SaveSystem.is_level_unlocked(2)
        
        # Assert
        assert is_unlocked is True
    
    def test_username_validation_flow(self):
        """Test username validation in game flow"""
        # Test valid username
        valid, error = validate_username("GoodPlayer")
        assert valid is True
        assert error == ""
        
        # Test invalid username
        valid, error = validate_username("BadWord123")
        assert valid is False
        assert "inappropriate content" in error


class TestLeaderboardFlow:
    """Test leaderboard submission and retrieval"""
    
    def test_local_leaderboard_sorting(self):
        """Test that leaderboard sorts scores correctly"""
        # Arrange
        SaveSystem.add_score(1, 3600, 5, "SlowPlayer", "Easy")  # 60 seconds
        SaveSystem.add_score(1, 1200, 10, "FastPlayer", "Hard")  # 20 seconds
        SaveSystem.add_score(1, 1800, 8, "MedPlayer", "Medium")  # 30 seconds
        
        # Act
        leaderboard = SaveSystem.get_leaderboard(1)
        
        # Assert
        assert len(leaderboard) >= 3
        # Fastest time should be first
        assert leaderboard[0]['username'] == "FastPlayer"
        assert leaderboard[0]['time'] == 1200
    
    def test_difficulty_filtering(self):
        """Test filtering scores by difficulty"""
        # Arrange
        SaveSystem.add_score(1, 1800, 10, "EasyPlayer", "Easy")
        SaveSystem.add_score(1, 1800, 10, "HardPlayer", "Hard")
        
        # Act
        all_scores = SaveSystem.get_leaderboard(1)
        easy_scores = [s for s in all_scores if s.get('difficulty') == 'Easy']
        hard_scores = [s for s in all_scores if s.get('difficulty') == 'Hard']
        
        # Assert
        assert len(easy_scores) >= 1
        assert len(hard_scores) >= 1
        assert easy_scores[0]['username'] == "EasyPlayer"
        assert hard_scores[0]['username'] == "HardPlayer"


class TestProgressionFlow:
    """Test game progression and unlocking"""
    
    def test_sequential_level_unlocking(self):
        """Test that levels unlock in sequence"""
        # Start with level 1 unlocked
        assert SaveSystem.is_level_unlocked(1) is True
        
        # Level 2 should be locked initially
        # (depends on save state, may vary)
        
        # Complete level 1
        SaveSystem.save_completion(1, 1800, 10, "TestPlayer", "Medium")
        
        # Level 2 should now be unlocked
        assert SaveSystem.is_level_unlocked(2) is True


# Placeholder for future integration tests
class TestOnlineLeaderboardFlow:
    """Test online leaderboard integration (requires Firebase)"""
    
    @pytest.mark.skip(reason="Requires Firebase credentials")
    def test_online_submission(self):
        """Test submitting score to online leaderboard"""
        # This test requires Firebase configuration
        # Skip in CI/CD environments without credentials
        pass
    
    @pytest.mark.skip(reason="Requires Firebase credentials")
    def test_online_retrieval(self):
        """Test retrieving scores from online leaderboard"""
        # This test requires Firebase configuration
        pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
