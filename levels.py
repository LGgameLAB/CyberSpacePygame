import pygame
from stgs import *
from enemy import *
from objects import *

class level:
    colliders = []
    enemies = []
    levelSize = (winWidth, winHeight)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.__dict__[k] = v
        
        for p in self.colliders:
            if p.rect.bottomright[0] > self.levelSize[0]:
                self.levelSize = (p.rect.bottomright[0], self.levelSize[1])
            
            if p.rect.bottomright[1] > self.levelSize[1]:
                self.levelSize = (self.levelSize[0], p.rect.bottomright[1])
        
        self.rect = pygame.Rect(0, 0, self.levelSize[0], self.levelSize[1])
        self.image = pygame.Surface(self.levelSize)

        for p in self.colliders:
            self.image.blit(p.image, p.rect)

#### Level creation
LEVEL1 = level(levelSize = (winWidth, winHeight),
                colliders = [
                    collider((200, 200, 150, 10)),
                    collider((0, winHeight-30, winWidth+1000, 30)),
                    collider((400, 400, 30, 300)),
                    collider((0, 0, 30, winHeight)),
                    collider((winWidth+1000, 0, 30, winHeight)),
                    collider((0, 0, winWidth, 30)),
                    ],
                enemies = [
                    #enemy(asset('alien.png'))
                    ])

### All Game levels
gameLevels = [LEVEL1]