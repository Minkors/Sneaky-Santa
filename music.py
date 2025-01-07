import pygame

pygame.init()
background = pygame.mixer.Sound('Music\Background.wav')
damage_sound = pygame.mixer.Sound('Music\Damaged.wav')
short_beep = pygame.mixer.Sound('Music\Shortbeep.wav')
long_beep = pygame.mixer.Sound('Music\Longbeep.wav')
clickbeep = pygame.mixer.Sound('Music\Beepboop.wav')
collect_sound = pygame.mixer.Sound('Music\Collect.wav')
jump_sound = pygame.mixer.Sound('Music\Jump.wav')
damage_sound.set_volume(0.5)
jump_sound.set_volume(0.5)
