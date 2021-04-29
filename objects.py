import pygame
from stgs import *
from animations import *
import math

def activatePlatform(game, platformId):
    game.getSprBylID(platformId).pause = False

class trigger(pygame.sprite.Sprite):
    def __init__(self, game, rect, func, params, **kwargs):
        self.groups = game.sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pygame.Rect(rect)
        self.func = lambda:func(params[0], params[1])
        self.touched = False
        for k, v in kwargs.items():
            self.__dict__[k] = v

    def update(self):
        if not self.touched:
            if self.rect.colliderect(self.game.player.rect):
                self.func()
                self.touched = True


class collider(pygame.sprite.Sprite):
    color = (255, 255, 255)

    def __init__(self, game, rect, **kwargs):
        self.groups = game.colliders
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.rect = pygame.Rect(rect)

        for k, v in kwargs.items():
            self.__dict__[k] = v

        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.fill(self.color)

class platWall(pygame.sprite.Sprite):
    color = (255, 255, 255)

    def __init__(self, game, rect, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(rect)

        for k, v in kwargs.items():
            self.__dict__[k] = v

        self.image = pygame.Surface((self.rect.width, self.rect.height))

class mPlatform(pygame.sprite.Sprite):
    def __init__(self, game, rect, **kwargs):
        self.groups = game.colliders, game.sprites, game.layer2
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pygame.Rect(rect)
        self.pos = pygame.Vector2((self.rect.x, self.rect.y))
        self.player = self.game.player
        self.pause = False
        self.dir = (1, 0)
        self.vertical = False
        self.vel = 5
        self.color = (255, 255, 255)
        for k, v in kwargs.items():
            self.__dict__[k] = v
        
        if self.vertical:
            self.dir = (0, 1)

        self.dir = pygame.Vector2(self.dir).normalize()

        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.render()
    
    def render(self):
        defaultTile = Spritesheet(asset('Tiled/tileset1.png')).get_image(0, 0, 32, 32)
        for x in range(0, self.image.get_width(), 32):
            self.image.blit(defaultTile, (x, 0))
    
    def update(self):
        if not self.pause:
            self.move()
            self.rect.x, self.rect.y = self.pos
    
    def move(self):
        testVec = pygame.Vector2((self.pos.x, self.pos.y))
        if self.collideCheck(pygame.Vector2(testVec.x+(self.dir.x*self.vel), testVec.y)):
            
            if self.dir.x > 0:
                self.dir = self.dir.reflect((-1,0))
            else:
                self.dir = self.dir.reflect((1,0))
        
        self.pos.x += self.dir.x*self.vel
        # If we hit player move the player
        testRect = pygame.Rect(self.pos.x, self.pos.y, self.rect.width, self.rect.height)
        if testRect.colliderect(self.player.rect):
            if self.dir.x < 0:
                self.player.rect.right = testRect.left
            else:
                self.player.rect.left = testRect.right

        if self.collideCheck(pygame.Vector2(testVec.x, testVec.y+(self.dir.y*self.vel))):
            if self.dir.y > 0:
                self.dir = self.dir.reflect((0, -1))
            else:
                self.dir = self.dir.reflect((0, 1))
        
        if self.dir.y > 0:
            moveP = self.checkPlayerAbove(testRect)
        else:
            moveP = False

        self.pos.y += self.dir.y*self.vel
        testRect = pygame.Rect(self.pos.x, self.pos.y, self.rect.width, self.rect.height)
        if moveP:
            self.player.rect.bottom = testRect.top
        
        testRect = pygame.Rect(self.pos.x, self.pos.y, self.rect.width, self.rect.height)
        if testRect.colliderect(self.player.rect):
            if self.dir.y < 0:
                self.player.rect.bottom = testRect.top
            else:
                self.player.rect.top = testRect.bottom

    def collideCheck(self, vector):
            returnVal = False
        
            testRect = pygame.Rect(round(vector.x), round(vector.y), self.rect.width, self.rect.height)
            for obj in self.game.colliders:
                if not obj == self:
                    if testRect.colliderect(obj.rect):
                        returnVal = True

            for obj in self.game.level.platWalls:
                if testRect.colliderect(obj.rect):
                    returnVal = True
                
            return returnVal

    def checkPlayerAbove(self, testRect):
        upRect = testRect.move(0, -1)
        if upRect.colliderect(self.player.rect):
            return True
        else:
            return False
        

class door(pygame.sprite.Sprite):
    color = (255, 255, 255)

    def __init__(self, game, rect, **kwargs):
        self.groups = game.sprites, game.layer1
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.rect = pygame.Rect(rect)

        for k, v in kwargs.items():
            self.__dict__[k] = v

        # self.image = pygame.Surface((self.rect.width, self.rect.height))
        # self.image.fill(self.color)
        self.image = pygame.image.load(asset('objects/door.png'))

class entrance(pygame.sprite.Sprite):
    color = (255, 255, 255)

    def __init__(self, game, rect, **kwargs):
        self.groups = game.sprites, game.layer1
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.rect = pygame.Rect(rect)

        for k, v in kwargs.items():
            self.__dict__[k] = v

        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.fill(self.color)
        #self.image = pygame.image.load(asset('objects/door.png'))

class key(pygame.sprite.Sprite):
    color = (255, 255, 255)

    def __init__(self, game, pos, image, **kwargs):
        self.groups = game.sprites, game.layer1
        pygame.sprite.Sprite.__init__(self, self.groups)

        for k, v in kwargs.items():
            self.__dict__[k] = v

        self.image = pygame.image.load(image)
        self.pos = pygame.Vector2(pos)
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.image.get_width(), self.image.get_height())

