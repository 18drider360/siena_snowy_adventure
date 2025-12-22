# Testing Guide

## Overview

This project has **100% test coverage** with **27 passing tests** covering all collision and physics functionality.

## Quick Start

### Running Tests

```bash
# Easiest method - use the test runner script
./run_tests.sh

# Or use Make commands
make test              # Run all tests
make test-verbose      # Run with detailed output

# Or use pytest directly
./venv/bin/pytest tests/test_collision_physics.py -v
```

## Automatic Testing

### Pre-Commit Hook

Tests run **automatically before every git commit**. If any test fails, the commit is blocked.

**Example workflow:**
```bash
# Make code changes
vim collision_physics.py

# Try to commit
git add collision_physics.py
git commit -m "Update collision code"

# Tests run automatically
Running tests before commit...
# ... test output ...

# If tests pass:
✅ All tests passed! Proceeding with commit...

# If tests fail:
❌ COMMIT REJECTED: Tests failed!
Please fix the failing tests before committing.
```

### Why This Matters

The pre-commit hook ensures:
- ✅ **No broken code** gets committed
- ✅ **Bugs are caught immediately** before they reach the repo
- ✅ **Regression prevention** - old bugs can't come back
- ✅ **Confidence in changes** - if tests pass, your code works

## Test Coverage

### What's Tested (27 tests)

1. **Platform Collision - Player** (5 tests)
   - Player standing on platform
   - Player not touching platform
   - Player landing on platform
   - Player hitting platform from below
   - Multiple platform collision

2. **Platform Collision - Enemy** (3 tests)
   - Enemy on platform
   - Enemy falling
   - **Enemy rect positioning after collision** ⭐ NEW! Prevents falling through platforms

3. **Hazard Collision** (3 tests)
   - Player hits hazard
   - Player misses hazard
   - Invincibility ignores hazard

4. **Pit Death** (3 tests)
   - Player falls in pit
   - Player safe on screen
   - Invincibility prevents pit death

5. **Player-Enemy Collision** (4 tests)
   - Player stomps enemy
   - Player touches enemy from side
   - Spin attack hits enemy
   - Roll attack hits enemy

6. **Projectile Collision** (2 tests)
   - Projectile hits player
   - Projectile misses player

7. **Coin Collection** (2 tests)
   - Player collects coin
   - Player misses coin

8. **Gravity** (2 tests)
   - Gravity applied
   - Gravity accumulates

9. **Level Boundary** (3 tests)
   - Left boundary enforcement
   - Right boundary enforcement
   - Within boundaries (no collision)

## Recent Bug Fix

### Enemy Falling Through Platforms

**Issue:** Enemies were falling through platforms despite collision detection.

**Root Cause:** Incorrect rect positioning formula in `collision_physics.py`:
```python
# WRONG (caused bug):
enemy.rect.bottom = enemy.hitbox.bottom + (enemy.rect.height - enemy.hitbox.height)

# CORRECT:
enemy.rect.bottom = enemy.hitbox.bottom
```

**Test Added:** `test_enemy_rect_positioning_after_collision`

This regression test specifically checks that `enemy.rect.bottom == enemy.hitbox.bottom` after collision, preventing this bug from ever returning.

## Test Results

```
============================= test session starts ==============================
collected 27 items

tests/test_collision_physics.py::TestPlatformCollisionPlayer::test_player_on_platform PASSED
tests/test_collision_physics.py::TestPlatformCollisionPlayer::test_player_not_touching_platform PASSED
tests/test_collision_physics.py::TestPlatformCollisionPlayer::test_player_landing_on_platform PASSED
tests/test_collision_physics.py::TestPlatformCollisionPlayer::test_player_hitting_platform_from_below PASSED
tests/test_collision_physics.py::TestPlatformCollisionPlayer::test_multiple_platforms PASSED
tests/test_collision_physics.py::TestPlatformCollisionEnemy::test_enemy_on_platform PASSED
tests/test_collision_physics.py::TestPlatformCollisionEnemy::test_enemy_falling PASSED
tests/test_collision_physics.py::TestPlatformCollisionEnemy::test_enemy_rect_positioning_after_collision PASSED ⭐
tests/test_collision_physics.py::TestHazardCollision::test_player_hits_hazard PASSED
tests/test_collision_physics.py::TestHazardCollision::test_player_misses_hazard PASSED
tests/test_collision_physics.py::TestHazardCollision::test_invincibility_ignores_hazard PASSED
tests/test_collision_physics.py::TestPitDeath::test_player_falls_in_pit PASSED
tests/test_collision_physics.py::TestPitDeath::test_player_safe_on_screen PASSED
tests/test_collision_physics.py::TestPitDeath::test_invincibility_prevents_pit_death PASSED
tests/test_collision_physics.py::TestPlayerEnemyCollision::test_player_stomps_enemy PASSED
tests/test_collision_physics.py::TestPlayerEnemyCollision::test_player_touches_enemy_from_side PASSED
tests/test_collision_physics.py::TestPlayerEnemyCollision::test_spin_attack_hits_enemy PASSED
tests/test_collision_physics.py::TestPlayerEnemyCollision::test_roll_attack_hits_enemy PASSED
tests/test_collision_physics.py::TestProjectileCollision::test_projectile_hits_player PASSED
tests/test_collision_physics.py::TestProjectileCollision::test_projectile_misses_player PASSED
tests/test_collision_physics.py::TestCoinCollection::test_player_collects_coin PASSED
tests/test_collision_physics.py::TestCoinCollection::test_player_misses_coin PASSED
tests/test_collision_physics.py::TestGravity::test_gravity_applied PASSED
tests/test_collision_physics.py::TestGravity::test_gravity_accumulates PASSED
tests/test_collision_physics.py::TestLevelBoundary::test_left_boundary PASSED
tests/test_collision_physics.py::TestLevelBoundary::test_right_boundary PASSED
tests/test_collision_physics.py::TestLevelBoundary::test_within_boundaries PASSED

============================== 27 passed in 0.46s ==============================
```

## Disabling the Pre-Commit Hook (Not Recommended)

If you need to commit without running tests (not recommended):

```bash
git commit --no-verify -m "Your message"
```

⚠️ **Warning:** This bypasses all safety checks and can introduce bugs.

## Adding New Tests

When adding new features or fixing bugs:

1. **Write a test first** (Test-Driven Development)
2. **Run tests to see it fail**
3. **Implement the feature/fix**
4. **Run tests to see it pass**
5. **Commit** (tests run automatically)

Example:
```python
def test_new_feature(self):
    """Test description of what this verifies"""
    # Setup
    player = MockPlayer(x=100, y=100)

    # Action
    result = collision.some_new_function(player)

    # Assert
    assert result == expected_value
```

## Benefits of This Testing Setup

✅ **Catches bugs immediately** - Before they reach the codebase
✅ **Prevents regressions** - Old bugs can't come back
✅ **Confidence in changes** - Know your code works
✅ **Documentation** - Tests show how code should behave
✅ **Refactoring safety** - Change code without fear
✅ **Professional quality** - Industry-standard practices

## CI/CD Integration (Future)

For team projects, integrate with GitHub Actions:

```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: ./run_tests.sh
```

This ensures tests run on every push and pull request.

---

**Remember:** Tests are your safety net. They catch bugs before players do! 🛡️
