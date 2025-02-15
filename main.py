import pygame
import sys
import random
from pygame.math import Vector2

class SNAKE:
    def __init__(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.direction = Vector2(1,0)
        self.new_block = False

    def draw_snake(self):
        for block in self.body:
            block_rect = pygame.Rect(int(block.x * cell_size), int(block.y * cell_size), cell_size, cell_size)
            pygame.draw.rect(screen, (183, 111, 122), block_rect)

    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

class FRUIT:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        pygame.draw.rect(screen, (126, 166, 114), fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.game_state = "start"  

    def update(self):
        if self.game_state == "playing":
            self.snake.move_snake()
            self.check_collision()
            self.check_fail()

    def draw_elements(self):
        if self.game_state == "start":
            self.draw_start_screen()
        elif self.game_state == "game_over":
            self.draw_game_over_screen()
        else:
            screen.fill((67, 138, 51))
            self.fruit.draw_fruit()
            self.snake.draw_snake()
            self.draw_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        self.game_state = "game_over"

    def draw_score(self):
        score_text = "Score: " + str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True, (56, 74, 12))
        score_x = int(cell_size * cell_number - 60)
        score_y = int(cell_size * cell_number - 40)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        background_rect = pygame.Rect(score_rect.left, score_rect.top, score_rect.width, score_rect.height)
        pygame.draw.rect(screen, (167, 209, 61), background_rect)
        screen.blit(score_surface, score_rect)

    def draw_start_screen(self):
        start_text = "Press Enter to Start"
        start_surface = game_font.render(start_text, True, (255, 255, 255))
        start_rect = start_surface.get_rect(center=(cell_size * cell_number // 2, cell_size * cell_number // 2))
        screen.fill((0, 0, 0))
        screen.blit(start_surface, start_rect)

    def draw_game_over_screen(self):
        game_over_text = "Game Over! Enter = Restart, Esc = Quit, H = Home"
        game_over_surface = game_font.render(game_over_text, True, (255, 0, 0))
        game_over_rect = game_over_surface.get_rect(center=(cell_size * cell_number // 2, cell_size * cell_number // 2))
        screen.fill((0, 0, 0))
        screen.blit(game_over_surface, game_over_rect)

    def reset_game(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.game_state = "playing"

pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()
game_font = pygame.font.Font(None, 25)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)
main_game = MAIN()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == SCREEN_UPDATE:
            main_game.update()

        if event.type == pygame.KEYDOWN:
            if main_game.game_state == "start":
                if event.key == pygame.K_RETURN:
                    main_game.game_state = "playing"

            elif main_game.game_state == "game_over":
                if event.key == pygame.K_RETURN:
                    main_game.reset_game()  
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_h:
                    main_game.reset_game()  
                    main_game.game_state = "start"  


            elif main_game.game_state == "playing":
                if event.key == pygame.K_UP and main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
                if event.key == pygame.K_DOWN and main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
                if event.key == pygame.K_RIGHT and main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)
                if event.key == pygame.K_LEFT and main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)

    screen.fill((67, 138, 51))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)