class coin(pygame.sprite.Sprite):
    color = (255, 255, 255)
    value = 10
    imgSheet = {'active': False, 'static': True,'tileWidth': 32}

    def __init__(self, game, pos, image, **kwargs):
        self.groups = game.sprites, game.layer1, game.items
        pygame.sprite.Sprite.__init__(self, self.groups)

        for k, v in kwargs.items():
            self.__dict__[k] = v

        self.image = pygame.image.load(image)
        if self.imgSheet['active']:
            self.animations = animation(self)
        self.pos = pygame.Vector2(pos)
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.image.get_width(), self.image.get_height())
    
    def update(self):
        if self.imgSheet['active']:
            self.animations.update()

class teleporter(pygame.sprite.Sprite):
    pos = (0,0)
    target = (0,0)

    def __init__(self, game, image, pos, target, **kwargs):
        self.groups = game.sprites, game.layer2
        pygame.sprite.Sprite.__init__(self, self.groups)

        for k, v in kwargs.items():
            self.__dict__[k] = v

        self.image = pygame.image.load(image)
        self.pos = pygame.Vector2(pos)
        self.target = pygame.Vector2((target.x, target.y))
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.image.get_width(), self.image.get_height())

    def update(self):
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.image.get_width(), self.image.get_height())

class button(pygame.sprite.Sprite):
    rect = (0, 0, 200, 60)
    #          Normal           Selected
    colors = ((50, 255, 255), (255, 255, 255))
    spriteInit = False
    hover = False
    clicked = False
    text = ''
    center = False
    def __init__(self, game, pos,**kwargs):
        self.game = game
        
        self.onClick = False
        self.groups = []
        self.addGroups = []
        for k, v in kwargs.items():
            self.__dict__[k] = v
        
        self.groups = self.groups + self.addGroups

        pygame.sprite.Sprite.__init__(self, self.groups)

        self.rect = pygame.Rect(self.rect)
        self.rect.x, self.rect.y = pos
        self.image = pygame.Surface(self.rect.size)

        self.rendText = self.game.menuFont.render(self.text, self.game.antialiasing, (0, 0, 0))
        self.textRect = self.rendText.get_rect()
        if self.center:
            self.textRect.center = pygame.Rect(0, 0, self.rect.width, self.rect.height).center
        else:
            self.textRect.x += 2
            self.textRect.y += 2

    def update(self):
        
        self.image = pygame.Surface(self.rect.size)
        self.hover = False
        self.clicked = False
        mouseRect = pygame.Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 1, 1)
        if mouseRect.colliderect(self.rect):
            self.hover = True
        
        if self.hover:
            for event in self.game.events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.clicked = True
                    if self.onClick:
                        self.onClick()

            self.image.fill(self.colors[1])
        else:
            self.image.fill(self.colors[0])
        
        self.image.blit(self.rendText, self.textRect)

