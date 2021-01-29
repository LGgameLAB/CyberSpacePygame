import pygame
import math
import random
from stgs import *
from animations import *

class enemy(pygame.sprite.Sprite):
    pos = pygame.Vector2((0, 0))
    moveType = 0
    health = 20
    damage = 5
    points = 5
    color = False
    imgSheet = {'active': False, 'tileWidth': 32}
    vel = 5
    startDir = (0, 0)
    def __init__(self, game, image, startPos, **kwargs):
        self.groups = game.sprites, game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.game = game
        for k, v in kwargs.items():
            self.__dict__[k] = v

        if self.imgSheet['active']:
            self.loadAnimations()
            self.width = self.imgSheet['tileWidth']
            self.height = self.imgSheet['tileWidth']
            self.rect = pygame.Rect(self.pos.x, self.pos.y, self.imgSheet['tileWidth'], self.imgSheet['tileWidth'])
        else:
            self.image = pygame.image.load(image)
            self.width = self.image.get_width()
            self.height = self.image.get_height()
            self.rect = pygame.Rect(self.pos.x, self.pos.y, self.image.get_width(), self.image.get_height())

        self.pos = pygame.Vector2((startPos[0], startPos[1]))
        self.dir = pygame.Vector2(self.startDir)
        
    
    def loadAnimations(self):
        self.animations = animation(self)

    def update(self):
        self.move1()
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)
        if self.health <= 0:
            self.kill()
        if self.imgSheet['active']:
            self.animations.update()
    
    def move1(self):
        testVec = pygame.Vector2((self.pos.x, self.pos.y))
        if self.collideCheck(testVec + (self.dir*self.vel)):
            self.dir = pygame.Vector2((-self.dir.x, 0))
        self.pos += self.dir *self.vel 

    def collideCheck(self, vector):
        returnVal = False
    
        testRect = pygame.Rect(round(vector.x), round(vector.y), self.rect.width, self.rect.height)
        for obj in self.game.colliders:
            if testRect.colliderect(obj.rect):
                returnVal = True
            
        return returnVal
def bit01(game, pos):
    return enemy(game, asset('enemies/bit01.png'), pos, health=2, imgSheet ={'active': True,'tileWidth': 32, 'r': asset('enemies/bit01.png')}, startDir=(random.randrange(-1, 1+1, 2), 0))