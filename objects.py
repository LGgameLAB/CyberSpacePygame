import pygame
from stgs import *
from animations import *

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

class door(pygame.sprite.Sprite):
    color = (255, 255, 255)

    def __init__(self, game, rect, **kwargs):
        self.groups = game.sprites, game.layer1
        pygame.sprite.Sprite.__init__(self, self.groups)
        
        self.rect = pygame.Rect(rect)

        for k, v in kwargs.items():
            self.__dict__[k] = v

        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.fill(self.color)

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
    rect = (0, 0, 162, 20)
    #          Normal           Selected
    colors = ((50, 255, 255), (255, 255, 255))
    spriteInit = False
    hover = False
    clicked = False
    text = ''
    center = False
    def __init__(self, game, pos,**kwargs):
        self.game = game
        
        for k, v in kwargs.items():
            self.__dict__[k] = v

        if self.spriteInit:
            pygame.sprite.Sprite.__init__(self, self.groups)
        else:
            pygame.sprite.Sprite.__init__(self)

        self.rect = pygame.Rect(self.rect)
        self.rect.x, self.rect.y = pos
        self.image = pygame.Surface(self.rect.size)

        self.rendText = self.game.menuFont.render(self.text, True, (0, 0, 0))
        self.textRect = self.rendText.get_rect()
        if self.center:
            self.textRect.center = pygame.Rect(0, 0, self.rect.width, self.rect.height).center
        else:
            self.textRect.x += 2
            self.textRect.y += 2
        print(self.rendText.get_rect())

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
            self.image.fill(self.colors[1])
        else:
            self.image.fill(self.colors[0])
        
        self.image.blit(self.rendText, self.textRect)
        
        
def menuBtn(game, pos):
    return button(game, pos)
def tp1(game, pos, target):
    return teleporter(game, asset('objects/teleporter1.png'), pos, target)

def bitCoin(game, pos):
    return coin(game, pos, asset('objects/bitCoin.png'))

def key1(game, pos):
    return key(game, pos, asset('objects/decryptor.png'))
