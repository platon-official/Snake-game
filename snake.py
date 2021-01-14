import pygame
from pygame.time import Clock
from pygame.math import Vector2
import random
from pygame.font import Font
from pygame import Color

WIDTH = 40
HEIGHT = 20

size = width, height = (WIDTH * HEIGHT), (WIDTH * HEIGHT)
screen = pygame.display.set_mode(size)


class Game:
    class Snake:
        def __init__(self):
            self.snake_elements = [Vector2(5, 5), Vector2(4, 5), Vector2(3, 5)]
            self.levels = 20
            self.new_element = False
            self.direction = Vector2(1, 0)
            self.sound_eating = pygame.mixer.Sound('Sound/Sound_eat.wav')
            self.main_sound = pygame.mixer.Sound('Sound/Sound_main.mp3')
            self.sound_menu = pygame.mixer.Sound('Sound/sound_mainmenu.mp3')
            self.head_right = pygame.image.load('Graphic/head_right.png').convert_alpha()
            self.head_left = pygame.image.load('Graphic/head_left.png').convert_alpha()
            self.head_up = pygame.image.load('Graphic/head_up.png').convert_alpha()
            self.head_down = pygame.image.load('Graphic/head_down.png').convert_alpha()
            self.tail_up = pygame.image.load('Graphic/tail_up.png').convert_alpha()
            self.tail_down = pygame.image.load('Graphic/tail_down.png').convert_alpha()
            self.tail_right = pygame.image.load('Graphic/tail_right.png').convert_alpha()
            self.tail_left = pygame.image.load('Graphic/tail_left.png').convert_alpha()
            self.vertical = pygame.image.load('Graphic/ver.png').convert_alpha()
            self.horizontal = pygame.image.load('Graphic/hor.png').convert_alpha()
            self.body_l2 = pygame.image.load('Graphic/body_l2.png').convert_alpha()
            self.body_r2 = pygame.image.load('Graphic/body_l1.png').convert_alpha()
            self.body_l1 = pygame.image.load('Graphic/body_r1.png').convert_alpha()
            self.body_r1 = pygame.image.load('Graphic/body_r2.png').convert_alpha()

        def play_main_music(self):
            self.main_sound.play(10000)

        def draw_snake(self):
            self.head_update()
            self.tail_update()
            for i, x in enumerate(self.snake_elements):
                x_pos = (x.x * WIDTH)
                y_pos = (x.y * WIDTH)
                block_rect = pygame.Rect(x_pos, y_pos, WIDTH, WIDTH)
                if i == 0:
                    screen.blit(self.head, block_rect)
                elif i == len(self.snake_elements) - 1:
                    screen.blit(self.tail, block_rect)
                else:
                    if (self.snake_elements[i + 1] - x).x == (self.snake_elements[i - 1] - x).x:
                        screen.blit(self.vertical, block_rect)
                    elif (self.snake_elements[i + 1] - x).y == (self.snake_elements[i - 1] - x).y:
                        screen.blit(self.horizontal, block_rect)
                    else:
                        if (self.snake_elements[i + 1] - x).x == -1 and (self.snake_elements[i - 1] - x).y == -1 or (
                                self.snake_elements[i + 1] - x).y == -1 and (self.snake_elements[i - 1] - x).x == -1:
                            screen.blit(self.body_l2, block_rect)
                        elif (self.snake_elements[i + 1] - x).x == -1 and (self.snake_elements[i - 1] - x).y == 1 or (
                                self.snake_elements[i + 1] - x).y == 1 and (self.snake_elements[i - 1] - x).x == -1:
                            screen.blit(self.body_r2, block_rect)
                        elif (self.snake_elements[i + 1] - x).x == 1 and (self.snake_elements[i - 1] - x).y == -1 or (
                                self.snake_elements[i + 1] - x).y == -1 and (self.snake_elements[i - 1] - x).x == 1:
                            screen.blit(self.body_l1, block_rect)
                        elif (self.snake_elements[i + 1] - x).x == 1 and (self.snake_elements[i - 1] - x).y == 1 or (
                                self.snake_elements[i + 1] - x).y == 1 and (self.snake_elements[i - 1] - x).x == 1:
                            screen.blit(self.body_r1, block_rect)

        def head_update(self):
            head_position = self.snake_elements[1] - self.snake_elements[0]
            if head_position == Vector2(1, 0):
                self.head = self.head_left
            elif head_position == Vector2(-1, 0):
                self.head = self.head_right
            elif head_position == Vector2(0, 1):
                self.head = self.head_up
            elif head_position == Vector2(0, -1):
                self.head = self.head_down

        def tail_update(self):
            tail_position = self.snake_elements[-2] - self.snake_elements[-1]
            if tail_position == Vector2(1, 0):
                self.tail = self.tail_left
            elif tail_position == Vector2(-1, 0):
                self.tail = self.tail_right
            elif tail_position == Vector2(0, 1):
                self.tail = self.tail_up
            elif tail_position == Vector2(0, -1):
                self.tail = self.tail_down

        def move_snake(self):
            if self.new_element:
                ball_copy = self.snake_elements[:]
                ball_copy.insert(0, ball_copy[0] + self.direction)
                self.snake_elements = ball_copy[:]
                self.new_element = False
            else:
                ball_copy = self.snake_elements[:-1]
                ball_copy.insert(0, ball_copy[0] + self.direction)
                self.snake_elements = ball_copy[:]

        def add_ball(self):
            self.new_element = True

        def draw_score(self):
            apple = pygame.image.load('Graphic/apple.png').convert_alpha()
            score_font = Font('Font/Arial.ttf', 25)
            score = score_font.render(f'{str(len(self.snake_elements) - 3)} / {str(self.levels)}', True,
                                      Color('orange'))
            level_text = score_font.render('Level: ', True, Color('orange'))
            level = score_font.render(f'{int(self.levels / 20)} / 5', True, Color('orange'))

            screen.blit(score, (685, 770))
            screen.blit(apple, (655, 765))
            screen.blit(level_text, (10, 770))
            screen.blit(level, (80, 770))

        def play_eat_sound(self):
            self.sound_eating.play()

    class Fruit:
        def __init__(self):
            self.y_random = random.randint(0, HEIGHT - 1)
            self.x_random = random.randint(0, HEIGHT - 1)
            self.position = Vector2(self.x_random, self.y_random)
            self.apple = pygame.image.load('Graphic/apple.png').convert_alpha()

        def draw_fruit(self):
            fruit = pygame.Rect(self.position.x * WIDTH, self.position.y * WIDTH, WIDTH, WIDTH)
            screen.blit(self.apple, fruit)

    class Logic:
        def __init__(self):
            self.snake = Game.Snake()
            self.fruit = Game.Fruit()

        def update(self):
            self.snake.move_snake()
            self.check_eating_apple()
            self.check_tail()

        def draw_elements(self):
            self.background()
            self.fruit.draw_fruit()
            self.snake.draw_snake()
            self.snake.draw_score()
            self.check_win()

        def check_eating_apple(self):
            if self.fruit.position == self.snake.snake_elements[0]:
                self.fruit.__init__()
                self.snake.add_ball()
                self.snake.play_eat_sound()

            for block in self.snake.snake_elements[1:]:
                if block == self.fruit.position:
                    self.fruit.__init__()

        def check_tail(self):
            if not 0 <= self.snake.snake_elements[0].x < HEIGHT:
                self.game_over()
            elif not 0 <= self.snake.snake_elements[0].y < HEIGHT:
                self.game_over()

            for block in self.snake.snake_elements[1:]:  # касается хвоста
                if block == self.snake.snake_elements[0]:
                    self.game_over()

        def reset(self):
            self.snake.snake_elements = [Vector2(5, 5), Vector2(4, 5), Vector2(3, 5)]
            self.snake.direction = Vector2(1, 0)

        def game_over(self):
            score = (len(self.snake.snake_elements) - 3)
            show = True
            while show:
                font = Font('Font/Arial.ttf', 25)
                render_end = font.render('Game Over', False, Color('orange'))
                render_score = font.render(f'Score: {score}', False, Color('orange'))
                render_restart = font.render('Tap space to restart', False, Color('orange'))
                screen.blit(render_end, (10, 10))
                screen.blit(render_score, (10, 35))
                screen.blit(render_restart, ((width // 2 - 110), (height // 2 - 40)))
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            show = False
                            self.reset()

        def game_start(self):
            show = True
            while show:
                img = pygame.image.load('Graphic/menu.png').convert_alpha()
                screen.blit(img, (0, 0))
                self.snake.sound_menu.play()
                self.snake.sound_menu.set_volume(0.5)
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            show = False
                            self.snake.sound_menu.stop()
                            self.snake.play_main_music()

        def win_game(self):
            if (self.snake.levels / 20) == 5:
                self.final_game_over()
            sound = pygame.mixer.Sound('Sound/sound_win.mp3').play()
            sound.set_volume(0.1)
            show = True
            while show:
                render = pygame.image.load('Graphic/win.png').convert_alpha()
                screen.blit(render, (0, 0))
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            show = False
                            self.reset()
                            self.snake.levels += 20

        def final_game_over(self):
            sound = pygame.mixer.Sound('Sound/sound_win.mp3').play()
            sound.set_volume(0.1)
            show = True
            while show:
                img = pygame.image.load('Graphic/lvl_10.png').convert_alpha()
                screen.blit(img, (0, 0))
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        exit()

        def check_win(self):
            if int(len(self.snake.snake_elements)) - 3 == self.snake.levels:
                self.win_game()

        def background(self):
            background_image = pygame.image.load('Graphic/background2.png').convert_alpha()
            screen.blit(background_image, (0, 0))

    class Init:
        def __init__(self):
            FPS = 200
            pygame.mixer.pre_init(44100, -16, 2, 512)
            pygame.init()
            pygame.display.set_caption('Snake')
            pygame.display.set_icon(pygame.image.load('icon/snake.png'))

            main_game = Game.Logic()
            main_game.game_start()
            clock = Clock()
            SCREEN_UPDATE = pygame.USEREVENT
            pygame.time.set_timer(SCREEN_UPDATE, 200)
            snake_run = True
            while snake_run:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        snake_run = False
                    if event.type == SCREEN_UPDATE:
                        main_game.update()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP and main_game.snake.direction.y == 0:
                            main_game.snake.direction = Vector2(0, -1)
                        elif event.key == pygame.K_DOWN and main_game.snake.direction.y == 0:
                            main_game.snake.direction = Vector2(0, 1)
                        elif event.key == pygame.K_LEFT and main_game.snake.direction.x == 0:
                            main_game.snake.direction = Vector2(-1, 0)
                        elif event.key == pygame.K_RIGHT and main_game.snake.direction.x == 0:
                            main_game.snake.direction = Vector2(1, 0)
                main_game.draw_elements()
                clock.tick(FPS)
                pygame.display.update()
            pygame.quit()


if __name__ == '__main__':
    Game.Init()
