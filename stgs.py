import os
import pygame

#### Establishes file paths ####
PATH = os.path.dirname(os.path.abspath(__file__))
ASSETSPATH = os.path.join(PATH, 'assets')

#### Either centers the player no matter what (False) or doesn't scroll over the boundary of the level (True and preferred) ####
CAMLIMIT = True

#### Returns the asset's path ####
def asset(assetName):
    global ASSETSPATH

    return os.path.join(ASSETSPATH, assetName)

#### Establishes window size ####
winWidth, winHeight = 1200, 700

#### Defines what key binding is set for each action ####
keySet = {'start': pygame.K_s, 'pRight': [pygame.K_RIGHT, pygame.K_d], 'pLeft': [pygame.K_LEFT, pygame.K_a], 'pUp': [pygame.K_UP, pygame.K_w]}

#### Changes movement from flying to platforming ####
platformer = False

def checkKey(move):
    returnVal = False
    keys = pygame.key.get_pressed()
    for k in move:
        if keys[k]:
            returnVal = True
        
    return returnVal


