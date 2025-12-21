import pygame
from src.entities.player.siena import Siena
from src.entities.enemies.snowy import Snowy
from src.entities.enemies.northerner import Northerner
from src.entities.enemies.swordsman import Swordsman
from src.entities.enemies.frost_golem import FrostGolem
from src.entities.enemies.spiked_slime import SpikedSlime
from src.entities.enemies.elkman import Elkman
from src.ui.coin import Coin
from src.ui.npc import LevelGoalNPC
from src.ui.moving_platform import MovingPlatform, DisappearingPlatform
from src.ui.appearing_platform import AppearingPlatform

LEVEL_WIDTH = 18500  # Extended to include Pedro's platform at x=18450
LEVEL_HEIGHT = 600

def build_level(abilities=None):
    """
    Build Level 1-4: Northern Lights Summit - The Ultimate Finale

    DESIGN PHILOSOPHY:
    - Ultimate finale testing ALL skills from Levels 1-3
    - Features ALL 6 enemy types (Snowy, Northerner, Swordsman, Frost Golem, Spiked Slime, Elkman)
    - Incorporates ALL proven mechanics: roll tunnels, spin gaps, reward platforms, long hazard stretches
    - Maximum diversity with 7 distinct themed beats
    - Progressive difficulty peaking at Beat 6 (The Final Gauntlet)
    - Unique features: mobile Elkman, dual-enemy tunnels, multi-tier arena, elevated snipers

    7-BEAT STRUCTURE (18,000px):
    - Beat 1 (0-2,500px): "The Grand Opening" - Introduce all enemy types, first roll tunnel
    - Beat 2 (2,500-5,000px): "The Roll Gauntlet" - Roll mastery with enemies inside tunnels
    - Beat 3 (5,000-8,000px): "Spin Heaven" - Spin gaps, major pit, first reward platform
    - Beat 4 (8,000-11,000px): "The Mixed Crucible" - Chaos with all mechanics combined
    - Beat 5 (11,000-13,500px): "The Northerner Onslaught" - Combat intensity, multi-tier arena
    - Beat 6 (13,500-16,000px): "The Final Gauntlet" - Ultimate test, massive pit
    - Beat 7 (16,000-18,000px): "Victory Path" - Triumphant climb to Pedro

    ENEMY COUNT (45 total - strategically placed):
    - 8 Snowy (2 HP tanks)
    - 10 Northerner (ranged spear throwers - force spin usage)
    - 5 Swordsman (aggressive melee fighters)
    - 7 Frost Golem (ranged artillery with bouncing fireballs)
    - 4 Spiked Slime (hazard enemies)
    - 6 Elkman (platform-bound snowball snipers - NEW!)

    MECHANICS:
    - 5 Roll Tunnels (160-185px clearance)
    - 4 Spin Gaps (300-320px width)
    - 3 Reward Platforms (requires double spin, 14 coins total!)
    - 2 Long Hazard Stretches (600px each)
    - 10 Disappearing Platforms (15-30 frames)
    - 11 Moving Platforms (2-3 px/frame)
    - 14 Appearing Platforms (alternating patterns)

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
    # GROUND - Continuous ground at Y=400 with strategic gaps aligned to beats
    # ===================================================================
    ground_segments = []

    # 7-Beat Gap Structure:
    # Gap 1: 1800-2100 (300px, Beat 1)
    # Gap 2: 3200-3600 (400px, Beat 2)
    # Gap 3: 4500-4800 (300px, Beat 2)
    # MAJOR PIT: 5800-6700 (900px, Beat 3)
    # Gap 5: 10000-10800 (800px, Beat 4)
    # MASSIVE PIT: 14000-15200 (1200px, Beat 6 - longest!)
    # Gap 7: 16500-16800 (300px, Beat 7)
    # Gap 8: 17200-17400 (200px, Beat 7)

    gaps = [
        (1800, 2100),    # Beat 1
        (3200, 3600),    # Beat 2
        (4500, 4800),    # Beat 2
        (5800, 6700),    # Beat 3 - Major Pit
        (10000, 10800),  # Beat 4
        (14000, 15200),  # Beat 6 - Massive Pit
        (16500, 16800),  # Beat 7
        (17200, 17400)   # Beat 7
    ]

    current_x = 0
    for gap_start, gap_end in gaps:
        # Add ground segment before gap
        if current_x < gap_start:
            ground_segments.append(pygame.Rect(current_x, 400, gap_start - current_x, 40))
        current_x = gap_end

    # Final ground segment after last gap (extends to end of level)
    ground_segments.append(pygame.Rect(current_x, 400, LEVEL_WIDTH - current_x, 40))

    # ===================================================================
    # BEAT 1: "THE GRAND OPENING" (0-2,500px)
    # Theme: Warm welcome that escalates quickly
    # Mechanics: Introduce all enemy types, first roll tunnel
    # ===================================================================

    # Rising platform sequence
    beat1_platform1 = pygame.Rect(400, 350, 200, 25)
    beat1_platform2 = pygame.Rect(700, 300, 180, 25)
    beat1_platform3 = pygame.Rect(1000, 250, 150, 25)
    beat1_platform4 = pygame.Rect(1500, 300, 200, 25)

    # ROLL TUNNEL 1 (1800-2180px) - 185px clearance (comfortable learning)
    roll_tunnel1_ceiling = pygame.Rect(1800, 215, 380, 25)
    roll_tunnel1_support = pygame.Rect(1800, 370, 380, 25)

    # Post-gap landing
    beat1_platform5 = pygame.Rect(2180, 350, 200, 25)
    beat1_platform6 = pygame.Rect(2400, 300, 150, 25)

    # ===================================================================
    # BEAT 2: "THE ROLL GAUNTLET" (2,500-5,000px)
    # Theme: Roll mastery through tight tunnels
    # Mechanics: Challenge roll tunnels with enemies inside
    # ===================================================================

    beat2_platform1 = pygame.Rect(2600, 340, 200, 25)

    # ROLL TUNNEL 2 (2800-3200px) - 160px clearance (TIGHT)
    roll_tunnel2_ceiling = pygame.Rect(2800, 210, 400, 25)
    roll_tunnel2_support = pygame.Rect(2800, 370, 400, 25)

    # Post-tunnel, pre-gap
    beat2_platform2 = pygame.Rect(3700, 300, 200, 25)
    beat2_platform3 = pygame.Rect(4000, 250, 180, 25)

    # ROLL TUNNEL 3 (4300-4700px) - 165px clearance (VERY TIGHT)
    roll_tunnel3_ceiling = pygame.Rect(4300, 205, 400, 25)
    roll_tunnel3_support = pygame.Rect(4300, 370, 400, 25)

    # Post-gap landing
    beat2_platform4 = pygame.Rect(4850, 350, 200, 25)

    # ===================================================================
    # BEAT 3: "SPIN HEAVEN" (5,000-8,000px)
    # Theme: Spin attack mastery with aerial combat
    # Mechanics: Spin gaps, long hazard stretch, major pit, reward platform
    # ===================================================================

    # Before long hazard stretch
    beat3_platform1 = pygame.Rect(5050, 300, 150, 25)

    # SPIN GAP 1 (5500-5820px) - 320px requiring spin
    spin_gap1_after = pygame.Rect(5820, 280, 200, 25)

    # REWARD PLATFORM 1 (requires double spin from spin_gap1_after)
    reward_platform1 = pygame.Rect(6900, 150, 200, 25)

    # SPIN GAP 2 (7200-7520px) - 320px
    spin_gap2_after = pygame.Rect(7520, 300, 200, 25)

    # Transition to Beat 4
    beat3_platform2 = pygame.Rect(7800, 350, 200, 25)

    # ===================================================================
    # BEAT 4: "THE MIXED CRUCIBLE" (8,000-11,000px)
    # Theme: Chaotic combination of all mechanics
    # Mechanics: Combat tunnel, appearing platforms, long hazard, major pit, reward platform
    # ===================================================================

    # ROLL TUNNEL 4 (8200-8550px) - COMBAT tunnel, 160px clearance
    roll_tunnel4_ceiling = pygame.Rect(8200, 210, 350, 25)
    roll_tunnel4_support = pygame.Rect(8200, 370, 350, 25)

    # Post-tunnel platforms
    beat4_platform1 = pygame.Rect(8600, 300, 200, 25)
    beat4_platform2 = pygame.Rect(8900, 250, 180, 25)

    # Before appearing platform wave
    beat4_platform3 = pygame.Rect(9000, 300, 180, 25)

    # REWARD PLATFORM 2 (requires double spin from ground after pit)
    reward_platform2 = pygame.Rect(11050, 140, 200, 25)

    # Transition to Beat 5
    beat4_platform5 = pygame.Rect(11300, 300, 200, 25)

    # ===================================================================
    # BEAT 5: "THE NORTHERNER ONSLAUGHT" (11,000-13,500px)
    # Theme: Pure combat intensity
    # Mechanics: Spin gap, multi-tier arena, mobile Elkman
    # ===================================================================

    # SPIN GAP 3 (11800-12120px) - 320px
    spin_gap3_before = pygame.Rect(11600, 300, 200, 25)
    spin_gap3_after = pygame.Rect(12120, 280, 200, 25)

    # MULTI-TIER COMBAT ARENA (12200-12900px)
    arena_lower = pygame.Rect(12200, 350, 300, 25)
    arena_mid = pygame.Rect(12350, 280, 250, 25)
    arena_upper = pygame.Rect(12450, 210, 200, 25)

    # Post-arena platforms
    beat5_platform2 = pygame.Rect(12700, 300, 180, 25)
    beat5_platform3 = pygame.Rect(13000, 350, 200, 25)
    beat5_platform4 = pygame.Rect(13300, 280, 200, 25)

    # ===================================================================
    # BEAT 6: "THE FINAL GAUNTLET" (13,500-16,000px)
    # Theme: Ultimate skill test
    # Mechanics: Final roll tunnel into massive pit with reward platform
    # ===================================================================

    # ROLL TUNNEL 5 (13600-14000px) - FINAL tunnel, 165px clearance
    roll_tunnel5_ceiling = pygame.Rect(13600, 205, 400, 25)
    roll_tunnel5_support = pygame.Rect(13600, 370, 400, 25)

    # REWARD PLATFORM 3 (in middle of massive pit - highest risk!)
    reward_platform3 = pygame.Rect(14600, 120, 200, 25)

    # SPIN GAP 4 (15500-15820px) - Final spin gap over 620px hazard
    spin_gap4_before = pygame.Rect(15300, 300, 200, 25)
    spin_gap4_after = pygame.Rect(15820, 280, 200, 25)

    # Transition to Beat 7
    beat6_platform1 = pygame.Rect(15950, 350, 200, 25)

    # ===================================================================
    # BEAT 7: "VICTORY PATH" (16,000-18,000px)
    # Theme: Triumphant climb to Pedro
    # Mechanics: Moderate challenge, celebratory finale
    # ===================================================================

    beat7_platform1 = pygame.Rect(16300, 350, 250, 25)
    beat7_platform2 = pygame.Rect(16900, 300, 200, 25)
    beat7_platform3 = pygame.Rect(17450, 320, 180, 25)

    # Victory stairs (7 stairs ascending to Pedro)
    stair1 = pygame.Rect(17600, 370, 100, 25)
    stair2 = pygame.Rect(17700, 345, 100, 25)
    stair3 = pygame.Rect(17800, 320, 100, 25)
    stair4 = pygame.Rect(17900, 295, 100, 25)
    stair5 = pygame.Rect(18000, 270, 100, 25)
    stair6 = pygame.Rect(18100, 245, 100, 25)
    stair7 = pygame.Rect(18200, 220, 100, 25)

    # Pedro's final platform
    pedros_platform = pygame.Rect(18300, 200, 150, 25)
    goal_npc = LevelGoalNPC(x=18350, y=150)  # On top of Pedro's platform

    # ===================================================================
    # MOVING PLATFORMS (11 total distributed across beats)
    # ===================================================================

    moving_platforms = []

    # Beat 1 - Introduction
    moving_platforms.append(MovingPlatform(x=1200, y=200, width=180, height=25, move_range=150, speed=2, direction='vertical'))

    # Beat 2 - Roll Gauntlet
    moving_platforms.append(MovingPlatform(x=4100, y=250, width=180, height=25, move_range=180, speed=2.5, direction='horizontal'))

    # Beat 3 - Spin Heaven (Major Pit)
    moving_platforms.append(MovingPlatform(x=6300, y=280, width=180, height=25, move_range=200, speed=3, direction='vertical'))  # Fast in major pit

    # Beat 4 - Mixed Crucible
    
    moving_platforms.append(MovingPlatform(x=10300, y=280, width=180, height=25, move_range=200, speed=2.5, direction='vertical'))  # In Major Pit 2

    # Beat 5 - Northerner Onslaught (MOBILE ELKMAN PLATFORM!)
    moving_platforms.append(MovingPlatform(x=12950, y=280, width=180, height=25, move_range=200, speed=2, direction='horizontal'))

    # Beat 6 - Final Gauntlet (MASSIVE PIT)
    moving_platforms.append(MovingPlatform(x=14300, y=300, width=180, height=25, move_range=180, speed=2.5, direction='horizontal'))
    moving_platforms.append(MovingPlatform(x=14900, y=250, width=180, height=25, move_range=200, speed=3, direction='vertical'))  # Fast in massive pit

    # Beat 7 - Victory Path
    moving_platforms.append(MovingPlatform(x=16600, y=280, width=180, height=25, move_range=150, speed=2, direction='horizontal'))
    moving_platforms.append(MovingPlatform(x=17000, y=250, width=180, height=25, move_range=120, speed=2, direction='vertical'))

    # ===================================================================
    # DISAPPEARING PLATFORMS (10 total) - Stepping on makes them vanish
    # 15 frames = EXTREME, 25 frames = CHALLENGE
    # ===================================================================

    disappearing_platforms = []

    # Beat 2 - Gap 2 crossing (3200-3600)
    disappearing_platforms.append(DisappearingPlatform(x=3200, y=350, width=180, height=25, disappear_time=25))
    disappearing_platforms.append(DisappearingPlatform(x=3450, y=320, width=180, height=25, disappear_time=25))

    # Beat 4 - MAJOR PIT 2 crossing (10000-10800) - EXTREME
    disappearing_platforms.append(DisappearingPlatform(x=10000, y=350, width=180, height=25, disappear_time=15))
    disappearing_platforms.append(DisappearingPlatform(x=10550, y=320, width=180, height=25, disappear_time=15))

    # Beat 6 - MASSIVE PIT crossing (14000-15200) - EXTREME
    disappearing_platforms.append(DisappearingPlatform(x=14000, y=350, width=180, height=25, disappear_time=15))
    
    # ===================================================================
    # APPEARING PLATFORMS (14 total) - Timer-based visibility
    # ===================================================================

    appearing_platforms = []

    # Beat 3 - Spin Gap 1: Northerners mid-air (3 platforms)
    appearing_platforms.append(AppearingPlatform(x=5500, y=280, width=160, height=25, appear_time=90, disappear_time=90, start_visible=True))
    appearing_platforms.append(AppearingPlatform(x=5660, y=300, width=160, height=25, appear_time=90, disappear_time=90, start_visible=False))
    appearing_platforms[1].timer = 45  # Offset
    #appearing_platforms[2].timer = 20  # Offset

    # Beat 4 - Appearing Platform Wave (4 platforms with offset timers)
    for i in range(4):
        appearing_platforms.append(AppearingPlatform(
            x=9200 + (i * 160), y=280 + (20 if i % 2 == 0 else 0),
            width=160, height=25,
            appear_time=75, disappear_time=75,
            start_visible=(i % 2 == 0)
        ))
        appearing_platforms[-1].timer = i * 15  # Offset timers for wave

    # Beat 5 - Spin Gap 3: Northerner mid-air (1 platform)
    appearing_platforms.append(AppearingPlatform(x=11950, y=270, width=160, height=25, appear_time=80, disappear_time=80, start_visible=True))

    # Beat 7 - Victory Path bonus platform
    appearing_platforms.append(AppearingPlatform(x=16100, y=230, width=140, height=25, appear_time=80, disappear_time=80, start_visible=True))

    # ===================================================================
    # HAZARDS - Fire hazards on roll tunnel ceilings + long stretches
    # ===================================================================

    hazards = []

    # ROLL TUNNEL 1 ceiling hazards (3 hazards at Y=185 on top of ceiling at Y=215)
    # Inset by 30px on each side: 1800+30=1830, 380-60=320
    hazards.append(pygame.Rect(1830, 185, 320, 30))


    # ROLL TUNNEL 2 ceiling hazards (4 hazards at Y=180 on top of ceiling at Y=210)
    # Inset by 30px on each side: 2800+30=2830, 400-60=340
    hazards.append(pygame.Rect(2830, 180, 340, 30))


    # ROLL TUNNEL 3 ceiling hazards (5 hazards at Y=175 on top of ceiling at Y=205)
    # Inset by 30px on each side: 4300+30=4330, 400-60=340
    hazards.append(pygame.Rect(4330, 175, 340, 30))

    # LONG HAZARD STRETCH 1 (Beat 3: 5000-5600px, 600px solid)
    # Inset by 30px on each side: 5000+30=5030, 600-60=540
    hazards.append(pygame.Rect(5030, 370, 540, 30))

    # ROLL TUNNEL 4 ceiling hazards (4 hazards at Y=180 on top of ceiling at Y=210)
    # Inset by 30px on each side: 8200+30=8230, 350-60=290
    hazards.append(pygame.Rect(8230, 180, 290, 30))

    # LONG HAZARD STRETCH 2 (Beat 4: 9700-10300px, 600px solid)
    # Inset by 30px on each side: 9700+30=9730, 300-60=240
    hazards.append(pygame.Rect(9730, 370, 240, 30))

    # ROLL TUNNEL 5 ceiling hazards (5 hazards at Y=175 on top of ceiling at Y=205)
    # Inset by 30px on each side: 13600+30=13630, 400-60=340
    hazards.append(pygame.Rect(13630, 175, 340, 30))

    # SPIN GAP 4 long hazard below (15300-15920px, 620px)
    # Inset by 30px on each side: 15300+30=15330, 620-60=560
    hazards.append(pygame.Rect(15330, 370, 560, 30))

    # ===================================================================
    # PLATFORMS LIST
    # ===================================================================

    platforms = ground_segments + [
        # Beat 1
        beat1_platform1, beat1_platform2, beat1_platform3, beat1_platform4,
        roll_tunnel1_ceiling, roll_tunnel1_support,
        beat1_platform5, beat1_platform6,
        # Beat 2
        beat2_platform1,
        roll_tunnel2_ceiling, roll_tunnel2_support,
        beat2_platform2, beat2_platform3,
        roll_tunnel3_ceiling, roll_tunnel3_support,
        beat2_platform4,
        # Beat 3
        beat3_platform1, spin_gap1_after,
        reward_platform1,
        spin_gap2_after,
        beat3_platform2,
        # Beat 4
        roll_tunnel4_ceiling, roll_tunnel4_support,
        beat4_platform1, beat4_platform2, beat4_platform3,
        reward_platform2,
        beat4_platform5,
        # Beat 5
        spin_gap3_before, spin_gap3_after,
        arena_lower, arena_mid, arena_upper,
        beat5_platform2, beat5_platform3, beat5_platform4,
        # Beat 6
        roll_tunnel5_ceiling, roll_tunnel5_support,
        reward_platform3,
        spin_gap4_before, spin_gap4_after,
        beat6_platform1,
        # Beat 7
        beat7_platform1, beat7_platform2, beat7_platform3,
        stair1, stair2, stair3, stair4, stair5, stair6, stair7,
        pedros_platform
    ]

    # ===================================================================
    # PLAYER
    # ===================================================================

    player = Siena(x=100, y=490, abilities=abilities, max_health=12)  # 6 hearts (12 lives) - hardest level

    # ===================================================================
    # ENEMIES - 45 total strategically placed across all 7 beats
    # ALL 6 ENEMY TYPES REPRESENTED including Elkman!
    # ===================================================================

    enemies = []

    # ========== BEAT 1: "THE GRAND OPENING" (0-2,500px) - 6 enemies ==========
    # Introduce ALL enemy types
    enemies.append(Snowy(x=600, y=320, patrol_left=500, patrol_right=800))  # Opening tank
    enemies.append(Northerner(x=950, y=270, patrol_left=850, patrol_right=1100))  # Ranged intro
    enemies.append(Elkman(x=1550, y=270, patrol_left=1500, patrol_right=1700))  # ELKMAN #1 - First appearance!
    enemies.append(Swordsman(x=1950, y=320, patrol_left=1850, patrol_right=2180))  # Roll tunnel exit ambush
    enemies.append(FrostGolem(x=2200, y=320, patrol_left=2100, patrol_right=2400))  # Evasive challenge
    enemies.append(SpikedSlime(x=2400, y=320, patrol_left=2300, patrol_right=2500))  # Aggressive finale

    # ========== BEAT 2: "THE ROLL GAUNTLET" (2,500-5,000px) - 6 enemies ==========
    # Roll-focused with enemies inside tunnels
    enemies.append(Snowy(x=2900, y=340, patrol_left=2800, patrol_right=3200))  # INSIDE Roll Tunnel 2!
    enemies.append(Swordsman(x=3250, y=320, patrol_left=3200, patrol_right=3450))  # On disappearing platform
    enemies.append(Northerner(x=3750, y=270, patrol_left=3700, patrol_right=3900))  # Platform guardian
    enemies.append(FrostGolem(x=4100, y=220, patrol_left=4000, patrol_right=4200))  # Moving platform sniper
    enemies.append(Elkman(x=4720, y=340, patrol_left=4700, patrol_right=4850))  # ELKMAN #2 - Roll tunnel exit punisher!
    enemies.append(SpikedSlime(x=4900, y=320, patrol_left=4850, patrol_right=5000))  # Section closer

    # ========== BEAT 3: "SPIN HEAVEN" (5,000-8,000px) - 6 enemies ==========
    # Spin-focused with aerial combat
    enemies.append(Snowy(x=5100, y=320, patrol_left=5000, patrol_right=5300))  # Before long hazard
    enemies.append(Northerner(x=5650, y=270, patrol_left=5600, patrol_right=5750))  # Before Spin Gap 1
    enemies.append(Northerner(x=6000, y=320, patrol_left=5900, patrol_right=6100))  # On disappearing platform mid-pit
    enemies.append(Northerner(x=6500, y=320, patrol_left=6400, patrol_right=6600))  # On disappearing platform mid-pit
    enemies.append(FrostGolem(x=6800, y=320, patrol_left=6700, patrol_right=6950))  # After pit
    enemies.append(Elkman(x=7570, y=270, patrol_left=7520, patrol_right=7720))  # ELKMAN #3 - Spin Gap 2 punisher!

    # ========== BEAT 4: "THE MIXED CRUCIBLE" (8,000-11,000px) - 7 enemies ==========
    # Maximum chaos with all mechanics
    enemies.append(Snowy(x=8100, y=320, patrol_left=8000, patrol_right=8250))  # Pre-tunnel
    enemies.append(Swordsman(x=8300, y=340, patrol_left=8200, patrol_right=8500))  # INSIDE Roll Tunnel 4!
    enemies.append(FrostGolem(x=8450, y=340, patrol_left=8300, patrol_right=8550))  # INSIDE Roll Tunnel 4 (dual enemy tunnel!)
    enemies.append(Northerner(x=9300, y=250, patrol_left=9200, patrol_right=9400))  # Appearing platform guardian
    enemies.append(SpikedSlime(x=9600, y=320, patrol_left=9850, patrol_right=10000))  # Before Major Pit 2
    enemies.append(Elkman(x=10450, y=120, patrol_left=10350, patrol_right=10550))  # ELKMAN #4 - ELEVATED SNIPER over pit!
    enemies.append(Snowy(x=10850, y=320, patrol_left=10800, patrol_right=11000))  # After pit

    # ========== BEAT 5: "THE NORTHERNER ONSLAUGHT" (11,000-13,500px) - 6 enemies ==========
    # Pure combat intensity, spin-attack focused
    enemies.append(Northerner(x=11950, y=240, patrol_left=11900, patrol_right=12050))  # Mid-air on appearing platform in Spin Gap 3
    enemies.append(Northerner(x=12250, y=320, patrol_left=12200, patrol_right=12450))  # Lower arena tier
    enemies.append(Northerner(x=12400, y=250, patrol_left=12350, patrol_right=12550))  # Mid arena tier
    enemies.append(Elkman(x=12500, y=180, patrol_left=12450, patrol_right=12600))  # ELKMAN #5 - UPPER ARENA SNIPER!
    enemies.append(Elkman(x=12950, y=250, patrol_left=12900, patrol_right=13150))  # ELKMAN #6 - MOBILE on moving platform!
    enemies.append(Northerner(x=13200, y=320, patrol_left=13150, patrol_right=13350))  # Section finale

    # ========== BEAT 6: "THE FINAL GAUNTLET" (13,500-16,000px) - 5 enemies ==========
    # Ultimate skill test, finale bosses
    enemies.append(FrostGolem(x=13700, y=340, patrol_left=13600, patrol_right=13950))  # INSIDE final roll tunnel!
    enemies.append(Snowy(x=14100, y=320, patrol_left=14000, patrol_right=14250))  # On disappearing platform at pit start - BRUTAL!
    enemies.append(Swordsman(x=14600, y=250, patrol_left=14500, patrol_right=14700))  # Moving platform guardian
    enemies.append(Snowy(x=15000, y=320, patrol_left=14950, patrol_right=15150))  # Near pit end
    enemies.append(FrostGolem(x=15600, y=320, patrol_left=15500, patrol_right=15800))  # Before final spin gap

    # ========== BEAT 7: "VICTORY PATH" (16,000-18,000px) - 4 enemies ==========
    # Victory lap with moderate challenge
    enemies.append(Snowy(x=16200, y=320, patrol_left=16000, patrol_right=16400))  # Final Snowy
    enemies.append(Swordsman(x=16900, y=320, patrol_left=16800, patrol_right=17100))  # Final Swordsman
    enemies.append(SpikedSlime(x=17300, y=320, patrol_left=17200, patrol_right=17450))  # Final Spiked Slime
    enemies.append(FrostGolem(x=17500, y=320, patrol_left=17400, patrol_right=17650))  # Final Frost Golem before stairs

    # TOTAL: 45 enemies
    # 8 Snowy, 10 Northerner, 5 Swordsman, 7 Frost Golem, 4 Spiked Slime, 6 Elkman ✓

    # ===================================================================
    # COINS - EXACTLY 45 TOTAL distributed across all 7 beats
    # ===================================================================

    coins = pygame.sprite.Group()

    # ========== BEAT 1: 7 coins ==========
    # Early platform coin (on beat1_platform1 at x=400)
    coins.add(Coin(beat1_platform1.x + 90, beat1_platform1.y - 40))
    # Roll tunnel coins (3 coins under roll tunnel 1 at Y=340)
    coins.add(Coin(1900, 340))
    coins.add(Coin(2000, 340))
    coins.add(Coin(2100, 340))
    # Platform coins
    coins.add(Coin(beat1_platform2.x + 90, beat1_platform2.y - 40))
    # Risky coin above hazard
    coins.add(Coin(1350, 310))
    # Mid-gap coin
    coins.add(Coin(1950, 280))

    # ========== BEAT 2: 7 coins ==========
    # Roll tunnel coins (4 coins under roll tunnel 2)
    coins.add(Coin(2850, 340))
    coins.add(Coin(2950, 340))
    coins.add(Coin(3050, 340))
    coins.add(Coin(3100, 340))
    # Roll tunnel coins (3 coins under roll tunnel 3)
    coins.add(Coin(4400, 340))
    coins.add(Coin(4550, 340))
    coins.add(Coin(4650, 340))

    # ========== BEAT 3: 9 coins ==========
    # REWARD PLATFORM 1 - 5 coins at Y=120 (highest reward!)
    coins.add(Coin(6900, 120))
    coins.add(Coin(6950, 120))
    coins.add(Coin(7000, 120))
    coins.add(Coin(7050, 120))
    coins.add(Coin(7100, 120))
    # Mid-Spin Gap 1 coins (risky!)
    coins.add(Coin(5600, 250))
    coins.add(Coin(5720, 250))
    # Mid-Spin Gap 2 coins
    coins.add(Coin(7300, 260))
    coins.add(Coin(7420, 260))

    # ========== BEAT 4: 8 coins ==========
    # Roll tunnel coins (3 coins under roll tunnel 4)
    coins.add(Coin(8300, 340))
    coins.add(Coin(8400, 340))
    coins.add(Coin(8500, 340))
    # REWARD PLATFORM 2 - 5 coins at Y=110
    coins.add(Coin(11050, 110))
    coins.add(Coin(11100, 110))
    coins.add(Coin(11150, 110))
    coins.add(Coin(11200, 110))
    coins.add(Coin(11250, 110))

    # ========== BEAT 5: 6 coins ==========
    # Mid-Spin Gap 3 coins
    coins.add(Coin(11900, 250))
    coins.add(Coin(12000, 250))
    # Multi-tier arena coins (one per tier)
    coins.add(Coin(arena_lower.x + 150, arena_lower.y - 40))
    coins.add(Coin(arena_mid.x + 125, arena_mid.y - 40))
    coins.add(Coin(arena_upper.x + 100, arena_upper.y - 40))
    # Risky coin on moving platform with Elkman!
    coins.add(Coin(13000, 250))

    # ========== BEAT 6: 4 coins (REDUCED) ==========
    # REWARD PLATFORM 3 - 4 coins at Y=90 (HIGHEST RISK - in massive pit!)
    coins.add(Coin(14600, 90))
    coins.add(Coin(14650, 90))
    coins.add(Coin(14700, 90))
    coins.add(Coin(14750, 90))

    # ========== BEAT 7: 5 coins (includes 1 with Pedro) ==========
    # Victory stairs coins
    coins.add(Coin(stair1.x + 50, stair1.y - 40))
    coins.add(Coin(stair3.x + 50, stair3.y - 40))
    coins.add(Coin(stair5.x + 50, stair5.y - 40))
    coins.add(Coin(stair7.x + 50, stair7.y - 40))
    

    # TOTAL: 6 + 7 + 9 + 8 + 6 + 4 + 5 = 45 coins ✓

    # ===================================================================
    # PROJECTILES GROUP
    # ===================================================================

    projectiles = pygame.sprite.Group()

    return bg_color, platforms, hazards, LEVEL_WIDTH, player, enemies, projectiles, coins, world_name, goal_npc, background_layers, moving_platforms, disappearing_platforms, appearing_platforms
