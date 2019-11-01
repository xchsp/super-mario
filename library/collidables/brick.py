import pygame

from library.collidables.block import Block
from library.entities.items.coin import Coin
from library.entities.items.star import Star


class Brick(Block):
    """Bounces when hit by player."""

    def __init__(self, settings, screen, position, image_name, level, re_entry, has_item):
        super(Brick, self).__init__(settings, screen, position, image_name, level, re_entry, has_item)
        self.type = "brick"
        self.coins = 5

    def show_item(self, mario):
        if self.has_item == 1 or self.has_item == 5:
            mario.player_score.coin_hit(mario)
            self.level.items.add(Coin(self.settings, self.screen,
                                 self.rect.topleft))
            pygame.mixer.Channel(1).stop()
            pygame.mixer.Channel(1).play(self.coin_sound)
            if self.has_item == 5:
                self.coins -= 1
            if self.coins == 0 or self.has_item == 1:
                self.has_item = 0
                self.image = self.empty_image
                self.type = "block"
        elif self.has_item == 4:
            self.has_item = 0
            self.type = "block"
            self.level.items.add(Star(self.settings, self.screen, self.rect.topleft))
        elif self.has_item == 5:
            self.coins -= 1
            if self.coins == 0:
                self.has_item = 0
                self.image = self.empty_image
                self.type = "block"
        elif mario.state is not "small":
            self.kill()
