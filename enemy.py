import pygame
import math
from stgs import *

class enemy(pygame.sprite.Sprite):
    x = 0
    y = 0
    moveType = 0
    color = False

    def __init__(self, image, **kwargs):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(image)

        for k, v in kwargs.items():
            self.__dict__[k] = v

        self.rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())

        