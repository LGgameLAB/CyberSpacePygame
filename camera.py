import pygame
from stgs import *

class cam:

    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height
        self.limit = CAMLIMIT
        self.offsetY = 40

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def applyRect(self, rect):
        return rect.move(self.camera.topleft)

    def update(self, target):

        x = -target.rect.centerx + int(winWidth / 2)
        y = -target.rect.centery + int(winHeight / 2)

        # limit scrolling to map size
        if self.limit:
            x = min(0, x)  # left
            y = min(self.offsetY, y)  # top
            x = max(-(self.width - winWidth), x)  # right
            y = max(-(self.height - winHeight), y)  # bottom

        self.camera = pygame.Rect(x, y, self.width, self.height)