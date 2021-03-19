import pygame
import math
import random
from stgs import *
from animations import *
from player import *

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
        self.move()

        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.width, self.height)
        if self.health <= 0:
            self.kill()
        
        self.animations.update()

    ## Vertical or horizontal movement
    def move(self):
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

#def bit01(game, pos, vertical):
#    if vertical:
#        return enemy(game, pos, health=2, imgSheet ={'tileWidth': 32, 'r': asset('enemies/bit01.png')}, startDir=(0, random.randrange(-1, 1+1, 2)))
#    else:
#        return enemy(game, pos, health=2, imgSheet ={'tileWidth': 32, 'r': asset('enemies/bit01.png')}, startDir=(random.randrange(-1, 1+1, 2), 0))

class bit01(enemy):

    def __init__(self, game, pos, vertical):
        imgSheet = {'tileWidth': 32, 'r': asset('enemies/bit01.png')}
        if vertical:
            startDir = (0, random.randrange(-1, 1+1, 2))
        else:
            startDir = (random.randrange(-1, 1+1, 2), 0)
        super().__init__(game, pos, health = 2, imgSheet = imgSheet, startDir = startDir)

class bit02(enemy):

    def __init__(self, game, pos):
        imgSheet = {'tileWidth': 32, 'r': asset('enemies/bit02.png')}
        vel = 10
        startDir = pygame.Vector2(1, 0).rotate(random.randint(1, 360))
        super().__init__(game, pos, health = 5, imgSheet = imgSheet, vel = vel, startDir = startDir)

    def move(self):
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

class bossyBit(enemy):
    def __init__(self, game, pos):
        imgSheet = {'tileWidth': 128, 'r': asset('enemies/alien.png')}
        vel = 5
        startDir = pygame.Vector2(1, 0)
        super().__init__(game, pos, health = 30, imgSheet = imgSheet, vel = vel, startDir = startDir)

        self.reloadTime = 1000
        self.lastFire = pygame.time.get_ticks()

    def move(self):
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
    
    def update(self):
        super().update()
        self.attack()
    
    def attack(self):
        if pygame.time.get_ticks() - self.lastFire >= self.reloadTime:
            pPos = pygame.Vector2(self.game.cam.apply(self.game.player).center)  
            myPos = self.game.cam.apply(self)  
            pPos.x -= myPos.centerx 
            pPos.y -= myPos.centery
            angle = math.degrees(math.atan2(-pPos.normalize().y, pPos.normalize().x))
            enemyBullet(self.game, self.rect.center, pPos, angle, offset = 5)
            enemyBullet(self.game, self.rect.center, pPos, angle)
            enemyBullet(self.game, self.rect.center, pPos, angle, offset = -5)
            self.lastFire = pygame.time.get_ticks()

class enemyBullet(pygame.sprite.Sprite):
    pos = pygame.Vector2((0,0))
    image = pygame.image.load(asset('objects/bullet2.png'))
    vel = 20
    offset = 0
    damage = 5
    def __init__(self, game, pos, target, angle, **kwargs):
        self.groups = game.sprites, game.eBullets, game.layer2
        pygame.sprite.Sprite.__init__(self, self.groups)

        for k, v in kwargs.items():
            self.__dict__[k] = v

        self.pos = pygame.Vector2(pos)
        self.dir = pygame.Vector2(target).normalize()
        self.dir = self.dir.rotate(self.offset)
        self.image = pygame.transform.rotate(self.image, angle - self.offset)
        self.rect = pygame.Rect(0, 0, self.image.get_width(), self.image.get_height())
        self.rect.center = self.pos
    
    def update(self):
        self.pos += self.dir *self.vel
        self.rect.center = self.pos