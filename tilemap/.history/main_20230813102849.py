# Tilemap Demo
# KidsCanCode 2016
import pygame as pg
import sys
from random import choice, random
from os import path
from settings import *
from sprites import *
from tilemap import *

# HUD functions
def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf, LIGHTGREY, outline_rect, 0, 7)
    pg.draw.rect(surf, col, fill_rect, 0, 7)
    pg.draw.rect(surf, WHITE, outline_rect, 2, 7)

class Game:
    def __init__(self):
        pg.mixer.pre_init(44100, -16, 4, 2048)
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()

    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        snd_folder = path.join(game_folder, 'snd')
        self.music_folder = path.join(game_folder, 'music')
        self.map_folder = path.join(game_folder, 'maps')
        self.title_font = path.join(img_folder, 'ZOMBIE.TTF')
        self.hud_font = path.join(img_folder, 'Impacted2.0.ttf')
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))
        self.player_imgs = {}
        for skin in PLAYER_IMGS:
            self.player_imgs[skin] = {}
            for state in PLAYER_IMGS[skin]:
                self.player_imgs[skin][state] = pg.image.load(path.join(img_folder, PLAYER_IMGS[skin][state])).convert_alpha()
        self.player_img_idx = 0
        self.player_skin = PLAYER_SKINS[0]
        self.player_img = self.player_imgs[self.player_skin]['gun']
        self.bullet_images = {}
        self.bullet_images['lg'] = pg.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()
        self.bullet_images['sm'] = pg.transform.scale(self.bullet_images['lg'], (40, 40))
        self.mob_img = pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()
        self.wall_img = pg.image.load(path.join(img_folder, WALL_IMG)).convert_alpha()
        self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE, TILESIZE))
        self.splat = pg.image.load(path.join(img_folder, SPLAT)).convert_alpha()
        self.splat = pg.transform.scale(self.splat, (64, 64))
        self.arrow = pg.image.load(path.join(img_folder, ARROW)).convert_alpha()
        self.arrow = pg.transform.scale(self.arrow, (32, 32))
        self.gun_flashes = []
        for img in MUZZLE_FLASHES:
            self.gun_flashes.append(pg.image.load(path.join(img_folder, img)).convert_alpha())
        self.explosion_imgs = []
        for img in EXPLOSION_IMGS:
            self.explosion_imgs.append(pg.image.load(path.join(img_folder, img)).convert_alpha())
        self.sparkle_imgs = []
        for img in SPARKLE_IMGS:
            self.sparkle_imgs.append(pg.image.load(path.join(img_folder, img)).convert_alpha())
        self.item_images = {}
        for item in ITEM_IMAGES:
            self.item_images[item] = pg.image.load(path.join(img_folder, ITEM_IMAGES[item])).convert_alpha()
        self.crosshair_imgs = {}
        for item in CROSSHAIR_IMGS:
            self.crosshair_imgs[item] = pg.image.load(path.join(img_folder, CROSSHAIR_IMGS[item])).convert_alpha()
            self.crosshair_imgs[item] = pg.transform.scale(self.crosshair_imgs[item], (48, 48))
        # lighting effect
        self.fog = pg.Surface((WIDTH, HEIGHT))
        self.fog.fill(NIGHT_COLOR)
        self.light_mask = pg.image.load(path.join(img_folder, LIGHT_MASK)).convert_alpha()
        self.light_mask = pg.transform.scale(self.light_mask, LIGHT_RADIUS)
        self.light_rect = self.light_mask.get_rect()
        # Sound loading
        self.pause_music = pg.mixer.Sound(path.join(self.music_folder, PAUSE_MUSIC))
        self.effects_sounds = {}
        for type in EFFECTS_SOUNDS:
            self.effects_sounds[type] = pg.mixer.Sound(path.join(snd_folder, EFFECTS_SOUNDS[type]))
        self.effects_sounds['game_over'].set_volume(0.5)
        self.effects_sounds['gun_reload'].set_volume(4)
        self.weapon_sounds = {}
        for weapon in WEAPON_SOUNDS:
            self.weapon_sounds[weapon] = []
            for snd in WEAPON_SOUNDS[weapon]:
                s = pg.mixer.Sound(path.join(snd_folder, snd))
                s.set_volume(0.3)
                self.weapon_sounds[weapon].append(s)
        self.weapon_sounds['grenade'][0].set_volume(3)
        self.zombie_moan_sounds = []
        for snd in ZOMBIE_MOAN_SOUNDS:
            s = pg.mixer.Sound(path.join(snd_folder, snd))
            s.set_volume(0.2)
            self.zombie_moan_sounds.append(s)
        self.boss_moan_sounds = []
        for snd in BOSS_MOAN_SOUNDS:
            s = pg.mixer.Sound(path.join(snd_folder, snd))
            s.set_volume(0.8)
            self.boss_moan_sounds.append(s)
        self.player_hit_sounds = []
        for snd in PLAYER_HIT_SOUNDS:
            self.player_hit_sounds.append(pg.mixer.Sound(path.join(snd_folder, snd)))
        self.zombie_hit_sounds = []
        for snd in ZOMBIE_HIT_SOUNDS:
            self.zombie_hit_sounds.append(pg.mixer.Sound(path.join(snd_folder, snd)))
        self.break_sounds = []
        for snd in BREAK_SOUNDS:
            self.break_sounds.append(pg.mixer.Sound(path.join(snd_folder, snd)))
        self.breakable_hit_sounds = []
        for snd in BREAKABLE_HIT_SOUNDS:
            self.breakable_hit_sounds.append(pg.mixer.Sound(path.join(snd_folder, snd)))

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.breakables = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.aoe = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.weapons_list = ['pistol']
        self.map = TiledMap(path.join(self.map_folder, 'level1.tmx'))
        self.map_img = self.map.make_map()
        self.map.rect = self.map_img.get_rect()
        # for row, tiles in enumerate(self.map.data):
        #     for col, tile in enumerate(tiles):
        #         if tile == '1':
        #             Wall(self, col, row)
        #         if tile == 'M':
        #             Mob(self, col, row)
        #         if tile == 'P':
        #             self.player = Player(self, col, row)
        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width / 2, tile_object.y + tile_object.height / 2)
            if tile_object.name == 'player':
                self.player = Player(self, obj_center.x, obj_center.y)
            if tile_object.name == 'zombie':
                Mob(self, obj_center.x, obj_center.y)
            if tile_object.name == 'breakable':
                Breakable(self, obj_center.x, obj_center.y, tile_object.hit_width, tile_object.hit_height, tile_object.image, tile_object.hp, False)
            if tile_object.name == 'breakable_drop':
                Breakable(self, obj_center.x, obj_center.y, tile_object.hit_width, tile_object.hit_height, tile_object.image, tile_object.hp, True)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name in DROPS:
                Item(self, obj_center, tile_object.name)
        Crosshair(self)
        self.player_inv = Inventory(self, WIDTH / 2 - 130.5, HEIGHT - 50, 1, 6)
        self.player_inv.add_item([InvItem(self, self.weapons_list[0]), WEAPONS[self.weapons_list[0]]['ammo']], (0, 0))
        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False
        self.paused = False
        self.night = False
        self.boss = False
        self.win = False
        pg.mixer.stop()
        self.effects_sounds['level_start'].play()

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        pg.mixer.music.load(path.join(self.music_folder, BG_MUSIC))
        pg.mixer.music.play(loops=-1)
        pg.mouse.set_visible(False)
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0 # fix for Python 2.x
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()
    
    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)
        # game over?
        if len(self.mobs) == 0:
            if self.boss:
                self.playing = False
                self.win = True
            else:
                for tile_object in self.map.tmxdata.objects:
                    obj_center = vec(tile_object.x + tile_object.width / 2, tile_object.y + tile_object.height / 2)
                    if tile_object.name == 'boss':
                        boss = Boss(self, obj_center.x, obj_center.y)
                        self.camera.focus(boss, 1500)
                        pg.mixer.music.load(path.join(self.music_folder, BOSS_MUSIC))
                        pg.mixer.music.play(loops=-1)
                        pg.mixer.music.set_volume(0.3)
                        self.boss = True
                        break
                else:
                    self.playing = False
                    self.win = True     
        # player hits items
        hits = pg.sprite.spritecollide(self.player, self.items, False)
        for hit in hits:
            if hit.type == 'health' and self.player.health < PLAYER_HEALTH:
                hit.kill()
                self.effects_sounds['health_up'].play()
                self.player.add_health(HEALTH_PACK_AMOUNT)
                Sparkle(self, self.player.pos)
            if hit.type == 'ammo' and self.player.weapon and not self.player.weapon in ['pistol', 'grenade']:
                hit.kill()
                self.effects_sounds['item_pickup'].play()
                self.player.add_ammo()
            if hit.type in ['shotgun', 'rpg', 'assault_rifle', 'sniper'] and hit.type not in self.weapons_list:
                hit.kill()
                for i in range(len(self.weapons_list)):
                    if self.weapons_list[i] == '':
                        self.weapons_list[i] = hit.type
                        self.player.weapon_clips[i] = WEAPONS[hit.type]['clip_size']
                        break
                else:
                    self.weapons_list.append(hit.type)
                    self.player.weapon_clips.append(WEAPONS[hit.type]['clip_size'])
                self.player_inv.add_item([InvItem(self, hit.type), WEAPONS[hit.type]['ammo']], (self.weapons_list.index(hit.type), 0))
                self.player.equip_weapon(self.weapons_list.index(hit.type) + 1)
            if hit.type == 'grenade':
                hit.kill()
                if 'grenade' not in self.weapons_list:
                    for i in range(len(self.weapons_list)):
                        if self.weapons_list[i] == '':
                            self.weapons_list[i] = 'grenade'
                            self.player.weapon_clips[i] = WEAPONS[hit.type]['clip_size']
                            break
                    else:
                        self.weapons_list.append('grenade')
                        self.player.weapon_clips.append(WEAPONS[hit.type]['clip_size'])
                self.player_inv.add_item([InvItem(self, 'grenade'), WEAPONS[hit.type]['ammo']], (self.weapons_list.index('grenade'), 0))
                self.player.equip_weapon(self.weapons_list.index(hit.type) + 1)
        # mobs hit player
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            if random() < 0.7:
                choice(self.player_hit_sounds).play()
            if isinstance(hit, Boss):
                damage = BOSS_DAMAGE
            else:
                damage = MOB_DAMAGE
            self.player.health -= damage
            hit.vel = vec(0, 0)
            if self.player.health <= 0:
                self.playing = False
        if hits:
            self.player.hit()
            self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)
        # bullets hit mobs
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, False, collide_hit_rect)
        for mob in hits:
            # hit.health -= WEAPONS[self.player.weapon]['damage'] * len(hits[hit])
            for bullet in hits[mob]:
                if bullet.weapon_name != 'grenade':
                    mob.health -= bullet.damage
                    mob.detect_bullet()
                    bullet.destroy()
                    mob.vel = vec(0, 0)
        # bullets hit breakables
        hits = pg.sprite.groupcollide(self.breakables, self.bullets, False, False, collide_hit_rect)
        for breakable in hits:
            choice(self.breakable_hit_sounds).play()
            for bullet in hits[breakable]:
                if bullet.weapon_name != 'grenade':
                    breakable.health -= bullet.damage
                    bullet.destroy()
        # aoe damage to mobs
        hits = pg.sprite.groupcollide(self.aoe, self.mobs, False, False, pg.sprite.collide_circle)
        hit_aoes = set()
        for aoe in hits:
            for mob in hits[aoe]:
                mob.health -= aoe.damage
                if aoe.weapon != 'grenade':
                    mob.detect_bullet()
                mob.vel = vec(0, 0)
            hit_aoes.add(aoe)
        # aoe damage to breakables
        hits = pg.sprite.groupcollide(self.aoe, self.breakables, False, False, pg.sprite.collide_circle)
        for aoe in hits:
            for breakable in hits[aoe]:
                choice(self.breakable_hit_sounds).play()
                breakable.health -= aoe.damage
            hit_aoes.add(aoe)
        for aoe in hit_aoes:
            aoe.kill()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def render_fog(self):
        # draw the light mask (gradient) onto fog image
        self.fog.fill(NIGHT_COLOR)
        self.light_rect.center = self.camera.apply(self.player).center
        self.fog.blit(self.light_mask, self.light_rect)
        self.screen.blit(self.fog, (0, 0), special_flags=pg.BLEND_MULT)

    def draw(self):
        # pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        # self.screen.fill(BGCOLOR)
        self.screen.blit(self.map_img, self.camera.apply(self.map))
        # self.draw_grid()
        self.player_skin = PLAYER_SKINS[self.player_img_idx]
        self.player_img = self.player_imgs[self.player_skin][self.player.state]
        for sprite in self.all_sprites:
            try:
                if isinstance(sprite, (Crosshair, Inventory)):
                    self.screen.blit(sprite.image, sprite.rect)
                else:
                    offset = self.camera.apply(sprite)
                    self.screen.blit(sprite.image, offset)
                    if isinstance(sprite, Player):
                        sprite.abs_pos = vec(offset.centerx, offset.centery)
            except:
                pass
            if isinstance(sprite, Mob) or isinstance(sprite, Breakable):
                sprite.draw_health()
            try:
                if self.draw_debug:
                    pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(sprite.hit_rect), 1)
            except:
                pass
        if self.draw_debug:
            for wall in self.walls:
                if wall not in self.breakables:
                    pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(wall.rect), 1)
            for aoe in self.aoe:
                pg.draw.circle(self.screen, CYAN, self.camera.apply_rect(aoe.rect).center, aoe.radius, 1)

        # pg.draw.rect(self.screen, WHITE, self.player.hit_rect, 2)
        if self.night:
            self.render_fog()
        # HUD functions
        draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)
        if not self.boss:
            self.draw_text('Zombies: {}'.format(len(self.mobs)), self.hud_font, 30, WHITE, WIDTH - 10, 10, align="ne")
        if self.paused:
            self.screen.blit(self.dim_screen, (0, 0))
            self.draw_text("Paused", self.title_font, 105, RED, WIDTH / 2, HEIGHT / 2, align="center")
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug
                if event.key == pg.K_p:
                    self.paused = not self.paused
                    if self.paused:
                        pg.mixer.music.pause()
                        pg.mixer.pause()
                        self.pause_music.play(-1)
                        pg.mixer.music.set_volume(0.5)
                        pg.mouse.set_visible(True)
                    else:
                        pg.mixer.music.unpause()
                        pg.mixer.unpause()
                        self.pause_music.stop()
                        if self.boss:
                            pg.mixer.music.set_volume(0.3)
                        else:
                            pg.mixer.music.set_volume(1)
                        pg.mouse.set_visible(False)
                if event.key == pg.K_n:
                    self.night = not self.night
                if event.key == pg.K_SPACE:
                    if not self.paused:
                        self.player_img_idx = (self.player_img_idx + 1) % len(PLAYER_SKINS)
                if event.key == pg.K_e:
                    if self.player_inv.active:
                        self.player_inv.slide_out(90)
                    else:
                        self.player_inv.slide_in()

    def show_start_screen(self):
        self.screen.fill(BLACK)
        self.draw_text("ZOMBIES", self.title_font, 100, RED, WIDTH / 2, HEIGHT * 1 / 4, align="center")
        self.draw_text("Arrow keys to move / Click to shoot", self.title_font, 40, WHITE, WIDTH / 2, HEIGHT / 2, align="center")
        self.draw_text("Press a key to start", self.title_font, 75, WHITE, WIDTH / 2, HEIGHT * 3 / 4, align="center")
        pg.display.flip()
        pg.mixer.music.load(path.join(self.music_folder, INTRO_MUSIC))
        pg.mixer.music.play(loops=-1)
        self.wait_for_key()

    def show_go_screen(self):
        pg.mixer.stop()
        pg.mixer.music.set_volume(1)
        pg.mouse.set_visible(True)
        self.screen.fill(BLACK)
        if self.win:
            self.draw_text("YOU SURVIVED", self.title_font, 100, GREEN, WIDTH / 2, HEIGHT / 2, align="center")
            self.zombie_hit_sounds[0].play()
            pg.mixer.music.load(path.join(self.music_folder, WIN_MUSIC))
        else:
            self.draw_text("GAME OVER", self.title_font, 100, RED, WIDTH / 2, HEIGHT / 2, align="center")
            self.effects_sounds['game_over'].play()
            pg.mixer.music.load(path.join(self.music_folder, LOSE_MUSIC))
        self.draw_text("Press a key to play again", self.title_font, 75, WHITE, WIDTH / 2, HEIGHT * 3 / 4, align="center")
        pg.display.flip()
        pg.mixer.music.play(loops=-1)
        self.wait_for_key()

    def wait_for_key(self):
        # wait until all keys are released
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            pg.event.get()
            keys = str(pg.key.get_pressed())
            if "True" not in keys:
                waiting = False
        # check if a key is pressed
        pg.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
