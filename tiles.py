import pygame 

class Tile(pygame.sprite.Sprite):
	def __init__(self,pos,size,num):
		super().__init__()
		self.image = pygame.Surface((size,size))
		if num == 1:
			self.image = pygame.image.load('Images\Tiles\Fill.png').convert_alpha()
		if num == 2:
			self.image = pygame.image.load('Images\Tiles\Top.png').convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)
	
	def update(self,shift):
		'''
		moves the background when needed
		'''
		self.rect.x += shift
