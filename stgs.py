import os
import pygame

#### Establishes file paths ####
PATH = os.path.dirname(os.path.abspath(__file__))
ASSETSPATH = os.path.join(PATH, 'assets')

#### Either centers the player no matter what (False) or doesn't scroll over the boundary of the level (True and preferred) ####
CAMLIMIT = True
SHOWFPS = True

#### Returns the asset's path ####
def asset(assetName):
    global ASSETSPATH

    return os.path.join(ASSETSPATH, assetName)

#### Establishes window size ####
winWidth, winHeight = 1200, 700

#### Defines what key binding is set for each action ####
keySet = {'start': pygame.K_s, 'pRight': [pygame.K_RIGHT, pygame.K_d], 'pLeft': [pygame.K_LEFT, pygame.K_a], 'pUp': [pygame.K_UP, pygame.K_w], 'fullScreen': pygame.K_f}

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

