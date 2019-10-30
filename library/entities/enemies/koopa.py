from library.entities.enemies.enemy import Enemy


class Koopa(Enemy):
    """An upright turtle."""

    def __init__(self, settings, screen, position):
        super().__init__(settings, screen, position, "resources/koopa.json", 150)

    def on_horizontal_collision(self):
        """Face the opposite direction when hitting a wall."""
        self.direction *= -1
