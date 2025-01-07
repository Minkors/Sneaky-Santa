import pygame, sys
from baselevel import *
# from tiles import Tile
# from level import Level
from chooselevel import mainmenu
from how2play import instructioning
from music import *

class playbutton (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('Images\Buttons\start.png').convert_alpha()
        self.rect = self.image.get_rect(center = (screen_width/2 - 25,screen_height/5*3))
    
    def unhovered(self):
        self.image = pygame.image.load('Images\Buttons\start.png').convert_alpha()
    def hovered (self):
        self.image = pygame.image.load('Images\Buttons\start-hover.png').convert_alpha()


class exitbutton (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('Images\Buttons\end.png').convert_alpha()
        self.rect = self.image.get_rect(center = (screen_width/2 - 25,screen_height/5*4))

    def unhovered(self):
        self.image = pygame.image.load('Images\Buttons\end.png').convert_alpha()
    def hovered (self):
        self.image = pygame.image.load('Images\Buttons\end-hover.png').convert_alpha()

class infobutton (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('Images\Buttons\instructions.png').convert_alpha()
        self.rect = self.image.get_rect(center = (screen_width*0.95,screen_height* 0.9))

    def unhovered(self):
        self.image = pygame.image.load('Images\Buttons\instructions.png').convert_alpha()
    def hovered (self):
        self.image = pygame.image.load('Images\Buttons\instructions-hover.png').convert_alpha()


pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height))
clock = pygame.time.Clock()



m = mainmenu(screen)
i = instructioning(screen)
mode = "Instruction"

Homebackground = pygame.image.load('Images\menu.png').convert()
options = pygame.sprite.Group()
selectvalues = [0,0,0]
start = playbutton()
exit = exitbutton()
info = infobutton()
options.add(start)
options.add(exit)
options.add(info)

def setmode ():
    global mode
    if m.home == False:
        mode = "LevelSelect"
    elif i.home == False:
        mode = "Instruction"
    else:
        mode = "Home"


def checkselect ():
        mousestate = pygame.mouse.get_pressed()
        count = 0
        for sprite in options.sprites():
            if sprite.rect.collidepoint(pygame.mouse.get_pos()):
                sprite.hovered()
                if mousestate[0] == True:
                    selectvalues[count] = 1
            else:
                sprite.unhovered()
            count += 1
        if selectvalues[0] == 1:
            m.home = False
            selectvalues[0] = 0
            clickbeep.play()
        if selectvalues [1] == 1:
            clickbeep.play()
            pygame.quit()
            sys.exit()
        if selectvalues [2] == 1:
            i.home = False
            selectvalues[2] = 0
            clickbeep.play()


background = pygame.mixer.music.load('Music\Background.wav')
pygame.mixer.music.play(-1)
while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill('black')
    

    setmode()

    if mode == "Home":
        screen.blit(Homebackground,(0,0))
        checkselect()
        options.draw(screen)
    elif mode == "Instruction":
        screen.blit(Homebackground,(0,0))
        options.draw(screen)
        i.update()

    elif mode == "LevelSelect":
        m.update()

    pygame.display.update()
    clock.tick(60)
