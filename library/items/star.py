from library.items.item import Item


class Star(Item):

    def __init__(self, settings, surface, position):
        super().__init__(settings, surface, position, "resources/images/star.png")
        self.item_type = 4
