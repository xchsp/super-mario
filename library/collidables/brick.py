from library.collidables.block import Block


class Brick(Block):
    """Bounces when hit by player."""

    def __init__(self, settings, screen, position):
        super(Brick, self).__init__(settings, screen, "resources/images/brick.png", position)

