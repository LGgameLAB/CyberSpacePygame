import pygame
import pytmx
from stgs import *
from enemy import *
from objects import *

class level:
    rendType = 0
    colliders = []
    width = winWidth
    height = winHeight
    levelSize = (width, height)
    rect = pygame.Rect(0, 0, width, height)
    mapDir = ''

    def __init__(self, **kwargs):
        self.objects = pygame.sprite.Group() 
        self.triggers = pygame.sprite.Group()
        self.platWalls = pygame.sprite.Group()
        for k, v in kwargs.items():
            self.__dict__[k] = v

    def load(self, game):
        self.keyObtained = False
        self.game = game
        if self.rendType == 0:
            for p in self.colliders:
                if p.rect.bottomright[0] > self.levelSize[0]:
                    self.levelSize = (p.rect.bottomright[0], self.levelSize[1])
                
                if p.rect.bottomright[1] > self.levelSize[1]:
                    self.levelSize = (self.levelSize[0], p.rect.bottomright[1])
            
            self.rect = pygame.Rect(0, 0, self.levelSize[0], self.levelSize[1])
            self.image = pygame.Surface(self.levelSize)

            for p in self.colliders:
                self.image.blit(p.image, p.rect)
        
        elif self.rendType == 1:
            self.loadTiled()
    
    def loadTiled(self): # Map needs to be specified
        self.tmxdata = pytmx.load_pygame(self.mapDir, pixelalpha=True)
        self.width = self.tmxdata.width * self.tmxdata.tilewidth
        self.height = self.tmxdata.height * self.tmxdata.tileheight
        self.levelSize = (self.width, self.height)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.image = pygame.Surface(self.levelSize)

        tile = self.tmxdata.get_tile_image_by_gid
        for layer in self.tmxdata.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid, in layer:
                    tileImage = tile(gid)
                    if not tileImage is None:
                        tileImage
                        self.image.blit(tileImage, (x * self.tmxdata.tilewidth, y * self.tmxdata.tileheight))

        self.teleporters = pygame.sprite.Group()

        for tile_object in self.tmxdata.objects:
            if tile_object.name == 'key':
                self.key = key1(self.game, (tile_object.x, tile_object.y))
                self.objects.add(self.key)

            if tile_object.name == 'door':
                self.door = door(self.game, (tile_object.x, tile_object.y, tile_object.width, tile_object.height))
                self.objects.add(self.door)

            if tile_object.name == 'entrance':
                self.entrance = entrance(self.game, (tile_object.x, tile_object.y, tile_object.width, tile_object.height))
                self.objects.add(self.entrance)

            if tile_object.name == 'wall':
                if tile_object.type == 'platform':
                    self.platWalls.add(platWall(self.game, (int(tile_object.x), int(tile_object.y), int(tile_object.width), int(tile_object.height))))
                else:
                    collider(self.game, (int(tile_object.x), int(tile_object.y), int(tile_object.width), int(tile_object.height)))

            if tile_object.name == 'enemy':
                if tile_object.type == 'bit01':
                    try:
                        if tile_object.vertical:
                            bit01(self.game, (tile_object.x, tile_object.y), True)
                        else:
                            bit01(self.game, (tile_object.x, tile_object.y), False)
                    except:
                            bit01(self.game, (tile_object.x, tile_object.y), False)

                if tile_object.type == 'bit02':
                    bit02(self.game, (tile_object.x, tile_object.y))
                
                if tile_object.type == 'bossyBit':
                    bossyBit(self.game, (tile_object.x, tile_object.y))
                
                if tile_object.type == 'turret1':
                    try:
                        turret1(self.game, (tile_object.x, tile_object.y), tile_object.vertical)
                    except:
                        turret1(self.game, (tile_object.x, tile_object.y), False)
                
                if tile_object.type == 'megaTurret':
                    megaTurret(self.game, (tile_object.x, tile_object.y), False)

            if tile_object.name == 'consumable':
                if tile_object.type == 'massFireGun':
                    massFireGunConsumable(self.game, (tile_object.x, tile_object.y))
                if tile_object.type == 'tripleGun':  
                    tripleGunConsumable(self.game, (tile_object.x, tile_object.y))
                if tile_object.type == 'lazerGun':  
                    lazerGunConsumable(self.game, (tile_object.x, tile_object.y))
                elif tile_object.type == 'hpPack1':
                    hpPack1(self.game, (tile_object.x, tile_object.y))
                elif tile_object.type == 'coinBit':
                    bitCoin(self.game, (tile_object.x, tile_object.y))
            
            if tile_object.name == 'teleporter':
                if tile_object.type == 'tp1':
                    for obj in self.tmxdata.objects:
                        if obj.id == tile_object.target:
                            target = obj
                    tp = tp1(self.game, (tile_object.x, tile_object.y), target)
                    self.objects.add(tp)
                    self.teleporters.add(tp)
            
            if tile_object.name == 'text':
                text = fonts['3'].render(tile_object.text, self.game.antialiasing, (255, 255, 255))
                self.image.blit(text, (tile_object.x, tile_object.y))

            if tile_object.name == 'dmgRect':
                dmgRect(self.game, (tile_object.x, tile_object.y, tile_object.width, tile_object.height))
            
            if tile_object.name == 'mPlatform':
                try:
                    self.objects.add(mPlatform(self.game, (tile_object.x, tile_object.y, tile_object.width, tile_object.height), lID = tile_object.id, vertical = tile_object.vertical, pause=tile_object.pause, vel=tile_object.speed))
                except:
                    self.objects.add(mPlatform(self.game, (tile_object.x, tile_object.y, tile_object.width, tile_object.height)))

            if tile_object.name == 'trigger':
                if tile_object.type == 'initPlat':
                    self.triggers.add(trigger(self.game, (tile_object.x, tile_object.y, tile_object.width, tile_object.height), activatePlatform, (self.game, tile_object.target)))
            

