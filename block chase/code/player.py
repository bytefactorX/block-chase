# initializes player 
# this file is currently unused - 1/18/24
import pygame
from main import *

class Player():
    def __init__(self, image, x, y):
        self.image = pygame.image.load(image)
        self.x = x
        self.y = y

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

