# -------------------------------- #
# Creation date: 1/10/24
# Made by me :> 
# -------------------------------- #

#todo: better enemy logic
#todo: tidy up the code
import pygame
import sys

def display_score():
    # gives time in ms, which is what is desired
    counter = pygame.time.get_ticks() - start_time
    score_surface = text.render(f'Score: {counter}', False, 'yellow')
    score_rect = score_surface.get_rect(center = (400, 50))
    screen.blit(score_surface, score_rect)

    return counter

# rewriting the main game loop 
# date: 1/15/24
width = 800
height = 400
FPS = 60

pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Block Chase")
clock = pygame.time.Clock()
game_active = True 
# sets starting score to 0
start_time = 0
score = 0 

# convert_alpha() gets rid of borders around graphics and improves performance
text = pygame.font.Font('text\\slkscrb.ttf', 42)
sky_surface = pygame.image.load('graphics\\sky.png').convert_alpha()
sky_rect = sky_surface.get_rect(midright = (800, 150))
ground_surface = pygame.image.load('graphics\\ground.png').convert_alpha()
character = pygame.image.load('graphics\\character.png').convert_alpha()
character_rect = character.get_rect(midbottom = (100, 300))
# initializes gravity
character_gravity = 0
spike_surface = pygame.image.load('graphics\\spike.png').convert_alpha()
spike_rect = spike_surface.get_rect(midbottom = (600, 300))

game_name = text.render('You died!', False, 'black')
game_name_rect = game_name.get_rect(center = (400, 80))

game_msg = text.render('Press RETURN to play!', False, 'black')
game_msg_rect = game_msg.get_rect(center = (400, 300))

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
                    # replacing spike rect to get out of way,
                    # makes game restart smoother
                    spike_rect.left = 800
                    start_time = int(pygame.time.get_ticks() / 100)

    if game_active:
        # blit draws these graphics to the screen
        screen.blit(sky_surface, sky_rect)
        screen.blit(ground_surface, (0, 300))
        # screen.blit(text_surface, (300, 50))

        # creates gravity when jumping
        character_gravity += 1
        character_rect.y += character_gravity
        # simulates the floor
        if character_rect.bottom >= 300:
            character_rect.bottom = 300
        screen.blit(character, character_rect)

        spike_rect.x -= 5
        if spike_rect.right <= 0:
            spike_rect.left = 800
        screen.blit(spike_surface, (spike_rect))

        score = display_score()

        # collisions
        if spike_rect.colliderect(character_rect):
            game_active = False
    else:
        screen.fill('dark red')
        screen.blit(game_name, game_name_rect)
        screen.blit(game_msg, game_msg_rect)

        score_msg = text.render(f'Your score: {score}', False, 'black')
        score_msg_rect = score_msg.get_rect(center = (400, 140))
        screen.blit(score_msg, score_msg_rect)

    pygame.display.flip()
    clock.tick(FPS)
