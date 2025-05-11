import pygame as pg
vec = pg.math.Vector2

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
DARKGREEN = (0, 128, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)
CYAN = (0, 255, 255)

# game settings
WIDTH = 1024   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 768  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "ZOMBIES"
BGCOLOR = BROWN

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

WALL_IMG = 'tileGreen_39.png'

# Player settings
PLAYER_HEALTH = 100
PLAYER_SPEED = 280
PLAYER_ROT_SPEED = 200
PLAYER_SKINS = ['manBlue', 'manBrown', 'manOld', 'womanGreen', 'hitman1', 'soldier1', 'survivor1', 'robot1']
PLAYER_STATES = ['gun', 'machine', 'silencer', 'stand', 'reload']
PLAYER_IMGS = {}
for skin in PLAYER_SKINS:
    PLAYER_IMGS[skin] = {}
    for state in PLAYER_STATES:
        PLAYER_IMGS[skin][state] = skin + '_' + state + '.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 32, 32)
BARREL_OFFSET = vec(20, 10)

# Weapon settings
BULLET_IMG = 'bullet.png'
WEAPONS = {}
WEAPONS['pistol'] = {'bullet_speed': 800,
                     'bullet_lifetime': 700,
                     'rate': 250,
                     'reload_delay': 100,
                     'reload_rate': 600,
                     'clip_size': 10,
                     'ammo': 40,
                     'kickback': 200,
                     'spread': 5,
                     'damage': 10,
                     'bullet_size': 'sm',
                     'bullet_count': 1,
                     'aoe_size': 0,
                     'aoe_damage': 0,
                     'look_dist': 200,
                     'state': 'gun'}
WEAPONS['shotgun'] = {'bullet_speed': 700,
                      'bullet_lifetime': 300,
                      'rate': 900,
                      'reload_delay': 200,
                      'reload_rate': 800,
                      'clip_size': 2,
                      'ammo': 20,
                      'kickback': 300,
                      'spread': 20,
                      'damage': 5,
                      'bullet_size': 'sm',
                      'bullet_count': 12,
                      'aoe_size': 0,
                      'aoe_damage': 0,
                      'look_dist': 100,
                      'state': 'machine'}
WEAPONS['rpg'] = {'bullet_speed': 500,
                  'bullet_lifetime': 1000,
                  'rate': 1200,
                  'reload_delay': 200,
                  'reload_rate': 800,
                  'clip_size': 1,
                  'ammo': 10,
                  'kickback': 300,
                  'spread': 2,
                  'damage': 10,
                  'bullet_size': 'lg',
                  'bullet_count': 1,
                  'aoe_size': 50,
                  'aoe_damage': 30,
                  'look_dist': 200,
                  'state': 'machine'}
WEAPONS['assault_rifle'] = {'bullet_speed': 800,
                            'bullet_lifetime': 700,
                            'rate': 100,
                            'reload_delay': 100,
                            'reload_rate': 600,
                            'clip_size': 30,
                            'ammo': 120,
                            'kickback': 200,
                            'spread': 5,
                            'damage': 6,
                            'bullet_size': 'sm',
                            'bullet_count': 1,
                            'aoe_size': 0,
                            'aoe_damage': 0,
                            'look_dist': 200,
                            'state': 'machine'}
WEAPONS['sniper'] = {'bullet_speed': 1000,
                     'bullet_lifetime': 1400,
                     'rate': 1400,
                     'reload_delay': 200,
                     'reload_rate': 1000,
                     'clip_size': 1,
                     'ammo': 10,
                     'kickback': 400,
                     'spread': 0,
                     'damage': 100,
                     'bullet_size': 'sm',
                     'bullet_count': 1,
                     'aoe_size': 0,
                     'aoe_damage': 0,
                     'look_dist': 400,
                     'state': 'silencer'}
WEAPONS['grenade'] = {'bullet_speed': 400,
                      'bullet_lifetime': 800,
                      'rate': 200,
                      'reload_delay': 0,
                      'reload_rate': 0,
                      'clip_size': -1,
                      'ammo': 1,
                      'kickback': 0,
                      'spread': 0,
                      'damage': 0,
                      'bullet_size': 'lg',
                      'bullet_count': 1,
                      'aoe_size': 50,
                      'aoe_damage': 100,
                      'look_dist': 200,
                      'state': 'stand'}

# Bullet settings
BULLET_HIT_RECT_SM = pg.Rect(0, 0, 10, 10)
BULLET_HIT_RECT_LG = pg.Rect(0, 0, 15, 15)

