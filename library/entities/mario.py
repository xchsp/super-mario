import pygame
from pygame.sprite import Group

from library.entities.entity import Entity
from library.timer import Timer
from library.entities.fireball import Fireball


class Mario(Entity):
    """The playable character, Mario."""

    def __init__(self, settings, screen, data):
        super().__init__(settings, screen, (100, 200), data, 1) # y, 525
        super().init_image(pygame.image.load("resources/images/mw2.png").convert_alpha())
        self.settings = settings
        self.still_image = self.image
        self.jump_image = pygame.image.load("resources/images/m_jump.png")
        self.throw_image = pygame.image.load("resources/images/m_throw.png")
        self.moving_left = self.moving_right = self.is_scrolling = False
        self.is_jumping = self.is_d_jumping = False
        self.walk_animation = self.load_walk_animation()
        self.jump_sound = pygame.mixer.Sound("resources/sounds/jump.wav")
        self.fireballs = Group()
        self.throw_time = 0

    def load_walk_animation(self):
        animation = []
        for x in range(self.data["frames"]["walking"]["sequence_sz"]):
            animation.append(pygame.image.load(self.data["frames"]["walking"]["sequence"][x]))
        return Timer(animation)

    def throw_fireball(self):
        fireball = Fireball(self.settings, self.screen, self.rect.center, self.direction)
        self.fireballs.add(fireball)
        self.throw_time = pygame.time.get_ticks()

    def jump(self):
        """Increases Mario's y-position. Must land before performing another jump."""
        if self.is_jumping:
            if not self.is_d_jumping:
                self.velocity.y = -15  # Weaker double jump
                self.is_d_jumping = True
                pygame.mixer.Channel(1).stop()
                pygame.mixer.Channel(1).play(self.jump_sound)
        else:
            self.velocity.y = -20  # Regular jump
            self.is_jumping = True
            pygame.mixer.Channel(1).stop()
            pygame.mixer.Channel(1).play(self.jump_sound)

    def reset_jump(self):
        """Allows Mario to perform jumps."""
        self.is_jumping = False
        self.is_d_jumping = False
        self.velocity.y = 0

    def handle_horizontal_collision(self, level):
        """Called after updating x-position."""
        collisions = pygame.sprite.spritecollide(self, level.terrain, False)
        for collision in collisions:
            if self.moving_right:
                self.is_scrolling = False
                self.rect.right = collision.rect.left
            elif self.moving_left:
                self.rect.left = collision.rect.right

    def handle_vertical_collision(self, level):
        """Called after updating y-position."""
        collisions = pygame.sprite.spritecollide(self, level.terrain, False)
        if collisions:
            for collision in collisions:
                # Mario is jumping
                if self.velocity.y < 0:
                    self.rect.top = collision.rect.bottom
                    self.velocity.y = 0
                    self.fall()
                    break
                # Mario is falling
                elif self.velocity.y > 0:
                    self.rect.bottom = collision.rect.top
                    self.reset_jump()
        # No vertical collisions, apply gravity
        else:
            self.fall()

    def update(self, level, scrolling=False):
        self.velocity.x = 20
        self.fireballs.update(level, self.is_scrolling)
        # Actually moves Mario horizontally, if on left side of screen. Otherwise, scroll screen to simulate movement
        if self.moving_right:
            self.direction = 1
            if self.rect.centerx + self.velocity.x <= self.screen_rect.centerx:
                self.rect.centerx += self.velocity.x
            else:
                self.is_scrolling = True
        elif self.moving_left:
            self.direction = -1
            if self.rect.x - self.velocity.x >= 0:
                self.rect.x -= self.velocity.x
            else:
                self.moving_left = False
                self.is_scrolling = False
        self.handle_horizontal_collision(level)
        # Jumping, moves Mario vertically
        self.rect.y += self.velocity.y
        self.handle_vertical_collision(level)

    def draw(self):
        # Fireballs
        for fireball in self.fireballs.sprites():
            fireball.draw()
        if pygame.time.get_ticks() - self.throw_time < 250:  # Duration of throw animation
            super().set_image(self.throw_image)
        else:
            # Moving
            if self.moving_right or self.moving_left:
                if self.is_jumping:
                    super().set_image(self.jump_image)
                else:
                    super().set_image(self.walk_animation.get_image())
            # Standing still
            else:
                if self.is_jumping:
                    super().set_image(self.jump_image)
                else:
                    super().set_image(self.still_image)
        # Parent draw() actually blits the image
        super().draw()
