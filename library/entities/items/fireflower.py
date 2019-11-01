from library.entities.items.item import Item


class FireFlower(Item):

    def __init__(self, settings, surface, position):
        super().__init__(settings, surface, position, "resources/images/fire_flower.png")
        self.item_type = 3

    def update(self, level, scrolling, vel_x=None):
        """Pops out and remains still."""
        if scrolling:
            if vel_x:
                self.rect.x += vel_x
            else:
                self.rect.x += self.scroll_rate
        self.rect.y += self.velocity.y
        if self.rect.bottom >= self.position[1]:
            self.rect.bottom = self.position[1]
        self.fall()
