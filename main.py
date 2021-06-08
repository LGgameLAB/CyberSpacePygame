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
from overlay import *
from player import *
from sfx import *
from stgs import *
from menu import *
import colors

loadSave(saveFile)
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
        self.layer1 = pygame.sprite.Group()
        self.layer2 = pygame.sprite.Group()
        self.fxLayer = pygame.sprite.Group()
        self.overlayer = pygame.sprite.Group()
        self.rendLayers = [self.layer1, self.layer2]
        self.mixer = gameMixer()
        self.mixer.setMusicVolume(musicVolume) # between 0 and 1
        self.mixer.setFxVolume(fxVolume)
        self.antialiasing = aalias

        pygame.display.set_icon(pygame.image.load(asset('logo.png')))
        self.win = pygame.display.set_mode((winWidth, winHeight))
        pygame.display.set_caption("Cyber Space")
        pygame.display.set_icon(pygame.image.load(asset('logo.png')))
        self.font1 = pygame.font.Font(os.path.join('fonts', 'YuseiMagic-Regular.ttf'), 30)
        self.font2 = pygame.font.SysFont('Comic Sans MS', 23)
        self.menuFont = pygame.font.Font(os.path.join('fonts', 'YuseiMagic-Regular.ttf'), 15)
        self.gameOverFont = pygame.font.Font(os.path.join('fonts', 'YuseiMagic-Regular.ttf'), 60)
        self.victoryFont = pygame.font.Font(os.path.join('fonts', 'YuseiMagic-Regular.ttf'), 72)
        self.lastPause = pygame.time.get_ticks()
        self.won = False
        self.points = 0
        self.gravity = 1.6
        self.currentFps = 0
        self.showFps = SHOWFPS
        self.fullScreen = False
        self.cam = cam(winWidth, winHeight)
        self.clock = pygame.time.Clock()
        self.new()


    def new(self):
        self.enemies = pygame.sprite.Group()
        self.sprites = pygame.sprite.Group()
        self.pSprites = pygame.sprite.Group()
        self.colliders = pygame.sprite.Group()
        self.dmgRects = pygame.sprite.Group()
        self.pBullets = pygame.sprite.Group()
        self.eBullets = pygame.sprite.Group()
        self.items = pygame.sprite.Group()
        self.levels = gameLevels
        self.player = player(self, asset('Space-ManR.png'), 'Cyber Man', imgSheet = 
            {'active': True, ## Will become deprecated but is usefulin current development. Allows use of sample image.
            'tileWidth': 64, 
            'r': asset('player/idleR(2).png'), 
            'l': asset('player/idleL(2).png'), 
            'idleR': asset('player/idleR(2).png'), 
            'idleL': asset('player/idleL(2).png'),
            'flyR': asset('player/flyR(2).png'), 
            'flyL': asset('player/flyL(2).png')})
            
        self.player.gravity = self.gravity
        self.end = False
        self.pause = False
        self.pauseScreen = pauseOverlay(self)

    ####  Determines how the run will function ####
    def run(self):
        self.menuLoop()
        self.mixer.playMusic(asset('sounds/track 1.wav'))
        self.mainLoop()
        self.mixer.stop()
        if self.won:
            self.victoryLoop()
        else:
            self.gameOver()

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
            if args[0] is None:
                levelDir = importLevelFile()
            else:
                levelDir = importLevel(args[0])

            if levelDir is None:
                self.reset()
            else:
                self.level = level(rendType=1, mapDir=levelDir)
                self.level.load(self)

                self.cam.width, self.cam.height = self.level.rect.width, self.level.rect.height

                try:
                    self.player.rect.topleft = self.level.entrance.rect.center
                except:
                    print("No player Pos")
                    self.reset()

        self.player.gun.recenter()

    #### Main game loop ####
    def mainLoop(self):
        
        while not self.end:
            self.clock.tick(FPS)
            self.refresh()

            ##Updates Game
            self.runEvents()
            self.update()

    def update(self): 
        self.getFps()
        self.getPause()
        if self.pause:
            self.pSprites.update()
            self.pauseScreen.update()
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
        
        self.win.blit(transparentRect((winWidth, 60), 120), (0, 0))
        visPoints = fonts['6'].render("Score: " + str(self.points), self.antialiasing, (255, 255, 255))
        self.win.blit(visPoints, (100, 20))

        for sprite in self.overlayer:
            self.win.blit(sprite.image, sprite.rect)
        
        
        if self.showFps:
            fpsText = fonts['6'].render(str(self.currentFps), self.antialiasing, (255, 255, 255))
            self.win.blit(fpsText, (1100, 5))
        

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

        hits = pygame.sprite.groupcollide(self.pBullets, self.colliders, True, False)
        for hit in hits:
            particles(self, hit.rect, lifeSpan = 300, tickSpeed=2, size = 5).setParticleKwargs(speed=1.5, shrink=0.6, life=140, color=colors.orangeRed)
        
        pygame.sprite.groupcollide(self.colliders, self.eBullets, False, True)

        items = pygame.sprite.spritecollide(self.player, self.items, True)
        for item in items:
            if isinstance(item, coin):
                self.points += item.value
                self.player.coinMeter.addCoin()
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
            self.player.gun.recenter()

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
        
        if self.player.health <= 0:
            self.pause = True
            def end():
                self.end = True
            fadeOut(self, speed = 2, alpha = 40, color = colors.dark(colors.red, 60), noKill = True, onEnd = lambda:end())

    def unPause(self):
        self.pause = False
        self.pauseScreen.deactivate()
        self.overlayer.remove(self.pauseScreen)

    def reset(self):
        for sprite in self.sprites:
            sprite.kill()
        for sprite in self.pSprites:
            sprite.kill()
        self.new()
        self.run()

    def nextLevel(self):
        if DEBUG:
            try:
                self.loadLevel(self.levels.index(self.level) + 2)
                fadeIn(self, speed = 20, onEnd = lambda:self.unPause())
            except IndexError:
                self.end = True
                self.won = True
        else:
            try:
                self.loadLevel(self.levels.index(self.level) + 2)
                fadeIn(self, onEnd = lambda:self.unPause())
            except:
                self.end = True
                self.won = True

    def quit(self):
        saveData(saveFile, self)
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
        self.getFullScreen()

    def getFps(self):
        self.currentFps = round(self.clock.get_fps(), 1)
        return self.currentFps
    
    def toggleFps(self):
        if self.showFps:
            self.showFps = False
        else:
            self.showFps = True

    def toggleAalias(self):
        if self.antialiasing:
            self.antialiasing = False
        else:
            self.antialiasing = True
        
        self.pauseScreen.loadComponents()

    def getFullScreen(self):
        keys = pygame.key.get_pressed()
        if keys[keySet['fullScreen']]:
            pygame.display.set_icon(pygame.image.load(asset('logo.png')))
            if self.fullScreen:
                self.win = pygame.display.set_mode((winWidth, winHeight))
                self.fullScreen = False
            else:
                self.win = pygame.display.set_mode((winWidth, winHeight), pygame.FULLSCREEN)
                self.fullScreen = True
            pygame.display.set_icon(pygame.image.load(asset('logo.png')))
            #pygame.display.toggle_fullscreen()

    def getPause(self):
        if pygame.time.get_ticks() - self.lastPause >= 180:
            keys = pygame.key.get_pressed()
            if keys[keySet['pause']]:
                if self.pause:
                    self.unPause()
                else:
                    self.pause = True
                    self.overlayer.add(self.pauseScreen)
                    self.pauseScreen.activate()

                self.lastPause = pygame.time.get_ticks()

    def getSprBylID(self, lID):
        for sprite in self.sprites:
            try:
                if sprite.lID == lID:
                    return sprite
            except:
                pass
        return False

    #### First menu loop ####
    def menuLoop(self):
        def dipMenu():
            returnButton = button(self, (winWidth/2, 100), text="Return", center = True)
            slider1 = settingSlider(self, (800, 600)) 
            comps = pygame.sprite.Group(returnButton, slider1)
            while True:
                pygame.time.delay(50)
                
                self.runEvents()
                self.refresh()

                comps.update()
                for comp in comps:
                    self.win.blit(comp.image, comp.rect)

                if returnButton.clicked:
                    break

                if checkKey(keySet['start']):
                    self.loadLevel(1)
                    break
                
                text2 = fonts['1'].render('Cyber Space', self.antialiasing, (50, 255, 255))
                self.win.blit(text2, (30,30))

                keys = pygame.key.get_pressed()
                
                pygame.display.update()

        def compendiumMenu():
            x, y = 100, 100
            stepX, stepY = 120, 120
            returnButton = button(self, (winWidth-240, 70), text="Return", center = True)
            #menuItem(self, (x, y), asset(''), desc='', text=''),
            itemCompendium = [
                menuItem(self, (x, y), asset('objects/gun.png'), desc='The Standard Blaster', text='Cyber Blaster'),
                menuItem(self, (x+stepX, y), asset('objects/gun.png'), desc='The Standard Blaster X3 -- THREE TIMES THE POWER', text='Cyber Blaster'),
                menuItem(self, (x+stepX*2, y), asset('objects/lazgun.png'), desc='The Standard Blaster X3 -- THREE TIMES THE POWER', text='Cyber Blaster'),
            ]
            comps = pygame.sprite.Group(itemCompendium, returnButton)
            while True:
                descText = ''
                pygame.time.delay(50)
                
                self.runEvents()
                self.refresh()

                comps.update()
                for comp in comps:
                    self.win.blit(comp.image, comp.rect)

                for i in itemCompendium:
                    if i.hover:
                        descText = i.desc

                if returnButton.clicked:
                    break

                if checkKey(keySet['start']):
                    self.loadLevel(1)
                    break
                
                text1 = fonts['1'].render('Cyber Space', self.antialiasing, (50, 255, 255))
                text2 = fonts['2'].render(descText, self.antialiasing, (50, 255, 255))
                self.win.blit(text1, (30,winHeight - 70))
                self.win.blit(text2, (winWidth- 1200,winHeight - 240))

                keys = pygame.key.get_pressed()
                
                pygame.display.update()

        def settingsMenu():
            returnButton = button(self, (winWidth-240, 70), text="Return", center = True)
            comps = pygame.sprite.Group(returnButton)
            audioSlider1 = settingSlider(self, (100, 350), addGroups = [comps])
            audioSlider2 = settingSlider(self, (100, 500), addGroups = [comps])
            audioSlider1.image.set_colorkey((0,0,0))
            audioSlider2.image.set_colorkey((0,0,0))
            fpsButton = button(self, (800, 250), text = 'Toggle FPS', onClick = lambda:self.toggleFps() ,addGroups = [comps], center = True)
            aaliasButton = button(self, (800, 330), text = 'Toggle Anti - Aliasing', onClick = lambda:self.toggleAalias() ,addGroups = [comps], center = True)
            texts = [
                text('5', 'Paused', colors.cyan, self.antialiasing, (winWidth/2.4, 10)),
                text('1', 'Audio Control', colors.cyan, self.antialiasing, (75, 250)),
                text('6', 'Music Volume', colors.cyan, self.antialiasing, (75, 325)),
                text('6', 'Fx Volume', colors.cyan, self.antialiasing, (75, 475))
            ]
            def applyComps():
                self.mixer.setMusicVolume(audioSlider1.get_ratio())
                self.mixer.setFxVolume(audioSlider2.get_ratio())

            audioSlider1.setRatio(self.mixer.musicVolume)
            audioSlider2.setRatio(self.mixer.fxVolume)

            while True:
                pygame.time.delay(50)
                
                self.runEvents()
                self.refresh()
                applyComps()

                comps.update()
                for comp in comps:
                    self.win.blit(comp.image, comp.rect)

                for t in texts:
                    self.win.blit(t.rend, t.pos)

                if returnButton.clicked:
                    break

                if checkKey(keySet['start']):
                    self.loadLevel(1)
                    break
                
                text2 = fonts['1'].render('Cyber Space', self.antialiasing, (50, 255, 255))
                self.win.blit(text2, (30,30))

                keys = pygame.key.get_pressed()
                
                pygame.display.update()

        def main():
            startButton = button(self, (winWidth/2, 100), text="Start", center = True)
            dipButton = button(self, (50, winHeight-120), text="Settings", center=True)
            compendButton = button(self, (275, winHeight-120), text="Item Compendium", center=True)
            loadCustomLevelBtn = button(self, (winWidth/2, 180), text="Load Custom Level (web)", center = True)
            loadCustomLevelBtn2 = button(self, (winWidth/2, 260), text="Load Custom Level (file)", center = True)
            comps = pygame.sprite.Group(startButton, loadCustomLevelBtn, loadCustomLevelBtn2, dipButton, compendButton) # Stands for components fyi
            while True:
                pygame.time.delay(50)
                
                self.runEvents()
                self.refresh(asset('objects/genBg/genBg/Nether.jpg'))

                comps.update()
                for comp in comps:
                    self.win.blit(comp.image, comp.rect)

                if startButton.clicked:
                    self.loadLevel(1)
                    break
                
                if loadCustomLevelBtn.clicked:
                    self.loadLevel(None, pyperclip.paste())
                    break

                if loadCustomLevelBtn2.clicked:
                    self.loadLevel(None, None)
                    break
                
                if dipButton.clicked:
                    settingsMenu()
                    dipButton.reset()
                
                if compendButton.clicked:
                    compendiumMenu()
                    compendButton.reset()
                
                text1 = self.font2.render('Press S to Start', self.antialiasing, (50, 255, 255))
                text2 = self.font1.render('Welcome to Cyber Space', self.antialiasing, (50, 255, 255))
                text3 = self.font1.render('Created by LGgameLAB', self.antialiasing, (50, 255, 255))
                
                self.win.blit(text1, (30,30))
                self.win.blit(text2, (100, 200))
                self.win.blit(text3, (100, 300))

                keys = pygame.key.get_pressed()

                if keys[keySet['start']]:
                    self.loadLevel(1)
                    break
                
                pygame.display.update()
        
        main()

    def victoryLoop(self):
        menuButton = button(self, (winWidth/2, winHeight/2), text="Back to Menu", center = True, colors = (colors.yellow, colors.white))
        buttons = pygame.sprite.Group(menuButton)
        while True:
            pygame.time.delay(50)
            
            self.runEvents()
            self.refresh()

            buttons.update()
            for btn in buttons:
                self.win.blit(btn.image, btn.rect)

            if menuButton.clicked:
                self.reset()
                break
            
            text1 = self.victoryFont.render('Victory', self.antialiasing, colors.yellow, 20)
            text2 = fonts['1'].render("Score: " + str(self.points), self.antialiasing, (colors.yellow))
            
            self.win.blit(text2, (800, 70))
            self.win.blit(text1, (winWidth/2 - text1.get_width()/2 ,30))
            
            pygame.display.update()

    def gameOver(self):
        restartButton = button(self, (winWidth/2, winHeight/2), text="Back to Menu", center = True, colors = (colors.yellow, colors.white))
        buttons = pygame.sprite.Group(restartButton)
        while True:
            pygame.time.delay(50)
            
            self.runEvents()
            self.refresh()

            buttons.update()
            for btn in buttons:
                self.win.blit(btn.image, btn.rect)

            if restartButton.clicked:
                self.reset()
                break
            
            text1 = self.gameOverFont.render('Game Over', self.antialiasing, colors.dark(colors.red, 20))
            text2 = fonts['1'].render("Score: " + str(self.points), self.antialiasing, (colors.yellow))
            
            self.win.blit(text1, (50,50))
            self.win.blit(text2, (800, 70))
            
            pygame.display.update()

    def refresh(self, bg = False):
        if bg:
            self.win.blit(pygame.transform.scale(pygame.image.load(bg), (winWidth, winHeight)), (0, 0))
        self.win.fill((0, 0, 0))

#### Creates and runs game ####
game1 = game()
while __name__ == '__main__':
    game1.run()