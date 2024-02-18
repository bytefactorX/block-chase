# -------------------------------- #
# Creation date: 1/10/24
# Made by me :> 
# -------------------------------- #

# todo: score does not return back to 0 upon restarting
# todo: enemy logic is fucked
import pygame
import sys
from random import randint

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        super().__init__
        self.image = pygame.image.load('block chase\\graphics\\character.png').convert_alpha()
        self.rect = self.image.get_rect(midbottom = (100, 300))
        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -15

    def apply_grav(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def update(self):
        self.player_input()
        self.apply_grav()

class Spike(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        super().__init__
        self.image = pygame.image.load('block chase\\graphics\\spike.png').convert_alpha()
        self.rect = spike_surface.get_rect(midbottom = (randint(900, 1100), 300))

    def update(self):
        self.rect.x -= 10
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def display_score():
    # gives time in ms, which is what is desired
    counter = pygame.time.get_ticks() - start_time
    score_surface = text.render(f'Score: {counter}', False, 'yellow')
    score_rect = score_surface.get_rect(center = (400, 50))
    screen.blit(score_surface, score_rect)

    return counter

def spike_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 10

            screen.blit(spike_surface, obstacle_rect)

        # only copies items of list if obstacle is on screen
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]

        return obstacle_list
    else:
        return []

def collisions(character, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if character.colliderect(obstacle_rect):
                return False
    return True

def sprite_collisions():
    if pygame.sprite.spritecollide(player.sprite, spike, False):
        spike.empty()
        return False
    else:
        return True

width = 800
height = 400
FPS = 60

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Block Chase")
clock = pygame.time.Clock()
game_active = True 
start_time = 0
score = 0 

player = pygame.sprite.GroupSingle()
player.add(Player())
spike = pygame.sprite.Group()

# convert_alpha() gets rid of borders around graphics and improves performance
text = pygame.font.Font('block chase\\text\\slkscrb.ttf', 42)
sky_surface = pygame.image.load('block chase\\graphics\\sky.png').convert_alpha()
sky_rect = sky_surface.get_rect(midright = (800, 150))
ground_surface = pygame.image.load('block chase\\graphics\\ground.png').convert_alpha()
character = pygame.image.load('block chase\\graphics\\character.png').convert_alpha()
character_rect = character.get_rect(midbottom = (100, 300))

# enemies
spike_surface = pygame.image.load('block chase\\graphics\\spike.png').convert_alpha()
spike_rect = spike_surface.get_rect(midbottom = (600, 300))

# game over screen
game_name = text.render('You died!', False, 'black')
game_name_rect = game_name.get_rect(center = (400, 80))

game_msg = text.render('Press RETURN to play!', False, 'black')
game_msg_rect = game_msg.get_rect(center = (400, 300))

#timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1200)

obstacle_list = []

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # lot of nesting going on
        if game_active:
            if event.type == pygame.KEYDOWN:
                # disables a character from jumping infinitely
                if event.key == pygame.K_SPACE and character_rect.bottom >= 300:
                    character_gravity = -15
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_active = True
                    start_time = int(pygame.time.get_ticks() / 100)

    if game_active:
        # blit draws these graphics to the screen
        screen.blit(sky_surface, sky_rect)
        screen.blit(ground_surface, (0, 300))

        player.draw(screen)
        player.update()
        spike.draw(screen)
        spike.update()

        score = display_score()

        if event.type == obstacle_timer and game_active:
            # randomly spawns spike on x-axis based off of timer
            max_spikes = 4
            if len(spike) < max_spikes:
                spike.add(Spike())

            game_active = sprite_collisions()

    else:
        screen.fill('dark red')
        screen.blit(game_name, game_name_rect)
        screen.blit(game_msg, game_msg_rect)

        # clearing list upon collision
        obstacle_list.clear()

        character_gravity = 0

        score_msg = text.render(f'Your score: {score}', False, 'black')
        score_msg_rect = score_msg.get_rect(center = (400, 140))
        screen.blit(score_msg, score_msg_rect)

    pygame.display.flip()
    clock.tick(FPS)
