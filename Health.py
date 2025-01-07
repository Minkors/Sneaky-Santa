import pygame

class heart (pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        self.image = pygame.image.load('Images\image (1) (1) (1).png').convert_alpha()
        self.rect = self.image.get_rect(topright = pos)
        