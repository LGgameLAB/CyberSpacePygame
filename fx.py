from stgs import *
from animations import animation

#### All screen effects/fx will be done in the fx specific layer or in the overlay.
#  Duration should be handled by the fx object.
#  Fx initiation into the fx layer will record its instance
#  
class fadeOut(pygame.sprite.Sprite):
    alpha = 0
    speed = 4 
    fadeBack = False
    def __init__(self, game, **kwargs):
        self.game = game
        self.onEnd = False
        for k, v in kwargs.items():
            self.__dict__[k] = v

        if self.onEnd:
            self.groups = game.pSprites, game.fxLayer
        else:
            self.groups = game.sprites, game.fxLayer
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.rect = pygame.Rect(0, 0, winWidth, winHeight)
        self.image = pygame.surface.Surface((self.rect.width, self.rect.height))
        

    def update(self):
        if self.alpha > 220:
            if self.fadeBack:
                fadeIn(self.game)
            self.end()
        else:
            self.alpha += self.speed

        self.image.set_alpha(self.alpha)

    def end(self):   
        if self.onEnd:
            self.onEnd()
        self.kill()

class fadeIn(pygame.sprite.Sprite):
    alpha = 255
    speed = 5 

    def __init__(self, game, **kwargs):
        self.game = game
        self.onEnd = False
        for k, v in kwargs.items():
            self.__dict__[k] = v

        if self.onEnd:
            self.groups = game.pSprites, game.fxLayer
        else:
            self.groups = game.sprites, game.fxLayer
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.rect = pygame.Rect(0, 0, winWidth, winHeight)
        self.image = pygame.surface.Surface((self.rect.width, self.rect.height))

    def update(self):
        if self.alpha < 2*self.speed:
            self.end()
        else:
            self.alpha -= self.speed

        self.image.set_alpha(self.alpha)

    def end(self):   
        if self.onEnd:
            self.onEnd()
        self.kill()

## Not in use yet
# class flash(pygame.sprite.Sprite):
#     def __init__(self, game,color, times, secondsBetween, **kwargs):
#         self.groups = game.sprites, game.layer2
#         pygame.sprite.Sprite.__init__(self, self.groups)

#         for k, v in kwargs.items():
#             self.__dict__[k] = v

#         self.active = True
#         self.rect = pygame.Rect(0, 0, winWidth, winHeight)
#         self.image = pygame.surface.Surface((self.rect.width, self.rect.height))
#         self.color = color
#         self.image.fill(self.color)
#         self.times = times
#         self.alpha = 255
#         self.between = secondsBetween
#         self.bufferTime = 0
#         self.between2 = self.between
        
        
#     def update(self):
#         if self.active:
#             if self.times > 0:
#                 if self.between2 < 0:
#                     if self.alpha == 0:
#                         self.alpha = 255
#                         self.image.set_alpha(self.alpha)
#                         self.between2 = self.between
#                     elif self.alpha == 255:
#                         self.alpha = 0
#                         self.image.set_alpha(self.alpha)
#                         self.between2 = self.between
#                         self.times = self.times - 1
#                 else:
#                     self.between2 = self.between2 - self.bufferTime
#             else:
#                 self.alpha = 0
#                 self.image.set_alpha(self.alpha)
#                 self.active = False