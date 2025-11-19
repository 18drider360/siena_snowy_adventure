import pygame
from player.siena import Siena
from enemies.elkman import Elkman
from enemies.spiked_slime import SpikedSlime
from ui.coin import Coin

LEVEL_WIDTH = 20000
LEVEL_HEIGHT = 600

def build_level():
    """
    Returns:
      - background color (None for parallax)
      - list of platform rects for collision
      - list of hazard rects (death zones)
      - total level width (for scrolling)
      - player instance (Siena)
      - enemies sprite group
      - projectiles sprite group (snowballs + iceballs)
      - coins sprite group
      - world name (for HUD display)
    """
    bg_color = None  # No background color, using parallax
    world_name = "1-1"  # Level identifier

    # --- PLATFORMS ---
    # Split ground into segments to create gaps for hazards
    ground_segments = [
        pygame.Rect(0, 570, 800, 40),           # Before hazard1
        pygame.Rect(1000, 570, 800, 40),        # After hazard1, before hazard2
        pygame.Rect(1950, 570, 1400, 40),       # After hazard2, before hazard3
        pygame.Rect(3530, 570, 1370, 40),       # After hazard3, before hazard4
        pygame.Rect(5100, 570, 1400, 40),       # After hazard4, before hazard5
        pygame.Rect(6750, 570, 1900, 40),       # After hazard5, before hazard6
        pygame.Rect(8830, 570, 1470, 40),       # After hazard6, before hazard7
        pygame.Rect(10500, 570, 2050, 40),      # After hazard7, before hazard8
        pygame.Rect(12730, 570, 1370, 40),      # After hazard8, before hazard9
        pygame.Rect(14320, 570, 1230, 40),      # After hazard9, before hazard10
        pygame.Rect(15700, 570, 1400, 40),      # After hazard10, before hazard11
        pygame.Rect(17300, 570, 2700, 40),      # After hazard11 to end
    ]
    
    # --- SINGLE BLOCK PLATFORMS (50x50 like Mario blocks) ---
    block1 = pygame.Rect(250, 500, 50, 50)
    block2 = pygame.Rect(550, 480, 50, 50)
    block3 = pygame.Rect(1000, 450, 50, 50)
    block4 = pygame.Rect(1300, 420, 50, 50)
    block5 = pygame.Rect(2500, 480, 50, 50)
    block6 = pygame.Rect(2700, 440, 50, 50)
    block7 = pygame.Rect(4200, 460, 50, 50)
    block8 = pygame.Rect(4400, 420, 50, 50)
    block9 = pygame.Rect(6650, 470, 50, 50)
    block10 = pygame.Rect(7100, 450, 50, 50)
    block11 = pygame.Rect(8800, 480, 50, 50)
    block12 = pygame.Rect(10500, 490, 50, 50)
    block13 = pygame.Rect(12000, 450, 50, 50)
    block14 = pygame.Rect(14500, 460, 50, 50)
    block15 = pygame.Rect(16400, 480, 50, 50)
    
    # Starting area - Tutorial section
    platform1 = pygame.Rect(400, 480, 150, 25)
    platform2 = pygame.Rect(650, 420, 150, 25)
    platform3 = pygame.Rect(900, 360, 150, 25)
    platform4 = pygame.Rect(1150, 300, 200, 25)
    
    # First gap with platforms
    platform5 = pygame.Rect(1450, 400, 120, 25)
    platform6 = pygame.Rect(1650, 450, 120, 25)
    
    # Elevated platform area
    platform7 = pygame.Rect(1900, 380, 250, 30)
    platform8 = pygame.Rect(2250, 380, 180, 30)
    platform9 = pygame.Rect(2150, 280, 150, 25)
    
    # Staircase section
    stair1 = pygame.Rect(2600, 520, 100, 25)
    stair2 = pygame.Rect(2750, 470, 100, 25)
    stair3 = pygame.Rect(2900, 420, 100, 25)
    stair4 = pygame.Rect(3050, 370, 100, 25)
    stair5 = pygame.Rect(3200, 320, 100, 25)
    
    # High platform section
    platform10 = pygame.Rect(3400, 320, 300, 30)
    platform11 = pygame.Rect(3800, 380, 150, 25)
    platform12 = pygame.Rect(4050, 320, 150, 25)
    
    # Gap jump section
    platform13 = pygame.Rect(4350, 400, 120, 25)
    platform14 = pygame.Rect(4550, 400, 120, 25)
    platform15 = pygame.Rect(4750, 400, 120, 25)
    
    # Descending section
    platform16 = pygame.Rect(5000, 350, 150, 25)
    platform17 = pygame.Rect(5250, 400, 150, 25)
    platform18 = pygame.Rect(5500, 450, 150, 25)
    platform19 = pygame.Rect(5750, 500, 200, 25)
    
    # Mid-level flat area with elevated platforms
    platform20 = pygame.Rect(6100, 520, 400, 30)
    platform21 = pygame.Rect(6200, 400, 150, 25)
    platform22 = pygame.Rect(6450, 350, 150, 25)
    
    # Zigzag section
    platform23 = pygame.Rect(6800, 480, 120, 25)
    platform24 = pygame.Rect(7000, 420, 120, 25)
    platform25 = pygame.Rect(7200, 360, 120, 25)
    platform26 = pygame.Rect(7400, 300, 120, 25)
    platform27 = pygame.Rect(7600, 360, 120, 25)
    platform28 = pygame.Rect(7800, 420, 120, 25)
    
    # Large platform area
    platform29 = pygame.Rect(8100, 450, 500, 30)
    platform30 = pygame.Rect(8300, 350, 150, 25)
    platform31 = pygame.Rect(8550, 300, 150, 25)
    
    # Challenge section - tight jumps
    platform32 = pygame.Rect(8850, 400, 100, 25)
    platform33 = pygame.Rect(9020, 380, 100, 25)
    platform34 = pygame.Rect(9190, 360, 100, 25)
    platform35 = pygame.Rect(9360, 340, 100, 25)
    platform36 = pygame.Rect(9530, 380, 100, 25)
    platform37 = pygame.Rect(9700, 420, 100, 25)
    
    # Recovery area
    platform38 = pygame.Rect(9950, 480, 300, 30)
    
    # Ascending tower section
    tower1 = pygame.Rect(10400, 520, 150, 25)
    tower2 = pygame.Rect(10600, 460, 150, 25)
    tower3 = pygame.Rect(10800, 400, 150, 25)
    tower4 = pygame.Rect(11000, 340, 150, 25)
    tower5 = pygame.Rect(11200, 280, 150, 25)
    tower6 = pygame.Rect(11400, 340, 150, 25)
    tower7 = pygame.Rect(11600, 400, 150, 25)
    
    # Long platform bridge
    platform39 = pygame.Rect(11900, 380, 600, 30)
    platform40 = pygame.Rect(12100, 280, 150, 25)
    platform41 = pygame.Rect(12350, 280, 150, 25)
    
    # Drop down section with catches
    platform42 = pygame.Rect(12700, 320, 120, 25)
    platform43 = pygame.Rect(12900, 380, 120, 25)
    platform44 = pygame.Rect(13100, 440, 120, 25)
    platform45 = pygame.Rect(13300, 500, 120, 25)
    
    # Wide platform area
    platform46 = pygame.Rect(13600, 480, 500, 30)
    platform47 = pygame.Rect(13750, 360, 200, 25)
    
    # Floating island section
    island1 = pygame.Rect(14300, 420, 180, 30)
    island2 = pygame.Rect(14550, 380, 180, 30)
    island3 = pygame.Rect(14800, 340, 180, 30)
    island4 = pygame.Rect(15050, 380, 180, 30)
    island5 = pygame.Rect(15300, 420, 180, 30)
    
    # Final approach - pyramid
    pyramid1 = pygame.Rect(15650, 520, 150, 25)
    pyramid2 = pygame.Rect(15800, 470, 150, 25)
    pyramid3 = pygame.Rect(15950, 420, 150, 25)
    pyramid4 = pygame.Rect(16100, 370, 150, 25)
    pyramid5 = pygame.Rect(16250, 320, 150, 25)
    pyramid6 = pygame.Rect(16100, 370, 150, 25)
    pyramid7 = pygame.Rect(15950, 420, 150, 25)
    pyramid8 = pygame.Rect(15800, 470, 150, 25)
    
    # Final stretch platforms
    platform48 = pygame.Rect(16600, 450, 200, 30)
    platform49 = pygame.Rect(16900, 400, 200, 30)
    platform50 = pygame.Rect(17200, 350, 200, 30)
    platform51 = pygame.Rect(17500, 400, 200, 30)
    platform52 = pygame.Rect(17800, 450, 200, 30)
    
    # Victory platform
    platform53 = pygame.Rect(18200, 380, 400, 40)
    
    # Bonus high platforms
    bonus1 = pygame.Rect(18400, 250, 150, 25)
    
    # Final landing area
    platform54 = pygame.Rect(18800, 520, 1200, 30)
    
    # --- DEATH/HAZARD PLATFORMS (red - instant death) ---
    # These are now pits in the ground (no platform underneath)
    hazard1 = pygame.Rect(800, 570, 200, 40)    # Gap in ground
    hazard2 = pygame.Rect(1800, 570, 150, 40)   # Gap in ground
    hazard3 = pygame.Rect(3350, 570, 180, 40)   # Gap in ground
    hazard4 = pygame.Rect(4900, 570, 200, 40)   # Gap in ground
    hazard5 = pygame.Rect(6500, 570, 250, 40)   # Gap in ground
    hazard6 = pygame.Rect(8650, 570, 180, 40)   # Gap in ground
    hazard7 = pygame.Rect(10300, 570, 200, 40)  # Gap in ground
    hazard8 = pygame.Rect(12550, 570, 180, 40)  # Gap in ground
    hazard9 = pygame.Rect(14100, 570, 220, 40)  # Gap in ground
    hazard10 = pygame.Rect(15550, 570, 150, 40) # Gap in ground
    hazard11 = pygame.Rect(17100, 570, 200, 40) # Gap in ground
    
    platforms = ground_segments + [
        # Single blocks
        block1, block2, block3, block4, block5, block6, block7, block8,
        block9, block10, block11, block12, block13, block14, block15,
        # Regular platforms
        platform1, platform2, platform3, platform4, platform5, platform6,
        platform7, platform8, platform9, platform10, platform11, platform12,
        platform13, platform14, platform15, platform16, platform17, platform18,
        platform19, platform20, platform21, platform22, platform23, platform24,
        platform25, platform26, platform27, platform28, platform29, platform30,
        platform31, platform32, platform33, platform34, platform35, platform36,
        platform37, platform38, platform39, platform40, platform41, platform42,
        platform43, platform44, platform45, platform46, platform47, platform48,
        platform49, platform50, platform51, platform52, platform53, platform54,
        stair1, stair2, stair3, stair4, stair5,
        tower1, tower2, tower3, tower4, tower5, tower6, tower7,
        island1, island2, island3, island4, island5,
        pyramid1, pyramid2, pyramid3, pyramid4, pyramid5, pyramid6, pyramid7, pyramid8,
        bonus1
    ]

    hazards = [hazard1, hazard2, hazard3, hazard4, hazard5, hazard6, hazard7, hazard8, hazard9, hazard10, hazard11]

    # --- PLAYER SETUP WITH ABILITIES ---
    # Level 1: Only basic abilities unlocked
    level_1_abilities = {
        'walk': True,
        'crouch': True,
        'jump': True,
        'double_jump': True,
        'roll': False,      # Locked for level 1
        'spin': False       # Locked for level 1
    }
    
    player = Siena(120, 569, abilities=level_1_abilities)

    # --- ENEMY SETUP ---
    enemies = pygame.sprite.Group()
    projectiles = pygame.sprite.Group()  # Combined group for all projectiles
    
    # Starting area enemies
    elkman1 = Elkman(x=400, y=575, patrol_left=200, patrol_right=700)
    enemies.add(elkman1)
    
    # Elevated platform enemies
    elkman2 = Elkman(x=2000, y=385, patrol_left=1900, patrol_right=2150)
    enemies.add(elkman2)
    
    slime1 = SpikedSlime(x=3500, y=325, patrol_left=3400, patrol_right=3700)
    enemies.add(slime1)
    
    # Mid section enemies
    elkman3 = Elkman(x=6300, y=525, patrol_left=6100, patrol_right=6500)
    enemies.add(elkman3)
    
    slime2 = SpikedSlime(x=8300, y=455, patrol_left=8100, patrol_right=8600)
    enemies.add(slime2)
    
    # Tower section enemy
    elkman4 = Elkman(x=11000, y=345, patrol_left=11000, patrol_right=11150)
    enemies.add(elkman4)
    
    # Bridge section
    slime3 = SpikedSlime(x=12200, y=385, patrol_left=11900, patrol_right=12500)
    enemies.add(slime3)
    
    # Wide platform enemy
    elkman5 = Elkman(x=13800, y=485, patrol_left=13600, patrol_right=14100)
    enemies.add(elkman5)
    
    # Floating islands
    slime4 = SpikedSlime(x=14800, y=345, patrol_left=14800, patrol_right=14980)
    enemies.add(slime4)
    
    # Final stretch
    elkman6 = Elkman(x=17000, y=405, patrol_left=16900, patrol_right=17100)
    enemies.add(elkman6)
    
    slime5 = SpikedSlime(x=18300, y=385, patrol_left=18200, patrol_right=18600)
    enemies.add(slime5)

    # --- COIN SETUP ---
    coins = pygame.sprite.Group()
    
    # Starting area coins - Ground level
    for i in range(5):
        coins.add(Coin(200 + i * 80, 530))
    
    # Tutorial platforms - Coins above each platform
    coins.add(Coin(475, 440))
    coins.add(Coin(725, 380))
    coins.add(Coin(975, 320))
    coins.add(Coin(1225, 260))
    
    # Coins on blocks
    coins.add(Coin(275, 460))
    coins.add(Coin(575, 440))
    coins.add(Coin(1025, 410))
    coins.add(Coin(1325, 380))
    
    # Elevated platform trail
    for i in range(3):
        coins.add(Coin(1975 + i * 60, 340))
    coins.add(Coin(2325, 340))
    
    # Bonus coin above platform9
    coins.add(Coin(2225, 240))
    
    # Staircase coins
    coins.add(Coin(2650, 480))
    coins.add(Coin(2800, 430))
    coins.add(Coin(2950, 380))
    coins.add(Coin(3100, 330))
    coins.add(Coin(3250, 280))
    
    # High platform section
    for i in range(4):
        coins.add(Coin(3475 + i * 70, 280))
    
    # Coins on more blocks
    coins.add(Coin(2525, 440))
    coins.add(Coin(2725, 400))
    coins.add(Coin(4225, 420))
    coins.add(Coin(4425, 380))
    
    # Gap jump section - coins between platforms
    coins.add(Coin(4410, 360))
    coins.add(Coin(4610, 360))
    coins.add(Coin(4810, 360))
    
    # Descending section coins
    coins.add(Coin(5075, 310))
    coins.add(Coin(5325, 360))
    coins.add(Coin(5575, 410))
    coins.add(Coin(5825, 460))
    
    # Mid-level flat area
    for i in range(5):
        coins.add(Coin(6150 + i * 70, 480))
    
    # Elevated coins above mid-level
    coins.add(Coin(6275, 360))
    coins.add(Coin(6525, 310))
    
    # Coins on blocks
    coins.add(Coin(6675, 430))
    coins.add(Coin(7125, 410))
    
    # Zigzag section - coin trail
    coins.add(Coin(6860, 440))
    coins.add(Coin(7060, 380))
    coins.add(Coin(7260, 320))
    coins.add(Coin(7460, 260))
    coins.add(Coin(7660, 320))
    coins.add(Coin(7860, 380))
    
    # Large platform area
    for i in range(6):
        coins.add(Coin(8150 + i * 80, 410))
    coins.add(Coin(8375, 310))
    coins.add(Coin(8625, 260))
    
    # Coin on block
    coins.add(Coin(8825, 440))
    
    # Challenge section - tight jumps (reward coins)
    coins.add(Coin(8910, 360))
    coins.add(Coin(9080, 340))
    coins.add(Coin(9250, 320))
    coins.add(Coin(9420, 300))
    coins.add(Coin(9590, 340))
    coins.add(Coin(9760, 380))
    
    # Recovery area coins
    for i in range(3):
        coins.add(Coin(10025 + i * 70, 440))
    
    # Tower section - coins at each level
    coins.add(Coin(10475, 480))
    coins.add(Coin(10675, 420))
    coins.add(Coin(10875, 360))
    coins.add(Coin(11075, 300))
    coins.add(Coin(11275, 240))
    coins.add(Coin(11475, 300))
    coins.add(Coin(11675, 360))
    
    # Coin on block
    coins.add(Coin(10525, 450))
    
    # Bridge section coins
    for i in range(6):
        coins.add(Coin(12000 + i * 80, 340))
    
    # Bonus coins above bridge
    coins.add(Coin(12175, 240))
    coins.add(Coin(12425, 240))
    
    # Coin on block
    coins.add(Coin(12025, 410))
    
    # Drop down section
    coins.add(Coin(12760, 280))
    coins.add(Coin(12960, 340))
    coins.add(Coin(13160, 400))
    coins.add(Coin(13360, 460))
    
    # Wide platform area
    for i in range(5):
        coins.add(Coin(13650 + i * 90, 440))
    coins.add(Coin(13825, 320))
    
    # Coin on block
    coins.add(Coin(14525, 420))
    
    # Floating islands - coins on each island
    coins.add(Coin(14390, 380))
    coins.add(Coin(14640, 340))
    coins.add(Coin(14890, 300))
    coins.add(Coin(15140, 340))
    coins.add(Coin(15390, 380))
    
    # Pyramid section - coins going up and down
    coins.add(Coin(15725, 480))
    coins.add(Coin(15875, 430))
    coins.add(Coin(16025, 380))
    coins.add(Coin(16175, 330))
    coins.add(Coin(16325, 280))
    
    # Coin on block
    coins.add(Coin(16425, 440))
    
    # Final stretch coins
    coins.add(Coin(16675, 410))
    coins.add(Coin(16975, 360))
    coins.add(Coin(17275, 310))
    coins.add(Coin(17575, 360))
    coins.add(Coin(17875, 410))
    
    # Victory platform - coin collection
    for i in range(5):
        coins.add(Coin(18250 + i * 70, 340))
    
    # Bonus high coin
    coins.add(Coin(18475, 210))
    
    # Final area coins
    for i in range(8):
        coins.add(Coin(18900 + i * 100, 480))

    return bg_color, platforms, hazards, LEVEL_WIDTH, player, enemies, projectiles, coins, world_name