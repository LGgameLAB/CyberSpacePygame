import pygame
import math
from stgs import *

class enemy(pygame.sprite.Sprite):
    x = 0
    y = 0
    moveType = 0
    health = 20
    color = False

    def __init__(self, game, image, startPos, **kwargs):
        self.groups = game.sprites, game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.image = pygame.image.load(image)
        self.x, self.y = startPos
        for k, v in kwargs.items():
            self.__dict__[k] = v

        self.rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())
    
    def update(self):
        if self.health <= 0:
            self.kill()

def bit01(game, pos):
    return enemy(game, asset('alien.png'), pos)