import pygame
from player.siena import Siena
from enemies.snowy import Snowy
from enemies.northerner import Northerner
from enemies.elkman import Elkman
from ui.coin import Coin
from ui.npc import LevelGoalNPC
from ui.moving_platform import MovingPlatform, DisappearingPlatform
from ui.appearing_platform import AppearingPlatform

LEVEL_WIDTH = 12000  # Ends at staircase
LEVEL_HEIGHT = 600

def build_level(abilities=None):
    """
    Build Level 1-3: Mountain Climb - Spin Attack Mechanic Tutorial

    DESIGN PHILOSOPHY:
    - Introduce spin attack for multi-enemy combat
    - Challenging platforming with harsh snowstorm background
    - Moving and disappearing platforms for added challenge
    - 30% difficulty increase from Level 2
    - Ground at Y=400 (matching level 2)

    SPIN ATTACK TEACHING PATTERN:
    1. Safe area to practice spin attack (0-1500px)
    2. Single enemy encounters with moving platforms (1500-3500px)
    3. Multi-enemy groups requiring spin attack (3500-7000px)
    4. Boss-like Northerner encounters with disappearing platforms (7000-11000px)

    ENEMY BREAKDOWN (15 total - reduced for better pacing):
    - 9 Snowy (ranged, 2 health, vulnerable to spin attack and roll)
    - 6 Northerner (melee, 1 health, vulnerable only to spin attack)

    Args:
        abilities: Dict of unlocked abilities (should include 'spin_attack': True)

    Returns:
        bg_color, platforms, hazards, level_width, player, enemies,
        projectiles, coins, world_name, goal_npc, background_layers,
        moving_platforms, disappearing_platforms, appearing_platforms
    """
    bg_color = None
    world_name = "1-3"

    # Background layers for snowstorm theme (parallax from back to front) - removed l9-block
    background_layers = [
        "assets/images/backgrounds/snowstorm/layers/l1-background.png",
        "assets/images/backgrounds/snowstorm/layers/l2-mountains01.png",
        "assets/images/backgrounds/snowstorm/layers/l3-fog01.png",
        "assets/images/backgrounds/snowstorm/layers/l4-winds01.png",
        "assets/images/backgrounds/snowstorm/layers/l5-mountains02.png",
        "assets/images/backgrounds/snowstorm/layers/l6-fog02.png",
        "assets/images/backgrounds/snowstorm/layers/l7-winds02.png",
        "assets/images/backgrounds/snowstorm/layers/l8-ground.png",
    ]

    # ===================================================================
    # GROUND - Segments with multiple GAPS for roll/spin practice
    # ===================================================================
    ground_segments = []

    # Define ground segments with gaps for roll-jump and combat space
    ground_segments.append(pygame.Rect(0, 400, 2000, 40))           # Start area
    # GAP 1: 2000-2400 (400px - roll practice)
    ground_segments.append(pygame.Rect(2400, 400, 1800, 40))        # Early-mid section
    # GAP 2: 4200-4600 (400px - more roll practice)
    ground_segments.append(pygame.Rect(4600, 400, 1000, 40))        # Before pit
    # MAJOR PIT: 5600-6400 (800px - challenging gap)
    ground_segments.append(pygame.Rect(6400, 400, 2400, 40))        # Mid-late section
    # GAP 3: 8800-9200 (400px - spin attack space)
    ground_segments.append(pygame.Rect(9200, 400, 2000, 40))        # Late section
    # GAP 4: 11200-11600 (400px - final challenge)
    ground_segments.append(pygame.Rect(11600, 400, 200, 40))       # Short landing at goal

    # ===================================================================
    # BEAT 1: SPIN ATTACK TUTORIAL ZONE (0-1,500px)
    # Goal: Teach spin attack mechanic safely
    # ===================================================================

    # Starting platforms - gradually ascending with more intermediate steps
    platform1 = pygame.Rect(200, 350, 300, 25)
    platform2 = pygame.Rect(650, 300, 250, 25)
    platform_early1 = pygame.Rect(800, 260, 150, 25)  # Additional intermediate platform
    platform3 = pygame.Rect(1050, 220, 250, 25)
    platform_early2 = pygame.Rect(1200, 180, 150, 25)  # Another challenge platform - repositioned

    # ===================================================================
    # BEAT 2: SNOWY ENCOUNTERS WITH MOVING PLATFORMS (1,500-3,500px)
    # Goal: Practice spin attack against Snowy enemies while platforming
    # ===================================================================

    platform4 = pygame.Rect(1500, 350, 200, 25)
    # moving_platform1 will go here (1800-2000, horizontal)
    platform5 = pygame.Rect(2200, 300, 200, 25)
    platform6 = pygame.Rect(2600, 250, 200, 25)
    # moving_platform2 will go here (2900, vertical)
    platform7 = pygame.Rect(3100, 300, 250, 25)

    # ===================================================================
    # BEAT 3: MULTI-ENEMY COMBAT (3,500-7,000px)
    # Goal: Use spin attack for crowd control with varied platforming
    # ===================================================================

    platform8 = pygame.Rect(3600, 350, 300, 25)
    platform9 = pygame.Rect(4100, 300, 200, 25)
    platform10 = pygame.Rect(4500, 250, 200, 25)

    # Moving platform section
    # moving_platform3 will go here (4900, horizontal)
    platform11 = pygame.Rect(5300, 300, 200, 25)
    # platform12 REMOVED - was in pit area (x=5700)

    # MANDATORY PIT SECTION (x=5600-6400) - disappearing platforms only!
    # No static platforms here - must use disappearing platforms to cross

    # After pit
    platform13 = pygame.Rect(6400, 300, 250, 25)

    # ===================================================================
    # BEAT 4: NORTHERNER CHALLENGES WITH DISAPPEARING PLATFORMS (7,000-9,500px)
    # Goal: Master spin attack against tougher enemies with time pressure
    # ===================================================================

    platform14 = pygame.Rect(7000, 350, 250, 25)
    # disappearing_platform1 will go here (7350)
    platform15 = pygame.Rect(7700, 300, 250, 25)

    # Vertical platforming section
    platform16 = pygame.Rect(8100, 250, 200, 25)
    platform17 = pygame.Rect(8450, 200, 200, 25)
    # disappearing_platform2 will go here (8750)
    platform18 = pygame.Rect(9100, 250, 250, 25)

    # Final approach with moving platforms
    # moving_platform5 will go here (9500, horizontal)
    platform19 = pygame.Rect(9900, 300, 250, 25)

    # ===================================================================
    # BEAT 5: FINAL CHALLENGE (10,000-11,750px)
    # Goal: Combination of all mechanics, ending with stairs to Pedro
    # ===================================================================

    platform20 = pygame.Rect(10200, 350, 300, 25)
    # disappearing_platform3 will go here (10600)
    platform21 = pygame.Rect(10950, 300, 250, 25)

    # Stairs leading up to Pedro (ascending from left to right)
    stair1 = pygame.Rect(11250, 370, 100, 25)
    stair2 = pygame.Rect(11350, 345, 100, 25)
    stair3 = pygame.Rect(11450, 320, 100, 25)
    stair4 = pygame.Rect(11550, 295, 100, 25)
    stair5 = pygame.Rect(11650, 270, 100, 25)  # Top stair where Pedro stands

    # ===================================================================
    # MOVING PLATFORMS
    # ===================================================================

    moving_platforms = []

    # Beat 2
    moving_platforms.append(MovingPlatform(x=1800, y=320, width=180, height=25, move_range=200, speed=2, direction='horizontal'))
    moving_platforms.append(MovingPlatform(x=2900, y=200, width=180, height=25, move_range=150, speed=1.5, direction='vertical'))

    # Beat 3
    # Adjusted move_range to prevent overlap with platform11 at x=5300
    moving_platforms.append(MovingPlatform(x=4900, y=280, width=180, height=25, move_range=200, speed=2.5, direction='horizontal'))
    # Moving platform at x=6100 removed - was in mandatory pit section (x=5600-6400)

    # Beat 5 - Adjusted position to avoid overlap with island platforms
    moving_platforms.append(MovingPlatform(x=10000, y=270, width=180, height=25, move_range=150, speed=3, direction='horizontal'))

    # ===================================================================
    # DISAPPEARING PLATFORMS
    # ===================================================================

    disappearing_platforms = []

    # TUTORIAL DISAPPEARING PLATFORMS (Beat 1, x=600-1100) - Learn the mechanic!
    # Very generous disappear time (120 frames = 2 seconds) to let players get comfortable
    disappearing_platforms.append(DisappearingPlatform(x=600, y=340, width=180, height=25, disappear_time=120))  # Tutorial platform 1
    disappearing_platforms.append(DisappearingPlatform(x=950, y=280, width=180, height=25, disappear_time=120))  # Tutorial platform 2

    # MANDATORY PIT CROSSING (x=5600-6400) - NO GROUND BELOW!
    # Player MUST use these disappearing platforms to cross the pit
    # VERY FAST disappear times for extreme challenge - only 15 frames (0.25 seconds)!
    disappearing_platforms.append(DisappearingPlatform(x=5600, y=350, width=180, height=25, disappear_time=15))  # First platform
    disappearing_platforms.append(DisappearingPlatform(x=5850, y=320, width=180, height=25, disappear_time=15))  # Second platform
    disappearing_platforms.append(DisappearingPlatform(x=6100, y=350, width=180, height=25, disappear_time=15))  # Third platform
    disappearing_platforms.append(DisappearingPlatform(x=6350, y=320, width=180, height=25, disappear_time=15))  # Final platform

    # Beat 4
    disappearing_platforms.append(DisappearingPlatform(x=7350, y=320, width=200, height=25, disappear_time=60))
    disappearing_platforms.append(DisappearingPlatform(x=8750, y=220, width=200, height=25, disappear_time=60))

    # Beat 5
    disappearing_platforms.append(DisappearingPlatform(x=10600, y=320, width=200, height=25, disappear_time=50))

    # ===================================================================
    # APPEARING/DISAPPEARING PLATFORMS (Rhythm Challenge & Mechanics)
    # ===================================================================

    appearing_platforms = []

    # MECHANIC 1: Rhythm Challenge (Beat 2, around x=1400-1900)
    # Platforms appear in sequence creating a wave pattern
    # Each platform offset by 15 frames (0.25 seconds) for flowing rhythm
    # MOVED to avoid overlap with platform6
    rhythm_start_x = 1400
    rhythm_y = 270
    for i in range(5):
        appearing_platforms.append(AppearingPlatform(
            x=rhythm_start_x + (i * 120),
            y=rhythm_y,
            width=100,
            height=25,
            appear_time=60,
            disappear_time=60,
            start_visible=(i == 0)  # First one starts visible
        ))
        # Offset each platform's timer to create wave effect
        appearing_platforms[-1].timer = i * 15

    # MECHANIC 2: Alternating Bridge (Beat 3, around x=6700-7400)
    # Two rows that alternate - when top is visible, bottom is invisible
    # MOVED to avoid overlap with platform11, platform12, and moving4
    bridge_start_x = 6700
    upper_bridge_y = 220
    lower_bridge_y = 290

    # Upper row (starts visible)
    for i in range(4):
        appearing_platforms.append(AppearingPlatform(
            x=bridge_start_x + (i * 180),
            y=upper_bridge_y,
            width=160,
            height=25,
            appear_time=90,
            disappear_time=90,
            start_visible=True
        ))

    # Lower row (starts invisible)
    for i in range(4):
        appearing_platforms.append(AppearingPlatform(
            x=bridge_start_x + (i * 180),
            y=lower_bridge_y,
            width=160,
            height=25,
            appear_time=90,
            disappear_time=90,
            start_visible=False
        ))

    # MECHANIC 3: Safe Island Pattern (Beat 4, around x=9400-9900)
    # Appearing platforms around a central area
    # MOVED to avoid overlap with platform16

    # Left approach
    appearing_platforms.append(AppearingPlatform(
        x=9400, y=260, width=120, height=25,
        appear_time=75, disappear_time=75, start_visible=True
    ))
    # Right exit
    appearing_platforms.append(AppearingPlatform(
        x=9750, y=260, width=120, height=25,
        appear_time=75, disappear_time=75, start_visible=False
    ))
    # Offset their timers so they alternate
    appearing_platforms[-2].timer = 0
    appearing_platforms[-1].timer = 40

    # ===================================================================
    # HAZARDS - Fire hazards throughout the level
    # Fire sprites are 40px tall (smaller flames), positioned above ground
    # ===================================================================

    hazard1 = pygame.Rect(1200, 360, 120,  30)  # On ground_1
    hazard2 = pygame.Rect(2500, 360, 150,  30)  # Moved to ground_2 (was floating in gap 2000-2400)
    hazard3 = pygame.Rect(3400, 360, 120,  30)  # On ground_2
    hazard4 = pygame.Rect(4700, 360, 180,  30)  # On ground_3
    # hazard5 REMOVED - was at x=6000, right after pit section (cleared for landing area)
    hazard6 = pygame.Rect(7500, 360, 200,  30)  # On ground_4
    hazard7 = pygame.Rect(9400, 360, 150,  30)  # Moved onto ground_5 (was on edge of gap 8800-9200)
    hazard8 = pygame.Rect(10800, 360, 180,  30)  # On ground_5

    hazards = [hazard1, hazard2, hazard3, hazard4, hazard6, hazard7, hazard8]

    # ===================================================================
    # PLATFORMS LIST
    # ===================================================================

    platforms = ground_segments + [
        platform1, platform2, platform_early1, platform3, platform_early2,
        platform4, platform5, platform6, platform7, platform8, platform9, platform10,
        platform11, platform13, platform14, platform15,  # platform12 removed (was in pit)
        platform16, platform17, platform18, platform19, platform20,
        platform21, stair1, stair2, stair3, stair4, stair5
    ]

    # ===================================================================
    # PLAYER
    # ===================================================================

    player = Siena(x=100, y=490, abilities=abilities, max_health=10)  # Ground at y=400, spawn 90px below like Level 1, 5 hearts (10 lives)

    # ===================================================================
    # ENEMIES - 9 Snowy + 6 Northerner (reduced for better pacing)
    # ===================================================================

    enemies = []

    # Beat 1: Tutorial - 1 Snowy
    enemies.append(Snowy(x=900, y=220, patrol_left=800, patrol_right=1000))

    # Rhythm Section - 1 Snowy
    enemies.append(Snowy(x=1500, y=370, patrol_left=1400, patrol_right=1900))

    # Beat 2: Snowy encounters - 2 Snowy (reduced from 3)
    enemies.append(Snowy(x=2300, y=270, patrol_left=2200, patrol_right=2400))
    enemies.append(Snowy(x=3200, y=270, patrol_left=3100, patrol_right=3300))

    # Beat 3: Multi-enemy - 2 Snowy + 1 Northerner (reduced)
    enemies.append(Snowy(x=3700, y=320, patrol_left=3600, patrol_right=3900))
    enemies.append(Northerner(x=4600, y=220, patrol_left=4500, patrol_right=4700))
    enemies.append(Snowy(x=5400, y=270, patrol_left=5300, patrol_right=5500))

    # Alternating Bridge - 1 Northerner
    enemies.append(Northerner(x=7000, y=190, patrol_left=6900, patrol_right=7100))

    # Beat 4: Northerner challenges - 3 Northerner (reduced from 4)
    enemies.append(Northerner(x=7800, y=270, patrol_left=7700, patrol_right=7900))
    enemies.append(Northerner(x=8550, y=170, patrol_left=8450, patrol_right=8650))
    enemies.append(Northerner(x=9200, y=220, patrol_left=9100, patrol_right=9300))

    # Beat 5: Final challenge - 2 Snowy + 1 Northerner (reduced)
    enemies.append(Snowy(x=10300, y=320, patrol_left=10200, patrol_right=10400))
    enemies.append(Northerner(x=10700, y=290, patrol_left=10600, patrol_right=10800))
    enemies.append(Snowy(x=11000, y=270, patrol_left=10950, patrol_right=11100))

    # ===================================================================
    # COINS - Collectibles throughout the level
    # ===================================================================

    coins = pygame.sprite.Group()

    # Early coins
    coins.add(Coin(400, 310))
    coins.add(Coin(450, 310))
    coins.add(Coin(750, 260))
    coins.add(Coin(850, 250))  # NEW - on platform_early1
    coins.add(Coin(1050, 200))  # NEW - on platform_early2

    # HIGH-RISK COINS - Above hazards for risk/reward gameplay
    coins.add(Coin(1250, 290))  # NEW - Above hazard1 (risky jump)
    coins.add(Coin(2350, 290))  # NEW - Above hazard2 (risky jump)
    coins.add(Coin(3450, 290))  # NEW - Above hazard3 (risky jump)
    coins.add(Coin(4750, 290))  # NEW - Above hazard4 (risky jump)
    # Coin above hazard5 removed - hazard5 was removed (was at x=6000)
    coins.add(Coin(9250, 290))  # NEW - Above hazard7 (risky jump)

    # RHYTHM SECTION COINS - Above appearing platforms (requires timing)
    coins.add(Coin(1450, 240))  # NEW - Above rhythm0
    coins.add(Coin(1570, 240))  # NEW - Above rhythm1
    coins.add(Coin(1810, 240))  # NEW - Above rhythm3
    coins.add(Coin(1930, 240))  # NEW - Above rhythm4

    # Beat 2 coins
    coins.add(Coin(1900, 280))
    coins.add(Coin(2400, 210))
    coins.add(Coin(3000, 260))

    # Beat 3 coins
    coins.add(Coin(4200, 260))
    coins.add(Coin(5000, 240))
    coins.add(Coin(5800, 210))
    coins.add(Coin(6500, 260))

    # ALTERNATING BRIDGE COINS - On appearing platforms (requires timing and combat)
    coins.add(Coin(6800, 190))  # NEW - On upper bridge with Northerner
    coins.add(Coin(7060, 190))  # NEW - On upper bridge
    coins.add(Coin(7240, 190))  # NEW - On upper bridge with Northerner
    coins.add(Coin(6880, 260))  # NEW - On lower bridge

    # Beat 4 coins
    coins.add(Coin(7450, 280))
    coins.add(Coin(7550, 290))  # NEW - Above hazard6 (risky)
    coins.add(Coin(8200, 210))
    coins.add(Coin(8850, 180))
    coins.add(Coin(9600, 230))

    # ISLAND SECTION COINS - Near appearing platforms
    coins.add(Coin(9450, 230))  # NEW - On island_left
    coins.add(Coin(9800, 230))  # NEW - On island_right

    # Beat 5 coins - ENHANCED FINAL GAUNTLET
    coins.add(Coin(10100, 240))  # NEW - Above moving5
    coins.add(Coin(10400, 310))
    coins.add(Coin(10650, 280))  # NEW - On disappear3 (risky timing)
    coins.add(Coin(10850, 290))  # NEW - Above hazard8 (final risky coin)
    coins.add(Coin(11100, 260))
    coins.add(Coin(11200, 340))  # NEW - Near new enemy before stairs
    coins.add(Coin(11400, 310))
    coins.add(Coin(11500, 310))

    # ===================================================================
    # LEVEL GOAL NPC
    # ===================================================================

    goal_npc = LevelGoalNPC(x=11700, y=220)  # Position Pedro on top of the stairs

    # ===================================================================
    # PROJECTILES (Empty - enemies will create them)
    # ===================================================================

    projectiles = pygame.sprite.Group()

    return (bg_color, platforms, hazards, LEVEL_WIDTH, player,
            enemies, projectiles, coins, world_name, goal_npc, background_layers,
            moving_platforms, disappearing_platforms, appearing_platforms)
