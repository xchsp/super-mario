import pygame


class Background:
    """Image in the background."""

    def __init__(self, settings, screen, image_name):
        # TODO: scroll rate to bg scroll rate
        self.scroll_rate = settings.bg_scroll_rate
        self.screen = screen
        self.image = None
        try:
            self.image = pygame.image.load(image_name).convert()
        except KeyError:
            pass
        # self.color = data["color"]
        self.x = 0

    def draw(self):
        # self.screen.fill(self.color)
        if self.image is not None:
            self.screen.blit(self.image, (self.x, 0))

    def update(self):
        self.x += self.scroll_rate
