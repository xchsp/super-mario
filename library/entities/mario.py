import pygame
from pygame.sprite import Group

from library.entities.entity import Entity
from library.timer import Timer
from library.entities.fireball import Fireball


class Mario(Entity):
    """The playable character, Mario."""

    def __init__(self, settings, screen, data):

        super().__init__(settings, screen, (100, 545), data, 1)
        self.settings = settings
        self.state = "small"
        super().init_image(pygame.image.load(self.data[self.state]["walking"]
                           ["sequence"][3]).convert_alpha())
        self.load_state()
        self.throw_image = pygame.image.load("resources/images/m_throw.png")
        self.moving_left = self.moving_right = self.is_scrolling = False
        self.is_jumping = self.is_d_jumping = False
        self.direction = True  # true is facing right
        self.jump_sound = pygame.mixer.Sound("resources/sounds/jump.wav")
        self.fireballs = Group()
        self.throw_time = 0
        # states
        self.invincible = False
        self.pipe_enterence = False
        self.pipe_exit = False
        self.underground = False
        self.fire_bullets = Group()

    def load_state(self):
        # load images
        super().init_mario_image(pygame.image.load(self.data[self.state]
                                 ["walking"]["sequence"][3]).convert_alpha())
        self.load_single_images()
        self.walk_animation = Timer(self.load_walk_animation())
        self.still_image = self.image
        self.still_image_right = self.image
        self.still_image_left = pygame.transform.flip(self.still_image_right, True, False)
        # Crouching
        self.crouch_image = pygame.image.load(self.data[self.state]
                                              ["crouch"]).convert_alpha()
        self.crouch_image_right = self.crouch_image
        self.crouch_image_left = pygame.transform.flip(self.crouch_image, True,
                                                       False)

    def load_single_images(self):
        self.jump_image = pygame.image.load(self.data[self.state]["jump"])
        self.hit_image = pygame.image.load(self.data[self.state]["hit"])
        self.crouch_image = pygame.image.load(self.data[self.state]["crouch"])

    def load_walk_animation(self):
        animation = []
        for x in range(self.data[self.state]["walking"]["sequence_sz"]):
            animation.append(pygame.image.load(self.data[self.state]["walking"]
                             ["sequence"][x]))
        return animation

    def jump(self):
        """Increases Mario's y. Must land before performing another jump."""


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
        # check for pipe if underground
        if self.underground:
            if pygame.sprite.collide_rect(self, level.exit_pipe):
                self.check_pipe_exit(level)

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
                    # check for block collisions
                    try:
                        if collision.has_item != 0:
                            collision.show_item(self.state)
                        elif collision.has_item is 0 and self.state is not \
                                "small" and collision.type is "brick":
                            collision.kill()
                        break
                    except AttributeError:
                        pass
                # Mario is falling
                elif self.velocity.y > 0:
                    # check if pipe is an enterence
                    try:
                        if collision.enter:
                            self.pipe_enterence = True
                    except AttributeError:
                        self.pipe_enterence = False
                    self.rect.bottom = collision.rect.top
                    self.reset_jump()
                # ADD KILL ZONE IF HE FALLS IN A HOLE

        # No vertical collisions, apply gravity
        else:
            self.fall()

    def update_fire_bullets(self, level):
        for bullet in self.fire_bullets:
            collisions = pygame.sprite.spritecollide(bullet, level.enemies,
                                                     False)
            for collision in collisions:
                if self.rect.bottom <= collision.rect.centery:
                    collision.hit_sequence()
                # mario.fire_bullets.remove(bullet)
            # else:
            # bullet.movement(level)
            bullet.update(level, self.is_scrolling)

    def check_pipe(self, level):
        """checks if it is an undergorudn pipe"""
        if self.pipe_enterence:
            level.create_underground()
            self.underground = True
            self.pipe_enterence = False
            # reposition
            self.position = (100, 0)
            super().init_image(pygame.image.load(self.data[self.state]
                               ["walking"]["sequence"][3]).convert_alpha())

    def check_pipe_exit(self, level):
        """checks if it is an undergorudn pipe"""
        if pygame.sprite.collide_rect(self, level.exit_pipe):
            self.underground = False
            self.pipe_exit = False
            # reposition
            self.position = (100, level.go_surface() - 100)
            super().init_image(pygame.image.load(self.data[self.state]
                               ["walking"]["sequence"][3]).convert_alpha())

    def update(self, level):
        # Actually moves Mario horizontally, if on left side of screen./
        # Otherwise, scroll screen to simulate movement
        self.fireballs.update(level, self.is_scrolling)

        if self.hit:
            pass
        else:
            if self.underground:
                if self.moving_right:
                    self.rect.centerx -= self.velocity.x
                elif self.moving_left:
                    self.rect.x += self.velocity.x
            elif self.moving_right:
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
            # Check enemy collisions
            self.check_enemy_collisions(level)
            # check item collisions
            self.check_item_collisions(level)

    def check_enemy_collisions(self, level):
        """Detect if jumped on enemy"""
        collisions = pygame.sprite.spritecollide(self, level.enemies, False)
        for collision in collisions:
            if self.rect.bottom <= collision.rect.centery:
                collision.hit_sequence()
                self.rect.bottom = collision.rect.top
                self.reset_jump()
            else:
                if not collision.hit and not self.invincible:
                    self.hit_sequence()
                    self.go_down_state()

    def check_item_collisions(self, level):
        """Detect if jumped on enemy"""
        collisions = pygame.sprite.spritecollide(self, level.items, True)
        for collision in collisions:
            if collision.item_type == 2:
                self.get_bigger()
            if collision.item_type == 3:
                self.get_fire()

    def get_bigger(self):
        self.state = "big"
        # PLAY ANIMATION HERE
        self.load_state()

    def get_fire(self):
        self.state = "fire"
        # PLAY ANIMATION HERE
        self.load_state()

    def go_down_state(self):
        if self.state == "big":
            self.state = "small"
        if self.state == "fire":
            self.state = "big"
        self.load_state()
        # PLAY ANIMATION HERE
        self.hit = False

    def draw_fire_bullets(self):
        for bullet in self.fire_bullets:
            bullet.draw()

    def draw(self):
        if self.hit:
            super().set_image(self.hit_image)
        else:   
            # Fireballs
            for fireball in self.fireballs.sprites():
                fireball.draw()
            if pygame.time.get_ticks() - self.throw_time < 250:  # Duration of throw animation
                super().set_image(self.throw_image)

            else:
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
