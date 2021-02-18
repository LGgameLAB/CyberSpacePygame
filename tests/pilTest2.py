import os
import pygame

# Importing Image class from PIL module 
from PIL import Image 

PATH = os.path.dirname(os.path.abspath(__file__))

mapDir = 'assets/Tiled/tileset1.png'
# Opens a image in RGB mode 
im = Image.open(mapDir) 

rect = pygame.Rect(0, 0, 32, 32)
# Setting the points for cropped image 
left = rect.x
top = rect.y
right = rect.x + rect.width
bottom = rect.y + rect.height
  
# Cropped image of above dimension 
# (It will not change orginal image) 
im1 = im.crop((left, top, right, bottom)) 
  
# Shows the image in image viewer 
im1.show() 