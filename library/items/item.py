import pygame
from pygame.sprite import Sprite


class Item(Sprite):
    """"Class that handles items"""
    def __init__(self, settings, surface, position, image):
        super(Item, self).__init__()
        self.is_active = True
        self.surface = surface
        self.scroll_rate = settings.scroll_rate
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()

        self.rect.topleft = position
        self.rect.y -= 50

    def draw(self):
        if self.is_active:
            self.surface.blit(self.image, self.rect)

    def scroll(self):
        self.rect.x += self.scroll_rate