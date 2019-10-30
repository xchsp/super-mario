import sys

import pygame
from pygame.locals import *


def on_event(mario, level):
    """Handles Pygame events."""
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            on_key_down(event, mario, level)
        elif event.type == KEYUP:
            on_key_up(event, mario)
        elif event.type == QUIT:
            sys.exit()


def on_key_down(event, mario, level):
    """Handles key presses."""
    if event.key == K_RIGHT:
        mario.moving_right = True
        mario.moving_left = False
        if mario.underground:
            mario.check_pipe_exit(level)
    elif event.key == K_LEFT:
        mario.moving_left = True
        mario.moving_right = False
    elif event.key == K_DOWN:
        if mario.direction == -1:
            mario.image = mario.crouch_image_left
        else:
            mario.image = mario.crouch_image_right
        mario.check_pipe(level)
    elif event.key == K_SPACE:
        if mario.state == "fire":
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

    if event.key == K_DOWN:
        if mario.image == mario.crouch_image_left:
            mario.image = mario.still_image_left
        else:
            mario.image = mario.still_image_right


def on_update(level, mario):
    """Handles positions and logic."""
    mario.update(level)
    level.update(mario, mario.is_scrolling)

def on_draw(level, mario):
    """Displays all objects to screen."""
    level.draw()
    mario.draw()
