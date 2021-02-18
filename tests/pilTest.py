import pytmx
from PIL import Image
import os
import pytmxloader as pgl

PATH = os.path.dirname(os.path.abspath(__file__))

mapDir = 'assets/Tiled/level1/level1.tmx'


tmxdata = pytmx.TiledMap(os.path.join(PATH, mapDir), image_loader=pgl.pil_image_loader)
width = tmxdata.width * tmxdata.tilewidth
height = tmxdata.height * tmxdata.tileheight
levelSize = (width, height)
img = Image.new("RGB", levelSize, (0, 0, 0))
tileSize = 32

tile = tmxdata.get_tile_image_by_gid
for layer in tmxdata.visible_layers:
    if isinstance(layer, pytmx.TiledTileLayer):
        for x, y, gid, in layer:
            tileData = tile(gid)
            if not tileData is None:
                img.paste(tileData, (x * tmxdata.tilewidth, y * tmxdata.tileheight))

img.save("map.png")