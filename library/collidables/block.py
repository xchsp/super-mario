from library.collidables.terrain import Terrain


class Block(Terrain):
    """A single, small, solid, square object."""

    def __init__(self, settings, screen, image_name, position):
        super().__init__(settings, screen, image_name, position)

    def on_collision(self):
        pass
