import pygame
from baselevel import *
from level import Level
from Homebutton import homebutton
from music import *
class levelbutton (pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.image = pygame.Surface((32,32)) 
        self.position = pos
        self.rect = self.image.get_rect(topleft = self.position)

    def gettingimage (self,num):
        path = 'Images\incomplete level\{nummy}complete.png'.format(nummy = num)
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect(topleft = self.position)

    def gettingfail(self,num):
        path = 'Images\complete level\{nummy}complete.png'.format(nummy = num)
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect(topleft = self.position)
        
class displayonwin (pygame.sprite.Sprite):
    def __init__ (self,pos):
        super().__init__()
        self.image = pygame.image.load('Images\you won.png').convert()
        self.rect = self.image.get_rect(center = pos)

class displayonlose (pygame.sprite.Sprite):
    def __init__ (self,pos):
        super().__init__()
        self.image = pygame.image.load('Images\you lose bg.png').convert()
        self.rect = self.image.get_rect(center = pos)
        
class mainmenu:
    def __init__(self,display_surface):
        self.levellist = [level_map,level_map2,level_map3,level_map4]
        self.levelcompletionarray = [0] * len(self.levellist)
        self.levelchose = 0
        self.gamestate = False
        self.display_surface = display_surface
        self.level = Level(self.levellist[0],self.display_surface)
        self.timed = 0
        self.buffer = 30


        self.losescreen = displayonlose((screen_width/2,screen_height/2))
        self.winscreen = displayonwin((screen_width/2,screen_height/2))
        self.losegroup = pygame.sprite.GroupSingle()
        self.losegroup.add(self.losescreen)
        self.wingroup = pygame.sprite.GroupSingle()
        self.wingroup.add(self.winscreen)


        self.chooseback = pygame.image.load('Images\chooselevel.png').convert()
        self.home = True
        self.gohome = homebutton()
        self.gohomegroup = pygame.sprite.GroupSingle()
        self.gohomegroup.add(self.gohome)
        self.buttonsoundcooldown = 0

    def menu (self):
        x = len(self.levellist)
        self.loadlevels = pygame.sprite.Group()
        for i in range (x):
            x = 160 + i * 230
            y = 380
            self.leveladd = levelbutton((x,y))       
            self.loadlevels.add(self.leveladd)


    def mousecheck (self):
        levelcount = 0
        if self.gamestate == False:
            pygame.mouse.set_visible(True)
        for box in self.loadlevels.sprites():  
            levelcount += 1
            mousestate = pygame.mouse.get_pressed()
            if box.rect.collidepoint(pygame.mouse.get_pos()) and mousestate[0] == True:
                self.gamestate = True
                self.levelchose = levelcount
                levelcount = 0

    
    def enterlevel (self):
        if self.gamestate:
            self.level = Level(self.levellist[self.levelchose-1],self.display_surface)
            pygame.mouse.set_visible(False)
            self.gamestate = True     

    def checkcompletion (self):
        counting = 0
        for sprite in self.loadlevels.sprites():
            sprite.gettingimage(counting+1)
            if 1 == self.levelcompletionarray[counting]:
                sprite.gettingfail(counting+1)
            counting += 1
    
    def checkhome (self):
        mousestate = pygame.mouse.get_pressed()
        if mousestate[0] and self.gohomegroup.sprite.rect.collidepoint(pygame.mouse.get_pos()):
            clickbeep.play()
            self.home = True
            self.buffer = 30
    
    def update(self):
        if self.buttonsoundcooldown >0:
            self.buttonsoundcooldown -=1
        else:
            self.buttonsoundcooldown = 8
        if self.gamestate == False:
            self.display_surface.blit(self.chooseback,(0,0))
            self.timed = 0 
            self.menu()
            self.checkcompletion()
            self.loadlevels.draw(self.display_surface)
            if not self.buffer > 0:
                self.mousecheck()
                self.enterlevel()
            else:
                self.buffer -= 1
            self.gohomegroup.draw(self.display_surface)
            self.checkhome()
        else:
            if not self.level.gamecomplete:
                self.level.run()
            if self.level.gamecomplete:
                self.buffer = 30
                self.display_surface.fill('white')
                if self.level.wonorlost and self.timed < 180:
                    self.wingroup.draw(self.display_surface)
                    self.timed += 1
                    self.levelcompletionarray [self.levelchose - 1] = 1
                elif not self.level.wonorlost and self.timed < 180:
                    self.losegroup.draw(self.display_surface)
                    self.timed += 1
                else:
                    self.gamestate = False


    
    