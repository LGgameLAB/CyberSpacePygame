import pygame
from stgs import *

class animation:
    #### Intializes first by grabbing sprite, sprite imgsheet data, and calculating a dir str ####
    ## Full image sheet can contain: 'active', 'tileWidth', 'tileHeight', 'r', 'l', 'idleR', 'idleL','flyR', 'flyL'
    def __init__(self, sprite):
        self.sprite = sprite
        self.loadSheet()
        self.framex = 0
        self.cycle = False
        self.dir = 'idleR'
        self.lastTick = pygame.time.get_ticks()

    def loadSheet(self):
        self.imgSheet = self.sprite.imgSheet
        for k, v in self.imgSheet.items():
            if not k == 'active' and not k == 'tileWidth' and not k == 'tileHeight':
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
        self.getStrDir()
        if self.framex >= int(self.imgSheet[self.dir].width - self.tileWidth):
            self.framex = 0
        else:
            if pygame.time.get_ticks() - self.lastTick >= 120:
                self.framex += self.tileWidth
                self.lastTick = pygame.time.get_ticks()
        try:
            if self.sprite.imgSheet['active']:
                self.sprite.image = self.imgSheet[self.dir].get_image(self.framex, 0, self.tileWidth, self.tileHeight)
                self.sprite.image.set_colorkey((0,0,0))
        except:
            self.sprite.image = self.imgSheet[self.dir].get_image(self.framex, 0, self.tileWidth, self.tileHeight)
            self.sprite.image.set_colorkey((0,0,0))
                 
        

    def getStrDir(self):
        ### Get the last specific direction
        
        lastDir = ''
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