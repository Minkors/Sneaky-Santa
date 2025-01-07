import pygame
import os

class Adult(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.image = pygame.Surface((37,48))
        self.image.fill('white')
        self.rect = self.image.get_rect(topleft = pos)
        self.direction = pygame.math.Vector2(1,0) #controls how much player will move
        self.walking = False
        self.gravity = 1
        self.speed = 2
        self.facing = True #right = True left = False
        self.animationspeed = 0.1
        self.animationframe = 0

    def gravityeffect (self):
        '''
        linear gravity effect
        '''
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def updateimage (self):
        folder = 'Images\Enemy'
        imagestates = os.listdir(folder)
        if self.animationframe < len(imagestates) - 1:
            self.animationframe += self.animationspeed
        else:
            self.animationframe = 0
        currentimage = '{foldery}\{image}'.format(foldery = folder,image = imagestates[int(self.animationframe)])
        self.image = pygame.image.load(currentimage).convert_alpha()
        if not self.facing:
            self.image = pygame.transform.flip(self.image,True,False)

    def update (self,shift):
        self.rect.x += self.direction.x * self.speed
        self.rect.x += shift
        self.updateimage()
