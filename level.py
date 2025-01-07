import pygame
from tiles import Tile
from baselevel import tile_size , screen_width, screen_height
from santa import Player
from enemy import Adult
from Health import heart
from presents import Present
from Levelpausemenu import *
from music import *

class Level:
    def __init__(self,level_data,surface):
        self.display_surface = surface
        self.setup_level(level_data)
        self.gamecomplete = False
        self.movesurronding = 0 #Surrondings will move at this pace if user tries to move past a certain part of the screen
        self.wonorlost = False #lose = False, Win = True
        self.backgrounds = pygame.image.load('Images\Background.png').convert_alpha()
        self.darken = pygame.image.load('Images\Darken.png').convert_alpha()

        self.paused = False

        self.pausemenu = pygame.sprite.Group()
        self.pauseback = pausebackground()
        self.resume = resumebutton()
        self.goback = returnselect() 
        self.pausemenu.add(self.pauseback)
        self.pausemenu.add(self.resume)
        self.pausemenu.add(self.goback)

        self.pausevalues = [0,0,0]

        self.countdowntimer = 220

    def setup_level(self,layout):
        '''
        Loops through the level map and places tiles based on whats in it
        '''
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.enemys = pygame.sprite.Group()
        self.gifts = pygame.sprite.Group()


        for row_index,row in enumerate(layout):
            for col_index,col in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if col == 'X':
                    tile = Tile((x,y),tile_size,1)
                    self.tiles.add(tile)
                if col == 'T':
                    tile = Tile((x,y),tile_size,2)
                    self.tiles.add(tile)
                if col == 'P':
                    player_sprite = Player((x,y))
                    self.player.add(player_sprite)
                if col == 'E':
                    player_sprite = Adult((x,y))
                    self.enemys.add(player_sprite)
        for row_index,row in enumerate(layout):
            for col_index,col in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if col == 'G':
                    gift_sprite = Present((x,y))
                    self.gifts.add(gift_sprite)
                    self.player.sprite.giftsleft += 1

    def scroll(self):
        '''
        scroll the background instead of character if needed
        '''
        player_sprite = self.player.sprite
        player_x = player_sprite.rect.centerx
        direction_x = player_sprite.direction.x

        if player_x < screen_width * 0.2 and direction_x < 0:
            self.movesurronding = 4
            player_sprite.speed = 0
        elif player_x > screen_width - screen_width * 0.2 and direction_x > 0:
            self.movesurronding = -4
            player_sprite.speed = 0
        else:
            self.movesurronding = 0
            player_sprite.speed = 4


    def left_right_collision(self):
        '''
        if player walking into block, no
        '''
        player_sprite = self.player.sprite
        player_sprite.rect.x += player_sprite.direction.x * player_sprite.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player_sprite.rect):
                if player_sprite.direction.x > 0:
                    player_sprite.rect.right = sprite.rect.left
                elif player_sprite.direction.x < 0:
                    player_sprite.rect.left = sprite.rect.right

    def up_down_collision(self):
        '''
        if player jumping or falling to block, no
        '''
        player_sprite = self.player.sprite
        player_sprite.gravityeffect()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player_sprite.rect):
                if player_sprite.direction.y > 0:
                    player_sprite.rect.bottom = sprite.rect.top
                    player_sprite.direction.y = 0
                    player_sprite.grounded = True
                elif player_sprite.direction.y < 0:
                    player_sprite.rect.top = sprite.rect.bottom
                    player_sprite.direction.y = 0

        if player_sprite.grounded and player_sprite.direction.y < 0 or player_sprite.direction.y > 1:
            player_sprite.grounded = False
    
    def countdowntracker (self):
        self.countdownimage = countdown(self.countdowntimer)
        self.countdowngroup = pygame.sprite.GroupSingle()
        self.countdowngroup.add(self.countdownimage)

    def enemy_left_right_movement(self):

        for enemy in self.enemys.sprites():
            enemy.gravityeffect()

        for enemy in self.enemys.sprites():
            enemy.walking = False
            for sprite in self.tiles.sprites():
                if enemy.facing:
                    if sprite.rect.collidepoint(enemy.rect.bottomright):
                        enemy.walking = True
                        enemy.rect.bottom = sprite.rect.top
                        enemy.direction.y = 0
                    if sprite.rect.collidepoint(enemy.rect.midright):
                        enemy.walking = False
                        enemy.rect.right = sprite.rect.left
                        enemy.direction.x = enemy.direction.x * -1
                        enemy.facing = not enemy.facing
                else:
                    if sprite.rect.collidepoint(enemy.rect.bottomleft) :
                        enemy.walking = True
                        enemy.rect.bottom = sprite.rect.top
                        enemy.direction.y = 0
                    if sprite.rect.collidepoint(enemy.rect.midleft):
                        enemy.walking = False
                        enemy.rect.left = sprite.rect.right
                        enemy.direction.x = enemy.direction.x * -1
                        enemy.facing = not enemy.facing


            if not enemy.walking:
                enemy.direction.x = enemy.direction.x * -1
                enemy.facing = not enemy.facing


    def enemydamage(self):

        for enemy in self.enemys.sprites():
            if enemy.rect.colliderect(self.player.sprite.rect):
                if self.player.sprite.invincibility == 0:
                    self.player.sprite.invincibility = 60
                    self.player.sprite.health -= 1
                    damage_sound.play()



    def invincibilitytimer (self):
        if self.player.sprite.invincibility != 0:
            self.player.sprite.invincibility -= 1


    def showhp (self):
        self.healthcurrent = pygame.sprite.Group()
        if self.player.sprite.health > 0:
            for number in range (self.player.sprite.health):
                y = screen_height * 0.05
                x = screen_width * 0.08 + 64 * (number)
                oneheart = heart((x,y))
                self.healthcurrent.add(oneheart)

    def giftcollision (self):
        for need in self.gifts.sprites():
            if need.rect.colliderect(self.player.sprite.rect):
                need.collected = True
                self.player.sprite.giftsleft -= 1
                collect_sound.play()

    def destroygift (self):
        for need in self.gifts.sprites():
            if need.collected:
                need.kill()

    def showgiftsleft(self):
        font = pygame.font.Font('freesansbold.ttf', 48)
        text = font.render(str(self.player.sprite.giftsleft), True, 'white', None)
        showgiftsleftbackground = pygame.image.load('Images\presentbig.png').convert_alpha()
        textrect = text.get_rect()
        textrect.midright = (screen_width-screen_width*0.1,screen_height*0.15 - 10)
        showrect = showgiftsleftbackground.get_rect()
        showrect.midtop = (screen_width-screen_width*0.1,screen_height*0.05)
        self.display_surface.blit(showgiftsleftbackground,showrect)
        self.display_surface.blit(text,textrect)

    def checkcompletion(self):
        if self.player.sprite.health <= 0 or self.player.sprite.rect.y > 720:
            self.gamecomplete = True
            self.wonorlost = False
        elif self.player.sprite.giftsleft == 0:
            self.gamecomplete = True
            self.wonorlost = True
    
    def checkpause (self):
        key = pygame.key.get_pressed()
        if key[pygame.K_ESCAPE]:
            self.paused = True
    
    def checkselect (self):
        mousestate = pygame.mouse.get_pressed()
        count = 0
        for sprite in self.pausemenu.sprites():
            if sprite.rect.collidepoint(pygame.mouse.get_pos()) and mousestate[0] == True:
                self.pausevalues[count] = 1
            count += 1
        
        if self.pausevalues[1] == 1:
            self.paused = False
            self.countdowntimer = 220
            self.pausevalues[1] = 0
            self.wonorlost = False
        if self.pausevalues [2] == 1:
            self.gamecomplete = True
            

    def run (self):

        if self.countdowntimer > 0:
            self.countdowntracker()
            self.countdowntimer -= 1
            self.display_surface.blit(self.backgrounds,(0,0))
            self.tiles.draw(self.display_surface)
            

            self.enemys.draw(self.display_surface)

            self.gifts.draw(self.display_surface)
            self.showgiftsleft()

            self.player.update()
            self.up_down_collision()
            self.player.draw(self.display_surface)


            self.showhp()
            self.healthcurrent.draw(self.display_surface)
            self.checkcompletion()
            self.display_surface.blit(self.darken,(0,0))
            self.countdowngroup.draw(self.display_surface)

        elif self.paused:
            pygame.mouse.set_visible(True)
            self.display_surface.blit(self.backgrounds,(0,0))
            self.tiles.draw(self.display_surface)
            

            self.enemys.draw(self.display_surface)

            self.gifts.draw(self.display_surface)
            self.showgiftsleft()

            self.player.update()
            self.up_down_collision()
            self.player.draw(self.display_surface)


            self.showhp()
            self.healthcurrent.draw(self.display_surface)
            self.checkcompletion()
            self.display_surface.blit(self.darken,(0,0))

            self.pausemenu.draw(self.display_surface)
            self.checkselect()

        else:
            pygame.mouse.set_visible(False)
            self.display_surface.blit(self.backgrounds,(0,0))
            self.tiles.update(self.movesurronding)
            self.tiles.draw(self.display_surface)
            self.scroll()

            self.enemydamage()
            self.invincibilitytimer()
            self.enemy_left_right_movement()
            self.enemys.update(self.movesurronding)
            self.enemys.draw(self.display_surface)

            self.giftcollision()
            self.destroygift()
            self.gifts.update(self.movesurronding)
            self.gifts.draw(self.display_surface)
            self.showgiftsleft()

            self.player.update()
            self.left_right_collision()
            self.up_down_collision()
            self.player.draw(self.display_surface)


            self.showhp()
            self.healthcurrent.draw(self.display_surface)
            self.checkcompletion()

            self.checkpause()
      

