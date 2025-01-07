import pygame
import os
from music import *
class Player (pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.image = pygame.Surface((63,63)) 
        self.image.fill('red')
        self.rect = self.image.get_rect(topleft = pos)
        self.direction = pygame.math.Vector2(0,0) #controls how much player will move
        self.speed = 4 #control how fast the movement is
        self.gravity = 1 #gravity rate
        self.jumpheight = -20 #how high player jumps
        self.facingleft = False
        self.grounded = True
        self.idle = True
        self.falling = False
        self.health = 3
        self.invincibility = 0
        self.giftsleft = 0
        self.animationspeed = 0.1
        self.animationframe = 0


    def updateimage (self):
        state = self.getstate()
        if self.invincibility == 0:
            folder = 'Images\Grinch\{s}'.format(s = state)
        else: 
            folder = 'Images\Grinch\Damaged\{s}'.format(s = state)
        imagestates = os.listdir(folder)
        if self.animationframe < len(imagestates) - 1:
            self.animationframe += self.animationspeed
        else: 
            self.animationframe = 0
        currentimage = '{foldery}\{image}'.format(foldery = folder,image = imagestates[int(self.animationframe)])
        self.image = pygame.image.load(currentimage).convert_alpha()
        if self.facingleft:
            self.image = pygame.transform.flip(self.image,True,False)

    def input_movement(self):
        '''
        Movement based on input
        '''
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facingleft = False
            self.idle = False

        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facingleft = True
            self.idle = False

        else:
            self.direction.x = 0
            self.idle = True
        
        if keys[pygame.K_SPACE] and self.grounded:
            self.jump()
            jump_sound.play()
            

    def gravityeffect (self):
        '''
        linear gravity effect
        '''
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
        if self.direction.y > 0:
            self.falling = False
        else: 
            self.falling = True

    def jump(self):
        '''
        jump
        '''
        self.direction.y = self.jumpheight
    
    def getstate(self):
        if self.grounded == True:
            if self.idle == False:
                return 'walk'
            elif self.idle == True:
                return 'idle'
        elif self.falling == False:
            return 'fall'
        elif self.falling == True:
            return 'jump'
    

    def update(self):
        self.updateimage()
        self.input_movement()
        

        