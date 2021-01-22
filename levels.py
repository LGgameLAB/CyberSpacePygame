import pygame
from stgs import *
from enemy import *
from platforms import *

class level:
    platforms = []
    enemies = []
    levelSize = (winWidth, winHeight)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.__dict__[k] = v
        
        

        for p in self.platforms:
            if p.rect.bottomright[0] > self.levelSize[0]:
                self.levelSize = (p.rect.bottomright[0], self.levelSize[1])
            
            if p.rect.bottomright[1] > self.levelSize[1]:
                self.levelSize = (self.levelSize[0], p.rect.bottomright[1])
        
        self.rect = pygame.Rect(0, 0, self.levelSize[0], self.levelSize[1])
        self.image = pygame.Surface(self.levelSize)

        for p in self.platforms:
            self.image.blit(p.image, p.rect)

#### Level creation
def level1():
    return level(levelSize = (winWidth, winHeight),
                platforms = [
                    platform((200, 200, 150, 10)),
                    platform((0, winHeight-30, winWidth+1000, 30)),
                    platform((400, 400, 30, 300)),
                    platform((0, 0, 30, winHeight)),
                    platform((winWidth+1000, 0, 30, winHeight)),
                    platform((0, 0, winWidth, 30)),
                    ],
                enemies = [
                    enemy(asset('alien.png'))
                    ])

### All Game levels
gameLevels = [level1()]