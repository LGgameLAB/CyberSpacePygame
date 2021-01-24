import pygame
import pytmx
from stgs import *
from enemy import *
from objects import *

class level:
    rendType = 0
    colliders = []
    enemies = []
    width = winWidth
    height = winHeight
    levelSize = (width, height)
    rect = pygame.Rect(0, 0, width, height)
    mapDir = ''

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.__dict__[k] = v


    def load(self):
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
        self.tmxdata = pytmx.load_pygame(asset(self.mapDir), pixelalpha=True)
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

        for tile_object in self.tmxdata.objects:
            if tile_object.name == 'player':
                self.pStartX, self.pStartY = int(tile_object.x), int(tile_object.y)

            if tile_object.name == 'wall':
                self.colliders.append(collider((int(tile_object.x), int(tile_object.y), int(tile_object.width), int(tile_object.height))))

            if tile_object.name == 'goblin':
                pass

#### Level creation
## Sample levl
LEVEL1 = level(
    levelSize = (winWidth, winHeight),
    colliders = [
        collider((200, 200, 150, 10)),
        collider((0, winHeight-30, winWidth+1000, 30)),
        collider((400, 400, 30, 300)),
        collider((0, 0, 30, winHeight)),
        collider((winWidth+1000, 0, 30, winHeight)),
        collider((0, 0, winWidth, 30)),
        ],
    enemies = [
        #enemy(asset('alien.png'))
        ],
    rendType = 0
)

## Remember to include tileset image and tsx file with the tmx file of the map
level1 = level(
    rendType = 1,
    mapDir = 'Tiled/level1/level1.tmx'
)
    

### All Game levels
gameLevels = [level1]