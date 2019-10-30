import pygame
from pygame.sprite import Sprite
from library.entities.entity import Entity


class FireBullet(Entity):

    def __init__(self, settings, surface, mario_rect, direction):
        super(FireBullet, self).__init__(settings, surface, mario_rect.center)
        self.image = pygame.image.load('resources/images/fire_ball.png')
        self.rect = self.image.get_rect()
        self.rect.center = mario_rect.center
        self.color = (255, 255, 255)
        self.mario_width = mario_rect.width
        self.x_velocity = 10
        self.height = 5
        self.surface = surface
        self.gravity = 1
        self.mass = 1
        self.direction = direction

    def movement(self, level):
        if self.rect.bottom >= 575:
            pass
           # self.height = 4

        if self.height > 0:
            f = ( 0.5 * self.mass * (self.height**2))

        else:
            f = -( 0.5 * self.mass * (self.height**2))

        # TODO: FIX
        try:
            self.rect.y -= f
        except TypeError:
            print('Error: ', f)

        self.height -= .5
        

        if self.direction:
            self.rect.x += self.x_velocity
        else:
            self.rect.x -= self.x_velocity

        self.handle_horizontal_collision(level)
    
    def collision(self, terrain):
        collisions = pygame.sprite.spritecollide(self, terrain, False)
        if collisions:
            for block in collisions:
                if block.rect.y > 580:
                    return True
        return False

    def handle_horizontal_collision(self, level):
        """Called after updating x-position."""
        collisions = pygame.sprite.spritecollide(self, level.terrain, False)
        for collision in collisions:
            pass

    def handle_vertical_collision(self, level):
        """Called after updating y-position."""
        collisions = pygame.sprite.spritecollide(self, level.terrain, False)
        if collisions:
            self.height = 4
        self.movement(level)


    def draw(self):
        #pygame.draw.rect(self.surface, self.color, self.rect)
        self.surface.blit(self.image, self.rect)

    def update(self, level, scrolling):
        if scrolling:
            self.rect.x += self.velocity.x
        # Sprite is out of screen, remove it

        self.handle_vertical_collision(level)
        
