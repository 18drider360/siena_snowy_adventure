import pygame
from player.siena import Siena
from enemies.snowy import Snowy
from enemies.northerner import Northerner
from enemies.swordsman import Swordsman
from enemies.frost_golem import FrostGolem
from enemies.spiked_slime import SpikedSlime
from ui.coin import Coin
from ui.npc import LevelGoalNPC
from ui.moving_platform import MovingPlatform, DisappearingPlatform
from ui.appearing_platform import AppearingPlatform

LEVEL_WIDTH = 18000  # Ends at staircase
LEVEL_HEIGHT = 600

def build_level(abilities=None):
    """
    Build Level 1-4: Northern Lights Summit - Final Challenge

    DESIGN PHILOSOPHY:
    - Ultimate challenge combining ALL mechanics from previous levels
    - Features ALL enemy types (Snowy, Northerner, Swordsman, Frost Golem, Spiked Slime)
    - Heavy use of disappearing platforms and appearing platforms
    - 50% difficulty increase from Level 3
    - Enemies spread out to avoid overwhelming player
    - Longer level with varied challenges

    LEVEL BREAKDOWN:
    - Tutorial Section (0-2000px): Remind players of all abilities
    - Early Gauntlet (2000-5000px): Mixed enemy types with platforming
    - Disappearing Platform Zone (5000-8000px): Pure platforming skill test
    - Combat Zones (8000-12000px): Strategic enemy placement
    - Appearing Platform Finale (12000-16000px): Timing-based challenge
    - Victory Path (16000-18000px): Stairs to Pedro

    ENEMY COUNT (25 total - well spread out):
    - 8 Snowy (aggressive chasers)
    - 5 Northerner (ranged warriors)
    - 4 Swordsman (melee fighters)
    - 5 Frost Golem (ranged artillery)
    - 3 Spiked Slime (hazard enemies)

    Returns:
        Complete level data tuple
    """
    bg_color = None
    world_name = "1-4"

    # Northern Lights background layers
    background_layers = [
        "assets/images/backgrounds/northern_lights/layers/l1-background.png",
        "assets/images/backgrounds/northern_lights/layers/l4-stars.png",
        "assets/images/backgrounds/northern_lights/layers/l2-northern-lights01.png",
        "assets/images/backgrounds/northern_lights/layers/l5-northern-lights02.png",
        "assets/images/backgrounds/northern_lights/layers/l6-moon.png",
        "assets/images/backgrounds/northern_lights/layers/l7-mountains01.png",
        "assets/images/backgrounds/northern_lights/layers/l8-mountains02.png",
        "assets/images/backgrounds/northern_lights/layers/l9-ground.png",
    ]

    # ===================================================================
    # GROUND - Continuous ground at Y=400 with strategic gaps
    # ===================================================================
    ground_segments = []

    # Segment layout: solid ground with gaps for pit challenges
    # Gap 1: 3500-4200 (700px gap)
    # Gap 2: 7200-8000 (800px gap)
    # Gap 3: 10000-10600 (600px gap - additional spin space)
    # Gap 4: 13000-13800 (800px gap)
    # Gap 5: 16000-17000 (1000px gap)

    gaps = [
        (3500, 4200),
        (7200, 8000),
        (10000, 10600),
        (13000, 13800),
        (16000, 17000)
    ]

    current_x = 0
    for gap_start, gap_end in gaps:
        # Add ground segment before gap
        if current_x < gap_start:
            ground_segments.append(pygame.Rect(current_x, 400, gap_start - current_x, 40))
        current_x = gap_end

    # Final ground segment after last gap
    ground_segments.append(pygame.Rect(current_x, 400, LEVEL_WIDTH - current_x, 40))

    # ===================================================================
    # TUTORIAL SECTION (0-2000px)
    # Platforms to demonstrate all abilities
    # ===================================================================

    # Jump tutorial
    platform1 = pygame.Rect(800, 350, 200, 25)
    platform2 = pygame.Rect(1100, 300, 200, 25)

    # Double jump tutorial
    platform3 = pygame.Rect(1400, 250, 150, 25)

    # Roll tutorial (low ceiling)
    ceiling1 = pygame.Rect(1600, 300, 400, 30)
    platform4 = pygame.Rect(1600, 350, 400, 25)

    # Spin attack reminder
    platform5 = pygame.Rect(2100, 300, 200, 25)

    # ===================================================================
    # EARLY GAUNTLET (2000-5000px)
    # Mixed platforming with enemies
    # ===================================================================

    platform6 = pygame.Rect(2400, 340, 250, 25)
    platform7 = pygame.Rect(2800, 260, 200, 25)
    platform8 = pygame.Rect(3100, 340, 200, 25)

    # Before first gap (3500-4200)
    platform9 = pygame.Rect(3300, 350, 150, 25)

    # Crossing first gap
    platform10 = pygame.Rect(3650, 320, 180, 25)
    platform11 = pygame.Rect(3950, 280, 180, 25)

    # After first gap
    platform12 = pygame.Rect(4300, 350, 200, 25)
    platform13 = pygame.Rect(4650, 280, 200, 25)
    platform14 = pygame.Rect(4950, 350, 200, 25)

    # ===================================================================
    # DISAPPEARING PLATFORM ZONE (5000-8000px)
    # Pure platforming challenge
    # ===================================================================

    platform15 = pygame.Rect(5200, 300, 200, 25)
    platform16 = pygame.Rect(5550, 350, 200, 25)
    platform17 = pygame.Rect(5900, 280, 200, 25)
    platform18 = pygame.Rect(6250, 350, 200, 25)
    platform19 = pygame.Rect(6600, 300, 200, 25)
    platform20 = pygame.Rect(6950, 350, 150, 25)

    # Gap 2 crossing (7200-8000) - handled by disappearing platforms

    # After second gap
    platform21 = pygame.Rect(8100, 350, 200, 25)
    platform22 = pygame.Rect(8450, 280, 200, 25)
    platform23 = pygame.Rect(8800, 350, 200, 25)

    # ===================================================================
    # COMBAT ZONES (8000-12000px)
    # Strategic enemy placement
    # ===================================================================

    platform24 = pygame.Rect(9150, 280, 250, 25)
    platform25 = pygame.Rect(9550, 350, 200, 25)
    platform26 = pygame.Rect(9900, 260, 200, 25)
    platform27 = pygame.Rect(10300, 340, 250, 25)
    platform28 = pygame.Rect(10700, 350, 200, 25)

    # Before third gap (11000-11800)
    platform29 = pygame.Rect(10950, 300, 150, 25)

    # Gap 3 crossing - handled by appearing platforms

    # After third gap
    platform30 = pygame.Rect(11900, 350, 200, 25)
    platform31 = pygame.Rect(12250, 280, 200, 25)

    # ===================================================================
    # APPEARING PLATFORM FINALE (12000-16000px)
    # Timing-based challenges
    # ===================================================================

    platform32 = pygame.Rect(12600, 350, 200, 25)
    platform33 = pygame.Rect(12950, 280, 200, 25)
    platform34 = pygame.Rect(13300, 350, 200, 25)
    platform35 = pygame.Rect(13650, 260, 200, 25)
    platform36 = pygame.Rect(14000, 340, 200, 25)
    platform37 = pygame.Rect(14350, 350, 150, 25)

    # Gap 4 crossing (14500-15500) - massive appearing platform challenge

    # After fourth gap
    platform38 = pygame.Rect(15600, 350, 200, 25)
    platform39 = pygame.Rect(15950, 280, 200, 25)

    # ===================================================================
    # VICTORY PATH (16000-17700px)
    # Stairs to Pedro
    # ===================================================================

    platform40 = pygame.Rect(16300, 350, 250, 25)
    platform41 = pygame.Rect(16700, 300, 200, 25)

    # Victory stairs
    stair1 = pygame.Rect(17000, 370, 100, 25)
    stair2 = pygame.Rect(17100, 345, 100, 25)
    stair3 = pygame.Rect(17200, 320, 100, 25)
    stair4 = pygame.Rect(17300, 295, 100, 25)
    stair5 = pygame.Rect(17400, 270, 100, 25)
    stair6 = pygame.Rect(17500, 245, 100, 25)
    stair7 = pygame.Rect(17600, 220, 100, 25)

    goal_npc = LevelGoalNPC(x=17650, y=170)  # On top of victory stairs

    # ===================================================================
    # MOVING PLATFORMS
    # ===================================================================

    moving_platforms = []

    # Tutorial area
    moving_platforms.append(MovingPlatform(x=500, y=320, width=180, height=25, move_range=150, speed=2, direction='horizontal'))

    # Early gauntlet
    moving_platforms.append(MovingPlatform(x=2600, y=250, width=180, height=25, move_range=180, speed=2.5, direction='vertical'))
    moving_platforms.append(MovingPlatform(x=4400, y=280, width=180, height=25, move_range=200, speed=2, direction='horizontal'))

    # Combat zones
    moving_platforms.append(MovingPlatform(x=9000, y=250, width=180, height=25, move_range=150, speed=2.5, direction='vertical'))
    moving_platforms.append(MovingPlatform(x=10500, y=280, width=180, height=25, move_range=180, speed=2, direction='horizontal'))

    # Finale section
    moving_platforms.append(MovingPlatform(x=13100, y=260, width=180, height=25, move_range=200, speed=3, direction='vertical'))
    moving_platforms.append(MovingPlatform(x=15800, y=280, width=180, height=25, move_range=150, speed=2, direction='horizontal'))

    # ===================================================================
    # DISAPPEARING PLATFORMS - Stepping on makes them vanish
    # ===================================================================

    disappearing_platforms = []

    # First gap crossing (3500-4200)
    disappearing_platforms.append(DisappearingPlatform(x=3500, y=350, width=180, height=25, disappear_time=30))
    disappearing_platforms.append(DisappearingPlatform(x=3750, y=320, width=180, height=25, disappear_time=30))
    disappearing_platforms.append(DisappearingPlatform(x=4000, y=350, width=180, height=25, disappear_time=30))

    # Second gap crossing (7200-8000) - CHALLENGING
    disappearing_platforms.append(DisappearingPlatform(x=7200, y=350, width=180, height=25, disappear_time=25))
    disappearing_platforms.append(DisappearingPlatform(x=7400, y=320, width=180, height=25, disappear_time=25))
    disappearing_platforms.append(DisappearingPlatform(x=7600, y=350, width=180, height=25, disappear_time=25))
    disappearing_platforms.append(DisappearingPlatform(x=7800, y=320, width=180, height=25, disappear_time=25))

    # Scattered throughout level - positioned to avoid overlap with static platforms
    disappearing_platforms.append(DisappearingPlatform(x=5400, y=220, width=180, height=25, disappear_time=35))
    disappearing_platforms.append(DisappearingPlatform(x=6400, y=220, width=180, height=25, disappear_time=35))
    disappearing_platforms.append(DisappearingPlatform(x=9400, y=200, width=180, height=25, disappear_time=35))

    # ===================================================================
    # APPEARING/DISAPPEARING PLATFORMS - Timer-based
    # ===================================================================

    appearing_platforms = []

    # Third gap crossing (11000-11800) - Alternating pattern
    for i in range(5):
        appearing_platforms.append(AppearingPlatform(
            x=11000 + (i * 180), y=330,
            width=160, height=25,
            appear_time=90, disappear_time=90,
            start_visible=(i % 2 == 0)
        ))

    # Fourth gap crossing (14500-15500) - MASSIVE CHALLENGE
    # Wave pattern
    for i in range(6):
        appearing_platforms.append(AppearingPlatform(
            x=14500 + (i * 180), y=300 + (20 if i % 2 == 0 else 0),
            width=160, height=25,
            appear_time=75, disappear_time=75,
            start_visible=(i == 0)
        ))
        appearing_platforms[-1].timer = i * 15  # Offset timers for wave

    # Scattered throughout for variety - positioned to avoid overlap with static platforms
    appearing_platforms.append(AppearingPlatform(x=8600, y=210, width=140, height=25, appear_time=80, disappear_time=80, start_visible=True))
    appearing_platforms.append(AppearingPlatform(x=12800, y=210, width=140, height=25, appear_time=80, disappear_time=80, start_visible=False))
    appearing_platforms.append(AppearingPlatform(x=16100, y=230, width=140, height=25, appear_time=80, disappear_time=80, start_visible=True))

    # ===================================================================
    # HAZARDS - Fire hazards (smaller flames, 40px tall)
    # ===================================================================

    hazard1 = pygame.Rect(1300, 360, 150,  30)
    hazard2 = pygame.Rect(2500, 360, 180,  30)
    hazard3 = pygame.Rect(4800, 360, 200,  30)
    hazard4 = pygame.Rect(6100, 360, 150,  30)
    hazard5 = pygame.Rect(8300, 360, 180,  30)
    hazard6 = pygame.Rect(9800, 360, 200,  30)
    hazard7 = pygame.Rect(12100, 360, 180,  30)
    hazard8 = pygame.Rect(14000, 360, 200,  30)  # Moved from 13500 (was in gap 13000-13800)
    hazard9 = pygame.Rect(15200, 360, 150,  30)
    hazard10 = pygame.Rect(17200, 360, 180,  30)  # Moved from 16500 (was in gap 16000-17000)

    hazards = [hazard1, hazard2, hazard3, hazard4, hazard5, hazard6, hazard7, hazard8, hazard9, hazard10]

    # ===================================================================
    # PLATFORMS LIST
    # ===================================================================

    platforms = ground_segments + [
        platform1, platform2, platform3, platform4, platform5,
        platform6, platform7, platform8, platform9, platform10,
        platform11, platform12, platform13, platform14, platform15,
        platform16, platform17, platform18, platform19, platform20,
        platform21, platform22, platform23, platform24, platform25,
        platform26, platform27, platform28, platform29, platform30,
        platform31, platform32, platform33, platform34, platform35,
        platform36, platform37, platform38, platform39, platform40,
        platform41, ceiling1,
        stair1, stair2, stair3, stair4, stair5, stair6, stair7
    ]

    # ===================================================================
    # PLAYER
    # ===================================================================

    player = Siena(x=100, y=490, abilities=abilities, max_health=12)  # 6 hearts (12 lives) - hardest level

    # ===================================================================
    # ENEMIES - 25 total, well spread throughout level
    # All enemy types represented
    # ===================================================================

    enemies = []

    # TUTORIAL AREA - 2 enemies (gentle intro)
    enemies.append(Snowy(x=1200, y=350, patrol_left=1000, patrol_right=1400))
    enemies.append(Snowy(x=1900, y=350, patrol_left=1700, patrol_right=2100))

    # EARLY GAUNTLET (2000-5000) - 6 enemies mixed
    enemies.append(Swordsman(x=2500, y=300, patrol_left=2300, patrol_right=2700))
    enemies.append(Snowy(x=2900, y=350, patrol_left=2750, patrol_right=3150))
    enemies.append(FrostGolem(x=3200, y=300, patrol_left=3000, patrol_right=3400))
    enemies.append(Northerner(x=3800, y=300, patrol_left=3650, patrol_right=4000))
    enemies.append(SpikedSlime(x=4350, y=350, patrol_left=4300, patrol_right=4500))
    enemies.append(Snowy(x=4750, y=350, patrol_left=4600, patrol_right=4950))

    # DISAPPEARING ZONE (5000-8000) - 5 enemies (less dense for platforming focus)
    enemies.append(Swordsman(x=5300, y=300, patrol_left=5150, patrol_right=5500))
    enemies.append(FrostGolem(x=6000, y=350, patrol_left=5850, patrol_right=6200))
    enemies.append(Snowy(x=6700, y=350, patrol_left=6550, patrol_right=6900))
    enemies.append(Northerner(x=7800, y=350, patrol_left=7650, patrol_right=7950))
    enemies.append(Northerner(x=8200, y=350, patrol_left=8050, patrol_right=8400))

    # COMBAT ZONES (8000-12000) - 8 enemies (moderate combat)
    enemies.append(Snowy(x=8900, y=350, patrol_left=8750, patrol_right=9100))
    enemies.append(Swordsman(x=9300, y=280, patrol_left=9150, patrol_right=9500))
    enemies.append(FrostGolem(x=9700, y=350, patrol_left=9550, patrol_right=9900))
    enemies.append(Northerner(x=10100, y=300, patrol_left=9950, patrol_right=10300))
    enemies.append(SpikedSlime(x=10500, y=350, patrol_left=10350, patrol_right=10700))
    enemies.append(Snowy(x=10850, y=350, patrol_left=10700, patrol_right=11050))
    enemies.append(FrostGolem(x=11400, y=350, patrol_left=11250, patrol_right=11550))
    enemies.append(Swordsman(x=11950, y=350, patrol_left=11800, patrol_right=12150))

    # APPEARING PLATFORM FINALE (12000-16000) - 4 enemies (focus on platforming)
    enemies.append(Northerner(x=12750, y=350, patrol_left=12600, patrol_right=12950))
    enemies.append(Snowy(x=13400, y=350, patrol_left=13250, patrol_right=13650))
    enemies.append(FrostGolem(x=14900, y=350, patrol_left=14750, patrol_right=15050))
    enemies.append(SpikedSlime(x=16200, y=350, patrol_left=16050, patrol_right=16400))

    # ===================================================================
    # COINS - Strategic placement (60 total)
    # ===================================================================

    coins = pygame.sprite.Group()

    # Tutorial area
    for x in range(300, 2000, 300):
        coins.add(Coin(x, 320))

    # Additional tutorial coins
    coins.add(Coin(platform1.x + 100, platform1.y - 40))
    coins.add(Coin(platform2.x + 100, platform2.y - 40))
    coins.add(Coin(platform3.x + 75, platform3.y - 40))
    coins.add(Coin(platform4.x + 200, platform4.y - 40))
    coins.add(Coin(platform5.x + 100, platform5.y - 40))

    # Above platforms
    coins.add(Coin(platform6.x + 100, platform6.y - 40))
    coins.add(Coin(platform7.x + 100, platform7.y - 40))
    coins.add(Coin(platform8.x + 100, platform8.y - 40))
    coins.add(Coin(platform10.x + 90, platform10.y - 40))
    coins.add(Coin(platform12.x + 100, platform12.y - 40))
    coins.add(Coin(platform13.x + 100, platform13.y - 40))
    coins.add(Coin(platform15.x + 100, platform15.y - 40))
    coins.add(Coin(platform17.x + 100, platform17.y - 40))
    coins.add(Coin(platform19.x + 100, platform19.y - 40))
    coins.add(Coin(platform20.x + 75, platform20.y - 40))
    coins.add(Coin(platform21.x + 100, platform21.y - 40))
    coins.add(Coin(platform22.x + 100, platform22.y - 40))
    coins.add(Coin(platform24.x + 100, platform24.y - 40))
    coins.add(Coin(platform26.x + 100, platform26.y - 40))
    coins.add(Coin(platform27.x + 125, platform27.y - 40))
    coins.add(Coin(platform28.x + 100, platform28.y - 40))
    coins.add(Coin(platform29.x + 75, platform29.y - 40))
    coins.add(Coin(platform30.x + 100, platform30.y - 40))
    coins.add(Coin(platform31.x + 100, platform31.y - 40))
    coins.add(Coin(platform32.x + 100, platform32.y - 40))
    coins.add(Coin(platform33.x + 100, platform33.y - 40))
    coins.add(Coin(platform34.x + 100, platform34.y - 40))
    coins.add(Coin(platform35.x + 100, platform35.y - 40))
    coins.add(Coin(platform36.x + 100, platform36.y - 40))
    coins.add(Coin(platform37.x + 75, platform37.y - 40))
    coins.add(Coin(platform38.x + 100, platform38.y - 40))
    coins.add(Coin(platform39.x + 100, platform39.y - 40))
    coins.add(Coin(platform40.x + 100, platform40.y - 40))
    coins.add(Coin(platform41.x + 100, platform41.y - 40))

    # High-risk coins above hazards
    for hazard in [hazard2, hazard4, hazard6, hazard8]:
        coins.add(Coin(hazard.x + 80, 310))

    # Gap crossing rewards
    coins.add(Coin(3750, 280))
    coins.add(Coin(7400, 280))
    coins.add(Coin(11400, 290))
    coins.add(Coin(14900, 260))

    # Victory path coins
    for x in range(16500, 17500, 200):
        coins.add(Coin(x, 280))

    # Staircase coins
    coins.add(Coin(stair1.x + 50, stair1.y - 40))
    coins.add(Coin(stair3.x + 50, stair3.y - 40))
    coins.add(Coin(stair5.x + 50, stair5.y - 40))
    coins.add(Coin(stair7.x + 50, stair7.y - 40))

    # ===================================================================
    # PROJECTILES GROUP
    # ===================================================================

    projectiles = pygame.sprite.Group()

    return bg_color, platforms, hazards, LEVEL_WIDTH, player, enemies, projectiles, coins, world_name, goal_npc, background_layers, moving_platforms, disappearing_platforms, appearing_platforms
