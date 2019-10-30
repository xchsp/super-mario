from library.collidables.terrain import Terrain
from library.items.mushroom import Mushroom
from library.items.fireflower import FireFlower
from library.items.coin import Coin

import pygame.image


class Block(Terrain):
    """A single, small, solid, square object.
    Item:
    0- Nothing
    1- Coin
    2- Mushroom
    """

    def __init__(self, settings, screen, image_name, position, level, re_entry,
                 has_item=0):
        super().__init__(settings, screen, image_name, position, re_entry)
        self.has_item = has_item
        self.level = level
        self.settings = settings
        self.screen = screen
        self.type = "block"

        # empty image
        self.empty_image = pygame.image.load("resources/images/block.png")

    def on_collision(self):
        pass

    def show_item(self, state):
        """creates item tells level to add it to terrain"""
        self.image = self.empty_image
        if self.has_item == 1:
            self.level.items.add(Coin(self.settings, self.screen,
                                 self.rect.topleft))
        elif state == "small":
            self.level.items.add(Mushroom(self.settings, self.screen,
                                 self.rect.topleft))
        elif state == "big":
            self.level.items.add(FireFlower(self.settings, self.screen,
                                 self.rect.topleft))
        self.has_item = 0