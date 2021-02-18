import pygame
import math
import random
from stgs import *
from animations import *

class enemy(pygame.sprite.Sprite):
    pos = pygame.Vector2((0, 0))
    moveType = 1
    health = 20
    damage = 5
    points = 5
    color = False
    imgSheet = {'tileWidth': 32 ,'r': pygame.surface.Surface((32,32))}
    vel = 5
    startDir = (0, 0)
    def __init__(self, game, startPos, **kwargs):
        self.groups = game.sprites, game.enemies, game.layer2
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.game = game
        for k, v in kwargs.items():
            self.__dict__[k] = v

        
        self.loadAnimations()
        self.width = self.imgSheet['tileWidth']
        self.height = self.imgSheet['tileWidth']
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.imgSheet['tileWidth'], self.imgSheet['tileWidth'])
        

        self.pos = pygame.Vector2((startPos[0], startPos[1]))
        self.dir = pygame.Vector2(self.startDir)
        
    
    def loadAnimations(self):
        self.animations = animation(self)

    def update(self):
        if self.moveType == 1:
            self.move1()
        elif self.moveType == 2:
            self.move2()

        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)
        if self.health <= 0:
            self.kill()
        
        self.animations.update()

    ## Vertical or horizontal movement
    def move1(self):
        testVec = pygame.Vector2((self.pos.x, self.pos.y))
        if self.collideCheck(testVec + (self.dir*self.vel)):
            if not self.dir.x == 0:
                self.dir = pygame.Vector2((-self.dir.x, 0))
            elif not self.dir.y == 0:
                self.dir = pygame.Vector2((0, -self.dir.y))

        self.pos += self.dir *self.vel 
    
    ## Bounces off walls
    def move2(self):
        testVec = pygame.Vector2((self.pos.x, self.pos.y))
        if self.collideCheck(pygame.Vector2(testVec.x+(self.dir.x*self.vel), testVec.y)):
            
            if self.dir.x > 0:
                self.dir = self.dir.reflect((-1,0))
            else:
                self.dir = self.dir.reflect((1,0))
        
        self.pos.x += self.dir.x*self.vel
        
        if self.collideCheck(pygame.Vector2(testVec.x, testVec.y+(self.dir.y*self.vel))):
            if self.dir.y > 0:
                self.dir = self.dir.reflect((0, -1))
            else:
                self.dir = self.dir.reflect((0, 1))
        
        self.pos.y += self.dir.y*self.vel
        

    def collideCheck(self, vector):
        returnVal = False
    
        testRect = pygame.Rect(round(vector.x), round(vector.y), self.rect.width, self.rect.height)
        for obj in self.game.colliders:
            if testRect.colliderect(obj.rect):
                returnVal = True
            
        return returnVal
        
def bit01(game, pos, vertical):
    if vertical:
        return enemy(game, pos, health=2, imgSheet ={'tileWidth': 32, 'r': asset('enemies/bit01.png')}, startDir=(0, random.randrange(-1, 1+1, 2)))
    else:
        return enemy(game, pos, health=2, imgSheet ={'tileWidth': 32, 'r': asset('enemies/bit01.png')}, startDir=(random.randrange(-1, 1+1, 2), 0))
    
def bit02(game, pos):
    return enemy(game, pos, health = 5, imgSheet = {'tileWidth': 32, 'r': asset('enemies/bit02.png')}, moveType = 2, vel = 10, startDir = pygame.Vector2(1, 0).rotate(random.randint(1, 360)))