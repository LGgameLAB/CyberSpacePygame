import pygame

class platform(pygame.sprite.Sprite):
    color = (255, 255, 255)

    def __init__(self, rect, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(rect)

        for k, v in kwargs.items():
            self.__dict__[k] = v

        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.fill(self.color)