class settingSlider(pygame.sprite.Sprite):
    
    def __init__(self, game, pos,**kwargs):
        self.game = game
        self.rect = (0, 0, 200, 60)
        self.sliderRect = (0, 0, 20, 10)
        self.bgColor = colors.black
        #          line (normal)           Rect
        self.colors = ((50, 255, 255), colors.yellow, (255, 255, 255))
        self.clicked = False
        self.spriteInit = False
        self.text = ''
        self.center = False

        self.groups = []       ## These few lines are the lines for component objects
        self.addGroups = []
        for k, v in kwargs.items():
            self.__dict__[k] = v
        
        self.groups = self.groups + self.addGroups
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.rect = pygame.Rect(self.rect)
        self.rect.x, self.rect.y = pos
        self.image = pygame.Surface(self.rect.size)
        self.sliderRect = pygame.Rect(self.sliderRect)
        self.sliderRect.centery = self.rect.height/2
        self.sliderRect.x = self.rect.width - self.sliderRect.width

    def reset(self):
        self.sliderRect = pygame.Rect(self.sliderRect)
        self.sliderRect.centery = self.rect.height/2
        self.sliderRect.x = self.rect.width - self.sliderRect.width
    
    def update(self):
        if self.clicked:
            if not pygame.mouse.get_pressed()[0]:  
               self.clicked = False
            else:
                self.sliderRect.x = min(self.rect.right-self.sliderRect.width, pygame.mouse.get_pos()[0]-self.sliderRect.width) - self.rect.x
                self.sliderRect.x = max(0, self.sliderRect.x)
        else:
            self.checkClicked()
        
        self.render()
    
    def get_ratio(self):
        return self.sliderRect.x/(self.rect.width-self.sliderRect.width)
    
    def setRatio(self, percent): # Set between 0 & 1
        self.sliderRect.x = (self.rect.width-self.sliderRect.width)*percent

    def render(self):
        self.image.fill(self.bgColor)
        pygame.draw.line(self.image, self.colors[1],(0, self.rect.height/2), (self.sliderRect.centerx, self.rect.height/2), 4)
        pygame.draw.line(self.image, self.colors[0],(self.sliderRect.centerx, self.rect.height/2), (self.rect.width, self.rect.height/2), 4)
        pygame.draw.rect(self.image, self.colors[2], self.sliderRect)

    
    def checkClicked(self):
        if pygame.mouse.get_pressed()[0]: 
            mouseRect = pygame.Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 1, 1)
            if mouseRect.colliderect(self.rect):
                self.clicked = True

class consumable(pygame.sprite.Sprite):
    imgSheet = {'active': False, 'static': True,'tileWidth': 32}
    image = pygame.Surface((imgSheet['tileWidth'], imgSheet['tileWidth']))

    def __init__(self, game, pos, **kwargs):
        self.game = game
        self.groups = game.sprites, game.items, game.layer1
        pygame.sprite.Sprite.__init__(self, self.groups)

        for k, v in kwargs.items():
            self.__dict__[k] = v

        if self.imgSheet['active']:
            self.animations = animation(self)

        self.pos = pygame.Vector2(pos)
        self.rect = pygame.Rect(0, 0, self.imgSheet['tileWidth'], self.imgSheet['tileWidth'])
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y

    def update(self):
        if self.imgSheet['active']:
            self.animations.update()
        
class dmgRect(pygame.sprite.Sprite):
    def __init__(self, game, rect, **kwargs):
        self.groups = game.dmgRects
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.damage = 5
        self.rect = pygame.Rect(rect)
        for k, v in kwargs.items():
            self.__dict__[k] = v

#### Player Objects ####

