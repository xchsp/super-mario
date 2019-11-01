import pygame

from library.entities.items.item import Item
from library.timer import Timer


class Coin(Item):

    def __init__(self, settings, surface, position, underground=False):
        super().__init__(settings, surface, position, "resources/images/coin.png")
        self.item_type = 1
        self.y_limit = 30
        self.underground = underground
        self.spin_animation = Timer([pygame.image.load("resources/images/coin.png"),
                                     pygame.image.load("resources/images/coin_2.png")])

    def update(self, level, scrolling, vel_x=None):
        """Pops out and remains still."""
        if scrolling:
            if vel_x:
                self.rect.x += vel_x
            else:
                self.rect.x += self.scroll_rate
        if not self.underground:
            self.rect.y += self.velocity.y
            if self.rect.bottom >= self.position[1]:
                self.rect.bottom = self.position[1]
            self.fall()

    def draw(self):
        super().set_image(self.spin_animation.get_image())
        if not self.underground:
            self.y_limit -= 2
            if self.y_limit < 0:
                self.kill()
            else:
                self.rect.y -= 4
        super().draw()
