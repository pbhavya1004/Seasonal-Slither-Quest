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
            self.body.insert(0, self.body[0] + self.direction)
            self.new_block = False
        else:
            self.body.insert(0, self.body[0] + self.direction)
            self.body.pop()

    def add_block(self):
        self.new_block = True

    def remove_block(self):
        if len(self.body) > 3:
            self.body.pop()


class FRUIT:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        pygame.draw.rect(screen, (126,166,114), fruit_rect)

    def randomize(self):
        self.pos = Vector2(random.randint(0, cell_number - 1), random.randint(0, cell_number - 1))


class BAD_FRUIT:
    def __init__(self):
        self.bad_fruits = []

    def draw_bad_fruits(self):
        for bad_fruit in self.bad_fruits:
            fruit_rect = pygame.Rect(int(bad_fruit.x * cell_size), int(bad_fruit.y * cell_size), cell_size, cell_size)
            pygame.draw.rect(screen, (0, 0, 0), fruit_rect)

    def randomize(self):
        
        if random.randint(1, 30) == 1:
            self.bad_fruits.append(Vector2(random.randint(0, cell_number - 1), random.randint(0, cell_number - 1)))

    def remove_bad_fruit(self, pos):
        if pos in self.bad_fruits:
            self.bad_fruits.remove(pos)


class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.bad_fruit = BAD_FRUIT()
        self.game_state = "START"  

    def update(self):
        if self.game_state == "PLAYING":
            self.snake.move_snake()
            self.check_collision()
            self.check_bad_fruit()
            self.check_fail()

            self.bad_fruit.randomize()  

    def draw_elements(self):
        if self.game_state == "START":
            self.draw_start_screen()
        elif self.game_state == "GAME_OVER":
            self.draw_game_over_screen()
        else:
            self.fruit.draw_fruit()
            self.bad_fruit.draw_bad_fruits()
            self.snake.draw_snake()
            self.draw_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()

    def check_bad_fruit(self):
        for bad_fruit in self.bad_fruit.bad_fruits:
            if self.snake.body[0] == bad_fruit:
                self.snake.remove_block()
                self.bad_fruit.remove_bad_fruit(bad_fruit)

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        self.game_state = "GAME_OVER"

    def reset_game(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.bad_fruit = BAD_FRUIT()
        self.game_state = "PLAYING"

    def go_to_home(self):
        self.game_state = "START"

    def draw_score(self):
        score_text = f"Score: {len(self.snake.body) - 3}"
        score_surface = game_font.render(score_text, True, (56, 74, 12))
        score_rect = score_surface.get_rect(center=(cell_size * cell_number - 60, cell_size * cell_number - 40))
        pygame.draw.rect(screen, (167, 209, 61), score_rect)
        screen.blit(score_surface, score_rect)

    def draw_start_screen(self):
        screen.fill((0, 0, 0))
        start_text = "Press Enter to Start the Game"
        start_surface = game_font.render(start_text, True, (255, 255, 255))
        start_rect = start_surface.get_rect(center=(cell_size * cell_number // 2, cell_size * cell_number // 2))
        screen.blit(start_surface, start_rect)

    def draw_game_over_screen(self):
        screen.fill((0, 0, 0))
        game_over_text = "Game Over! Press Enter to Restart. Press Esc to Quit. Press H for Home."
        game_over_surface = game_font.render(game_over_text, True, (255, 0, 0))
        game_over_rect = game_over_surface.get_rect(center=(cell_size * cell_number // 2, cell_size * cell_number // 2))
        screen.blit(game_over_surface, game_over_rect)


pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()
game_font = pygame.font.Font(None, 30)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)
main_game = MAIN()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if main_game.game_state == "START":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                main_game.reset_game()

        elif main_game.game_state == "GAME_OVER":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    main_game.reset_game()
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_h:
                    main_game.go_to_home()

        elif main_game.game_state == "PLAYING":
            if event.type == SCREEN_UPDATE:
                main_game.update()
            if event.type == pygame.KEYDOWN:
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
