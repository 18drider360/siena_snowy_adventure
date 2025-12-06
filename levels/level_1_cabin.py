import pygame
from player.siena import Siena
from enemies.elkman import Elkman
from enemies.spiked_slime import SpikedSlime
from ui.coin import Coin
from ui.npc import LevelGoalNPC

LEVEL_WIDTH = 5300
LEVEL_HEIGHT = 600

def build_level(abilities=None):
    """
    Build Level 1-1: Cabin Base - Tutorial Level
    
    Designed following Mario 1-1 principles:
    - Teaches mechanics through level design, not text
    - Safe practice before dangerous challenges
    - Gradual difficulty curve
    - Strategic coin placement guides learning
    
    Args:
        abilities: Dict of unlocked abilities (from GameProgression)
    
    Returns:
      - background color (None for parallax)
      - list of platform rects for collision
      - list of hazard rects (death zones)
      - total level width (for scrolling)
      - player instance (Siena)
      - enemies sprite group
      - projectiles sprite group
      - coins sprite group
      - world name (for HUD display)
      - goal_npc (NPC at level end)
      - background_layers (list of image paths)
    """
    bg_color = None
    world_name = "1-1"
    
    # Background layers for mountain theme (parallax from back to front)
    background_layers = [
        "assets/images/backgrounds/mountains/5.png",
        "assets/images/backgrounds/mountains/4.png",
        "assets/images/backgrounds/mountains/3.png",
        "assets/images/backgrounds/mountains/2.png",
        "assets/images/backgrounds/mountains/1.png",
    ]

    # ===================================================================
    # CHAPTER 1: SAFE EXPLORATION (0-1000px)
    # Teaches: Basic movement, first enemy encounter, jumping basics
    # ===================================================================

    # First platforms - teach basic jumping (easy jumps)
    platform1 = pygame.Rect(600, 500, 100, 25)      # Low platform - easy reach
    platform2 = pygame.Rect(800, 450, 100, 25)      # Higher with better spacing
    block1 = pygame.Rect(950, 420, 50, 50)          # Mario-style block with coin
    
    # ===================================================================
    # CHAPTER 2: JUMP MASTERY (1000-2500px)
    # Teaches: Double-jump mechanic, platform chains, vertical jumping
    # ===================================================================

    # Double-jump introduction - coins mark the path
    platform3 = pygame.Rect(1400, 480, 120, 25)
    platform4 = pygame.Rect(1600, 420, 120, 25)     # Requires jump
    platform5 = pygame.Rect(1800, 360, 120, 25)     # Requires double-jump (coins guide)

    # Platform chain - practice consecutive jumps
    platform6 = pygame.Rect(2100, 480, 100, 25)
    platform7 = pygame.Rect(2250, 480, 100, 25)
    platform8 = pygame.Rect(2400, 480, 100, 25)
    
    # ===================================================================
    # CHAPTER 3: SAFE HAZARD INTRODUCTION (2500-3500px)
    # Teaches: Pit mechanics safely, elevated enemy encounters
    # ===================================================================

    # FIRST PIT - Safe with floor (non-lethal)
    hazard0 = pygame.Rect(2700, 530, 100, 30)  # Fire hazard (40px tall, smaller flames) - shortened to not overlap platforms

    # Platforms around safe pit
    platform9 = pygame.Rect(2550, 520, 150, 30)      # Before pit
    platform10 = pygame.Rect(2800, 520, 100, 30)     # After pit

    # Elevated area with enemies
    platform11 = pygame.Rect(3150, 450, 200, 30)
    block2 = pygame.Rect(3300, 398, 50, 50)          # Block above platform (2px gap)

    # ===================================================================
    # CHAPTER 4: REAL DANGER (3500-4500px)
    # Teaches: Lethal consequences, precision jumping, enemy + pit combo
    # ===================================================================

    # FIRST LETHAL PIT - Similar to safe pit but deadly
    hazard1 = pygame.Rect(3700, 530, 200, 30)  # Fire hazard (40px tall, smaller flames) - positioned between platforms

    # Platforms around lethal pit
    platform12 = pygame.Rect(3550, 520, 150, 30)     # Before pit
    platform13 = pygame.Rect(3950, 520, 150, 30)     # After pit - enemy on this

    # Challenge section - wider gap requiring running jump
    hazard2 = pygame.Rect(4300, 530, 300, 30)  # Fire hazard (40px tall, smaller flames) - shortened to not overlap platforms

    platform14 = pygame.Rect(4150, 450, 150, 30)     # Launch platform
    platform15 = pygame.Rect(4600, 500, 100, 30)     # Landing platform
    
    # ===================================================================
    # CHAPTER 5: VICTORY LAP (4500-5300px)
    # Teaches: Confidence, completion satisfaction
    # ===================================================================

    # Final staircase - ascending to victory
    stair1 = pygame.Rect(4800, 520, 80, 25)
    stair2 = pygame.Rect(4880, 470, 80, 25)
    stair3 = pygame.Rect(4960, 420, 80, 25)
    
    # ENDING: Goal platform where player lands after coin arc (large enough for both player and NPC)
    goal_platform = pygame.Rect(5180, 380, 120, 30)  # Where Siena and NPC stand
    
    
    # ===================================================================
    # COMPILE PLATFORMS AND HAZARDS
    # ===================================================================

    # INVISIBLE GROUND - spans entire level so enemies don't fall through
    invisible_ground = pygame.Rect(0, 570, LEVEL_WIDTH,  30)

    platforms = [
        invisible_ground,  # Full-width invisible ground (drawn first, will be hidden by SHOW_GROUND = False)
        # Removed redundant ground_1-8 segments that overlap with invisible_ground
        platform1, platform2, platform3, platform4, platform5, platform6, platform7,
        platform8, platform9, platform10, platform11, platform12, platform13, platform14,
        platform15, goal_platform,
        # Removed npc_platform as it overlaps with goal_platform
        block1, block2,
         # Safe pit has floor
        stair1, stair2, stair3
    ]

    hazards = [hazard0, hazard1, hazard2]  # Only 2 lethal pits

    # ===================================================================
    # PLAYER SETUP
    # ===================================================================
    
    if abilities is None:
        abilities = {
            'walk': True,
            'crouch': True,
            'jump': True,
            'double_jump': True,
            'roll': False,
            'spin': False
        }
    
    # Player spawn: Ground platform top is at Y=570
    # Working backwards from desired hitbox.bottom = 570:
    # - hitbox.bottom = 570
    # - hitbox height = 45, so hitbox.y = 525
    # - After -90 offset applied, hitbox.y should be 525, so before offset: hitbox.y = 615
    # - hitbox.bottom before offset = 615 + 45 = 660 = rect.bottom
    # So spawn at Y=660
    player = Siena(120, 660, abilities=abilities, max_health=6)  # 3 hearts (6 lives)

    # ===================================================================
    # ENEMY PLACEMENT - Strategic and Educational
    # Total: 12 enemies (following Mario 1-1 density)
    # ===================================================================
    
    enemies = pygame.sprite.Group()
    projectiles = pygame.sprite.Group()
    
    # CHAPTER 1: First enemy - The "tutorial death" at 500px
    elkman1 = Elkman(x=500, y=575, patrol_left=400, patrol_right=600)
    enemies.add(elkman1)
    
    # CHAPTER 2: Enemies while learning jumps
    elkman2 = Elkman(x=1300, y=575, patrol_left=1200, patrol_right=1400)
    enemies.add(elkman2)
    
    # Enemy on elevated platform (teaches aerial combat)
    elkman3 = Elkman(x=1650, y=425, patrol_left=1600, patrol_right=1700)
    enemies.add(elkman3)
    
    # CHAPTER 2-3: Ground enemies in safe area
    slime0 = SpikedSlime(x=2150, y=575, patrol_left=3450, patrol_right=3650)
    enemies.add(slime0)
    
    
    # CHAPTER 3: Elevated platform enemy
    elkman6 = Elkman(x=3250, y=455, patrol_left=3150, patrol_right=3350)
    enemies.add(elkman6)
    
    # CHAPTER 4: NEW ENEMY TYPE - Introduce Slime (different behavior)
    slime1 = SpikedSlime(x=3550, y=575, patrol_left=3450, patrol_right=3650)
    enemies.add(slime1)
    
    # Enemy on platform after first lethal pit (high stakes!)
    slime2 = SpikedSlime(x=3950, y=525, patrol_left=3900, patrol_right=4000)
    enemies.add(slime2)
    
    # Enemies before wide pit
    elkman7 = Elkman(x=4100, y=575, patrol_left=4050, patrol_right=4200)
    enemies.add(elkman7)
    
    # Enemy on landing platform after wide pit
    slime3 = SpikedSlime(x=4650, y=505, patrol_left=4550, patrol_right=4700)
    enemies.add(slime3)
    

    # ===================================================================
    # COIN PLACEMENT - Teaching and Guiding
    # Total: ~50 coins (Mario 1-1 has 60-70)
    # ===================================================================
    
    coins = pygame.sprite.Group()
    
    # CHAPTER 1: First coins - ground level (safe collection)
    for i in range(2):
        coins.add(Coin(250 + i * 60, 530))
    
    # Coin above first platform (teaches jumping for rewards)
    coins.add(Coin(650, 460))
    
    # Coin in block (teaches block hitting) - FIXED: Y=385 to clear platform at Y=420
    coins.add(Coin(975, 385))
    
    # CHAPTER 2: Coins teaching double-jump
    # Horizontal line leading to elevated platforms
    for i in range(2):
        coins.add(Coin(1350 + i * 60, 530))
    
    # Coins on platforms
    coins.add(Coin(1450, 440))
    coins.add(Coin(1650, 380))
    
    # VERTICAL ARC - Teaches double-jump trajectory (IMPORTANT!)
    coins.add(Coin(1780, 360))  # Peak - requires double-jump
    coins.add(Coin(1810, 320))
    
    # Coin trail across platform chain
    coins.add(Coin(2150, 440))
    coins.add(Coin(2450, 440))
    
    # CHAPTER 3: Coins around safe pit (teaching trajectory)
    # COIN ARC ABOVE SAFE PIT - Shows jump path
    coins.add(Coin(2720, 460))
    coins.add(Coin(2790, 460))
    
    # Coins on elevated platform with enemy
    coins.add(Coin(3237, 410))
    
    # Coin in elevated block
    coins.add(Coin(3325, 360))
    
    # CHAPTER 4: Fewer coins, higher stakes
    # Coins before first lethal pit - FIXED: Y=485 to clear platform20 at Y=520
    coins.add(Coin(3500, 530))
    coins.add(Coin(3570, 485))

    # COIN ARC ABOVE LETHAL PIT (same pattern as safe pit)
    coins.add(Coin(3650, 480))
    coins.add(Coin(3720, 460))
    coins.add(Coin(3790, 460))
    coins.add(Coin(3860, 480))

    # Coin on platform with enemy (risk/reward)
    coins.add(Coin(3975, 480))

    # Coins before wide pit - FIXED: Y=485 to clear platform21 at Y=520
    for i in range(2):
        coins.add(Coin(4050 + i * 70, 485))

    # COIN TRAIL ACROSS WIDE GAP - Shows it's possible - FIXED: Y=415 to clear platform22 at Y=450
    coins.add(Coin(4300, 415))
    coins.add(Coin(4470, 470))
    
    # CHAPTER 5: Victory coins - generous reward
    # Coins on stairs
    coins.add(Coin(4840, 480))
    coins.add(Coin(4920, 430))
    coins.add(Coin(4985, 380))

    # ===================================================================
    # LEVEL GOAL NPC
    # ===================================================================
    
    goal_npc = LevelGoalNPC(x=5260, y=320)  # Standing on npc_platform

    return bg_color, platforms, hazards, LEVEL_WIDTH, player, enemies, projectiles, coins, world_name, goal_npc, background_layers