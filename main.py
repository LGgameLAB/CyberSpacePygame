import pygame
pygame.init()
import random
import sys
from stgs import *
from player import *
from enemy import *
from camera import *
from objects import *
from levels import *

#### Game object ####
class game:

    #### Initialize game object ####
    #
    # Groups each sprite type to perform targetted tasks
    # All sprites do go into the sprites group
    # Sets up window, font, gravity, and cam
    # Loads data for the game levels and the player

    def __init__(self):
        self.enemies = pygame.sprite.Group()
        self.sprites = pygame.sprite.Group()
        self.colliders = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()

        self.win = pygame.display.set_mode((winWidth, winHeight))

        self.font1 = pygame.font.SysFont('Comic Sans MS', 25)
        self.font2 = pygame.font.SysFont('Comic Sans MS', 23)
        self.loop = 0
        self.gravity = 1
        self.currentFps = 0
        self.cam = cam(winWidth, winHeight)
        self.clock = pygame.time.Clock()
        self.loadData()
    
    def loadData(self):
        self.levels = gameLevels
        self.player = player(self, asset('Space-ManR.png'), 'Space Man')
        self.player.gravity = self.gravity

    ####  Determines how the run will function ####
    def run(self):
        self.menuLoop()
        self.mainLoop()

    #### Controls how the levels will load ####
    def loadLevel(self, levelNum):
        self.level = self.levels[levelNum-1]
        self.level.load()
    
        for p in self.level.colliders:
            self.colliders.add(p)
        
        colliderRects = []
        for p in self.colliders:
            colliderRects.append(p.rect)
        
        self.player.colliders = colliderRects
        self.cam.width, self.cam.height = self.level.rect.width, self.level.rect.height

    #### Main game loop ####
    def mainLoop(self):
        self.loadLevel(1)
        
        while True:
            self.loop += 1
            self.clock.tick(60)
            self.refresh()

            ##Updates Game
            self.runEvents()
            self.update()

    def update(self): 
        self.getFps()
        self.sprites.update()
        self.cam.update(self.player)
        self.win.blit(self.level.image, self.cam.apply(self.level))

        for sprite in self.sprites:
            self.win.blit(sprite.image, self.cam.apply(sprite))

        if SHOWFPS:
            fpsText = self.font2.render(str(self.currentFps), True, (255, 255, 255))
            self.win.blit(fpsText, (1100, 5))
            
        ### Checks for bullet collision among enemies and bullets
        hits = pygame.sprite.groupcollide(self.enemies, self.bullets, False, True)
        for hit in hits:
            hit.health -= 5
        
        pygame.sprite.groupcollide(self.colliders, self.bullets, False, True)
        pygame.display.update()

    def quit(self):
        pygame.quit()
        sys.exit()

    def runEvents(self):
        ## Catch all events here
        self.events = pygame.event.get()
        for event in self.events:
            if event.type == pygame.QUIT:
                self.quit()
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.quit()

    def getFps(self):
        if self.loop > 1:
            if self.loop == 2:
                self.lastFrame = pygame.time.get_ticks()
            
            else:
                newFrame = pygame.time.get_ticks()
                self.currentFps = 1/((newFrame-self.lastFrame)/1000) 
                self.lastFrame = newFrame
                
                

    #### First menu loop ####
    def menuLoop(self):
        run = True

        while run:
            pygame.time.delay(50)
            
            self.runEvents()
            self.refresh()

            text1 = self.font1.render('Press S to Start', True, (50, 255, 255))
            text2 = self.font1.render('Welcome to Cyber Space', True, (50, 255, 255))
            text3 = self.font1.render('Created by Luke Gonsalves', True, (50, 255, 255))
            
            self.win.blit(text1, (30,30))
            self.win.blit(text2, (300, 300))
            self.win.blit(text3, (310, 400))

            keys = pygame.key.get_pressed()

            if keys[keySet['start']]:
                break
            
            pygame.display.update()
    
    def refresh(self):
        self.win.fill((0, 0, 0))

#### Creates and runs game ####
game1 = game()
print(gameLevels)
game1.run()