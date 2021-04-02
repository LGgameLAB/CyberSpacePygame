#### Imports ####

import pygame
import math
from stgs import *
from animations import *
from objects import *
#### Player object ####
class player(pygame.sprite.Sprite):
    x = 71
    y = 71
    yModMin = -0.12
    yModMax = 0.25
    hitCooldown = 500
    lastHit = 0
    roomBound = False
    imgSheet = {'active': False, 'tileWidth': 64, 'r': False, 'l': False, 'idleR': False, 'flyR': False, 'flyL': False}
    width, height = 48, 64
    health = 50
    maxHp = 50
    #### Player Initializations ####
    def __init__(self, game, image, name, **kwargs):
        self.groups = game.sprites, game.layer2
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.game = game
        self.image = pygame.image.load(image)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.pos = pygame.math.Vector2(self.x, self.y)
        self.dir = pygame.math.Vector2((0, 0))
        self.vel = 8
        self.fall = 0
        self.yMod = 0
        self.ground = False
        self.gun = standardGun(self.game, self)

        for k, v in kwargs.items():
            self.__dict__[k] = v
        
        self.loadAnimations()
        self.hpBar = healthBar2(self.game, self)

    def loadAnimations(self):
        self.animations = animation(self)

    #### Updates player ####
    def update(self):
        self.move()
        self.rect.topleft = round(self.pos.x), round(self.pos.y)
        self.animations.update()
    
    def takeDamage(self, damage):
        if pygame.time.get_ticks() - self.lastHit >= self.hitCooldown:
            self.health -= damage
            self.lastHit = pygame.time.get_ticks()
    #### Move Physics ####
    def move(self):
        keys = pygame.key.get_pressed()
        self.dir = pygame.math.Vector2((0, 0))

        #### Right movement ####
        if checkKey(keySet['pRight']):
            rightVec = pygame.math.Vector2((1, 0))
            
            if self.collideCheck(self.pos + rightVec*self.vel):
                x=0
                while not self.collideCheck(self.pos + (x*self.vel, 0)):
                    x += 0.05
                if x == 0:
                    self.dir -= (0.00, 0)
                else:
                    self.dir += (x-0.05,0)
            else:
                self.dir += rightVec

        #### Left movement ####
        if checkKey(keySet['pLeft']):
            leftVec = pygame.math.Vector2((-1, 0))
            
            if self.collideCheck(self.pos + leftVec*self.vel):
                self.dir += (0,0)
            else:
                self.dir += leftVec

        
        self.fall = 0.01*self.gravity

        #### Checks top collide ####
        roofCollide = False
        if self.yMod < 0:
            self.ground = False
            upVec = pygame.math.Vector2((0, self.yMod-0.02))
            if self.collideCheck(self.pos + upVec*self.vel ): #, ('u', (self.yMod-0.02)*self.vel)):
                x=0
                while self.collideCheck(self.pos + (0, x*self.vel)):
                    x += 0.01
            
                self.dir += (0, x - 0.0)
                roofCollide = True
                self.yMod = max(0, self.yMod)
        else:
            #### Checks bottom collide ####
            downVec = pygame.math.Vector2((0, self.yMod+self.fall))
            if self.collideCheck(self.pos + downVec*self.vel, 'd'):
                x=0
                while self.collideCheck(self.pos + (0, x*self.vel)):
                    x -= 0.01

                self.dir += (0, x-0.00)
                self.yMod = min(0, self.yMod)
                self.ground = True
            else:
                self.ground = False
        
        #### Falling mechanic ####
        if not self.ground:
            self.yMod = min(self.yModMax, self.yMod+self.fall)


        #### Checks game type for flying or jumping ####
        if platformer:
            if self.ground:
                if checkKey(keySet['pUp']):
                    self.yMod = -0.5 
        else:
            if not roofCollide:
                if checkKey(keySet['pUp']):
                    self.yMod = max(self.yModMin, self.yMod-0.02)

        self.dir += (0, self.yMod*self.vel)
        self.pos += self.dir * self.vel

        if self.roomBound:
            self.pos.x = max(0, self.pos.x)
            self.pos.x = min(winWidth-self.rect.width, self.pos.x)
            self.pos.y = max(0, self.pos.y)
            self.pos.y = min(winHeight-self.rect.height, self.pos.y)

    #### Collide checker for player ####
    def collideCheck(self, vector, *args):
        returnVal = False
        #### Checks for super collision. Not in current use - still needs developing and attempts to fix bug of teleportation through platforms
        if len(args) > 0:
            if args[0] == 'd':
                testRect = pygame.Rect(vector.x, vector.y, self.rect.width, self.rect.height)
                for obj in self.game.colliders:
                    if testRect.colliderect(obj.rect):
                        returnVal = True
                        if isinstance(obj, mPlatform):
                            print(obj.dir)
                            self.dir += (obj.dir * obj.vel)/self.vel
            else:
                arg = args[0]
                colDir = arg[0]
                dist = abs(arg[1])
                x = 0
                while x < dist:
                    if colDir == 'r':
                        testRect = pygame.Rect(round(vector.x) - x, round(vector.y), self.rect.width, self.rect.height)
                    elif colDir == 'l':
                        testRect = pygame.Rect(round(vector.x) + x, round(vector.y), self.rect.width, self.rect.height)
                    elif colDir == 'u':
                        testRect = pygame.Rect(round(vector.x), (vector.y) + x, self.rect.width, self.rect.height)
                    elif colDir == 'd':
                        testRect = pygame.Rect(round(vector.x), round(vector.y) - x, self.rect.width, self.rect.height)
                    for obj in self.game.colliders:
                        if testRect.colliderect(obj.rect):
                            returnVal = True
                    x += 0.05
        else: 
            testRect = pygame.Rect(vector.x, vector.y, self.rect.width, self.rect.height)
            for obj in self.game.colliders:
                if testRect.colliderect(obj.rect):
                    returnVal = True
            
        return returnVal

