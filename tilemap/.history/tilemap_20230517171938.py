import pygame as pg
from settings import *
import pytmx
import math

def collide_hit_rect(one, two):
    try:
        return one.hit_rect.colliderect(two.hit_rect)
    except:
        try:
            return one.hit_rect.colliderect(two.rect)
        except:
            return one.rect.colliderect(two.rect)

class Map:
    def __init__(self, filename):
        self.data = []
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line.strip())

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE

class TiledMap:
    def __init__(self, filename):
        tm = pytmx.load_pygame(filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm

    def render(self, surface):
        ti = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = ti(gid)
                    if tile:
                        surface.blit(tile, (x * self.tmxdata.tilewidth,
                                            y * self.tmxdata.tileheight))

    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface

class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.pos = vec(0, 0)
        self.width = width
        self.height = height
        self.shaking = False

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):
        self.pos.x = -target.rect.centerx + int(WIDTH / 2)
        self.pos.y = -target.rect.centery + int(HEIGHT / 2)

        # limit scrolling to map size
        self.pos.x = min(0, self.pos.x)  # left
        self.pos.y = min(0, self.pos.y)  # top
        self.pos.x = max(-(self.width - WIDTH), x)  # right
        self.pos.y = max(-(self.height - HEIGHT), y)  # bottom
        shake_amount = 0
        if self.shaking:
            t = pg.time.get_ticks() / 1000
            shake_amount = math.exp(-t) * math.cos(2 * math.pi * t)
            if abs(shake_amount) < 1:
                shake_amount = 0
                self.shaking = False
        self.camera = pg.Rect(self.pos.x + shake_amount, self.pos.y + shake_amount, self.width, self.height)
    
    def shake(self):
        self.shaking = True