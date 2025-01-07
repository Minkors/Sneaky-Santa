import pygame 

class Present(pygame.sprite.Sprite): 
  def __init__(self,pos):
    super().__init__()
    self.image = pygame.image.load('Images\present.png').convert_alpha()
    self.rect = self.image.get_rect(topleft = pos)
    self.collected = False

  def update (self,shift):
    self.rect.x += shift
  