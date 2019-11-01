import pygame
from pygame.sprite import Sprite

class Coin(Sprite):
    def __init__(self, screen):
        super(Coin, self).__init__()
        self.screen = screen
        self.image = pygame.image.load('resources/images/coin.png')
        self.rect = self.image.get_rect()
        self.rect.center = (100, 300)

    def draw(self):
        self.screen.blit(self.image, self.rect)