class gun(pygame.sprite.Sprite):
    
    def __init__(self, game, image, player, **kwargs):
        self.groups = game.sprites, game.layer2
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.game = game
        self.player = player
        self.imgSource  = pygame.image.load(image)
        self.image = pygame.image.load(image)
        self.rect = pygame.Rect(0, 0, self.image.get_width(), self.image.get_height())
        self.pos = pygame.Vector2(self.player.rect.center)

        self.damage = 5
        self.speed = 15
        self.moveDist = 20
        self.reloadTime = 200
        self.lastFire = -self.reloadTime

        for k, v in kwargs.items():
            self.__dict__[k] = v
    
    def update(self):
        self.move()
        self.rect.center = self.pos
        self.rect.x += 20
        self.setAngle()
        if pygame.time.get_ticks() - self.lastFire >= self.reloadTime:
            self.checkFire()

    def move(self):
        pPos = pygame.Vector2(self.player.rect.center)
        if dist(self.pos, pPos) >= self.moveDist:
            vel = pygame.Vector2(self.pos.x-pPos.x, self.pos.y-pPos.y).normalize()
            self.pos += -vel*self.speed
    
    def recenter(self):
        self.pos = pygame.Vector2(self.player.rect.center)
            
    #### Checks for bullet fire ####
    def checkFire(self):   ## This got complicated so I will break it down
        if pygame.mouse.get_pressed()[0]: ## Checks on click 
            mPos = pygame.Vector2(pygame.mouse.get_pos())  ## Gets mouse position and stores it in vector. This will be translated into the vector that moves the bullet
            pPos = self.game.cam.apply(self.player)  ## Gets actual position of player on screen
            mPos.x -= pPos.centerx ## Finds the x and y relativity between the mouse and player and then calculates the offset
            mPos.y -= pPos.centery
            self.setAngle(False)
            self.fire(mPos) ## Inputs values. Notice how I used rect.center instead of pPos.
            self.lastFire = pygame.time.get_ticks()
            self.game.mixer.playFx('gunFx1')
    
    def fire(self, mPos):
        bullet(self.game, self.rect.center, mPos, self.angle)

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

class massFireGun(gun):
    def __init__(self, game, player):
        super().__init__(game, asset('objects/gun.png'), player, damage = 2)
    
    def fire(self, mPos):
        bullet(self.game, self.rect.center, mPos, self.angle, offset = 180)
        bullet(self.game, self.rect.center, mPos, self.angle, offset = 90)
        bullet(self.game, self.rect.center, mPos, self.angle, offset = 5)
        bullet(self.game, self.rect.center, mPos, self.angle, offset = 2.5)
        bullet(self.game, self.rect.center, mPos, self.angle)
        bullet(self.game, self.rect.center, mPos, self.angle, offset = -2.5)
        bullet(self.game, self.rect.center, mPos, self.angle, offset = -5)
        bullet(self.game, self.rect.center, mPos, self.angle, offset = -90)

class tripleGun(gun):

    def __init__(self, game, player):
        super().__init__(game, asset('objects/gun.png'), player, damage = 2)

    def fire(self, mPos):
        bullet(self.game, self.rect.center, mPos, self.angle, offset = 5)
        bullet(self.game, self.rect.center, mPos, self.angle)
        bullet(self.game, self.rect.center, mPos, self.angle, offset = -5)

class lazerGun(gun):

    def __init__(self, game, player):
        super().__init__(game, asset('objects/gun.png'), player, damage = 1)

    def fire(self, mPos):
        lazer(self.game, self.rect.center, mPos, self.angle)

class standardGun(gun):
    def __init__(self, game, player):
        super().__init__(game, asset('objects/gun.png'), player, damage = 2)

#### Bullet Class #### 
class bullet(pygame.sprite.Sprite):
    pos = pygame.Vector2((0,0))
    image = pygame.image.load(asset('objects/bullet2.png'))
    vel = 20
    offset = 0
    static = False
    def __init__(self, game, pos, target, angle, **kwargs):
        self.groups = game.sprites, game.pBullets, game.layer2
        self.game = game
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
        if not self.static:
            self.pos += self.dir *self.vel
            self.rect.center = self.pos

