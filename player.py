#### Imports ####

import pygame
import math
from stgs import *
from animations import *

def standGun(game, player):
    return gun(game, asset('objects/gun.png'), player, damage = 2)
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
        self.gun = standGun(self.game, self)

        for k, v in kwargs.items():
            self.__dict__[k] = v
        
        self.loadAnimations()
        self.hpBar = healthBar(self.game, self)

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
            testRect = pygame.Rect(round(vector.x), round(vector.y), self.rect.width, self.rect.height)
            for obj in self.game.colliders:
                if testRect.colliderect(obj.rect):
                    returnVal = True
            
        return returnVal

class gun(pygame.sprite.Sprite):
    x = 0
    y = 0
    rect = pygame.Rect(x, y, 64, 64)
    damage = 5
    reloadTime = 200
    imgSource = ''
    def __init__(self, game, image, player, **kwargs):
        self.groups = game.sprites, game.layer2
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.game = game
        self.player = player
        self.imgSource  = pygame.image.load(image)
        self.image = pygame.image.load(image)
        self.lastFire = -self.reloadTime
        self.rect = pygame.Rect(0, 0, self.image.get_width(), self.image.get_height())
        self.pos = pygame.Vector2(self.player.rect.center)

        for k, v in kwargs.items():
            self.__dict__[k] = v
    
    def update(self):
        self.pos = pygame.Vector2(self.player.rect.center)
        self.rect.center = self.pos
        self.rect.x += 20
        self.setAngle()
        if pygame.time.get_ticks() - self.lastFire >= self.reloadTime:
            self.checkFire()

    #### Checks for bullet fire ####
    def checkFire(self):   ## This got complicated so I will break it down
        for event in self.game.events:
            if event.type == pygame.MOUSEBUTTONUP:  ## Checks on click release
                mPos = pygame.Vector2(pygame.mouse.get_pos())  ## Gets mouse position and stores it in vector. This will be translated into the vector that moves the bullet
                pPos = self.game.cam.apply(self.player)  ## Gets actual position of player on screen
                pPosVec = pygame.Vector2((pPos.x, pPos.y))
                angle = pPosVec.angle_to(mPos) ## Gets angle between player vector and mouse vector
                mPos.x -= pPos.centerx ## Finds the x and y relativity between the mouse and player and then calculates the offset
                mPos.y -= pPos.centery
                self.setAngle(False)
                bullet(self.game, self.rect.center, mPos, self.angle) ## Inputs values. Notice how I used rect.center instead of pPos.
                self.lastFire = pygame.time.get_ticks()
    
    def setAngle(self, *args):
        if len(args) > 0:
            move = args[0]
        else:
            move = True
        mPos = pygame.Vector2(pygame.mouse.get_pos())
        pPos = self.game.cam.apply(self.player)  ## Gets actual position of player on screen
        mPos.x -= pPos.centerx ## Finds the x and y relativity between the mouse and player and then calculates the offset
        mPos.y -= pPos.centery
        try:
            self.angle = math.degrees(math.atan2(-mPos.normalize().y, mPos.normalize().x))
        except ValueError:
            self.angle = 0

        if self.angle > 90 or self.angle < -90:
            self.rotCenter(-(self.angle))
            self.image = pygame.transform.flip(self.image, False, True)
            if move:
                self.rect.x -= 25
        else:
            self.rotCenter()
        

    def rotCenter(self, *args):
        if len(args) > 0:
            angle = args[0]
        else:
            angle = self.angle
        
        self.image = pygame.transform.rotate(self.imgSource, angle)
        self.rect = self.image.get_rect(center = self.image.get_rect(center = self.rect.center).center)

    

    




#### Bullet Class #### 
class bullet(pygame.sprite.Sprite):
    pos = pygame.Vector2((0,0))
    image = pygame.image.load(asset('objects/bullet2.png'))
    vel = 20
    def __init__(self, game, pos, target, angle, **kwargs):
        self.groups = game.sprites, game.pBullets, game.layer2
        pygame.sprite.Sprite.__init__(self, self.groups)

        for k, v in kwargs.items():
            self.__dict__[k] = v

        self.pos = pygame.Vector2(pos)
        self.dir = pygame.Vector2(target).normalize()
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = pygame.Rect(0, 0, self.image.get_width(), self.image.get_height())
        self.rect.center = self.pos
        

    
    def update(self):
        self.pos += self.dir *self.vel
        self.rect.center = self.pos

class healthBar(pygame.sprite.Sprite):
    x = winWidth/3
    y = 3
    width = 100
    height = 30
    bgColor = colors.black
    hpColor = colors.green
    def __init__(self, game, player, **kwargs):
        self.groups = game.sprites, game.overlayer
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        for k, v in kwargs.items():
            self.__dict__[k] = v

        self.player = player
        self.image = pygame.Surface((self.width, self.height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.barRect = pygame.Rect(0, 0, self.width-2, self.height-2)
        self.barRect.centerx, self.barRect.centery = self.rect.centerx - self.x, self.rect.centery - self.y
    
    def update(self):
        self.image.fill((self.bgColor))
        pygame.draw.rect(self.image, self.hpColor, (1, 1, (self.width - 2)*(self.player.health/self.player.maxHp), self.height -2))