# Mob settings
MOB_IMG = 'zombie1_hold.png'
MOB_SPEEDS = [150, 100, 75, 125]
BOSS_SPEED = 50
MOB_IDLE_SPEED = 50
BOSS_IDLE_SPEED = 30
MOB_HIT_RECT = pg.Rect(0, 0, 32, 32)
BOSS_HIT_RECT = pg.Rect(0, 0, 85, 85)
MOB_HEALTH = 100
BOSS_HEALTH = 1000
MOB_DAMAGE = 10
BOSS_DAMAGE = 50
MOB_KNOCKBACK = 20
AVOID_RADIUS = 50
BOSS_AVOID_RADIUS = 100
DETECT_RADIUS = 400

# Effects
MUZZLE_FLASHES = ['whitePuff15.png', 'whitePuff16.png', 'whitePuff17.png',
                  'whitePuff18.png']
EXPLOSION_IMGS = ['regularExplosion00.png', 'regularExplosion01.png', 'regularExplosion02.png',
                  'regularExplosion03.png', 'regularExplosion04.png', 'regularExplosion05.png',
                  'regularExplosion06.png', 'regularExplosion07.png', 'regularExplosion08.png']
SPARKLE_IMGS = ['sparkle' + str(i + 1) + '.png' for i in range(16)]
SPLAT = 'splat green.png'
ARROW = 'arrow.png'
FLASH_DURATION = 50
DAMAGE_ALPHA = [i for i in range(0, 255, 55)]
NIGHT_COLOR = (20, 20, 20)
LIGHT_RADIUS = (500, 500)
LIGHT_MASK = "light_350_med.png"

# Layers
WALL_LAYER = 1
PLAYER_LAYER = 2
BULLET_LAYER = 3
MOB_LAYER = 2
BREAKABLE_LAYER = 1
EFFECTS_LAYER = 4
ITEMS_LAYER = 1
UI_LAYER = 5
CROSSHAIR_LAYER = 6

# Items
ITEM_IMAGES = {'health': 'health_pack.png',
               'pistol': 'pistol.png',
               'shotgun': 'obj_shotgun.png',
               'rpg': 'rpg.png',
               'assault_rifle': 'rifle.png',
               'sniper': 'sniper.png',
               'grenade': 'grenade.png',
               'ammo': 'ammo.png'}
CROSSHAIR_IMGS = {'pistol': 'cross_pistol.png',
                  'shotgun': 'cross_shotgun.png',
                  'rpg': 'cross_rocket.png',
                  'assault_rifle': 'cross_pistol.png',
                  'sniper': 'cross_sniper.png',
                  'grenade': 'cross_default.png',
                  '': 'cross_default.png'}
HEALTH_PACK_AMOUNT = 20
BOB_RANGE = 15
ARROW_BOB_RANGE = 10
BOB_SPEED = 0.4
DROPS = ['health', 'shotgun', 'rpg', 'assault_rifle', 'sniper', 'grenade', 'ammo']

# Sounds
INTRO_MUSIC = 'Dark Intro.ogg'
BG_MUSIC = 'espionage.ogg'
PAUSE_MUSIC = 'Offline.ogg'
BOSS_MUSIC = 'epic_boss_battle.ogg'
WIN_MUSIC = 'win_screen.ogg'
LOSE_MUSIC = 'lose_screen.ogg'
PLAYER_HIT_SOUNDS = ['pain/8.wav', 'pain/9.wav', 'pain/10.wav', 'pain/11.wav']
ZOMBIE_MOAN_SOUNDS = ['brains2.wav', 'brains3.wav', 'zombie-roar-1.wav', 'zombie-roar-2.wav',
                      'zombie-roar-3.wav', 'zombie-roar-5.wav', 'zombie-roar-6.wav', 'zombie-roar-7.wav']
BOSS_MOAN_SOUNDS = ['zombie-boss-roar.wav']
ZOMBIE_HIT_SOUNDS = ['splat-15.wav']
WEAPON_SOUNDS = {'pistol': ['pistol.wav'],
                 'shotgun': ['shotgun.wav'],
                 'rpg': ['rpg.wav'],
                 'assault_rifle': ['rifle.wav'],
                 'sniper': ['sniper.wav'],
                 'grenade': ['throw.wav']}
EFFECTS_SOUNDS = {'level_start': 'level_start.wav',
                  'game_over': 'game_over.wav',
                  'health_up': 'health_pack.wav',
                  'item_pickup': 'item_pickup.wav',
                  'gun_pickup': 'gun_pickup.wav',
                  'gun_reload': 'gun_reload.wav',
                  'gun_empty': 'out_of_ammo.wav',
                  'explosion': 'explosion01.wav',
                  'countdown': 'bomb_countdown.mp3'}
BREAK_SOUNDS = ['break1.mp3', 'break2.mp3', 'break3.mp3', 'break4.mp3', 'break5.mp3', 'break6.mp3']
BREAKABLE_HIT_SOUNDS = ['wood_hit1.ogg', 'wood_hit2.ogg', 'wood_hit3.ogg']