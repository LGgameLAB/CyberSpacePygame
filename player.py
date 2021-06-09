#### Imports ####

import math

import pygame

from animations import *
from objects import *
from stgs import *
import fx


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
    width, height = 36, 64
    health = 50
    maxHp = 50
    maxLives = 3
    #### Player Initializations ####
    def __init__(self, game, image, name, **kwargs):
        self.groups = [game.sprites, game.layer2]
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.game = game
        self.image = pygame.image.load(image)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.dir = pygame.math.Vector2((0, 0))
        self.vel = 8
        self.fall = 0
        self.yMod = 0
        self.ground = False
        self.gun = standardGun(self.game, self)
        self.lives = self.maxLives

        for k, v in kwargs.items():
            self.__dict__[k] = v
        
        self.loadAnimations()
        self.hpBar = healthBar(self.game, self)
        self.coinMeter = coinMeter(self.game, self)
        self.particleFx = fx.particles(self.game, self.rect, size = 15, dirRange=(55, 115))
        self.particleFx.setParticleKwargs(color=colors.cyan, speed=5, shrink=0.6)
        self.mascara = pygame.mask.from_surface(self.image)
                

    def loadAnimations(self):
        self.animations = animation(self)   

    #### Updates player ####
    def update(self):
        self.move()
        self.animations.update()
        if self.ground:
            self.particleFx.hide = True
        else:
            self.particleFx.hide = False
        
    def takeDamage(self, damage):
        if pygame.time.get_ticks() - self.lastHit >= self.hitCooldown:
            self.health -= damage
            self.lastHit = pygame.time.get_ticks()
            self.game.mixer.playFx('pHit')

    #### Move Physics ####
    def move(self):
        self.dir = pygame.math.Vector2((0, 0))

        

        ## Calculates the Gravity and sets the yMod to going down
        self.fall = 0.01*self.gravity
        ## min func limits the fall speed to yModMax
        self.yMod = min(self.yModMax, self.yMod+self.fall)

        #### Checks game type for flying or jumping ####
        if platformer:
            if self.ground:
                if checkKey(keySet['pUp']):
                    self.yMod = -0.5 
        else:
            if checkKey(keySet['pUp']):
                self.yMod = max(self.yModMin, self.yMod-0.05)

        ## Applies yMod to the direction. Still applies velocity to downwards movement 
        self.dir.y += self.yMod*self.vel
        collide = self.collideCheck()
        if self.dir.y < 0:
            self.ground = False

        if collide:
            if self.dir.y > 0:
                self.rect.bottom = collide.top
                self.ground = True
            else: 
                self.rect.top = collide.bottom
                self.ground = False
            self.dir.y = 0
            self.yMod = 0
        
        ## Checks for left and right movement. They counterbalance if both are pressed.
        if checkKey(keySet['pRight']):
            self.dir.x += 1
        if checkKey(keySet['pLeft']):
            self.dir.x -= 1
        
        ## Checks collision after horizontal movement
        collide = self.collideCheck()
        if collide:
            if self.dir.x > 0:
                self.rect.right = collide.left
            else: 
                self.rect.left = collide.right
            self.dir.x = 0

        self.rect.x += self.dir.x * self.vel
        self.rect.y += self.dir.y * self.vel

        if self.roomBound:
            self.rect.x = max(0, self.rect.x)
            self.rect.x = min(winWidth-self.rect.width, self.rect.x)
            self.rect.y = max(0, self.rect.y)
            self.rect.y = min(winHeight-self.rect.height, self.rect.y)

    #### Collide checker for player ####
    def collideCheck(self):
        returnVal = False
        testPos = pygame.Vector2(self.rect.topleft)
        testPos += self.dir*self.vel
        testRect = pygame.Rect(testPos.x, testPos.y, self.rect.width, self.rect.height)
        for obj in self.game.colliders:
            if testRect.colliderect(obj.rect):
                returnVal = obj.rect
                if isinstance(obj, mPlatform):
                    self.dir.x += (obj.dir.x * obj.vel)/self.vel
                    if self.dir.y > 0 and obj.dir.y > 0:
                        self.rect.bottom = obj.rect.top
            
        return returnVal