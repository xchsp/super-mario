# Corner Crew
# Super Mario

import pygame

import library.game_methods as game_methods
from library.level import Level
from library.entities.mario import Mario
from library.settings import Settings


def run_game():
    """ Main function of Super Mario."""

    # Pygame initialization
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.mixer.init()
    #pygame.mixer_music.load("resources/sounds/background.mp3")
    #pygame.mixer_music.play(-1)
    pygame.init()
    pygame.display.set_caption("Super Mario")
    settings = Settings()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))

    # Other objects
    mario = Mario(settings, screen, "resources/mario.json")
    level = Level(settings, screen, "resources/w1_2.json")

    # Game loop
    while True:
        game_methods.on_event(mario)
        game_methods.on_update(level, mario)
        game_methods.on_draw(level, mario)
        pygame.display.flip()
        clock.tick(60)


run_game()
