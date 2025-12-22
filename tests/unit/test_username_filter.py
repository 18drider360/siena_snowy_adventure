#!/usr/bin/env python3
"""
Test script for username filter
Tests various username inputs to verify filtering works correctly
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.utils.username_filter import validate_username

# Test cases: (username, expected_valid)
test_cases = [
    # Valid usernames (more restrictive now)
    ("Player123", True),
    ("CoolGamer", True),
    ("Swift_Fox", True),
    ("Epic-Hero", True),
    ("Sn0wyPlayer", True),
    ("GamerPro99", True),
    ("Cool_Gamer", True),
    ("Epic-Player", True),

    # Too short
    ("A", False),
    ("", False),

    # Too long
    ("ThisUsernameIsWayTooLongForTheSystem", False),

    # Inappropriate content - profanity
    ("BadWord123", False),
    ("DamnPlayer", False),
    ("Player_Shit", False),
    ("F*ckGamer", False),
    ("HellRaiser", False),
    ("CrapGamer", False),
    ("Pissed123", False),

    # Inappropriate content - slurs
    ("Nazi123", False),
    ("HitlerFan", False),
    ("Retard99", False),

    # Inappropriate content - sexual
    ("SexyGamer", False),
    ("PornStar", False),
    ("XXXPlayer", False),

    # Inappropriate content - violence
    ("KillZone", False),
    ("DeathGamer", False),
    ("Terrorist99", False),
    ("Shooter123", False),

    # Inappropriate content - drugs
    ("WeedLover", False),
    ("HighPlayer", False),
    ("DrugDealer", False),

    # Leetspeak variants
    ("B4dW0rd", False),
    ("D4mn", False),
    ("Sh1t", False),
    ("Fu(k", False),

    # Repeated characters
    ("aaaaaaaaaa", False),
    ("lololololol", False),

    # Too many numbers (stricter now - 50% limit)
    ("12345678901234", False),
    ("999999999", False),
    ("1234567", False),
    ("Player1234567", False),  # More than 50% numbers

    # URLs and spam
    ("visit.com", False),
    ("www.spam", False),
    ("http://bad", False),
    ("check.io", False),

    # Special character abuse (stricter now)
    ("!!!!!!!", False),
    ("@#$%^&*", False),
    ("___---___", False),
    ("Player!!!", False),  # Invalid special chars
    ("Cool@Gamer", False),  # @ not allowed
    ("___Player", False),  # Starts with special char
    ("Player---", False),  # Ends with special char
    ("--Player", False),  # Starts with special char

    # Multiple spaces
    ("Cool  Gamer", False),

    # Valid edge cases
    ("A1", True),
    ("Player_2024", True),
    ("Cool-Gamer", True),
    ("Epic_Hero", True),
    ("Snow-Player", True),

    # More examples of blocked content
    ("IdiotGamer", False),
    ("LoserPlayer", False),
    ("DumbGuy", False),
    ("StupidKid", False),
    ("FartMaster", False),
    ("PoopHead", False),
]

def run_tests():
    """Run all test cases"""
    print("Testing Username Filter")
    print("=" * 60)

    passed = 0
    failed = 0

    for username, expected_valid in test_cases:
        is_valid, error_msg = validate_username(username)

        # Check if result matches expectation
        if is_valid == expected_valid:
            status = "✓ PASS"
            passed += 1
        else:
            status = "✗ FAIL"
            failed += 1

        # Print result
        username_display = f'"{username}"' if username else '(empty)'
        expected = "VALID" if expected_valid else "INVALID"
        actual = "VALID" if is_valid else "INVALID"

        print(f"{status} | {username_display:30} | Expected: {expected:7} | Got: {actual:7}", end="")
        if not is_valid:
            print(f" | Error: {error_msg}", end="")
        print()

    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed out of {len(test_cases)} tests")

    if failed == 0:
        print("✓ All tests passed!")
    else:
        print(f"✗ {failed} test(s) failed")

    return failed == 0

if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