## Handles loading a level from a Cyberspace website link
import requests
from zipfile import ZipFile

def importLevel(link):
    unZipPath = asset('custom/import')
    for file in os.listdir(unZipPath):
         os.remove(os.path.join(unZipPath, file))
    
    for file in os.listdir(asset('custom/')):
        try:
            os.remove(asset('custom/' + file))
        except:
            pass

    try:
        req = requests.get(link.split()[0], allow_redirects=True)
    except:
        try:
            req = requests.get("https://cyberspace-media.s3.amazonaws.com/maps/" + link.split()[0], allow_redirects=True)
        except:
            print("Not a link")
            return
    
    if not req.status_code == 403:
            
            # Gets the zip file from s3 and downloads it into the unzips folder with the title as the name
            zipPath = os.path.join(unZipPath, 'import.zip')
            open(zipPath, 'wb').write(req.content)

            with ZipFile(zipPath, 'r') as zipObj:
                zipObj.extractall(path=unZipPath)
            
            for file in os.listdir(unZipPath):
                if file.endswith(".tmx"):
                    tmxFile = os.path.join(unZipPath, file)
                else:
                    os.replace(os.path.join(unZipPath, file), asset('custom/' + file))
            
            return tmxFile

    else:
        print("map does not exist")
        return


def importLevelFile():
    import tkinter as tk
    from tkinter import filedialog
    import os

    root = tk.Tk()
    root.withdraw() #use to hide tkinter window

    currdir = os.getcwd()
    tempdir = filedialog.askopenfile(parent=root, initialdir=currdir, title='Please select a directory')

    return tempdir.name
#### Level creation
## Sample levl
# LEVEL1 = level(
#     levelSize = (winWidth, winHeight),
#     colliders = [
#         collider((200, 200, 150, 10)),
#         collider((0, winHeight-30, winWidth+1000, 30)),
#         collider((400, 400, 30, 300)),
#         collider((0, 0, 30, winHeight)),
#         collider((winWidth+1000, 0, 30, winHeight)),
#         collider((0, 0, winWidth, 30)),
#         ],
#     enemies = [
#         #enemy(asset('alien.png'))
#         ],
#     rendType = 0
# )

## Remember to include tileset image and tsx file with the tmx file of the map
level1 = level(
    rendType = 1,
    mapDir = asset('Tiled/level1/level1(2).tmx')
)
level2 = level(
    rendType = 1,
    mapDir = asset('Tiled/level2/level2.tmx')
)
level3 = level(
    rendType = 1,
    mapDir = asset('Tiled/level3/level3.tmx')
)
level4 = level(
    rendType = 1,
    mapDir = asset('Tiled/level4/level4.tmx')
)
level5 = level(
    rendType = 1,
    mapDir = asset('Tiled/level5/level5.tmx')
)
level6 = level(
    rendType = 1,
    mapDir = asset('Tiled/level6/level6.tmx')
)
### All Game levels
#gameLevels = [level6]
gameLevels = [level1, level2, level3, level4,level5, level6, ]