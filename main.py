import pygame
import pyperclip

pygame.init()
import os
import random
import sys

from camera import *
from enemy import *
from fx import *
from levels import *
from objects import *
from player import *
from sfx import *
from stgs import *


#### Game object ####
class game:

    #### Initialize game object ####
    #
    # Groups each sprite type to perform targetted tasks
    # All sprites go into the sprites group
    # Sets up window, font, gravity, and cam
    # Loads data for the game levels and the player

    def __init__(self):
        self.enemies = pygame.sprite.Group()
        self.sprites = pygame.sprite.Group()
        self.pSprites = pygame.sprite.Group()
        self.colliders = pygame.sprite.Group()
        self.dmgRects = pygame.sprite.Group()
        self.pBullets = pygame.sprite.Group()
        self.eBullets = pygame.sprite.Group()   
        self.items = pygame.sprite.Group()
        self.layer1 = pygame.sprite.Group()
        self.layer2 = pygame.sprite.Group()
        self.fxLayer = pygame.sprite.Group()
        self.overlayer = pygame.sprite.Group()
        self.rendLayers = [self.layer1, self.layer2]
        self.mixer = gameMixer()

        self.win = pygame.display.set_mode((winWidth, winHeight))
        self.font1 = pygame.font.Font(os.path.join('fonts', 'YuseiMagic-Regular.ttf'), 30)
        self.font2 = pygame.font.SysFont('Comic Sans MS', 23)
        self.menuFont = pygame.font.Font(os.path.join('fonts', 'YuseiMagic-Regular.ttf'), 15)
        self.pause = False
        self.lastPause = pygame.time.get_ticks()
        self.loop = 0
        self.points = 0
        self.gravity = 1.6
        self.currentFps = 0
        self.fullScreen = False
        self.cam = cam(winWidth, winHeight)
        self.clock = pygame.time.Clock()
        self.loadData()

    def loadData(self):
        self.levels = gameLevels
        self.player = player(self, asset('Space-ManR.png'), 'Space Man', imgSheet = 
            {'active': True, ## Will become deprecated but is usefulin current development. Allows use of sample image.
            'tileWidth': 64, 
            'r': asset('player/idleR.png'), 
            'l': asset('player/idleL.png'), 
            'idleR': asset('player/idleR.png'), 
            'flyR': asset('player/flyR.png'), 
            'flyL': asset('player/flyL.png')})
            
        self.player.gravity = self.gravity

    ####  Determines how the run will function ####
    def run(self):
        self.menuLoop()
        self.mainLoop()

    #### Controls how the levels will load ####
    def loadLevel(self, levelNum, *args):   
        for enemy in self.enemies:
            enemy.kill()
        
        for sprite in  self.colliders:
            sprite.kill()
            
        for sprite in  self.eBullets:
            sprite.kill()

        for sprite in  self.pBullets:
            sprite.kill()

        for sprite in  self.dmgRects:
            sprite.kill()
        
        for sprite in self.items:
            sprite.kill()

        if len(args) < 1:
            try:
                for obj in self.level.objects:
                    obj.kill()
            except:
                pass

            self.level = self.levels[levelNum-1] 
            self.level.load(self)
            
            self.cam.width, self.cam.height = self.level.rect.width, self.level.rect.height
            
            try:
                self.player.rect.topleft = self.level.entrance.rect.center
            except:
                print("No player Pos")
            

        else:
            self.level = level(rendType=1, mapDir=importLevel(args[0]))
            self.level.load(self)

            self.cam.width, self.cam.height = self.level.rect.width, self.level.rect.height

            try:
                self.player.rect.topleft = self.level.entrance.rect.center
            except:
                print("No player Pos")

    #### Main game loop ####
    def mainLoop(self):
        
        while True:
            self.loop += 1
            self.clock.tick(60)
            self.refresh()

            ##Updates Game
            self.runEvents()
            self.update()

    def update(self): 
        self.getFps()
        self.getFullScreen()
        self.getPause()
        if self.pause:
            self.pSprites.update()
        else:
            self.sprites.update()
            self.checkHits()
        self.cam.update(self.player)
        
        self.render()

        
        pygame.display.update()

    def render(self):
        self.win.blit(self.level.image, self.cam.apply(self.level))

        for layer in self.rendLayers:
            for sprite in layer:
                try:
                    self.win.blit(sprite.image, self.cam.apply(sprite))
                except:
                    pass
        
        for fx in self.fxLayer:
            self.win.blit(fx.image, fx.rect)
        
        for sprite in self.overlayer:
            self.win.blit(sprite.image, sprite.rect)
        
        
        if SHOWFPS:
            fpsText = self.font2.render(str(self.currentFps), True, (255, 255, 255))
            self.win.blit(fpsText, (1100, 5))
        
        visPoints = self.font2.render(str(self.points), False, (255, 255, 255))
        self.win.blit(visPoints, (winWidth/2 - 100, 5))

    def checkHits(self):
        ### Checks for bullet collision among enemies and bullets
        hits = pygame.sprite.groupcollide(self.enemies, self.pBullets, False, True)
        for hit in hits:
            hit.health -= self.player.gun.damage
            if hit.health <= 0:
                self.points += hit.points
        
        hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
        for hit in hits:
            self.player.takeDamage(hit.damage)
        
        hits = pygame.sprite.spritecollide(self.player, self.dmgRects, False)
        for hit in hits:
            
            self.player.takeDamage(hit.damage)

        hits = pygame.sprite.spritecollide(self.player, self.eBullets, False)
        for hit in hits:
            self.player.takeDamage(hit.damage)

        pygame.sprite.groupcollide(self.colliders, self.pBullets, False, True)
        pygame.sprite.groupcollide(self.colliders, self.eBullets, False, True)

        items = pygame.sprite.spritecollide(self.player, self.items, True)
        for item in items:
            if isinstance(item, coin):
                self.points += item.value
            elif isinstance(item, gunConsumable):
                self.player.gun.kill()
                
                self.player.gun = item.gun(self, self.player)
                self.points += 50

            elif isinstance(item, hpPack1):
                self.player.health += item.value

        tpCols = pygame.sprite.spritecollide(self.player, self.level.teleporters, False)
        for tp in tpCols:
            fadeOut(self, speed = 20, alpha = 120, fadeBack = True)
            self.player.rect.topleft = tp.target

        ### DEcryptor/key collision detection
        try:
            if pygame.sprite.collide_rect(self.player, self.level.key):
                self.level.keyObtained = True
                self.level.key.kill()
        except:
            pass
        
        if pygame.sprite.collide_rect(self.player, self.level.door) and self.level.keyObtained:
            self.pause = True
            fadeOut(self, speed = 8, alpha = 40, onEnd = lambda:self.nextLevel())
    def unPause(self):
        self.pause = False

    def nextLevel(self):
        
        if DEBUG:
            try:
                self.loadLevel(self.levels.index(self.level) + 2)
                fadeIn(self, speed = 20, onEnd = lambda:self.unPause())
            except IndexError:
                self.loadData()
                self.run()
        else:
            try:
                self.loadLevel(self.levels.index(self.level) + 2)
                fadeIn(self, onEnd = lambda:self.unPause())
            except:
                self.loadData()
                self.run()

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
                    if self.fullScreen:
                        self.win = pygame.display.set_mode((winWidth, winHeight))
                        self.fullScreen = False
                    else:
                        self.quit()

    def getFps(self):
        if self.loop > 1:
            if self.loop == 2:
                self.lastFrame = pygame.time.get_ticks()
            
            else:
                newFrame = pygame.time.get_ticks()
                self.currentFps = 1/((newFrame-self.lastFrame)/1000) 
                self.lastFrame = newFrame
                
    def getFullScreen(self):
        keys = pygame.key.get_pressed()
        if keys[keySet['fullScreen']]:
            if self.fullScreen:
                self.win = pygame.display.set_mode((winWidth, winHeight))
                self.fullScreen = False
            else:
                self.win = pygame.display.set_mode((winWidth, winHeight), pygame.FULLSCREEN)
                self.fullScreen = True
            #pygame.display.toggle_fullscreen()

    def getPause(self):
        if pygame.time.get_ticks() - self.lastPause >= 120:
            keys = pygame.key.get_pressed()
            if keys[keySet['pause']]:
                if self.pause:
                    self.pause = False
                else:
                    self.pause = True
                self.lastPause = pygame.time.get_ticks()

    #### First menu loop ####
    def menuLoop(self):
        run = True
        startButton = button(self, (winWidth/2, 140), text="Start", center = True)
        loadCustomLevelBtn = button(self, (winWidth/2, 100), text="Load Custom Level", center = True)
        buttons = pygame.sprite.Group(startButton, loadCustomLevelBtn)
        while run:
            pygame.time.delay(50)
            
            self.runEvents()
            self.refresh()

            buttons.update()
            for btn in buttons:
                self.win.blit(btn.image, btn.rect)

            if startButton.clicked:
                self.loadLevel(1)
                break
            
            if loadCustomLevelBtn.clicked:
                self.loadLevel(None, pyperclip.paste())
                break
            
            text1 = self.font1.render('Press S to Start', True, (50, 255, 255))
            text2 = self.font1.render('Welcome to Cyber Space', True, (50, 255, 255))
            text3 = self.font1.render('Created by Luke Gonsalves', True, (50, 255, 255))
            
            self.win.blit(text1, (30,30))
            self.win.blit(text2, (300, 300))
            self.win.blit(text3, (310, 400))

            keys = pygame.key.get_pressed()

            if keys[keySet['start']]:
                self.loadLevel(1)
                break
            
            pygame.display.update()
    
    def refresh(self):
        self.win.fill((0, 0, 0))

#### Creates and runs game ####
game1 = game()
game1.run()
