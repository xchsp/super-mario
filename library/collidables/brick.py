from library.collidables.block import Block
from library.items.coin import Coin


class Brick(Block):
    """Bounces when hit by player."""

    def __init__(self, settings, screen, position, level, re_entry, has_item):
        super(Brick, self).__init__(settings, screen,
                                    "resources/images/brick.png", position,
                                    level, re_entry, has_item)
        self.type = "brick"

    def show_item(self, state):
        if self.has_item == 1:
            self.level.items.add(Coin(self.settings, self.screen,
                                 self.rect.topleft))
            self.has_item = 0
            self.image = self.empty_image
            self.type = "block"
        elif state is not "small":
            self.kill()