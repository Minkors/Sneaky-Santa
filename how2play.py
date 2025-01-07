import pygame
from Homebutton import  homebutton,instruction
from music import *
from baselevel import *
class instructioning:
    def __init__(self,display_surface):
        self.home = True
        self.display_surface = display_surface
        self.gohome = homebutton()
        self.gohomegroup = pygame.sprite.GroupSingle()
        self.gohomegroup.add(self.gohome)


        self.back = instruction('Images\icons.png')
        self.blur = instruction('Images\colour.png')
        self.backgroup = pygame.sprite.Group()
        self.backgroup.add(self.blur)
        self.backgroup.add(self.back)


    def checkhome (self):
        mousestate = pygame.mouse.get_pressed()
        if mousestate[0] and self.gohomegroup.sprite.rect.collidepoint(pygame.mouse.get_pos()):
            self.home = True
            clickbeep.play()
    
    def update (self):
        self.backgroup.draw(self.display_surface)
        self.gohomegroup.draw(self.display_surface)
        self.checkhome()