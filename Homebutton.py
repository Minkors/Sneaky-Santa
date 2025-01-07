import pygame
from baselevel import *

class homebutton (pygame.sprite.Sprite):
    def __init__ (self):
        super().__init__()
        self.image = pygame.image.load('Images\Buttons\close-button.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = (screen_height*0.05,screen_height*0.05))

class instruction (pygame.sprite.Sprite):
    def __init__ (self,path):
        super().__init__()
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect(center = (screen_width/2,screen_height/2))