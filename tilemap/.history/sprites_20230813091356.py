from typing import Any
import pygame as pg
import math
from random import uniform, choice, randint, random
from settings import *
from tilemap import collide_hit_rect
import pytweening as tween
from itertools import chain
vec = pg.math.Vector2

def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            try:
                if hits[0].hit_rect.centerx > sprite.hit_rect.centerx:
                    sprite.pos.x = hits[0].hit_rect.left - sprite.hit_rect.width / 2 - 1
                if hits[0].hit_rect.centerx < sprite.hit_rect.centerx:
                    sprite.pos.x = hits[0].hit_rect.right + sprite.hit_rect.width / 2
            except:
                if hits[0].rect.centerx > sprite.hit_rect.centerx:
                    sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2 - 1
                if hits[0].rect.centerx < sprite.hit_rect.centerx:
                    sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            if isinstance(sprite, Bullet):
                if sprite.weapon_name == 'grenade':
                    if not sprite.detonating:
                        if hits[0] in sprite.game.breakables:
                            choice(sprite.game.breakable_hit_sounds).play()
                        sprite.spawn_time = pg.time.get_ticks()
                        sprite.detonating = True
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
            if isinstance(sprite, Mob):
                if not sprite.following:
                    if sprite.vel.y == 0:
                        orig_hit_centy = sprite.hit_rect.centery
                        sprite.hit_rect.centery -= 10
                        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
                        if hits:
                            sprite.target_rot = -90
                        else:
                            sprite.hit_rect.centery = orig_hit_centy + 10
                            hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
                            if hits:
                                sprite.target_rot = 90
                            else:
                                sprite.target_rot = choice([-1, 1]) * 90
                        sprite.hit_rect.centery = orig_hit_centy
                    else:
                        sprite.target_rot = sprite.vel.y / abs(sprite.vel.y) * -90
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            try:
                if hits[0].hit_rect.centery > sprite.hit_rect.centery:
                    sprite.pos.y = hits[0].hit_rect.top - sprite.hit_rect.height / 2 - 1
                if hits[0].hit_rect.centery < sprite.hit_rect.centery:
                    sprite.pos.y = hits[0].hit_rect.bottom + sprite.hit_rect.height / 2
            except:
                if hits[0].rect.centery > sprite.hit_rect.centery:
                    sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2 - 1
                if hits[0].rect.centery < sprite.hit_rect.centery:
                    sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            if isinstance(sprite, Bullet):
                if sprite.weapon_name == 'grenade':
                    if not sprite.detonating:
                        if hits[0] in sprite.game.breakables:
                            choice(sprite.game.breakable_hit_sounds).play()
                        sprite.spawn_time = pg.time.get_ticks()
                        sprite.detonating = True
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y
            if isinstance(sprite, Mob):
                if not sprite.following:
                    if sprite.vel.x == 0:
                        orig_hit_centx = sprite.hit_rect.centerx
                        sprite.hit_rect.centerx -= 10
                        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
                        if hits:
                            sprite.target_rot = 0
                        else:
                            sprite.hit_rect.centerx = orig_hit_centx + 10
                            hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
                            if hits:
                                sprite.target_rot = 180
                            else:
                                sprite.target_rot = choice([-1, 1]) * 180
                        sprite.hit_rect.centerx = orig_hit_centx
                    else:
                        sprite.target_rot = sprite.vel.x / abs(sprite.vel.x) * -90 + 90

