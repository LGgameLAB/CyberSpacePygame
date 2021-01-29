import pygame
from stgs import *

class collider(pygame.sprite.Sprite):
    color = (255, 255, 255)

    def __init__(self, rect, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(rect)

        for k, v in kwargs.items():
            self.__dict__[k] = v

        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.fill(self.color)

class door(pygame.sprite.Sprite):
    color = (255, 255, 255)

    def __init__(self, game, rect, **kwargs):
        self.groups = game.sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.rect = pygame.Rect(rect)

        for k, v in kwargs.items():
            self.__dict__[k] = v

        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.fill(self.color)

class key(pygame.sprite.Sprite):
    color = (255, 255, 255)

    def __init__(self, game, pos, image, **kwargs):
        self.groups = game.sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        for k, v in kwargs.items():
            self.__dict__[k] = v

        self.image = pygame.image.load(image)
        self.pos = pygame.Vector2(pos)
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.image.get_width(), self.image.get_height())

def key1(game, pos):
    return key(game, pos, asset('objects/decryptor.png'))
