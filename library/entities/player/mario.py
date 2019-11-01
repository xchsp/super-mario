from itertools import cycle

import pygame
from pygame.sprite import Group

from library.entities.entity import Entity
from library.entities.player.fireball import Fireball
from library.timer import Timer

iterator = cycle(range(10))


def now():
    return pygame.time.get_ticks()


def play_sound(sound):
    pygame.mixer.Channel(1).stop()
    pygame.mixer.Channel(1).play(sound)


def load_bigger_animation():
    animation = []
    small_image = pygame.image.load("resources/images/s_mw1.png").convert_alpha()
    scale = small_image.get_rect().width, small_image.get_rect().height + 5
    medium_image = pygame.transform.scale(small_image, scale).convert_alpha()
    scale = small_image.get_rect().width, small_image.get_rect().height + 10
    big_image = pygame.transform.scale(small_image, scale).convert_alpha()
    bigger_image = pygame.image.load("resources/images/mw1.png").convert_alpha()
    animation.append(medium_image)
    animation.append(big_image)
    animation.append(bigger_image)
    animation.append(big_image)
    animation.append(medium_image)
    animation.append(small_image)
    animation.append(medium_image)
    animation.append(big_image)
    animation.append(bigger_image)
    return Timer(animation, wait=80, loop_once=True)


def load_fire_animation():
    animation = []
    normal_image = pygame.image.load("resources/images/mw1.png").convert_alpha()
    fire_image = pygame.image.load("resources/images/fm1.png").convert_alpha()
    for i in range(4):
        animation.append(fire_image)
        animation.append(normal_image)
    animation.append(fire_image)
    return Timer(animation, wait=80, loop_once=True)


