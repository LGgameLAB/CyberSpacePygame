import os

classname = 'player'
vel = 5
content = f'''
import pygame

class {classname}:
    def __init__(self):
        self.vel = {vel}

p1 = {classname}()
print(p1.vel)

'''

PATH = os.path.dirname(os.path.abspath(__file__))
open('object1.py', 'w').write(content)