import os
import pygame
import colors
import math

#### Establishes file paths ####
PATH = os.path.dirname(os.path.abspath(__file__))
ASSETSPATH = os.path.join(PATH, 'assets')

#### File for saving settings in game. Every variable set here is default. Clearing the settings file should load everything as default. ####
saveFile = 'save.p'

#### Either centers the player no matter what (False) or doesn't scroll over the boundary of the level (True and preferred) ####
CAMLIMIT = True
SHOWFPS = True

#### FPS BOIS ####
FPS = 60

#### Volumes ####
musicVolume = 1
fxVolume = 1

#### Returns the asset's path ####
def asset(assetName):
    global ASSETSPATH

    return os.path.join(ASSETSPATH, assetName)

#### Establishes window size ####
winWidth, winHeight = 1200, 700

#### Anti-Aliasing on text ####
aalias = True

#### Defines what key binding is set for each action ####
keySet = {'start': pygame.K_s, 'pRight': [pygame.K_RIGHT, pygame.K_d], 'pLeft': [pygame.K_LEFT, pygame.K_a], 'pUp': [pygame.K_UP, pygame.K_w], 'fullScreen': pygame.K_f, 'pause': pygame.K_p}

#### Changes movement from flying to platforming ####
platformer = False

def checkKey(move):
    returnVal = False
    keys = pygame.key.get_pressed()
    for k in move:
        if keys[k]:
            returnVal = True
        
    return returnVal

#### Method works well however you have to set the black color (0,0,0) as the transparent color key in order to make the surface see through
class Spritesheet:
    # utility class for loading and parsing spritesheets
    def __init__(self, file, *args):
        if len(args) > 0:
            if args[0]:
                self.image = file
            else:
                self.image = pygame.image.load(file)
        else:
            self.image = pygame.image.load(file)
        
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def get_image(self, x, y, width, height):
        # grab an image out of a larger spritesheet
        img = pygame.Surface((width, height))
        img.blit(self.image, (0, 0), (x, y, width, height))
        img = pygame.transform.scale(img, (width, height))
        return img

if not __name__ == '__main__':
    fonts = {'1': pygame.font.Font(os.path.join('fonts', 'YuseiMagic-Regular.ttf'), 40),
            '2': pygame.font.SysFont('Comic Sans MS', 23),
            '3': pygame.font.Font(os.path.join('fonts', 'PottaOne-Regular.ttf'), 32),
            '4': pygame.font.Font(os.path.join('fonts', 'PottaOne-Regular.ttf'), 24),
            '5': pygame.font.Font(os.path.join('fonts', 'YuseiMagic-Regular.ttf'), 60),
            '6': pygame.font.Font(os.path.join('fonts', 'YuseiMagic-Regular.ttf'), 24),
            }

def sAsset(assetName):
    global ASSETSPATH

    return os.path.join(ASSETSPATH, 'sounds', assetName)
    
DEBUG = True ## Not much use right now. Can be used to control try/except statement flows.

def dist(vec1, vec2):
    dist1 = (vec1.x-vec2.x)**2
    dist2 = (vec1.y-vec2.y)**2
    return math.sqrt(dist1+dist2)

import pickle

def loadSave(file):
    try:
        with open(file, 'rb') as f:
            data = pickle.load(f)
            for k, v in data.items():
                globals()[k] = v
    except:
        print("No Save File")

def saveData(file, game):
    saveDict = {    # Each value must corresponde to a global variable in this file
        'musicVolume': game.mixer.musicVolume,
        'fxVolume': game.mixer.fxVolume,
        'aalias': game.antialiasing,
        'SHOWFPS': game.showFps,
    }
    with open(file, 'wb') as f:
        pickle.dump(saveDict, f)
    