import pygame
from pygame.sprite import Sprite


class Terrain(Sprite):
    """Can be collided with to stop movement."""

    def __init__(self, settings, screen, image_name, position):
        super().__init__()
        self.scroll_rate = settings.scroll_rate
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.image = pygame.image.load(image_name).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = position

    def is_visible(self):
        """Has scrolled into view from the right."""
        return self.rect.x < self.screen_rect.width

    def update(self):
        self.rect.x += self.scroll_rate
        if self.out_of_bounds():
            self.kill()

    def draw(self):
        if self.is_visible():
            self.screen.blit(self.image, self.rect)

    def out_of_bounds(self):
        """Sprite is to left of screen."""
        return self.rect.right <= 0
