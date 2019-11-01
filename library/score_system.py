import pygame


class ScoreSystem:

    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 35)
        self.color = (0, 0, 0)
        self.score_header = self.font.render('SCORE', True, self.color)
        self.score_header_rect = self.score_header.get_rect()
        self.score_header_rect.x = 50
        self.lives = 3
        self.coin_counter = 0

        # Enemy score values
        self.coin = 10
        self.goomba = 10
        self.koopa = 20
        self.mushroom = 50
        self.fire_flower = 80

        # Maximum flag score
        self.flag_lower = 40
        self.flag_middle = 80
        self.flag_upper = 200
        self.flag_heigth = 460

        # Player score
        self.score = 0

    def flag_score(self, mario, level_over):
        if not level_over:
            # Upper score
            if mario.rect.y in range(100, 268):
                self.score += self.flag_upper
            
            # Middle score
            elif mario.rect.y in range(267, 435):
                self.score += self.flag_middle            
            
            # Lower score, Mario can just walk across
            else:
                self.score += self.flag_lower

    def goomba_hit(self):
        self.score += self.goomba

    def koopa_hit(self):
        self.score += self.koopa

    def coin_hit(self, mario):
        self.coin_counter += 1
        if self.coin_counter == 10:
            mario.lifes.lifes += 1
            self.coin_counter = 0
        self.score += self.coin

    def mushroom_hit(self):
        self.score += self.mushroom

    def fire_flower_hit(self):
        self.score += self.fire_flower

    def draw(self, underground):
        if underground:
            self.color = (255, 255, 255)
        else:
            self.color = (0, 0, 0)
        self.score_header = self.font.render('SCORE', True, self.color)
        text = self.font.render(str(self.score), True, self.color)
        text_rect = text.get_rect()

        # Positions the text bottom center of score_header
        text_rect.center = self.score_header_rect.center
        text_rect.top = self.score_header_rect.bottom

        # Score
        self.screen.blit(self.score_header, self.score_header_rect)
        self.screen.blit(text, text_rect)