def collide_line_rect(line, rect):
    """ Get the list of points where the line and rect intersect. The result may be zero, one or two points.

        BUG: This function fails when the line and the side of the rectangle overlap """

    def lines_are_parallel(x1, y1, x2, y2, x3, y3, x4, y4):
        """ Return True if the given lines (x1, y1) - (x2, y2) and (x3, y3) - (x4, y4) are parallel """
        return (((x1 - x2) * (y3 - y4)) - ((y1 - y2) * (x3 - x4)) == 0)

    def intersection_point(x1, y1, x2, y2, x3, y3, x4, y4):
        """ Return the point where the lines through (x1, y1) - (x2, y2) and (x3, y3) - (x4, y4) cross. This may not be on-screen """
        # Use determinant method, as per
        # Ref: https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection
        px = ((((x1 * y2) - (y1 * x2)) * (x3 - x4)) - ((x1 - x2) * ((x3 * y4) - (y3 * x4)))) / (((x1 - x2) * (y3 - y4)) - ((y1 - y2) * (x3 - x4)))
        py = ((((x1 * y2) - (y1 * x2)) * (y3 - y4)) - ((y1 - y2) * ((x3 * y4) - (y3 * x4)))) / (((x1 - x2) * (y3 - y4)) - ((y1 - y2) * (x3 - x4)))
        return px, py

    # Begin the intersection tests
    result = []
    line_x1, line_y1, line_x2, line_y2 = line # split into components
    pos_x, pos_y, width, height = rect

    # Convert the rectangle into 4 lines
    rect_lines = [(pos_x, pos_y, pos_x + width, pos_y), (pos_x, pos_y + height, pos_x + width, pos_y + height), # top & bottom
                  (pos_x, pos_y, pos_x, pos_y + height), (pos_x + width, pos_y, pos_x + width, pos_y + height)] # left & right

    # intersect each rect-side with the line
    for r in rect_lines:
        rx1, ry1, rx2, ry2 = r
        if not lines_are_parallel(line_x1, line_y1, line_x2, line_y2, rx1, ry1, rx2, ry2):       # not parallel
            px, py = intersection_point(line_x1, line_y1, line_x2, line_y2, rx1, ry1, rx2, ry2) # so intersecting somewhere
            px = round(px)
            py = round(py)
            # Lines intersect, but is on the rectangle, and between the line end-points?
            try:
                if rect.collidepoint(px, py) and px >= min(line_x1, line_x2) and px <= max(line_x1, line_x2) and py >= min(line_y1, line_y2) and py <= max(line_y1, line_y2):
                    result.append((px, py)) # keep it
                    if (len(result) == 2):
                        break # Once we've found 2 intersection points, that's it
            except:
                pass
    return result

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.abs_pos = self.pos
        self.rot = 0
        self.last_shot = 0
        self.reload_state_start = 0
        self.health = PLAYER_HEALTH
        self.weapon = 'pistol'
        self.active_slot = 1
        self.weapon_clips = [WEAPONS[self.weapon]['clip_size']]
        self.state = 'gun'
        self.reload_state = None
        self.reloaded = False
        self.damaged = False

    def get_keys(self):
        self.rot_speed = 0
        self.vel = vec(0, 0)
        mouse_pos = pg.mouse.get_pos()
        angle = (180 / math.pi) * -math.atan2(mouse_pos[1] - self.abs_pos.y, mouse_pos[0] - self.abs_pos.x)
        self.rot = angle
        keys = pg.key.get_pressed()
        joy_x = (keys[pg.K_RIGHT] or keys[pg.K_d]) - (keys[pg.K_LEFT] or keys[pg.K_a])
        joy_y = (keys[pg.K_DOWN] or keys[pg.K_s]) - (keys[pg.K_UP] or keys[pg.K_w])
        self.vel.x = PLAYER_SPEED * joy_x
        self.vel.y = PLAYER_SPEED * joy_y
        if joy_x != 0 and joy_y != 0:
            self.vel = self.vel.normalize() * PLAYER_SPEED
        if pg.mouse.get_pressed()[0]:
            if self.game.player_inv.hover:
                self.equip_weapon(self.game.player_inv.hover)
            else:
                if self.weapon and not self.reload_state:
                    self.shoot()
        if keys[pg.K_1]:
            self.equip_weapon(1)
        if keys[pg.K_2]:
            self.equip_weapon(2)
        if keys[pg.K_3]:
            self.equip_weapon(3)
        if keys[pg.K_4]:
            self.equip_weapon(4)
        if keys[pg.K_5]:
            self.equip_weapon(5)
        if keys[pg.K_6]:
            self.equip_weapon(6)

    def equip_weapon(self, slot):
        if not self.reload_state:
            self.active_slot = slot
            curr_weapon = self.weapon
            try:
                self.weapon = self.game.weapons_list[slot - 1]
                self.game.camera.mouse_limit = WEAPONS[self.weapon]['look_dist']
                self.state = WEAPONS[self.weapon]['state']
                if self.weapon != curr_weapon:
                    if self.weapon == 'grenade':
                        self.game.effects_sounds['item_pickup'].play()
                    else:
                        self.game.effects_sounds['gun_pickup'].play()
            except:
                self.weapon = ''
                self.game.camera.mouse_limit = 0
                self.state = 'stand'

    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > WEAPONS[self.weapon]['rate']:
            self.last_shot = now
            if self.game.player_inv.active_item[1] > 0 or self.weapon == 'pistol':
                dir = vec(1, 0).rotate(-self.rot)
                pos = self.pos + BARREL_OFFSET.rotate(-self.rot)
                self.pos += vec(-WEAPONS[self.weapon]['kickback'], 0).rotate(-self.rot) * self.game.dt
                for _ in range(WEAPONS[self.weapon]['bullet_count']):
                    spread = uniform(-WEAPONS[self.weapon]['spread'], WEAPONS[self.weapon]['spread'])
                    Bullet(self.game, pos, dir.rotate(spread), WEAPONS[self.weapon]['damage'])
                    snd = choice(self.game.weapon_sounds[self.weapon])
                    if snd.get_num_channels() > 2:
                        snd.stop()
                    snd.play()
                if self.weapon == 'grenade':
                    self.game.player_inv.remove_item(1, self.game.player_inv.active_pos)
                    if self.game.player_inv.active_item[1] == 0:
                        self.game.weapons_list[self.active_slot - 1] = ''
                        self.weapon = ''
                else:
                    MuzzleFlash(self.game, pos)
                    self.game.player_inv.remove_item(1, self.game.player_inv.active_pos, False)
                self.weapon_clips[self.active_slot - 1] -= 1
                if self.weapon_clips[self.active_slot - 1] == 0:
                    if self.game.player_inv.active_item[1] > 0 or self.weapon == 'pistol':
                        self.reload_state = 'begin'
                        self.reload_state_start = pg.time.get_ticks()
            else:
                self.game.effects_sounds['gun_empty'].play()
    
    def reload(self):
        self.state = 'reload'
        self.reload_state = 'reload'
        self.reload_state_start = pg.time.get_ticks()
        self.weapon_clips[self.active_slot - 1] = WEAPONS[self.weapon]['clip_size']

    def add_ammo(self):
        self.game.player_inv.add_item([InvItem(self.game, self.weapon), WEAPONS[self.weapon]['clip_size']], self.game.player_inv.active_pos)

    def hit(self):
        self.damaged = True
        self.damage_alpha = chain(DAMAGE_ALPHA * 4)

    def update(self):
        self.get_keys()
        if self.reload_state:
            now = pg.time.get_ticks()
            if self.reload_state == 'begin':
                if now - self.reload_state_start > WEAPONS[self.weapon]['reload_delay']:
                    self.reload()
            elif self.reload_state == 'reload':
                if now - self.reload_state_start > WEAPONS[self.weapon]['reload_rate']:
                    self.state = WEAPONS[self.weapon]['state']
                    self.reload_state = 'end'
                    self.reload_state_start = pg.time.get_ticks()
                elif now - self.reload_state_start > WEAPONS[self.weapon]['reload_rate'] / 2 and not self.reloaded:
                    self.game.effects_sounds['gun_reload'].play()
                    self.reloaded = True
            elif self.reload_state == 'end':
                if now - self.reload_state_start > WEAPONS[self.weapon]['reload_delay']:
                    self.reload_state = None
                    self.reloaded = False
        self.image = pg.transform.rotate(self.game.player_img, self.rot)
        if self.damaged:
            try:
                self.image.fill((255, 255, 255, next(self.damage_alpha)), special_flags=pg.BLEND_RGBA_MULT)
            except:
                self.damaged = False
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center

    def add_health(self, amount):
        self.health += amount
        if self.health > PLAYER_HEALTH:
            self.health = PLAYER_HEALTH

