import pygame as pg
from settings import *

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

class Camera: # As the player moves around, however much the player moves is the offset. the map is shifted by this offset
    # to reflect the movement of the player
    # The offset is how much the map needs to shift by -- the opposite of where hte player moves
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height) # This rectangle stores how far the player has moved
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target): # Target is the sprite (player) that the camera follows. Camera needs to update by however much the player has moved.
        x = -target.rect.x + int(WIDTH / 2)
        y = -target.rect.y + int(HEIGHT / 2)

        # limit scrolling to map size
        x = min(0, x) # left
        y = min(0, y) # top
        x = max(-(self.width - WIDTH), x) # right
        y = max(-(self.height - HEIGHT), y) # bottom

        self.camera = pg.Rect(x, y, self.width, self.height)