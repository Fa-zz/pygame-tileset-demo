import pygame as pg
from settings import *


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE)) # Square the size of one of the tiles
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect() # We call this because pygame.Surface() does not create a rectangle.
        # get_rect() will create a rectangle at the x,y pos of the object, and from there the x and y of the rect can be
        # moved to move the object
        self.vx, self.vy = (0, 0)
        self.x = x * TILESIZE
        self.y = y * TILESIZE # This x and y keeps track of which grid coordinate we are on

    def get_keys(self): # get keys is checked every frame. vx and vy are set to zero, unless one of the keys is pressed
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -PLAYER_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = PLAYER_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -PLAYER_SPEED
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = PLAYER_SPEED
        if self.vx != 0 and self.vy != 0: # Diagonal movement is no longer as fast as regular movement
            self.vx *= 0.7071
            self.vy *= 0.7071

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits: # If player has hit from x, then player either should be on the right or left side of the object
                if self.vx > 0: # Hit from left
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0: # Hit from right
                    self.x = hits[0].rect.right
                self.vx = 0 # Once player has hit an object, it should stop.
                self.rect.x = self.x # Update the player's location
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits: # If player has hit from x, then player either should be on the top or bottom of the object
                if self.vy > 0: # Hit from top
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0: # Hit from bottom
                    self.y = hits[0].rect.bottom
                self.vy = 0 # Once player has hit an object, it should stop.
                self.rect.y = self.y # Update the player's location

        # for wall in self.game.walls:
        #     if wall.x == self.x + dx and wall.y == self.y + dy:
        #         return False
        # return True

    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

