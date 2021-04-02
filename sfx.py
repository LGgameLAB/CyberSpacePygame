import pygame

pygame.mixer.init()
pygame.mixer.pre_init(44100, -16, 2, 2048)

class gameMixer:
    def __init__(self):
        self.volume = 1
        self.musicChannel = pygame.mixer.Channel(0)
    
    def setVolume(self, volume):
        if isinstance(volume, str):
            pass
        else:
            self.volume = volume/100

        pygame.mixer.music.set_volume(self.volume)

    def playFx(self, sfile, *args):
        sound = pygame.mixer.Sound(sfile)
        sound.play()

        if args:
            volume = args[0]/100

    def playMusic(self, sfile):
        sound = pygame.mixer.Sound(sfile)
        self.musicChannel.play(sound)

sfx = gameMixer()