class healthBar(pygame.sprite.Sprite):
    x = winWidth/3
    y = 3
    width = 100
    height = 30
    bgColor = colors.light(colors.black, 50)
    hpColor = colors.lightGreen
    offset = 10
    gap = offset
    def __init__(self, game, player, **kwargs):
        self.groups = game.sprites, game.overlayer
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        for k, v in kwargs.items():
            self.__dict__[k] = v

        self.player = player
        self.image = pygame.Surface((self.width, self.height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.barRect = pygame.Rect(self.offset/2, self.offset/2, self.width-self.gap, self.height-self.gap)
    
    def update(self):
        self.image.fill((self.bgColor))
        self.renderBar()
    
    def renderBar(self):
        pygame.draw.rect(self.image, self.hpColor, (self.barRect.x, self.barRect.y, (self.barRect.width)*(self.player.health/self.player.maxHp), self.barRect.height))
    # def renderBar(self):
    #     pygame.draw.rect(self.image, self.hpColor, (1, 1, (self.barRect.width)*(self.player.health/self.player.maxHp), self.barRect.height))

class healthBar2(healthBar):
    x = 5
    y = winHeight/3
    width = 30
    height = 100
    bgColor = colors.light(colors.black, 100)
    offset = 6
    gap = offset

    def __init__(self, game, player):
        super().__init__(game, player)
    def renderBar(self):
        pygame.draw.rect(self.image, self.hpColor, (self.barRect.x, self.barRect.y+(self.barRect.height)*(1 - self.player.health/self.player.maxHp), self.barRect.width, (self.barRect.height)*(self.player.health/self.player.maxHp)))

class coinMeter(consumable):

    def __init__(self, game, player, **kwargs):
        self.groups = game.sprites, game.overlayer
        pygame.sprite.Sprite.__init__(self, self.groups)

        ## Setup
        self.x = 0
        self.y = 40
        self.width = 30
        self.height = 100
        self.bgColor = colors.rgba(colors.light(colors.black, 20), 120)
        self.coinColor = colors.yellow
        self.offset = 5
        self.gap = self.offset*2
        
        self.meterLevel = 0
        self.coins = 0
        self.coinsPerLevel = 5
        self.healthAddPerc = 0.2
        for k, v in kwargs.items():
            self.__dict__[k] = v

        self.player = player
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.barRect = pygame.Rect(self.offset, self.offset, self.width-self.gap, self.height-self.gap)
        
    
    def update(self):
        self.image.fill((self.bgColor))
        self.renderBar()
    
    def renderBar(self):
        pygame.draw.rect(self.image, self.coinColor, (self.barRect.x, self.barRect.y+(self.barRect.height)*(1 - self.meterLevel/self.coinsPerLevel), self.barRect.width, (self.barRect.height)*(self.meterLevel/self.coinsPerLevel)))

    def addCoin(self):
        self.coins += 1
        self.meterLevel += 1
        if self.meterLevel >= self.coinsPerLevel:
            self.meterLevel = 0
            self.player.health += self.player.maxHp*self.healthAddPerc
            self.player.health = min(self.player.maxHp, self.player.health)

class lazer(bullet):
    def __init__(self, game, pos, target, angle):
        self.limit = 40
        self.colAcc = 9 # collision accuracy
        self.beamWidth = 5
        self.pPos = pos
        self.lazers = []
        self.angle = angle
        self.initTime = pygame.time.get_ticks()
        super().__init__(game, pos, target, angle, static=True)
        self.render()
    
    def render(self):
        x = 0
        checkPos = self.pos
        checkDir = self.dir*self.colAcc
        checkRect = self.rect
        while x < self.limit:
            x+=1
            checkPos += checkDir
            checkRect.center = checkPos
            self.lazers.append(bullet(self.game, checkPos, checkPos, self.angle, static=True, image=pygame.image.load(asset('objects/lazer.png'))))
            if self.checkCol(checkRect):
                break

        self.finalPoint = checkPos
        self.pos = self.finalPoint
        self.rect = (self.pos.x, self.pos.y, self.beamWidth, self.beamWidth)
    
    def checkCol(self, rect):
        returnVal = False
        for obj in self.game.colliders:
            if rect.colliderect(obj.rect):
                returnVal = True
        return returnVal
    
    def update(self):
        super().update()
        if pygame.time.get_ticks() - self.initTime >= 200:
            for l in self.lazers:
                l.kill()
            self.kill()
   
class tp1(teleporter):
    def __init__(self, game, pos, target):
        super().__init__(game, asset('objects/teleporter1.png'), pos, target)

class gunConsumable(consumable):
    def __init__(self, game, pos, gun, **kwargs):  
        self.gun = gun
        super().__init__(game, pos, **kwargs)

class massFireGunConsumable(gunConsumable):
    def __init__(self, game, pos):  
        gun = massFireGun
        image = pygame.image.load(asset('objects/gun.png'))
        super().__init__(game, pos, gun, image = image)

class tripleGunConsumable(gunConsumable):
    def __init__(self, game, pos):  
        gun = tripleGun
        image = pygame.image.load(asset('objects/gun.png'))
        super().__init__(game, pos, gun, image = image)

class hpPack1(consumable):
    def __init__(self, game, pos):
        self.value = 15
        image = pygame.image.load(asset('objects/decryptor.png'))
        super().__init__(game, pos, image = image)
    

def menuBtn(game, pos):
    return button(game, pos)

def bitCoin(game, pos):
    return coin(game, pos, asset('objects/bitCoin.png'))

def key1(game, pos):
    return key(game, pos, asset('objects/decryptor.png'))
