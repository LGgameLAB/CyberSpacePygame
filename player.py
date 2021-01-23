#### Imports ####

import pygame
import math
from stgs import *

#### Player object ####
class player(pygame.sprite.Sprite):
    x = 71
    y = 71
    yModMin = -0.1
    yModMax = 0.1
    roomBound = False
    
    #### Player Initializations ####
    def __init__(self, game, image, name):
        pygame.sprite.Sprite.__init__(self)

        self.game = game
        self.image = pygame.image.load(image)
        self.rect = pygame.Rect(0, 0, self.image.get_width(), self.image.get_height())
        self.pos = pygame.math.Vector2(self.x, self.y)
        self.dir = pygame.math.Vector2((0, 0))
        self.vel = 15
        self.fall = 0
        self.yMod = 0
        self.colliders = []
        self.ground = False
    
    #### Updates player ####
    def update(self):
        self.move()
        self.rect.topleft = round(self.pos.x), round(self.pos.y)
        self.checkFire()
    
    #### Checks for bullet fire ####
    def checkFire(self):
        for event in self.game.events:
            if event.type == pygame.MOUSEBUTTONUP:
                mPos = pygame.Vector2(pygame.mouse.get_pos())
                mPos.x -= self.rect.x
                mPos.y -= self.rect.y
                self.game.sprites.add(bullet(self.rect.center, mPos))

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
                    self.dir -= (0.01, 0)
                else:
                    self.dir += (x-0.5,0)
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
            if self.collideCheck(self.pos + downVec*self.vel):
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
                    self.yMod = -0.1 
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
                for obj in self.colliders:
                    if testRect.colliderect(obj):
                        returnVal = True
                x += 0.05
        else: 
            testRect = pygame.Rect(round(vector.x), round(vector.y), self.rect.width, self.rect.height)
            for obj in self.colliders:
                if testRect.colliderect(obj):
                    returnVal = True
            
        return returnVal


#### Bullet Class ####
class bullet(pygame.sprite.Sprite):
    pos = pygame.Vector2((0,0))
    image = pygame.image.load(asset('bullet_alt.png'))
    vel = 40

    def __init__(self, pos, target, **kwargs):
        pygame.sprite.Sprite.__init__(self)

        for k, v in kwargs.items():
            self.__dict__[k] = v

        self.pos = pygame.Vector2(pos)
        self.dir = pygame.Vector2(target).normalize()
        self.rect = pygame.Rect(0, 0, self.image.get_width(), self.image.get_height())
        self.rect.center = self.pos
        

    
    def update(self):
        self.pos += self.dir *self.vel
        self.rect.center = self.pos
        

        
