# Integration Tests

This directory contains integration tests that test complete game flows and interactions between multiple components.

## Test Categories

### Game Flow Tests (`test_game_flow.py`)
Tests end-to-end gameplay scenarios:
- Level completion and score saving
- Username validation in context
- Level unlocking progression
- Leaderboard submission and retrieval

### Running Integration Tests

```bash
# Run all integration tests
pytest tests/integration/ -v

# Run specific test file
pytest tests/integration/test_game_flow.py -v

# Run with coverage
pytest tests/integration/ --cov=src --cov-report=html
```

## Test Environment

Integration tests use a headless Pygame display (`SDL_VIDEODRIVER=dummy`) to run without requiring a display server. This allows tests to run in CI/CD environments.

## Writing Integration Tests

Integration tests should:
1. Test interactions between multiple components
2. Use real implementations (not mocks)
3. Clean up resources in `teardown_method()`
4. Skip tests that require external services (Firebase) in CI

Example:
```python
class TestMyFeature:
    def setup_method(self):
        """Initialize test environment"""
        pygame.init()
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
    
    def teardown_method(self):
        """Clean up resources"""
        pygame.quit()
    
    def test_complete_flow(self):
        """Test end-to-end feature flow"""
        # Arrange, Act, Assert
        pass
```

## Future Tests

Planned integration tests:
- [ ] Audio playback and music transitions
- [ ] Enemy AI and spawn systems
- [ ] Collision detection in full game context
- [ ] Particle system and visual effects
- [ ] Story cutscene progression
- [ ] Settings persistence
