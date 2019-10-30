import pygame
from pygame.sprite import Sprite
from library.items.item import Item


class Mushroom(Item):
    def __init__(self, settings, surface, position):
        super().__init__(settings, surface, position, "resources/images/mushroom.png")
        self.item_type = 2
