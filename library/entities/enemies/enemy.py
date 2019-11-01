import pygame

from library.entities.entity import Entity
from library.timer import Timer


class Enemy(Entity):
    """Entities that can harm Mario."""

    def __init__(self, settings, screen, position, data, animation_speed=100):
        super().__init__(settings, screen, position, data, -1)
        self.scroll_rate = settings.scroll_rate
        self.walk_animation = self.load_walk_animation(animation_speed)
        super().init_image(self.walk_animation.get_image())
        self.gravity = settings.gravity * 0.1

    def load_walk_animation(self, wait):
        animation = []
        for x in range(self.data["frames"]["walking"]["sequence_sz"] - 1):
            animation.append(pygame.image.load(self.data["frames"]["walking"]["sequence"][x]).convert_alpha())
        return Timer(animation, wait)

    def set_image(self, image):
        """Enemy image asset is typically facing left. Changed logic of direction."""
        self.image = image if self.direction == -1 else pygame.transform.flip(image, True, False)
        
    def draw(self):
        if not self.hit:
            self.set_image(self.walk_animation.get_image())
        else:
            self.set_image(self.hit_image)
        super().draw()
