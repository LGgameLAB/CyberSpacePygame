import pygame
from stgs import *

class animation:
    #### Intializes first by grabbing sprite, sprite imgsheet data, and calculating a dir str ####
    ## Full image sheet can contain: 'active', 'tileWidth', 'tileHeight', 'r', 'l', 'idleR', 'idleL','flyR', 'flyL'
    ## Warning! Never use black RBG(0, 0, 0) on a sprite sheet! It will become transparent! If you want black use a similar color ex. RGB(1, 0, 0)
    def __init__(self, sprite):
        self.sprite = sprite
        self.loadSheet()
        self.framex = 0
        self.delay = 120
        self.lastTint = -20
        self.cycle = False
        self.dir = 'idleR'
        self.lastTick = pygame.time.get_ticks()
        self.frameReset = True

    def loadSheet(self):
        self.imgSheet = self.sprite.imgSheet
        for k, v in self.imgSheet.items():
            if not k == 'active' and not k == 'tileWidth' and not k == 'tileHeight' and not k == 'static':
                self.imgSheet[k] = Spritesheet(v)
        
        self.tileWidth = self.imgSheet['tileWidth']
        self.hasIdle = True 
        self.hasFly = True

        try:
            self.imgSheet['l']
        except:
            self.imgSheet['l'] = Spritesheet(pygame.transform.flip(self.imgSheet['r'].image, True, False), True)
        try:
            self.imgSheet['idleL']
        except:
            try:
                self.imgSheet['idleL'] = Spritesheet(pygame.transform.flip(self.imgSheet['idleR'].image, True, False), True)
            except:
                self.hasIdle = False
        try:
            self.imgSheet['flyL']
        except:
            try:
                self.imgSheet['flyL'] = Spritesheet(pygame.transform.flip(self.imgSheet['flyR'].image, True, False), True)
            except:
                self.hasFly = False
        try:
            self.tileHeight = self.imgSheet['tileHeight']
        except:
            self.tileHeight = self.tileWidth
        
    def update(self):
        try:
            self.getStrDir()
        except AttributeError:
            self.dir = 'r'

        if pygame.time.get_ticks() - self.lastTick >= self.delay:
            self.framex += self.tileWidth
            self.lastTick = pygame.time.get_ticks()
            if self.framex > int(self.imgSheet[self.dir].width - self.tileWidth):
                self.framex = 0
        try:
            if self.sprite.imgSheet['active']:
                self.sprite.image = self.imgSheet[self.dir].get_image(self.framex, 0, self.tileWidth, self.tileHeight)
                #self.sprite.image.set_colorkey((0,0,0))
                self.imageFx()
        except:
            self.sprite.image = self.imgSheet[self.dir].get_image(self.framex, 0, self.tileWidth, self.tileHeight)
            #self.sprite.image.set_colorkey((0,0,0))
            

    def getStrDir(self):
        ### Get the last specific direction
        lastDir = ''
        fullLastDir = self.dir
        if len(self.dir) == 1:
            lastDir = self.dir
        elif self.dir[0:4] == 'idle':
            lastDir = self.dir[4]
        else:
            lastDir = self.dir[3]

        if self.hasFly:
            if self.sprite.ground:
                if self.sprite.dir.x > 0:
                    self.dir = 'r'
                elif self.sprite.dir.x < 0:
                    self.dir = 'l'
                elif self.hasIdle:
                    self.dir = 'idle' + lastDir.capitalize()
                else:
                    self.dir = lastDir.lower()
            else:
                if self.sprite.dir.x > 0:
                    self.dir = 'flyR'
                elif self.sprite.dir.x < 0:
                    self.dir = 'flyL'
                else:
                    self.dir = 'fly' + lastDir.capitalize()
        else:
            if self.sprite.dir.x > 0:
                self.dir = 'r'
            elif self.sprite.dir.x < 0:
                self.dir = 'l'
            elif self.hasIdle:
                self.dir = 'idle' + lastDir.capitalize()
            else:
                self.dir = lastDir.lower()
        
        if self.frameReset and not self.dir == fullLastDir:
            self.framex = 0
    
    def imageFx(self):
        try:
            lastHit = pygame.time.get_ticks() - self.sprite.lastHit
            duration = 100
            if lastHit < duration:
                darkness = min(255, max(0, round(255 * (lastHit/duration))))
                self.sprite.image.fill((255, darkness, darkness), special_flags = pygame.BLEND_MULT)
        except :
            pass