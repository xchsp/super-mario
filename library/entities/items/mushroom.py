from library.entities.items.item import Item


class Mushroom(Item):

    def __init__(self, settings, surface, position):
        super().__init__(settings, surface, position, "resources/images/mushroom.png")
        self.item_type = 2

    def on_horizontal_collision(self):
        if self.is_active:
            self.direction *= -1
