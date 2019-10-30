from library.entities.enemies.enemy import Enemy


class Goomba(Enemy):
    """A strange mushroom."""

    def __init__(self, settings, screen, position):
        super().__init__(settings, screen, position, "resources/goomba.json")

    def on_horizontal_collision(self):
        """Face the opposite direction when hitting a wall."""
        self.direction *= -1
