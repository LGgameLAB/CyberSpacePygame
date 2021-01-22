import pygame
import random
from stgs import *
from player import *
from enemy import *
from camera import *
from platforms import *
from levels import *

pygame.init()

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
        self.platforms = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()

        self.win = pygame.display.set_mode((winWidth, winHeight))

        self.font1 = pygame.font.SysFont('Comic Sans MS', 20)

        self.gravity = 1
        self.cam = cam(winWidth, winHeight)

        self.loadData()
    
    def loadData(self):
        self.levels = gameLevels
        self.player = player(self, asset('Space-ManR.png'), 'Space Man')
        self.player.gravity = self.gravity
        self.sprites.add(self.player)

    ####  Determines how the run will function ####
    def run(self):
        self.menuLoop()
        self.mainLoop()

    #### Controls how the levels will load ####
    def loadLevel(self, levelNum):
        self.level = self.levels[levelNum-1]
        
        for p in self.level.platforms:
            self.platforms.add(p)
        
        platformRects = []
        for p in self.platforms:
            platformRects.append(p.rect)
        
        self.player.colliders = platformRects
        self.cam.width, self.cam.height = self.level.rect.width, self.level.rect.height

    #### Main game loop ####
    def mainLoop(self):

        self.loadLevel(1)

        run = True
        while run:
            pygame.time.delay(50)

            self.events = pygame.event.get()

            for event in self.events:
                if event.type == pygame.QUIT:
                    run = False

            self.refresh()

            ##Game functions go here
            self.sprites.update()
            self.cam.update(self.player)

            self.win.blit(self.level.image, self.cam.apply(self.level))

            for sprite in self.sprites:
                self.win.blit(sprite.image, self.cam.apply(sprite))
            
            pygame.display.update()

    #### First menu loop ####
    def menuLoop(self):
        run = True

        while run:
            pygame.time.delay(50)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            self.refresh()

            text1 = self.font1.render('Press S to Start', False, (50, 255, 255))
            text2 = self.font1.render('Welcome to Cyber Space', False, (50, 255, 255))
            text3 = self.font1.render('Created by Luke Gonsalves', False, (50, 255, 255))
            
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