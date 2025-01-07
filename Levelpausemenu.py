import pygame
from baselevel import *
from music import *

class pausebackground (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('Images\Buttons\ButtonBack.png').convert_alpha()
        self.rect = self.image.get_rect(center = (screen_width/2,screen_height/2))

class resumebutton (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('Images\Buttons\Resume.png').convert_alpha()
        self.rect = self.image.get_rect(center = (screen_width*0.425,screen_height/2))

class returnselect (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('Images\Buttons\Home.png').convert_alpha()
        self.rect = self.image.get_rect(center = (screen_width*0.575,screen_height/2))

class countdown (pygame.sprite.Sprite):
    def __init__(self,time):
        super().__init__()
        if time > 160:
            self.image = pygame.image.load('Images\Countdown\\3.png').convert_alpha()
            if time == 220:
                short_beep.play()
        elif time > 100: 
            self.image = pygame.image.load('Images\Countdown\\2.png').convert_alpha()
            if time == 160:
                short_beep.play()
        elif time > 40:  
            self.image = pygame.image.load('Images\Countdown\\1.png').convert_alpha()
            if time == 100:
                short_beep.play()
        else:
            self.image = pygame.image.load('Images\Countdown\\Go.png').convert_alpha()
            if time == 40:
                long_beep.play()
        self.rect= self.image.get_rect(center = (screen_width/2,screen_height/2))