class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.mob_img.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.orig_width = self.rect.width
        self.orig_height = self.rect.height
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = uniform(-180, 180)
        self.target_rot = self.rot
        self.health = MOB_HEALTH
        self.max_health = MOB_HEALTH
        self.health_col = (0, 0, 0)
        self.max_speed = choice(MOB_SPEEDS)
        self.idle_speed = MOB_IDLE_SPEED
        self.speed = self.idle_speed
        self.target = game.player
        self.detect_radius = DETECT_RADIUS
        self.avoid_radius = AVOID_RADIUS
        self.aggro = False
        self.following = False
        self.wait = uniform(60, 200)
        self.iter = 0
        self.walking = False
        self.moan_sounds = self.game.zombie_moan_sounds

    def avoid_mobs(self):
        for mob in self.game.mobs:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < self.avoid_radius:
                    self.acc += dist.normalize()

    def detect_bullet(self):
        self.aggro = True
        target_dist = self.target.pos - self.pos
        self.target_rot = target_dist.angle_to(vec(1, 0)) + uniform(-10, 10)
        self.speed = self.max_speed
        self.iter = 0
        self.wait = 180

    def update(self):
        target_dist = self.target.pos - self.pos
        if self.target_rot < 0:
                self.target_rot += 360
        if self.rot - self.target_rot > 180:
            self.rot -= 360
        elif self.rot - self.target_rot < -180:
            self.rot += 360
        self.rot = pg.math.lerp(self.rot, self.target_rot, 0.08)
        self.image = pg.transform.rotate(self.game.mob_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.hit_rect.center
        intersections = 0
        if target_dist.length_squared() < self.detect_radius**2:
            for wall in self.game.walls:
                try:
                    hit_rect = wall.hit_rect
                except:
                    hit_rect = wall.rect
                intersections += len(collide_line_rect((self.pos.x, self.pos.y, self.target.pos.x, self.target.pos.y), hit_rect))
                if intersections > 0:
                    break
        if target_dist.length_squared() < self.detect_radius**2 and intersections == 0:
            if not self.following:
                self.following = True
                if not self.aggro:
                    self.vel = vec(0, 0)
            self.aggro = False
            self.speed = self.max_speed
            if random() < 0.002:
                choice(self.moan_sounds).play()
                if isinstance(self, Boss):
                    if self.spawning:
                        self.spawn(4)
            self.target_rot = target_dist.angle_to(vec(1, 0))
            self.acc = vec(1, 0).rotate(-self.rot)
            self.avoid_mobs()
            if self.acc != vec(0, 0):
                self.acc.scale_to_length(self.speed)
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            if self.iter > 0:
                self.iter = 0
                self.walking = False
                self.wait = uniform(60, 200)
        else:
            self.following = False
            if self.aggro:
                if self.iter < self.wait:
                    self.acc = vec(1, 0).rotate(-self.target_rot)
                    self.avoid_mobs()
                    if self.acc != vec(0, 0):
                        self.acc.scale_to_length(self.speed)
                    self.acc += self.vel * -1
                    self.vel += self.acc * self.game.dt
                    self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
                    self.iter += 1
                else:
                    self.aggro = False
                    self.iter = 0
                    self.walking = False
                    self.wait = uniform(60, 200)
            else:
                self.speed = self.idle_speed
                if self.iter < self.wait:
                    if self.walking:
                        if self.iter == 0:
                            self.target_rot = uniform(-180, 180)
                            self.vel = vec(0, 0)
                        self.acc = vec(1, 0).rotate(-self.target_rot)
                        self.avoid_mobs()
                        if self.acc != vec(0, 0):
                            self.acc.scale_to_length(self.speed)
                        self.acc += self.vel * -1
                        self.vel += self.acc * self.game.dt
                        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
                    else:
                        self.vel = vec(0, 0)
                    self.iter += 1
                else:
                    self.iter = 0
                    self.walking = bool(randint(0, 1))
                    if self.walking:
                        self.wait = uniform(120, 420)
                    else:
                        self.wait = uniform(60, 200)
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        if self.health <= 0:
            choice(self.game.zombie_hit_sounds).play()
            self.kill()
            splat_size = self.orig_height * 64/43
            self.game.map_img.blit(pg.transform.scale(self.game.splat, (splat_size, splat_size)), self.pos - vec(splat_size / 2, splat_size / 2))

    def draw_health(self):
        if self.health > self.max_health * 3/5:
            self.health_col = DARKGREEN
        elif self.health > self.max_health * 3/10:
            self.health_col = YELLOW
        else:
            self.health_col = RED
        if self.health < self.max_health:
            self.health_surf = pg.Surface((self.rect.width + 20, self.rect.height + 20))
            self.health_surf.set_colorkey((0, 0, 0))
            self.health_rect = self.health_surf.get_rect()
            pos_rect = pg.Rect(self.rect.centerx - self.health_rect.width / 2, self.rect.centery - self.health_rect.height / 2, self.health_rect.width, self.health_rect.height)
            width = int(self.orig_width * self.health / self.max_health)
            self.health_bar = pg.Rect((self.health_rect.width - self.orig_width) / 2, (self.health_rect.height - self.orig_height) / 2, width, 7)
            pg.draw.rect(self.health_surf, self.health_col, self.health_bar)
            self.game.screen.blit(self.health_surf, self.game.camera.apply_rect(pos_rect))

class Boss(Mob):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.health = BOSS_HEALTH
        self.image = pg.transform.scale(self.game.mob_img, (100, 123))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = BOSS_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.orig_width = self.rect.width
        self.orig_height = self.rect.height
        self.max_health = BOSS_HEALTH
        self.max_speed = BOSS_SPEED
        self.idle_speed = BOSS_IDLE_SPEED
        self.speed = self.idle_speed
        self.detect_radius = float('inf')
        self.avoid_radius = BOSS_AVOID_RADIUS
        self.moan_sounds = self.game.boss_moan_sounds
        self.tick = 0
        self.spawning = False
    
    def update(self):
        super().update()
        self.image = pg.transform.rotate(pg.transform.scale(self.game.mob_img, (100, 100)), self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.hit_rect.center
        if self.health < self.max_health:
            if self.tick == 0:
                self.health += 5
                if self.health > self.max_health:
                    self.health = self.max_health
            if self.health < 0.75 * self.max_health:
                self.spawning = True
            else:
                self.spawning = False
        self.tick = (self.tick + 1) % (FPS / 2)

    def spawn(self, amount):
        for _ in range(amount):
            Mob(self.game, self.pos.x, self.pos.y)

    def draw_health(self):
        super().draw_health()
        max_width = 300
        height = 20
        width = int(max_width * self.health / self.max_health)
        x = (WIDTH - max_width) / 2
        y = 10
        big_health = pg.Rect(x, y, width, height)
        outline_rect = pg.Rect(x, y, max_width, height)
        pg.draw.rect(self.game.screen, LIGHTGREY, outline_rect, 0, 7)
        pg.draw.rect(self.game.screen, self.health_col, big_health, 0, 7)
        pg.draw.rect(self.game.screen, WHITE, outline_rect, 2, 7)
        self.game.draw_text('ZOMBIE KING', self.game.hud_font, 30, WHITE, WIDTH / 2, 50, align="center")

class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, dir, damage):
        self._layer = BULLET_LAYER
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.weapon = WEAPONS[game.player.weapon]
        self.weapon_name = game.player.weapon
        self.size = self.weapon['bullet_size']
        self.aoe_size = self.weapon['aoe_size']
        self.image = game.bullet_images[self.size]
        self.rect = self.image.get_rect()
        if self.size == 'sm':
            self.hit_rect = BULLET_HIT_RECT_SM.copy()
        elif self.size == 'lg':
            self.hit_rect = BULLET_HIT_RECT_LG.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(pos)
        self.rect.center = pos
        # spread = uniform(-GUN_SPREAD, GUN_SPREAD)
        self.speed = self.weapon['bullet_speed'] * uniform(0.9, 1.1)
        self.dir = dir
        self.vel = self.dir * self.speed
        self.spawn_time = pg.time.get_ticks()
        self.detonating = False
        self.damage = damage
        self.aoe_damage = self.weapon['aoe_damage']
        self.lifetime = self.weapon['bullet_lifetime']

    def update(self):
        if self.weapon_name == 'grenade':
            if self.detonating:
                self.vel = vec(0, 0)
                if pg.time.get_ticks() - self.spawn_time > 1000:
                    self.destroy()
            else:
                self.vel = self.dir * self.speed * (1 - (pg.time.get_ticks() - self.spawn_time) / self.lifetime)
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        if self.weapon_name == 'grenade':
            self.hit_rect.centerx = self.pos.x
            collide_with_walls(self, self.game.walls, 'x')
            self.hit_rect.centery = self.pos.y
            collide_with_walls(self, self.game.walls, 'y')
        else:
            self.hit_rect.center = self.pos
            for hit in pg.sprite.spritecollide(self, self.game.walls, False, collide_hit_rect):
                if hit not in self.game.breakables:
                    self.destroy()
        if pg.time.get_ticks() - self.spawn_time > self.lifetime:
            if self.weapon_name == 'grenade':
                if not self.detonating:
                    self.spawn_time = pg.time.get_ticks()
                    self.detonating = True
            else:
                self.destroy()
    
    def destroy(self):
        if self.aoe_size > 0:
            AOE(self.game, self.pos, self.aoe_size, self.aoe_damage, self.weapon_name)
        self.kill()

class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

class AOE(pg.sprite.Sprite):
    def __init__(self, game, pos, radius, dmg, weapon):
        self._layer = BULLET_LAYER
        self.groups = game.all_sprites, game.aoe
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(0, 0, radius * 2, radius * 2)
        self.radius = radius
        self.pos = pos
        self.rect.center = pos
        self.damage = dmg
        self.weapon = weapon
        self.spawn_time = pg.time.get_ticks()
        Explosion(self.game, self.pos, self.radius)
    
    def update(self):
        if pg.time.get_ticks() - self.spawn_time > FLASH_DURATION:
            self.kill()

class Explosion(pg.sprite.Sprite):
    def __init__(self, game, pos, radius):
        self._layer = EFFECTS_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rot = randint(0, 360)
        self.image = pg.transform.rotate(pg.transform.scale(game.explosion_imgs[0], (radius * 2, radius * 2)), self.rot)
        self.rect = self.image.get_rect()
        self.radius = radius
        self.pos = pos
        self.rect.center = pos
        self.frame = 0
        self.game.effects_sounds['explosion'].play()
        angle = math.atan2(self.game.player.pos.y - self.pos.y, self.game.player.pos.x - self.pos.x)
        self.game.camera.shake(angle)

    def update(self):
        try:
            self.image = pg.transform.rotate(pg.transform.scale(self.game.explosion_imgs[math.floor(self.frame)], (self.radius * 2, self.radius * 2)), self.rot)
            self.rect.center = self.pos
            self.frame += 0.5
        except:
            self.kill()

class MuzzleFlash(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self._layer = EFFECTS_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        size = randint(20, 50)
        self.image = pg.transform.scale(choice(game.gun_flashes), (size, size))
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = pos
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        if pg.time.get_ticks() - self.spawn_time > FLASH_DURATION:
            self.kill()

class Item(pg.sprite.Sprite):
    def __init__(self, game, pos, type):
        self._layer = ITEMS_LAYER
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.item_images[type]
        self.rect = self.image.get_rect()
        self.hit_rect = self.rect
        self.type = type
        self.pos = pos
        self.rect.center = pos
        self.tween = tween.easeInOutSine
        self.step = 0
        self.dir = 1

    def update(self):
        # bobbing motion
        offset = BOB_RANGE * (self.tween(self.step / BOB_RANGE) - 0.5)
        self.rect.centery = self.pos.y + offset * self.dir
        self.step += BOB_SPEED
        if self.step > BOB_RANGE:
            self.step = 0
            self.dir *= -1

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = WALL_LAYER
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wall_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Breakable(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h, image, health, drop):
        self._layer = BREAKABLE_LAYER
        self.groups = game.all_sprites, game.breakables, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = image.copy()
        self.orig_image = image.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.hit_rect = pg.Rect(0, 0, w, h)
        self.hit_rect.center = self.rect.center
        self.health = health
        self.max_health = health
        self.drop = []
        self.arrow = None
        if drop:
            self.arrow = Arrow(game, vec(self.rect.x + self.rect.w / 2, self.rect.y - 10))
            drops = DROPS.copy()
            self.drop.append(drops.pop(randint(0, len(drops) - 1)))
            if w >= 48:
                self.drop.append(choice(drops))
    
    def update(self):
        if self.health <= 0:
            choice(self.game.break_sounds).play()
            if self.drop:
                self.arrow.kill()
                for i in range(len(self.drop)):
                    Item(self.game, vec(self.rect.centerx + i * 20 - (len(self.drop) - 1) * 10, self.rect.centery + i * 20 - (len(self.drop) - 1) * 10), self.drop[i])
            self.kill()
    
    def draw_health(self):
        if self.health > self.max_health * 3/5:
            col = GREEN
        elif self.health > self.max_health * 3/10:
            col = YELLOW
        else:
            col = RED
        width = int(self.rect.width * self.health / self.max_health)
        self.health_bar = pg.Rect(0, 0, width, 7)
        if self.health < self.max_health:
            self.image = self.orig_image.copy()
            pg.draw.rect(self.image, col, self.health_bar)

class Arrow(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self._layer = EFFECTS_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.arrow.copy()
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = pos
        self.tween = tween.easeInOutSine
        self.step = 0
        self.dir = 1
    
    def update(self):
        offset = ARROW_BOB_RANGE * (self.tween(self.step / ARROW_BOB_RANGE) - 0.5)
        self.rect.centery = self.pos.y + offset * self.dir
        self.step += BOB_SPEED
        if self.step > ARROW_BOB_RANGE:
            self.step = 0
            self.dir *= -1

class Sparkle(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self._layer = EFFECTS_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rot = randint(-180, 180)
        self.size = randint(100, 120)
        self.image = pg.transform.rotate(pg.transform.scale(game.sparkle_imgs[0], (self.size, self.size)), self.rot)
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = pos
        self.frame = 0
    
    def update(self):
        try:
            self.image = pg.transform.rotate(pg.transform.scale(self.game.sparkle_imgs[self.frame], (self.size, self.size)), self.rot)
        except:
            self.kill()
        self.rect.center = self.pos
        self.frame += 1

class InvItem:
    def __init__(self, game, type):
        self.type = type
        self.surface = game.item_images[type]

    def resize(self, bw, bh):
        iw, ih = self.surface.get_size()
        if iw > ih:
            # fit to width
            scale_factor = bw / float(iw)
            sh = scale_factor * ih
            if sh > bh:
                scale_factor = bh / float(ih)
                sw = scale_factor * iw
                sh = bh
            else:
                sw = bw
        else:
            # fit to height
            scale_factor = bh / float(ih)
            sw = scale_factor * iw
            if sw > bw:
                scale_factor = bw / float(iw)
                sw = bw
                sh = scale_factor * ih
            else:
                sh = bh

        return pg.transform.scale(self.surface, (sw, sh))

class Inventory(pg.sprite.Sprite):
    def __init__(self, game, x, y, rows, col):
        self._layer = UI_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rows = rows
        self.col = col
        self.items = [[None for _ in range(self.rows)] for _ in range(self.col)]
        self.box_size = 40
        self.x = x
        self.y = y
        self.orig_x = x
        self.orig_y = y
        self.vel = vec(0, 0)
        self.border = 3
        self.image = pg.surface.Surface(((self.box_size + self.border) * self.col + self.border, (self.box_size + self.border) * self.rows + self.border), pg.SRCALPHA)
        self.image.set_alpha(230)
        self.rect = self.image.get_rect()
        self.rect.topleft = vec(self.x, self.y)
        self.font = pg.font.Font(self.game.hud_font, 14)
        self.hover = None
        self.slide_speed = 10
        self.slide_dir = 0
        self.active = True
        self.active_pos = (0, 0)
        self.active_item = None

    def update(self):
        self.hover = None
        self.x += self.vel.x
        self.y += self.vel.y
        self.rect.topleft = vec(self.x, self.y)
        if not self.game.screen.get_rect().colliderect(self.rect) or (self.x == self.orig_x and self.y == self.orig_y):
            self.vel = vec(0, 0)

        # draw background
        pg.draw.rect(self.image, (50, 50, 50), (0, 0, self.rect.w, self.rect.h), 0, 6)
        for x in range(self.col):
            for y in range(self.rows):
                slot_num = 1 + x + self.col * y
                rect = pg.Rect((self.box_size + self.border) * x + self.border * 5 / 4, (self.box_size + self.border) * y + self.border, self.box_size, self.box_size)
                col = (150, 150, 150)
                if self.get_pos() == (x, y):
                    col = (200, 200, 200)
                    self.hover = slot_num
                pg.draw.rect(self.image, col, rect, 0, 3)
                if self.game.player.active_slot == slot_num:
                    self.active_pos = (x, y)
                    self.active_item = self.items[x][y]
                    border_rect = pg.Rect(rect.x - self.border, rect.y - self.border, self.box_size + self.border * 2, self.box_size + self.border * 2)
                    pg.draw.rect(self.image, (230, 230, 230), border_rect, self.border, 6)
                if self.items[x][y]:
                    item_img = self.items[x][y][0].resize(self.box_size, self.box_size)
                    self.image.blit(item_img, (rect.centerx - item_img.get_width() / 2, rect.centery - item_img.get_height() / 2))
                    if self.items[x][y][1] > 0 and not self.items[x][y][0].type == 'pistol':
                        obj = self.font.render(str(self.items[x][y][1]), True, (255, 255, 0))
                        self.image.blit(obj, (rect.x + self.box_size / 2 + 10 - 5 * (len(str(self.items[x][y][1])) - 1), rect.y + self.box_size / 2 + 2))
                slot_text = self.font.render(str(slot_num), True, (0, 0, 0))
                self.image.blit(slot_text, (rect.x + self.box_size / 2 + 10, rect.y - self.box_size / 2 + 17))
    
    def reset(self):
        self.items = [[None for _ in range(self.rows)] for _ in range(self.col)]

    def slide_out(self, dir):
        self.active = False
        self.slide_dir = dir
        self.vel = vec(self.slide_speed, 0).rotate(dir)
    
    def slide_in(self):
        self.active = True
        self.vel = vec(self.slide_speed, 0).rotate(-self.slide_dir)

    # get the square that the mouse is over
    def get_pos(self):
        mouse = pg.mouse.get_pos()

        x = mouse[0] - self.x
        y = mouse[1] - self.y
        x = x // (self.box_size + self.border)
        y = y // (self.box_size + self.border)
        return (x, y)

    # add an item/s
    def add_item(self, InvItem, xy):
        x, y = xy
        if self.items[x][y]:
            if self.items[x][y][0].type == InvItem[0].type:
                self.items[x][y][1] += InvItem[1]
            else:
                temp = self.items[x][y]
                self.items[x][y] = InvItem
                return temp
        else:
            self.items[x][y] = InvItem
    
    # remove an item/s
    def remove_item(self, amount, xy, remove=True):
        x, y = xy
        if self.items[x][y]:
            self.items[x][y][1] -= amount
            if self.items[x][y][1] < 1:
                if remove:
                    self.items[x][y] = None
                else:
                    self.items[x][y][1] = 0

    # check whether the square is in the grid
    def in_grid(self, x, y):
        if 0 > x > self.col-1:
            return False
        if 0 > y > self.rows-1:
            return False
        return True

class Crosshair(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = CROSSHAIR_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rot = randint(-180, 180)
        self.size = randint(100, 120)
        self.image = game.crosshair_imgs[game.player.weapon]
        self.rect = self.image.get_rect()
        self.pos = pg.mouse.get_pos()
        self.rect.center = self.pos
    
    def update(self):
        self.image = self.game.crosshair_imgs[self.game.player.weapon]
        self.rect = self.image.get_rect()
        self.pos = pg.mouse.get_pos()
        self.rect.center = self.pos