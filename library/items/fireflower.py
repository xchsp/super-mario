import pygame
from pygame.sprite import Sprite
from library.items.item import Item


class FireFlower(Item):
    def __init__(self, settings, surface, position):
        super().__init__(settings, surface, position, "resources/images/fire_flower.png")
        self.item_type = 3