class Mario(Entity):
    """The playable character, Mario."""

    def __init__(self, settings, screen, data, player_score, game_time, lifes):
        super().__init__(settings, screen, (100, 525), data, 1)
        self.settings = settings
        self.velocity.x = -settings.scroll_rate
        self.player_score = player_score
        self.game_time = game_time
        self.lifes = lifes
        self.state = "small"
        # Will be initialized later
        self.walk_animation = self.run_animation = None
        self.still_image = self.jump_image = self.hit_image = self.crouch_image = None
        super().init_image(pygame.image.load(self.data[self.state]["walking"]["sequence"][3]).convert_alpha())
        self.load_state()
        self.bigger_animation = load_bigger_animation()
        self.fire_animation = load_fire_animation()
        self.pole_slide_image = pygame.image.load("resources/images/m_pole.png").convert_alpha()
        self.fire_pole_slide_image = pygame.image.load("resources/images/m_fpole.png").convert_alpha()
        self.throw_image = pygame.image.load("resources/images/m_throw.png").convert_alpha()
        self.death_image = pygame.image.load("resources/images/sm_hit.png")
        self.moving_left = self.moving_right = self.is_scrolling = False
        self.is_jumping = self.is_d_jumping = False
        self.jump_sound = pygame.mixer.Sound("resources/sounds/jump.wav")
        self.fireballs = Group()
        self.throw_time = 0
        self.animation_time = 0
        self.invincible_time = 0
        self.dead = False
        # True if animating going through pipe
        self.pipe_down = False
        self.pipe_up = False
        self.pipe_side = False

        # Sounds
        self.coin_sound = pygame.mixer.Sound("resources/sounds/coin.wav")
        self.enemy_kill_sound = pygame.mixer.Sound("resources/sounds/enemy_killed.wav")
        self.fireball_sound = pygame.mixer.Sound("resources/sounds/fireball.wav")
        self.powerup_sound = pygame.mixer.Sound("resources/sounds/powerup.wav")
        self.brick_break_sound = pygame.mixer.Sound("resources/sounds/brick_break.wav")
        self.pipe_sound = pygame.mixer.Sound("resources/sounds/pipe.wav")
        self.death_sound = pygame.mixer.Sound("resources/sounds/mario_dies.wav")
        self.switch_bg_music = False
        self.level_2 = False

        # States
        self.invincible = False
        self.pipe_entrance = False
        self.pipe_exit = False
        self.underground = False
        self.running = False
        self.crouching = False
        self.animating = False

        # Horizontal movement variables
        self.acceleration_x = 0
        self.x_change = 0
        self.castle_entrance_x = 778

    def load_state(self):
        """State animations and images."""
        super().init_mario_image(pygame.image.load(self.data[self.state]["walking"]["sequence"][3]).convert_alpha())
        self.load_state_images()
        self.walk_animation = self.load_walk_animation(100)
        self.run_animation = self.load_walk_animation(50)

    def load_state_images(self):
        self.still_image = self.image
        self.jump_image = pygame.image.load(self.data[self.state]["jump"]).convert_alpha()
        self.hit_image = pygame.image.load(self.data[self.state]["hit"]).convert_alpha()
        self.crouch_image = pygame.image.load(self.data[self.state]["crouch"]).convert_alpha()

    def load_walk_animation(self, animation_speed):
        animation = []
        for x in range(self.data[self.state]["walking"]["sequence_sz"]):
            animation.append(pygame.image.load(self.data[self.state]["walking"]["sequence"][x]).convert_alpha())
        return Timer(animation, wait=animation_speed)

    def throw_fireball(self):
        fireball = Fireball(self.settings, self.screen, self.rect.center, self.direction)
        play_sound(self.fireball_sound)
        self.fireballs.add(fireball)
        self.throw_time = now()

    def jump(self):
        print(self.rect.topleft)
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
            if collision.is_castle:
                continue
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
                            collision.show_item(self)
                        elif collision.has_item is 0 and self.state is not "small" and collision.type is "brick":
                            play_sound(self.brick_break_sound)
                            collision.kill()
                    except AttributeError:
                        pass
                    break
                # Mario is falling
                elif self.velocity.y > 0:
                    # check if pipe is an enterence
                    try:
                        if collision.enter:
                            self.pipe_entrance = True
                    except AttributeError:
                        self.pipe_entrance = False
                    self.rect.bottom = collision.rect.top
                    self.reset_jump()

        # No vertical collisions, apply gravity
        else:
            self.fall()

    def update_fire_balls(self, level, vel_x=None):
        for bullet in self.fireballs:
            if not bullet.hit:
                collisions = pygame.sprite.spritecollide(bullet, level.enemies, False)
                for collision in collisions:
                    if not collision.hit:
                        play_sound(self.enemy_kill_sound)
                        collision.hit_sequence()
                        bullet.hit_sequence()
            bullet.update(level, self.is_scrolling, vel_x)

    def check_pipe(self):
        """Checks if it is an underground pipe."""
        if self.pipe_entrance:
            play_sound(self.pipe_sound)
            self.moving_left = False
            self.moving_right = False
            self.pipe_down = True
            self.crouching = False
            self.pipe_entrance = False

    def check_pipe_exit(self, level):
        """Checks if it is an underground pipe."""
        if pygame.sprite.collide_rect(self, level.exit_pipe):
            play_sound(self.pipe_sound)
            self.moving_left = False
            self.moving_right = False
            self.pipe_side = True
            self.pipe_exit = False

    def update(self, level, scrolling=None, vel_x=None):
        if self.game_time.seconds <= 0 and not self.dead:
            self.died()
            pygame.mixer.music.stop()
            pygame.mixer.music.load("resources/sounds/mario_dies.wav")
            pygame.mixer.music.play()
        # Actually moves Mario horizontally, if on left side of screen.
        # Otherwise, scroll screen to simulate movement
        if self.dead:
            if now() - self.death_time >= 2500:
                self.dead = False
                self.game_time.seconds = 350

                if self.lifes.lifes == 0:
                    self.player_score.score = 0
                    self.game_time.seconds = 350
                    self.lifes.lifes = 3
                    level.load("resources/w1_1.json")
                    self.level_2 = False
                elif self.level_2:
                    level.load("resources/w1_2.json")
                else:
                    level.load("resources/w1_1.json")
                self.position = (100, 0)
                super().init_image(pygame.image.load(self.data[self.state]["walking"]["sequence"][3]).convert_alpha())
                pygame.mixer.music.load("resources/sounds/background.mp3")
                pygame.mixer.music.play(-1)
        elif self.rect.y > self.settings.screen_height and not self.dead:
            pygame.mixer.music.stop()
            pygame.mixer.music.load("resources/sounds/mario_dies.wav")
            pygame.mixer.music.play()
            self.switch_bg_music = False
            self.died()

        # Falling death movement
        if self.dead:
            self.fall()
            self.rect.y += self.velocity.y
            return

        if self.running:
            self.update_fire_balls(level, -self.velocity.x)
        else:
            self.update_fire_balls(level)

        # Freeze Mario on taking damage
        if self.hit:
            self.moving_left = False
            self.moving_right = False
            self.is_scrolling = False
        # Going down pipe animation
        elif self.pipe_down:
            self.rect.y += 2
            if self.rect.y >= 500:
                self.underground = True
                self.pipe_down = False
                # reposition
                self.position = (100, -300)
                super().init_image(pygame.image.load(self.data[self.state]["walking"]["sequence"][3]).convert_alpha())
                level.create_underground()
        # Going into pipe from side animation
        elif self.pipe_side:
            self.rect.x += 2
            if self.rect.x >= 900:
                self.pipe_side = False
                self.pipe_up = True
                self.underground = False
                self.position = (25, level.go_surface() + 80)
                play_sound(self.pipe_sound)
                super().init_image(pygame.image.load(self.data[self.state]["walking"]["sequence"][3]).convert_alpha())
        # Coming out of pipe animation
        elif self.pipe_up:
            self.rect.y -= 2
            if self.rect.bottom <= 505:
                self.pipe_up = False
        else:
            # running
            if self.running:
                self.velocity.x = -self.settings.scroll_rate * 2
            # resets scroll if not running
            else:
                self.velocity.x = -self.settings.scroll_rate
            if self.underground:
                if self.moving_right:
                    self.rect.centerx += self.velocity.x
                    self.direction = 1
                elif self.moving_left:
                    self.direction = -1
                    self.rect.x -= self.velocity.x
            # end of level
            elif self.settings.level_over:
                self.castle_walk(level)
                return
            # normal stuff
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
        if self.dead:
            return
        collisions = pygame.sprite.spritecollide(self, level.enemies, False)
        for collision in collisions:
            if not collision.hit:
                # Jumping on enemy
                if self.invincible or (self.rect.bottom <= collision.rect.centery):
                    play_sound(self.enemy_kill_sound)
                    collision.hit_sequence()
                    if collision.type == "koopa":
                        self.player_score.koopa_hit()
                    if collision.type == "goomba":
                        self.player_score.goomba_hit()
                    if not self.invincible:
                        self.rect.bottom = collision.rect.top
                        self.is_jumping = True  # Prevent jumping after bounce
                        self.is_d_jumping = True
                        self.velocity.y = -10  # Small bounce when jumping on enemies
                else:
                    # Touched enemy, Mario takes damage
                    if not self.hit and not self.invincible:
                        if self.state is "small":
                            pygame.mixer.music.stop()
                            pygame.mixer.music.load("resources/sounds/mario_dies.wav")
                            pygame.mixer.music.play()
                            self.died()
                        else:
                            play_sound(self.pipe_sound)
                            self.hit_sequence()
                            self.go_down_state()

    def check_item_collisions(self, level):
        """Detect if touched power-up."""
        collisions = pygame.sprite.spritecollide(self, level.items, True)
        for collision in collisions:
            if collision.item_type == 1:
                play_sound(self.coin_sound)
                self.player_score.coin_hit(self)
            if collision.item_type == 2:
                play_sound(self.powerup_sound)
                self.get_bigger()
            if collision.item_type == 3:
                play_sound(self.powerup_sound)
                self.get_fire()
            if collision.item_type == 4:
                play_sound(self.powerup_sound)
                self.get_star()

    def get_bigger(self):
        self.player_score.mushroom_hit()
        self.state = "big"
        self.load_state()
        self.animation_time = now()
        self.bigger_animation.reset()
        self.animating = True

    def get_fire(self):
        self.player_score.fire_flower_hit()
        self.state = "fire"
        self.load_state()
        self.animation_time = now()
        self.fire_animation.reset()
        self.animating = True

    def get_star(self):
        self.player_score.star_hit()
        pygame.mixer.music.stop()
        pygame.mixer.music.load("resources/sounds/star_power.mp3")
        pygame.mixer.music.play(-1)
        self.invincible = True
        self.invincible_time = now()

    def go_down_state(self):
        if self.state == "big":
            self.state = "small"
            self.bigger_animation.reset()
        elif self.state == "fire":
            self.fire_animation.reset()
            self.state = "big"
        self.load_state()
        self.animation_time = now()

    def prep_castle_walk(self):
        self.settings.level_over = True
        self.moving_right = False
        self.is_scrolling = False
        self.switch_bg_music = True

    def castle_walk(self, level):
        # Cleared level music
        if self.switch_bg_music:
            self.player_score.score += self.game_time.seconds * 2
            pygame.mixer.music.stop()
            pygame.mixer.music.load("resources/sounds/level_cleared.wav")
            pygame.mixer.music.play()
            self.switch_bg_music = False
        # Sliding down pole
        if not self.moving_right:
            if self.rect.bottom <= 598:
                self.rect.bottom += 3
                self.player_score.score += 5
            else:
                self.moving_right = True
                super().init_mario_image(
                    pygame.image.load(self.data[self.state]["walking"]["sequence"][3]).convert_alpha())
        else:
            # Walking towards castle
            if self.rect.x < self.castle_entrance_x + 120:
                self.rect.x += 2
            # Fall into level 2
            else:
                self.moving_right = False
                self.running = False
                self.settings.level_over = False
                level.load("resources/w1_2.json")
                self.switch_bg_music = False
                self.level_2 = True
                pygame.mixer.music.stop()
                pygame.mixer.music.load("resources/sounds/background.mp3")
                pygame.mixer.music.play(-1)
                self.game_time.seconds = 350
                self.position = (100, -300)
                super().init_image(pygame.image.load(self.data[self.state]["walking"]["sequence"][3]).convert_alpha())

    def draw(self):
        # Fireballs
        for fireball in self.fireballs.sprites():
            fireball.draw()

        # Sliding image
        if self.settings.level_over:
            if self.moving_right:
                super().set_image(self.walk_animation.get_image())
            else:
                if self.state == "fire":
                    super().set_image(self.fire_pole_slide_image)
                else:
                    super().set_image(self.pole_slide_image)
        elif self.dead:
            super().set_image(self.death_image)

        elif self.hit:
            # Big to small Mario
            if self.state == "small" and now() - self.animation_time <= 800:
                super().init_mario_image(self.bigger_animation.get_image(True))
                super().set_image(self.image)
            # Fire to big Mario
            elif self.state == "big" and now() - self.animation_time <= 640:
                super().init_mario_image(self.fire_animation.get_image(True))
                super().set_image(self.image)
            else:
                # Fixing image offsets
                super().init_mario_image(
                    pygame.image.load(self.data[self.state]["walking"]["sequence"][3]).convert_alpha())
                self.hit = False
        elif self.animating:
            self.moving_left = False
            self.moving_right = False
            # Bigger Mario animation
            if self.state == "big" and now() - self.animation_time <= 800:
                super().init_mario_image(self.bigger_animation.get_image())
                super().set_image(self.image)
            # Fire Mario animation
            elif self.state == "fire" and now() - self.animation_time <= 640:
                super().init_mario_image(self.fire_animation.get_image())
                super().set_image(self.image)
            else:
                self.animating = False
        else:
            # Throw animation
            if now() - self.throw_time < 250:
                super().set_image(self.throw_image)
            elif self.crouching:
                super().set_image(self.crouch_image)
            else:
                if self.moving_right or self.moving_left:
                    if self.is_jumping:
                        super().set_image(self.jump_image)
                    elif self.running:
                        super().set_image(self.run_animation.get_image())
                    else:
                        super().set_image(self.walk_animation.get_image())
                # Standing still
                else:
                    if self.is_jumping:
                        super().set_image(self.jump_image)
                    else:
                        super().set_image(self.still_image)

        # Brighten image
        if self.invincible:
            if now() - self.invincible_time <= 8000:
                if next(iterator) < 5:
                    brightness = 100
                    brighter_image = self.image.copy().convert_alpha()
                    brighter_image.fill((brightness, brightness, brightness), special_flags=pygame.BLEND_RGB_ADD)
                    self.screen.blit(brighter_image, self.rect)
                    return
            else:
                self.invincible = False
                pygame.mixer.music.stop()
                pygame.mixer.music.load("resources/sounds/background.mp3")
                pygame.mixer.music.play(-1)
        # Parent draw() actually blits the image
        super().draw()

    def died(self):
        self.moving_left = False
        self.moving_right = False
        self.is_scrolling = False
        self.jump()
        self.dead = True
        self.lifes.lifes -= 1
        self.death_time = now()
