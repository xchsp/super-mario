import sys

import pygame
from pygame.locals import *


def on_event(mario):
    """Handles Pygame events."""
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            on_key_down(event, mario)
        elif event.type == pygame.KEYUP:
            on_key_up(event, mario)
        elif event.type == QUIT:
            sys.exit()


def on_key_down(event, mario):
    """Handles key presses."""
    if event.key == K_RIGHT:
        mario.moving_right = True
        mario.moving_left = False
    elif event.key == K_LEFT:
        mario.moving_left = True
        mario.moving_right = False
    elif event.key == K_SPACE:
        mario.throw_fireball()
    elif event.key == K_UP:
        mario.jump()


def on_key_up(event, mario):
    """Handles key releases."""
    if event.key == K_RIGHT:
        mario.moving_right = False
        mario.is_scrolling = False
    if event.key == K_LEFT:
        mario.moving_left = False
        mario.is_scrolling = False


def on_update(level, mario):
    """Handles positions and logic."""
    mario.update(level)
    level.update(mario.is_scrolling)


def on_draw(level, mario):
    """Displays all objects to screen."""
    level.draw()
    mario.draw()
