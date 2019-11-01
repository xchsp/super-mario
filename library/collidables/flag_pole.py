from library.collidables.terrain import Terrain


class FlagPole(Terrain):
    """Does absolutely nothing."""

    def __init__(self, settings, screen, position, re_entry, level, mario):
        super().__init__(settings, screen, "resources/images/flag_pole.png", position, re_entry)
        self.level = level
        self.mario = mario
        self.is_flag_pole = True

    def scroll(self, vel_x=None):
        if not self.settings.level_over:
            if vel_x:
                self.scroll_rate = vel_x
            else:
                self.scroll_rate = self.settings.scroll_rate
            self.rect.x += self.scroll_rate

            if self.mario.rect.right >= self.rect.left:
                self.mario.prep_castle_walk()
                self.mario.rect.x = self.rect.x - 15
                self.mario.rect.y = max(self.mario.rect.y, self.rect.y)
