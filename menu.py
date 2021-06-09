import pygame
import colors

class button(pygame.sprite.Sprite):
    def __init__(self, game, pos,**kwargs):
        self.game = game
        
        self.onClick = False
        self.groups = []
        self.rect = (0, 0, 200, 60)
        #          Normal           Selected
        self.colors = ((50, 255, 255), (255, 255, 255))
        self.spriteInit = False
        self.hover = False
        self.clicked = False
        self.instaKill = False
        self.text = ''
        self.center = False
        for k, v in kwargs.items():
            self.__dict__[k] = v

        pygame.sprite.Sprite.__init__(self, self.groups)

        self.rect = pygame.Rect(self.rect)
        self.rect.x, self.rect.y = pos
        self.image = pygame.Surface(self.rect.size, pygame.SRCALPHA)

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
                        if self.instaKill:
                            self.kill()

            self.image.fill(self.colors[1])
        else:
            self.image.fill(self.colors[0])
        
        self.image.blit(self.rendText, self.textRect)
    
    def reset(self):
        self.clicked = False

class settingSlider(pygame.sprite.Sprite):
    
    def __init__(self, game, pos,**kwargs):
        self.game = game
        self.rect = (0, 0, 200, 60)
        self.sliderRect = (0, 0, 20, 10)
        self.bgColor = colors.black
        #          line (normal)           Rect
        self.colors = ((50, 255, 255), colors.yellow, (255, 255, 255))
        self.clicked = False
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

class menuItem(pygame.sprite.Sprite):
    def __init__(self, game, pos, image, **kwargs):
        self.game = game
        self.rect = (0, 0, 100, 100)
        self.bgColor = (0, 0, 0, 0)
        #          line (normal)           Rect
        self.hover = False
        self.zoom = 1
        self.zoomMax = 2
        self.zoomSpeed = 0.4
        self.desc = ''
        self.text = ''
        self.groups = []       ## These few lines are the lines for component objects
        for k, v in kwargs.items():
            self.__dict__[k] = v
        
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.rect = pygame.Rect(self.rect)
        self.rect.topleft = pos
        self.image = pygame.Surface((self.rect.w, self.rect.h), pygame.SRCALPHA)
        self.imageSrc = pygame.image.load(image)

    def setIcon(self):
        self.icon = pygame.transform.scale(self.imageSrc, (int(self.imageSrc.get_width()*self.zoom), int(self.imageSrc.get_height()*self.zoom)))
        
    def setRect(self):
        self.rect = self.imageSrc.get_rect()
    
    def render(self):
        self.image.fill(self.bgColor)
        self.setIcon()
        rect = self.icon.get_rect(center=(self.rect.w/2, self.rect.h/2))
        self.image.blit(self.icon, rect)
    
    def update(self):
        self.hover = False
        mouseRect = pygame.Rect(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], 1, 1)
        if mouseRect.colliderect(self.rect):
            self.hover = True
        if self.hover:
            self.zoom = min(self.zoomMax, self.zoom + self.zoomSpeed)
        else:
            self.zoom = max(1, self.zoom - self.zoomSpeed)
        
        self.render()





        
