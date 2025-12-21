import pygame
from src.entities.player.siena import Siena
from src.entities.enemies.snowy import Snowy
from src.entities.enemies.northerner import Northerner
from src.entities.enemies.elkman import Elkman
from src.ui.coin import Coin
from src.ui.npc import LevelGoalNPC
from src.ui.moving_platform import MovingPlatform, DisappearingPlatform
from src.ui.appearing_platform import AppearingPlatform

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

    # ===================================================================
    # BEAT 1: SPIN ATTACK TUTORIAL ZONE (0-1,500px)
    # Goal: Teach spin attack mechanic safely
    # ===================================================================

    # Starting platforms - gradually ascending with more intermediate steps
    platform1 = pygame.Rect(200, 350, 300, 25)
    platform2 = pygame.Rect(650, 300, 250, 25)
    platform_early1 = pygame.Rect(800, 260, 150, 25)  # Additional intermediate platform
    # platform3 REMOVED - overlaps with roll_ceiling1
    # platform_early2 REMOVED - conflicts with roll tunnel 1

    # ROLL TUNNEL 1 (Beat 1, x=1200-1600) - Compact tutorial tunnel
    roll_ceiling1 = pygame.Rect(1200, 215, 400, 25)  # Ceiling at Y=215
    roll_support1 = pygame.Rect(1200, 370, 400, 25)  # Support below at Y=370 (185px clearance) - ADJUSTED to not touch ground

    # ===================================================================
    # BEAT 2: SNOWY ENCOUNTERS WITH MOVING PLATFORMS (1,500-3,500px)
    # Goal: Practice spin attack against Snowy enemies while platforming
    # ===================================================================

    # platform4 REMOVED - overlaps with roll_support1
    # moving_platform1 will go here (1800-2000, horizontal)
    platform5 = pygame.Rect(2200, 300, 200, 25)
    # platform6 REMOVED - replaced by long hazard stretch at x=2600-3200
    # moving_platform2 will go here (2900, vertical)

    # SPIN SECTION: Landing platform after long hazard stretch
    platform_hazard_landing1 = pygame.Rect(3250, 350, 200, 25)

    # ROLL TUNNEL 2 (Beat 2, x=3600-3950) - Very compact tunnel
    roll_ceiling2 = pygame.Rect(3600, 220, 350, 25)  # Ceiling at Y=220
    roll_support2 = pygame.Rect(3600, 370, 350, 25)  # Support below at Y=370 (180px clearance - very tight!) - ADJUSTED to not touch ground

    platform7 = pygame.Rect(3100, 300, 250, 25)

    # ===================================================================
    # BEAT 3: MULTI-ENEMY COMBAT (3,500-7,000px)
    # Goal: Use spin attack for crowd control with varied platforming
    # ===================================================================

    # platform8 REMOVED - overlaps with roll_support2
    # platform9 REMOVED - creates spin gap 1 (x=4200-4520)
    # platform10 REMOVED - creates spin gap 1 (x=4200-4520)

    # SPIN GAP 1 platforms (Beat 3, 320px gap requiring spin)
    platform_spin_before1 = pygame.Rect(3950, 300, 200, 25)  # Before gap
    platform_spin_after1 = pygame.Rect(4520, 280, 200, 25)   # After gap

    # Moving platform section
    # moving_platform3 will go here (4900, horizontal)
    platform11 = pygame.Rect(5300, 300, 200, 25)

    # MANDATORY PIT SECTION (x=5600-6400) - disappearing platforms only!
    # No static platforms here - must use disappearing platforms to cross

    # After pit
    platform13 = pygame.Rect(6400, 300, 250, 25)

    # REWARD PLATFORM SYSTEM (Beat 4, requires DOUBLE SPIN to reach)
    # Final reward platform - requires second spin to reach from platform13
    platform_reward = pygame.Rect(7050, 150, 180, 25)  # 750px from platform13, Y=170 (130px up)

    # ===================================================================
    # BEAT 4: NORTHERNER CHALLENGES WITH DISAPPEARING PLATFORMS (7,000-9,500px)
    # Goal: Master spin attack against tougher enemies with time pressure
    # ===================================================================

    # disappearing_platform1 will go here (7350)
    # platform15 REMOVED - replaced by long hazard stretch at x=7800-8400

    # SPIN SECTION: Landing platform after long hazard stretch 2
    platform_hazard_landing2 = pygame.Rect(8450, 320, 200, 25)

    # Vertical platforming section
    platform16 = pygame.Rect(8100, 250, 200, 25)
    platform17 = pygame.Rect(8450, 200, 200, 25)

    # ROLL TUNNEL 3 (Beat 4, x=8700-9000) - Compact tunnel
    roll_ceiling3 = pygame.Rect(8700, 218, 300, 25)  # Ceiling at Y=218
    roll_support3 = pygame.Rect(8700, 370, 300, 25)  # Support below at Y=370 (182px clearance) - ADJUSTED to not touch ground

    # disappearing_platform2 will go here (8750)
    platform18 = pygame.Rect(9100, 250, 250, 25)

    # Final approach with moving platforms
    # moving_platform5 will go here (9500, horizontal)

    # SPIN GAP 2 platforms (Beat 5, 300px gap requiring spin)
    platform_spin_before2 = pygame.Rect(9200, 320, 180, 25)  # Before gap

    # ===================================================================
    # BEAT 5: FINAL CHALLENGE (10,000-11,750px)
    # Goal: Combination of all mechanics, ending with stairs to Pedro
    # ===================================================================
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
    moving_platforms.append(MovingPlatform(x=10600, y=150, width=180, height=25, move_range=150, speed=3, direction='horizontal'))

    # ===================================================================
    # DISAPPEARING PLATFORMS
    # ===================================================================

    disappearing_platforms = []

    # TUTORIAL DISAPPEARING PLATFORMS (Beat 1, x=600-1100) - Learn the mechanic!
    # Very generous disappear time (120 frames = 2 seconds) to let players get comfortable
    disappearing_platforms.append(DisappearingPlatform(x=600, y=340, width=180, height=25, disappear_time=30))  # Tutorial platform 1
    #disappearing_platforms.append(DisappearingPlatform(x=950, y=280, width=180, height=25, disappear_time=30))  # Tutorial platform 2

    # MANDATORY PIT CROSSING (x=5600-6400) - NO GROUND BELOW!
    # Player MUST use these disappearing platforms to cross the pit
    # VERY FAST disappear times for extreme challenge - only 15 frames (0.25 seconds)!
    disappearing_platforms.append(DisappearingPlatform(x=5600, y=350, width=180, height=25, disappear_time=15))  # First platform
    disappearing_platforms.append(DisappearingPlatform(x=5850, y=320, width=180, height=25, disappear_time=15))  # Second platform
    disappearing_platforms.append(DisappearingPlatform(x=6100, y=350, width=180, height=25, disappear_time=15))  # Third platform

    # Beat 4
    disappearing_platforms.append(DisappearingPlatform(x=7500, y=340, width=200, height=25, disappear_time=15))


    # Beat 5
    disappearing_platforms.append(DisappearingPlatform(x=10600, y=320, width=200, height=25, disappear_time=15))

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

    # MECHANIC 2: Alternating Bridge (Beat 5, around x=9800-10500)
    # Two rows that alternate - when top is visible, bottom is invisible
    # MOVED to Beat 5 to avoid overlap with reward platform area
    bridge_start_x = 9800
    upper_bridge_y = 240
    lower_bridge_y = 310

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

    # MECHANIC 3: Safe Island Pattern - REMOVED
    # Island platforms at x=9400 and x=9750 removed to create spin gap 2

    # ===================================================================
    # HAZARDS - Fire hazards throughout the level
    # Fire sprites are 40px tall (smaller flames), positioned above ground
    # ===================================================================

    # ROLL TUNNEL 1 HAZARDS (on ceiling top at Y=185)
    # Position hazards to align with roll_ceiling1 (x=1200-1600)
    # Inset by 10px: 1250+10=1260, 80-20=60
    hazard_roll1_ceiling1 = pygame.Rect(1260, 185, 60, 30)
    # Inset by 10px: 1380+10=1390, 80-20=60
    hazard_roll1_ceiling2 = pygame.Rect(1390, 185, 60, 30)
    # Inset by 10px: 1510+10=1520, 80-20=60
    hazard_roll1_ceiling3 = pygame.Rect(1520, 185, 60, 30)

    # Ground hazards at Y=370 (sit ON ground at Y=400)
    # hazard1 REMOVED - overlaps with roll_support1

    # LONG HAZARD STRETCH 1 (Beat 2, x=2600-3200) - Forces spin to cross
    # Inset by 10px: 2600+10=2610, 600-20=580
    hazard_long_stretch1 = pygame.Rect(2610, 370, 580, 30)

    # Inset by 10px: 2500+10=2510, 150-20=130
    hazard2 = pygame.Rect(2510, 370, 130, 30)
    # hazard3 REMOVED - overlaps with platform_hazard_landing1

    # ROLL TUNNEL 2 HAZARDS (on ceiling top at Y=190)
    # Inset by 10px: 3630+10=3640, 80-20=60
    hazard_roll2_ceiling1 = pygame.Rect(3640, 190, 60, 30)
    # Inset by 10px: 3780+10=3790, 80-20=60
    hazard_roll2_ceiling2 = pygame.Rect(3790, 190, 60, 30)

    # Inset by 10px: 4700+10=4710, 180-20=160
    hazard4 = pygame.Rect(4710, 370, 160, 30)
    # hazard5 REMOVED - was at x=6000, right after pit section (cleared for landing area)
    # Inset by 10px: 7500+10=7510, 200-20=180
    hazard6 = pygame.Rect(7510, 370, 180, 30)

    # LONG HAZARD STRETCH 2 (Beat 4, x=7800-8400) - Forces spin to cross
    # Inset by 10px: 7800+10=7810, 600-20=580
    hazard_long_stretch2 = pygame.Rect(7810, 370, 580, 30)

    # ROLL TUNNEL 3 HAZARDS (on ceiling top at Y=188)
    # Inset by 10px: 8730+10=8740, 80-20=60
    hazard_roll3_ceiling1 = pygame.Rect(8740, 188, 60, 30)
    # Inset by 10px: 8900+10=8910, 80-20=60
    hazard_roll3_ceiling2 = pygame.Rect(8910, 188, 60, 30)

    # Inset by 10px: 9400+10=9410, 150-20=130
    hazard7 = pygame.Rect(9410, 370, 130, 30)
    # Inset by 10px: 10800+10=10810, 180-20=160
    hazard8 = pygame.Rect(10810, 370, 160, 30)

    hazards = [
        hazard_roll1_ceiling1, hazard_roll1_ceiling2, hazard_roll1_ceiling3,
        hazard_long_stretch1, hazard2,
        hazard_roll2_ceiling1, hazard_roll2_ceiling2,
        hazard4, hazard6, hazard_long_stretch2,
        hazard_roll3_ceiling1, hazard_roll3_ceiling2,
        hazard7, hazard8
    ]

    # ===================================================================
    # PLATFORMS LIST
    # ===================================================================

    platforms = ground_segments + [
        # Beat 1
        platform1, platform2, platform_early1,
        # platform3 REMOVED - overlaps with roll_ceiling1
        # platform_early2 REMOVED
        roll_ceiling1, roll_support1,  # Roll tunnel 1
        # Beat 2
        # platform4 REMOVED - overlaps with roll_support1
        platform5,
        # platform6 REMOVED (replaced by hazard stretch)
        platform_hazard_landing1,  # Landing after hazard stretch 1
        roll_ceiling2, roll_support2,  # Roll tunnel 2
        platform7,
        # Beat 3
        # platform8 REMOVED - overlaps with roll_support2
        # platform9, platform10 REMOVED (create spin gap 1)
        platform_spin_before1, platform_spin_after1,  # Spin gap 1 platforms
        platform11, platform13,
        # Reward platform system (requires double spin)
        platform_reward,
        # Beat 4
        # platform14 REMOVED
        # platform15 REMOVED (replaced by hazard stretch)
        platform_hazard_landing2,  # Landing after hazard stretch 2
        platform16, platform17,
        roll_ceiling3, roll_support3,  # Roll tunnel 3
        # platform12 removed (was in pit)
        platform18,
        # Beat 5
        platform_spin_before2,  # Spin gap 2 before platform
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
    enemies.append(Snowy(x=700, y=370, patrol_left=500, patrol_right=1100))

    # Rhythm Section - 1 Snowy
    enemies.append(Snowy(x=1500, y=370, patrol_left=1400, patrol_right=1900))

    # Beat 2: Snowy encounters - 2 Snowy (reduced from 3)
    enemies.append(Snowy(x=2300, y=270, patrol_left=2200, patrol_right=2400))
    enemies.append(Snowy(x=3200, y=270, patrol_left=3100, patrol_right=3300))

    # Beat 3: Multi-enemy - 2 Snowy + 2 Northerner
    enemies.append(Snowy(x=3700, y=320, patrol_left=3600, patrol_right=3900))
    enemies.append(Northerner(x=4600, y=220, patrol_left=4500, patrol_right=4700))
    # NEW: Northerner after spin gap 1 - forces spin attack
    enemies.append(Northerner(x=4570, y=250, patrol_left=4520, patrol_right=4700))
    enemies.append(Snowy(x=5400, y=270, patrol_left=5300, patrol_right=5500))

    # Beat 4: Mid-section area - 1 Northerner
    enemies.append(Northerner(x=7000, y=190, patrol_left=6900, patrol_right=7100))

    # Beat 4: Northerner challenges - 4 Northerner
    enemies.append(Northerner(x=7800, y=270, patrol_left=7700, patrol_right=7900))
    # NEW: Northerner after long hazard stretch 2 - forces spin attack
    enemies.append(Northerner(x=8500, y=290, patrol_left=8450, patrol_right=8650))
    enemies.append(Northerner(x=8550, y=170, patrol_left=8450, patrol_right=8650))
    enemies.append(Northerner(x=9200, y=220, patrol_left=9100, patrol_right=9300))

    # Beat 5: Final challenge - 2 Snowy + 2 Northerner
    enemies.append(Snowy(x=10300, y=320, patrol_left=10200, patrol_right=10400))
    # NEW: Northerner mid-air in spin gap 2 - must spin through
    enemies.append(Northerner(x=9550, y=280, patrol_left=9500, patrol_right=9600))
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
    coins.add(Coin(850, 225))  # FIXED: Y=225 to clear platform at Y=260
    # REMOVED: Coin on platform_early2 (platform removed)

    # NEW: ROLL TUNNEL 1 COINS (under tunnel as reward)
    coins.add(Coin(1300, 340))  # ADJUSTED: Y=340 to match support at Y=370
    coins.add(Coin(1400, 340))
    coins.add(Coin(1500, 340))

    # HIGH-RISK COINS - Above hazards for risk/reward gameplay
    coins.add(Coin(1250, 290))  # Above hazard1 (risky jump)
    coins.add(Coin(2350, 265))  # FIXED: Y=265 to clear platform at Y=300
    # REMOVED: Coin above hazard3 (will add new coins instead)
    # REMOVED: Coin above hazard4 (will add new coins instead)

    # REMOVED: RHYTHM SECTION COINS (4 coins removed to make room for new coins)

    # Beat 2 coins
    coins.add(Coin(1900, 280))
    coins.add(Coin(2400, 210))

    # NEW: LONG HAZARD STRETCH 1 COINS (risky coins above hazards)
    coins.add(Coin(2800, 290))
    coins.add(Coin(3000, 290))

    coins.add(Coin(3000, 260))

    # NEW: ROLL TUNNEL 2 COINS (under tunnel as reward)
    coins.add(Coin(3700, 340))  # ADJUSTED: Y=340 to match support at Y=370
    coins.add(Coin(3850, 340))

    # Beat 3 coins
    # REMOVED: coin at x=4200 (old platform9 removed)
    # NEW: SPIN GAP 1 COINS (mid-gap requiring risky spin timing)
    coins.add(Coin(4300, 250))
    coins.add(Coin(4400, 250))

    coins.add(Coin(5000, 240))
    coins.add(Coin(5800, 210))
    coins.add(Coin(6200, 280))  # NEW - After disappearing platform section
    coins.add(Coin(6500, 260))

    # NEW: REWARD PLATFORM COINS (4 coins on tall distant platform requiring DOUBLE SPIN)
    coins.add(Coin(7050, 120))  # Adjusted for new platform position at x=7150, y=170
    coins.add(Coin(7100, 120))
    coins.add(Coin(7150, 120))
    coins.add(Coin(7200, 120))

    # ALTERNATING BRIDGE COINS - REMOVED (bridge moved to Beat 5 at x=9800+)

    # Beat 4 coins
    coins.add(Coin(6900, 260))  # NEW - Beat 4 area
    coins.add(Coin(7100, 320))  # NEW - Beat 4 area
    coins.add(Coin(7450, 280))
    # REMOVED: coin above hazard6 (will keep existing coins)
    coins.add(Coin(8200, 120))
    coins.add(Coin(8850, 120))

    # NEW: ROLL TUNNEL 3 COINS (under tunnel as reward)
    coins.add(Coin(8800, 340))  # ADJUSTED: Y=340 to match support at Y=370
    coins.add(Coin(8950, 340))

    # REMOVED: coin at x=9600 (near old island platforms)

    # REMOVED: ISLAND SECTION COINS (2 coins - platforms removed for spin gap 2)

    # NEW: SPIN GAP 2 COINS (mid-gap coins)
    coins.add(Coin(9500, 260))
    coins.add(Coin(9600, 260))

    # Beat 5 coins - ADJUSTED
    # REMOVED: 5 coins to make room (x=10100, 10400, 10650, 10850, 11200)
    # ADDING BACK: 4 coins to reach exactly 40 total
    coins.add(Coin(10250, 320))  # On platform20
    coins.add(Coin(11000, 270))  # Near final area
    coins.add(Coin(11100, 260))
    coins.add(Coin(11400, 310))
    coins.add(Coin(11500, 285))  # FIXED: Y=285 to clear platform at Y=320

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
