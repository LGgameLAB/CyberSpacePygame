import pygame
import stgs

class animation:
    #### Intializes first by grabbing sprite, sprite imgsheet data, and calculating a dir str ####
    ## Full image sheet can contain
    def __init__(self, sprite):
        self.sprite = sprite
        self.imgSheet = sprite.imgSheet
        self.tileWidth = sprite.imgSheet['tileWidth']
        try:
            self.imgSheet['l']
        except:
            self.imgSheet['l'] = pygame.transform.flip(self.imgSheet['r'], True, False)
        try:
            self.tileHeight = sprite.imgSheet['tileWidth']
        except:
            self.tileHeight = self.tileWidth
        self.framex = 0
        self.cycle = False
        self.dir = 'idleR'

    def update(self):
        self.dir = self.getStrDir()
        if self.framex == self.imgSheet[self.dir].get_width() - self.tileWidth:
            self.framex = 0
        else:
            self.framex += self.tileWidth

        self.sprite.image = self.sprite.imgSheet[self.dir].get_image(self.framex, 0, self.tileWidth, self.tileHeight)

    def getStrDir(self):
        if self.sprite.dir.x > 0:
            return 'r'
        elif self.sprite.dir.x < 0:
            return 'l'
        else:
            if self.dir[0:5] == 'idle':
                return self.dir
            else:
                return 'idle' + self.dir.capitalize()