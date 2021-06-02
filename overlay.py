import pygame
import colors
from stgs import *
from objects import *

pygame.font.init()
class text:
    def __init__(self, fNum, text, color, aalias, pos):
        self.rend = fonts[fNum].render(text, aalias, color)
        self.pos = pygame.Vector2(pos)
    
    def __str__(self):
        return self.rend

def transparentRect(size, alpha, color=(0, 0, 0)):
    surf = pygame.Surface(size, pygame.SRCALPHA)
    surf.fill((color[0], color[1], color[2], alpha))
    return surf 

class pauseOverlay(pygame.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        pygame.sprite.Sprite.__init__(self)
        self.components = pygame.sprite.Group()
        self.text = []
        self.active = False
        self.rect = pygame.Rect(0, 0, winWidth, winHeight)
        self.image = pygame.Surface((winWidth, winHeight), pygame.SRCALPHA)
        self.transparent = (255,182,193)
        self.image.set_colorkey(self.transparent)
        self.loadComponents()
        self.render()

    def loadComponents(self):
        for comp in self.components:
            comp.kill()
            
        self.audioSlider1 = settingSlider(self.game, (100, 350), addGroups = [self.components])
        self.audioSlider2 = settingSlider(self.game, (100, 500), addGroups = [self.components])
        self.audioSlider1.image.set_colorkey((0,0,0))
        self.audioSlider2.image.set_colorkey((0,0,0))
        self.fpsButton = button(self.game, (800, 250), text = 'Toggle FPS', onClick = lambda:self.game.toggleFps() ,addGroups = [self.components], center = True)
        self.aaliasButton = button(self.game, (800, 330), text = 'Toggle Anti - Aliasing', onClick = lambda:self.game.toggleAalias() ,addGroups = [self.components], center = True)
        self.text = [
            text('5', 'Paused', colors.cyan, self.game.antialiasing, (self.rect.width/2.4, 10)),
            text('1', 'Audio Control', colors.cyan, self.game.antialiasing, (75, 250)),
            text('6', 'Music Volume', colors.cyan, self.game.antialiasing, (75, 325)),
            text('6', 'Fx Volume', colors.cyan, self.game.antialiasing, (75, 475))
        ]

        self.audioSlider1.setRatio(self.game.mixer.musicVolume)
        self.audioSlider2.setRatio(self.game.mixer.fxVolume)
        
    def applyComponents(self):
        self.game.mixer.setMusicVolume(self.audioSlider1.get_ratio())
        self.game.mixer.setFxVolume(self.audioSlider2.get_ratio())

    def activate(self):
        self.active = True
        self.audioSlider1.setRatio(self.game.mixer.musicVolume)
        self.audioSlider2.setRatio(self.game.mixer.fxVolume)

    def deactivate(self):
        self.active = False

    def update(self):
        if self.active:
            self.render()
            self.components.update()
            self.applyComponents()
    
    def render(self):
        self.image.fill((0,0,0,160)) #self.transparent)
        for comp in self.components:
            self.image.blit(comp.image, comp.rect)
        for text in self.text:
            self.image.blit(text.rend, text.pos)
        
