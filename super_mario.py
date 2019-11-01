# Corner Crew
# Super Mario

import pygame

import library.game_methods as game_methods
from library.level import Level
from library.entities.mario import Mario
from library.settings import Settings
from library.game_time import GameTime
from library.score_system import ScoreSystem
from library.lifes import Lifes


def run_game():
    """ Main function of Super Mario."""

    # Pygame initialization
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.mixer.init()
    pygame.mixer.music.load("resources/sounds/background.mp3")
    pygame.mixer.music.play(-1)

    pygame.init()
    pygame.display.set_caption("Super Mario")
    settings = Settings()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))

    # time factors
    SECOND = pygame.USEREVENT
    pygame.time.set_timer(SECOND, 1000)
    game_time = GameTime(screen)

    player_score = ScoreSystem(screen)
    lifes = Lifes(screen)

    # Other objects
    mario = Mario(settings, screen, "resources/mario.json", player_score, game_time, lifes)
    level = Level(settings, screen, "resources/w1_1.json", mario)

    # Game loop
    while True:
        game_methods.on_event(mario, level, SECOND, game_time, settings)
        game_methods.on_update(level, mario)
        game_methods.on_draw(level, mario, game_time, player_score)
        pygame.display.flip()
        clock.tick(60)


run_game()
