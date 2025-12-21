import pygame
from src.entities.player.siena import Siena
from src.entities.enemies.swordsman import Swordsman
from src.entities.enemies.frost_golem import FrostGolem
from src.ui.coin import Coin
from src.ui.npc import LevelGoalNPC

LEVEL_WIDTH = 9000  # Extended from 7500
LEVEL_HEIGHT = 600

def build_level(abilities=None):
    """
    Build Level 1-2: Ski Lift Area - Roll Mechanic Tutorial
    
    DESIGN PHILOSOPHY:
    - Teach roll through INESCAPABLE GEOMETRY (low ceilings force rolling)
    - Sequential enemy introduction: Swordsman first, then Frost Golem
    - 25% difficulty increase from Level 1
    - Ground at Y=400 (continuous invisible safety net)
    
    ROLL TEACHING PATTERN:
    1. Safe low ceiling with no enemies (800-1000px)
    2. Low ceiling + single weak enemy (1200px) 
    3. Wide gaps requiring roll-jump (1500-2000px)
    4. Enemy lines making roll efficient (2500px)
    
    ENEMY BREAKDOWN (12 total - reduced for better pacing):
    - 5 Swordsmen (melee, track player)
    - 7 Frost Golems (ranged, bouncing fireballs)
    
    Args:
        abilities: Dict of unlocked abilities (should include 'roll': True)
    
    Returns:
        bg_color, platforms, hazards, level_width, player, enemies, 
        projectiles, coins, world_name, goal_npc, background_layers
    """
    bg_color = None
    world_name = "1-2"
    
    # Background layers for snow cabin theme (parallax from back to front)
    background_layers = [
        "assets/images/backgrounds/snow_cabin/layers/l1-background.png",
        "assets/images/backgrounds/snow_cabin/layers/l2-mountains01.png",
        "assets/images/backgrounds/snow_cabin/layers/l3-clouds.png",
        "assets/images/backgrounds/snow_cabin/layers/l4-forest.png",
        "assets/images/backgrounds/snow_cabin/layers/l5-houses.png",
        "assets/images/backgrounds/snow_cabin/layers/l6-ground.png",
    ]
    
    # ===================================================================
    # GROUND - Segments with GAPS for roll-jump challenges
    # ===================================================================
    ground_1 = pygame.Rect(0, 400, 1400, 30)           # Start area
    # GAP 1: 1400-1700 (300px - roll-jump required)
    ground_2 = pygame.Rect(1700, 400, 1000, 30)        # Mid section
    # GAP 2: 2700-3100 (400px - longer roll-jump)
    ground_3 = pygame.Rect(3100, 400, 1400, 30)        # Middle section
    # GAP 3: 4500-4850 (350px - medium gap)
    ground_4 = pygame.Rect(4850, 400, 1400, 30)        # Another middle section
    # GAP 4: 6250-6600 (350px - another gap)
    ground_5 = pygame.Rect(6600, 400, 1100, 30)        # Late section
    # GAP 5: 7700-8000 (300px - final gap challenge)
    ground_6 = pygame.Rect(8510, 400, 490, 30)         # End section to goal (10px gap from platform25)
    
    # ===================================================================
    # BEAT 1: ROLL TUTORIAL ZONE (0-1,500px)
    # Goal: Teach roll mechanic safely through geometry
    # ===================================================================
    
    # First low ceiling at 1000px - FORCES crouch/roll discovery
    # Ceiling at Y=315 (85px above ground) - just below standing height
    low_ceiling_1 = pygame.Rect(800, 330, 350, 30)
    
    # ===================================================================
    # BEAT 2: ROLL APPLICATION (1,500-2,800px)
    # Goal: Require roll in real challenges
    # ===================================================================
    
    # Wide gap requiring roll-jump
    platform2 = pygame.Rect(1600, 350, 180, 25)
    platform3 = pygame.Rect(1950, 350, 180, 25)  # 170px gap needs roll
    
    # Low ceiling section with narrow platforms
    low_ceiling_2 = pygame.Rect(2200, 285, 500, 30)
    platform4 = pygame.Rect(2250, 365, 100, 25)
    platform5 = pygame.Rect(2450, 365, 100, 25)
    platform6 = pygame.Rect(2650, 365, 100, 25)  # Enemy line spans these 3
    
    # Checkpoint
    checkpoint1 = pygame.Rect(2900, 350, 180, 25)
    
    # ===================================================================
    # BEAT 3: SWORDSMAN MASTERY (2,800-4,000px)
    # Goal: Learn melee combat on varied terrain
    # ===================================================================
    
    # Elevated platform section
    platform7 = pygame.Rect(3200, 280, 200, 25)
    platform8 = pygame.Rect(3550, 220, 200, 25)
    
    # Return to ground with low ceiling combat
    low_ceiling_3 = pygame.Rect(3900, 295, 450, 30)
    platform9 = pygame.Rect(3950, 365, 350, 25)
    
    # ===================================================================
    # BEAT 4: FROST GOLEM INTRODUCTION (4,000-5,200px)
    # Goal: Learn ranged enemy patterns
    # ===================================================================

    # High platform for FIRST Golem - visible from far away
    platform10 = pygame.Rect(4200, 185, 250, 25)

    # Approach platforms - dodging fireballs
    platform11 = pygame.Rect(4550, 300, 150, 25)
    # Removed platform12 - overlaps with platform_tunnel_1

    # NEW: Frost Tunnel - Long forced roll section under hazards
    hazard_ceiling_1 = pygame.Rect(4600, 200, 430, 25)  # Low ceiling forces roll (165px clearance from platform below) - Extended to 5030 to match hazard_ceiling_1c
    platform_tunnel_1 = pygame.Rect(4600, 365, 430, 25)  # Platform underneath entire tunnel

    # Checkpoint
    checkpoint2 = pygame.Rect(5100, 350, 180, 25)

    # ===================================================================
    # BEAT 5: MIXED CHALLENGES (5,200-6,400px)
    # Goal: Combine both enemy types
    # ===================================================================

    # Removed platform13 and platform14 - overlap with tunnel platforms below

    # NEW: Double Hazard Squeeze - Two consecutive low ceilings
    hazard_ceiling_2a = pygame.Rect(5500, 205, 150, 25)  # First squeeze section (160px clearance)
    platform_tunnel_2a = pygame.Rect(5500, 365, 150, 25)  # Platform under first squeeze
    hazard_ceiling_2b = pygame.Rect(5700, 200, 150, 25)  # Second squeeze section (tighter! 165px clearance)
    platform_tunnel_2b = pygame.Rect(5700, 365, 150, 25)  # Platform under second squeeze

    # Narrow platform gauntlet
    platform15 = pygame.Rect(5860, 340, 100, 25)  # Added 60px gap from platform_tunnel_2b
    platform16 = pygame.Rect(6000, 290, 100, 25)
    platform17 = pygame.Rect(6200, 340, 100, 25)

    # ===================================================================
    # BEAT 6: CLIMAX (6,400-7,000px)
    # Goal: Peak difficulty test
    # ===================================================================

    # Removed checkpoint3 - overlaps with platform_tunnel_3

    # NEW: Climax Crawl - Longest forced roll section with dual enemy fire
    hazard_ceiling_3 = pygame.Rect(6500, 200, 470, 25)  # Longest ceiling (165px clearance from platform) - Extended to 6970 to match hazard_new_3d
    platform_tunnel_3 = pygame.Rect(6500, 365, 470, 25)  # Platform underneath entire tunnel

    # Multi-level boss arena
    # Removed platform18 - overlaps with platform_tunnel_3
    platform19 = pygame.Rect(6550, 230, 150, 25)  # High level
    platform20 = pygame.Rect(6800, 300, 150, 25)  # Mid level

    # ===================================================================
    # BEAT 7: EXTENDED SECTION (7,500-8,500px)
    # More roll practice with platforms
    # ===================================================================

    # NEW: Narrow Passage - Medium roll tunnel with swordsman ambush at exit
    hazard_ceiling_4 = pygame.Rect(7100, 205, 330, 25)  # Forces roll before enemy encounter (160px clearance) - Extended to 7430 to match hazard_new_4c
    platform_tunnel_4 = pygame.Rect(7100, 365, 330, 25)  # Platform underneath tunnel

    # Additional platforms for extended section
    # Removed platform21 - overlaps with platform_tunnel_4
    platform22 = pygame.Rect(7600, 300, 150, 25)

    # Bridge to victory section (fill the gap)
    platform23 = pygame.Rect(7850, 350, 150, 25)
    platform24 = pygame.Rect(8100, 330, 150, 25)
    platform25 = pygame.Rect(8350, 380, 150, 25)

    # ===================================================================
    # BEAT 8: RESOLUTION (8,500-9,000px)
    # Goal: Victory lap
    # ===================================================================

    # Staircase to summit
    stair1 = pygame.Rect(8550, 360, 120, 25)
    stair2 = pygame.Rect(8670, 305, 120, 25)
    stair3 = pygame.Rect(8790, 250, 120, 25)

    # Goal area
    goal_platform = pygame.Rect(8920, 200, 80, 25)
    
    # ===================================================================
    # HAZARDS - Ceiling hazards force rolling
    # ===================================================================

    # NEW: Hazards on ceiling platforms (visual danger above forcing player to stay low)
    # Ceilings at Y=200-205, hazards sit on top at Y=170-175
    # This creates visual danger above the tunnel forcing players to roll/crouch

    # Beat 4 - Frost Tunnel hazards (on top of ceiling platform at Y=200)
    # Inset by 10px: 4630+10=4640, 100-20=80
    hazard_ceiling_1a = pygame.Rect(4640, 170, 80, 30)
    # Inset by 10px: 4780+10=4790, 100-20=80
    hazard_ceiling_1b = pygame.Rect(4790, 170, 80, 30)
    # Inset by 10px: 4930+10=4940, 90-20=70
    hazard_ceiling_1c = pygame.Rect(4940, 170, 70, 30)

    # Beat 5 - Double Squeeze hazards (on top of ceiling platforms)
    # Inset by 10px: 5520+10=5530, 80-20=60
    hazard_ceiling_2a_top = pygame.Rect(5530, 170, 60, 30)
    # Inset by 10px: 5720+10=5730, 80-20=60
    hazard_ceiling_2b_top = pygame.Rect(5730, 170, 60, 30)

    # Beat 6 - Climax Crawl hazards (on top of ceiling platform at Y=200)
    # Inset by 10px: 6530+10=6540, 80-20=60
    hazard_ceiling_3a = pygame.Rect(6540, 170, 60, 30)
    # Inset by 10px: 6650+10=6660, 80-20=60
    hazard_ceiling_3b = pygame.Rect(6660, 170, 60, 30)
    # Inset by 10px: 6770+10=6780, 80-20=60
    hazard_ceiling_3c = pygame.Rect(6780, 170, 60, 30)
    # Inset by 10px: 6890+10=6900, 80-20=60
    hazard_ceiling_3d = pygame.Rect(6900, 170, 60, 30)

    # Beat 7 - Narrow Passage hazards (on top of ceiling platform at Y=205)
    # Inset by 10px: 7130+10=7140, 80-20=60
    hazard_ceiling_4a = pygame.Rect(7140, 175, 60, 30)
    # Inset by 10px: 7240+10=7250, 80-20=60
    hazard_ceiling_4b = pygame.Rect(7250, 175, 60, 30)
    # Inset by 10px: 7350+10=7360, 70-20=50
    hazard_ceiling_4c = pygame.Rect(7360, 175, 50, 30)

    # Beat 8 - Final challenge hazard on ground (before victory stairs)
    # Inset by 10px: 8360+10=8370, 120-20=100
    hazard_final = pygame.Rect(8370, 350, 100, 30)
    
    # ===================================================================
    # COMPILE PLATFORMS
    # ===================================================================
    
    platforms = [
        ground_1, ground_2, ground_3, ground_4, ground_5, ground_6,  # Ground segments with gaps
        low_ceiling_1,
        platform2, platform3,
        low_ceiling_2, platform4, platform5, platform6,
        checkpoint1,
        platform7, platform8,
        low_ceiling_3, platform9,
        platform10, platform11,
        # Removed platform12 - overlaps with platform_tunnel_1
        hazard_ceiling_1, platform_tunnel_1,  # NEW: Beat 4 - Frost Tunnel (ceiling + platform below)
        checkpoint2,
        # Removed platform13, platform14 - overlap with tunnel platforms
        hazard_ceiling_2a, platform_tunnel_2a,  # NEW: Beat 5 - Double Squeeze (ceiling + platform)
        hazard_ceiling_2b, platform_tunnel_2b,  # NEW: Beat 5 - Double Squeeze (ceiling + platform)
        platform15, platform16, platform17,
        # Removed checkpoint3 - overlaps with platform_tunnel_3
        hazard_ceiling_3, platform_tunnel_3,  # NEW: Beat 6 - Climax Crawl (ceiling + platform)
        # Removed platform18 - overlaps with platform_tunnel_3
        platform19, platform20,
        hazard_ceiling_4, platform_tunnel_4,  # NEW: Beat 7 - Narrow Passage (ceiling + platform)
        # Removed platform21 - overlaps with platform_tunnel_4
        platform22,  # Extended section platforms
        platform23, platform24, platform25,  # Bridge to victory section
        stair1, stair2, stair3,
        goal_platform
    ]
    
    hazards = [
        # Ceiling hazards (on top of low ceiling platforms - force rolling)
        hazard_ceiling_1a, hazard_ceiling_1b, hazard_ceiling_1c,  # Frost Tunnel
        hazard_ceiling_2a_top, hazard_ceiling_2b_top,  # Double Squeeze
        hazard_ceiling_3a, hazard_ceiling_3b, hazard_ceiling_3c, hazard_ceiling_3d,  # Climax Crawl
        hazard_ceiling_4a, hazard_ceiling_4b, hazard_ceiling_4c,  # Narrow Passage
        hazard_final  # Final ground hazard before victory
    ]
    
    # ===================================================================
    # PLAYER SETUP
    # ===================================================================
    
    if abilities is None:
        abilities = {
            'walk': True,
            'crouch': True,
            'jump': True,
            'double_jump': True,
            'roll': True,  # NOW UNLOCKED!
            'spin': False
        }
    
    # Player spawns at start - ground at Y=400
    # Level 2 gives 4 hearts (8 health) instead of 3 hearts (6 health)
    player = Siena(120, 490, abilities=abilities, max_health=8)
    
    # ===================================================================
    # ENEMY PLACEMENT - 15 enemies total (reduced for better spacing)
    # RULE: Enemy Y position = Platform Y - Enemy Height
    # Swordsman height = 130, Frost Golem height = 80
    # ===================================================================
    
    enemies = pygame.sprite.Group()
    projectiles = pygame.sprite.Group()
    
    # BEAT 1: Tutorial enemy under low ceiling
    # Platform1 at Y=365, Swordsman height=130, spawn at Y=235
    swordsman1 = Swordsman(x=1050, y=285, patrol_left=1020, patrol_right=1300, stay_on_platform=True)
    enemies.add(swordsman1)

    # BEAT 2: Reduced enemy line - only 2 swordsmen instead of 3
    # Enemy line across platforms 4,5 (Y=365), spawn at 235
    swordsman2 = Swordsman(x=2300, y=235, patrol_left=2250, patrol_right=2530, stay_on_platform=True)
    enemies.add(swordsman2)

    swordsman3 = Swordsman(x=2550, y=235, patrol_left=2450, patrol_right=2730, stay_on_platform=True)
    enemies.add(swordsman3)

    # BEAT 3: One swordsman on elevated platform
    # Platform7 at Y=280, spawn at 150
    swordsman4 = Swordsman(x=3300, y=150, patrol_left=3200, patrol_right=3380, stay_on_platform=True)
    enemies.add(swordsman4)

    # Platform9 under ceiling (Y=365), spawn at 235
    swordsman5 = Swordsman(x=4100, y=235, patrol_left=3950, patrol_right=4280, stay_on_platform=True)
    enemies.add(swordsman5)

    # BEAT 4: Frost Golem introduction - reduced count
    # Platform10 elevated (Y=185), Golem height=80, spawn at 105
    frost1 = FrostGolem(x=4320, y=105, patrol_left=4200, patrol_right=4430, stay_on_platform=True)
    enemies.add(frost1)

    # Ground level Golem (Y=400), spawn at 320
    frost2 = FrostGolem(x=4650, y=320, patrol_left=4550, patrol_right=4750, stay_on_platform=True)
    enemies.add(frost2)

    # Platform12 (Y=350), spawn at 270
    frost3 = FrostGolem(x=4870, y=270, patrol_left=4800, patrol_right=4930, stay_on_platform=True)
    enemies.add(frost3)

    # BEAT 5: Mixed encounters - reduced
    # Platform14 upper tier (Y=200), Golem at 120
    frost4 = FrostGolem(x=5550, y=120, patrol_left=5450, patrol_right=5630, stay_on_platform=True)
    enemies.add(frost4)

    # Platform15 (Y=340), Golem at 260
    frost5 = FrostGolem(x=5850, y=260, patrol_left=5800, patrol_right=5880, stay_on_platform=True)
    enemies.add(frost5)

    # BEAT 6: Climax encounter - reduced
    # Platform19 elevated (Y=230), Golem at 150
    frost6 = FrostGolem(x=6630, y=150, patrol_left=6550, patrol_right=6680, stay_on_platform=True)
    enemies.add(frost6)

    # BEAT 7: Extended section enemies - final challenge before stairs
    # Ground level (Y=400), Swordsman height=130, spawn at 270
    # ADJUSTED: Moved to x=7420 to create ambush immediately after Narrow Passage tunnel exit
    swordsman6 = Swordsman(x=7420, y=270, patrol_left=7100, patrol_right=7550, stay_on_platform=True)
    enemies.add(swordsman6)

    # Platform22 (Y=300), Golem at 220
    frost8 = FrostGolem(x=7700, y=220, patrol_left=7600, patrol_right=7750, stay_on_platform=True)
    enemies.add(frost8)

    # BEAT 8: Final enemy on bridge platforms
    # Platform24 (Y=330), Swordsman height=130, spawn at 200
    swordsman7 = Swordsman(x=8100, y=200, patrol_left=8050, patrol_right=8230, stay_on_platform=True)
    enemies.add(swordsman7)

    # ===================================================================
    # COIN PLACEMENT (~50 coins total)
    # Original: ~35 coins
    # NEW: +15 coins under forced roll tunnels (3+4+5+4)
    # Coin height = 30px, so Y position is the TOP of the coin
    # Platform top positions: 365, 350, 340, etc.
    # Safe above platform: coin Y < platform_top - 40 (gives 10px+ clearance)
    # Safe below platform: coin Y > platform_top + 30 (coin below platform)
    # ===================================================================
    
    coins = pygame.sprite.Group()

    # Roll tutorial under low ceiling (3 coins)
    for i in range(3):
        coins.add(Coin(900 + i * 80, 380))

    # BEAT 2: Roll-jump teaching arc (3 coins)
    coins.add(Coin(1700, 300))
    coins.add(Coin(1860, 280))
    coins.add(Coin(1940, 300))

    # Under second low ceiling (3 coins)
    for i in range(3):
        coins.add(Coin(2270 + i * 120, 220))

    # Checkpoint approach (2 coins)
    coins.add(Coin(2750, 300))
    coins.add(Coin(2850, 300))

    # BEAT 3: Elevated platforms (2 coins)
    coins.add(Coin(3300, 230))
    coins.add(Coin(3650, 300))

    # Under third low ceiling (3 coins) - FIXED: Y=260 to clear platform at Y=295
    for i in range(3):
        coins.add(Coin(4000 + i * 100, 340))

    # BEAT 4: Frost Golem section - spread around platforms (4 coins)
    coins.add(Coin(4150, 260))  # In air before platform10 - FIXED: below platform at Y=295
    coins.add(Coin(4320, 240))  # Above platform10 (Y=185), coin at Y=155 clears by 30px
    coins.add(Coin(4600, 270))  # Between platforms, well above platform12 (Y=350)
    coins.add(Coin(5000, 310))  # Approaching checkpoint2

    # Checkpoint approach (2 coins)
    coins.add(Coin(5050, 300))
    coins.add(Coin(5150, 300))

    # BEAT 5: Narrow platforms (3 coins)
    coins.add(Coin(5850, 290))
    coins.add(Coin(6050, 240))
    coins.add(Coin(6250, 290))

    # BEAT 6: Climax (5 coins)
    coins.add(Coin(6630, 300))  # Above platform19 (Y=230)
    coins.add(Coin(6750, 270))  # Above platform20 (Y=300)
    coins.add(Coin(6870, 250))
    coins.add(Coin(6950, 265))  # Between platforms - FIXED: below platform20 at Y=300
    coins.add(Coin(7050, 360))  # Before Narrow Passage tunnel

    # BEAT 7: Narrow Passage area (2 coins)
    coins.add(Coin(7250, 320))  # Above platform21 (Y=350)
    coins.add(Coin(7500, 360))  # In air above ground

    # Final staircase (3 coins)
    coins.add(Coin(8580, 320))
    coins.add(Coin(8700, 265))
    coins.add(Coin(8820, 210))

    # ===================================================================
    # LEVEL GOAL NPC
    # ===================================================================
    
    goal_npc = LevelGoalNPC(x=8960, y=140)  # At end of level on goal_platform after staircase
    
    return bg_color, platforms, hazards, LEVEL_WIDTH, player, enemies, projectiles, coins, world_name, goal_npc, background_layers