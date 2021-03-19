import pygame

class enemy(pygame.sprite.Sprite):

    def __init__(self, game, image, pos):
        self.game = game
        pygame.sprite.Sprite.__init__(self)

        self.image = image
        self.pos = pos

    def move(self):
        print("moving" + str(self.pos[0]))
    
    def update(self):
        self.move()
        print(self.image)

class bitEnemy(enemy):

    def __init__(self, game, image, pos):
        super().__init__(game, image, pos)

    def move(self):
        print("nowmoving" + str(self.pos[0]))

bit1 = bitEnemy("GAMA", ":)", (99, 99))
print(isinstance(bit1, enemy))
