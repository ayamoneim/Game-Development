import pygame
import random
import time
# Definitions  for the Game
white = (255, 255, 255)
red = (255, 20, 20)
brown = (80, 130, 50)
black = (0, 0, 0)
game_bg = pygame.image.load("Bg.jpg")
apple = pygame.image.load("apple.png")
start_bg = pygame.image.load("start.jpg")
snake_part = pygame.image.load("part.png")
snake_head = pygame.image.load("head.png")
end_bg = pygame.image.load("end_menu.jpg")
dying_snake = pygame.image.load("dying_snake.png")
screen_width = 900 + 40
screen_height = 600 + 40
start_menu = ['Start Game', 'Quit']
end_menu = ['Start Again!', 'Give Up']
delta = 10


pygame.init()

frames_per_sec = 18
clock = pygame.time.Clock()

# Set Game Window
game_display = pygame.display.set_mode((screen_width, screen_height))

# Set Game Title
pygame.display.set_caption('SNAKE ONE LAST TIME !')

def set_start_menu(menu_pointer):
    game_display.blit(start_bg, (0, 0))
    font = pygame.font.Font(None, 50)
    if menu_pointer == 0:
        text = font.render(start_menu[0], 3, red)
    else:
        text = font.render(start_menu[0], 3, white)

    game_display.blit(text, (250, 300))
    if menu_pointer == 1:
        text = font.render(start_menu[1], 3, red)
    else:
        text = font.render(start_menu[1], 3, white)
    game_display.blit(text, (250, 300 + 60))

def set_end_menu(menu_pointer, score):
    game_display.blit(end_bg, (0, 0))
    game_display.blit(dying_snake, (450, 250))
    font = pygame.font.Font(None, 50)
    if menu_pointer == 0:
        text = font.render(end_menu[0], 3, red)
    else:
        text = font.render(end_menu[0], 3, white)

    game_display.blit(text, (200, 250))
    if menu_pointer == 1:
        text = font.render(end_menu[1], 3, red)
    else:
        text = font.render(end_menu[1], 3, white)

    game_display.blit(font.render('SCORE : ' + str(score), 3, brown), (600, 350))

    game_display.blit(text, (200, 300 + 10))


def draw_snake(snake_movements, snake_parts_needed):
    index = 0
    while snake_parts_needed > 0:
        coordinates = snake_movements[len(snake_movements) - index - 1]
        if index == 0:
            game_display.blit(snake_head, (int(coordinates[0]), int(coordinates[1])))
        else:
            game_display.blit(snake_part, (int(coordinates[0]), int(coordinates[1])))

        snake_parts_needed -= 1
        index += 1

def game():
    visited = 0
    current_x = 400
    current_y = 400
    delta_x = delta
    delta_y = 0
    menu_pointer = 0
    game_phase = 1
    running = True
    snake_movements = []
    snake_length = 1
    apple_x = round(random.randrange(10, 900) / 10.0) * 10
    apple_y = round(random.randrange(10, 600) / 10.0) * 10
    pygame.mixer.stop()
    pygame.mixer.Sound('2.wav').play(loops=-1)
    score = 0
    # Game Loop
    while running:
        # Clear List
        if len(snake_movements) > 1000:
            snake_movements[0] = []

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if game_phase == 1 or game_phase == 3:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        menu_pointer = (menu_pointer + 1) % 2
                        pygame.mixer.music.load('tick.mp3')
                        pygame.mixer.music.play(0)
                    elif event.key == pygame.K_UP:
                        pygame.mixer.music.load('tick.mp3')
                        pygame.mixer.music.play(0)
                        if menu_pointer - 1 < 0:
                            menu_pointer -= 1
                            menu_pointer += 2
                        else:
                            menu_pointer -= 1

                        menu_pointer %= 2
                    elif event.key == pygame.K_RETURN:
                        pygame.mixer.music.load('tick.mp3')
                        pygame.mixer.music.play(0)
                        if game_phase == 1:
                            if menu_pointer == 0:
                                game_phase = 2
                                pygame.mixer.stop()
                                pygame.mixer.Sound('1.wav').play(loops=-1)
                            else:
                                quit()
                        elif game_phase == 3:
                            if menu_pointer == 0:
                                game()
                            else:
                                quit()

            elif game_phase == 2:
                # if a key is pressed
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and delta_x != 10:
                        delta_x = - delta
                        delta_y = 0
                    elif event.key == pygame.K_RIGHT and delta_x != -10:
                        delta_x = delta
                        delta_y = 0
                    elif event.key == pygame.K_UP and delta_y != 10:
                        delta_y = - delta
                        delta_x = 0
                    elif event.key == pygame.K_DOWN and delta_y != -10:
                        delta_y = delta
                        delta_x = 0
                    elif event.key == pygame.K_SPACE:
                            game_phase = 4
            elif game_phase == 4:
                # if a key is pressed
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game_phase = 2
        if game_phase == 1:
            set_start_menu(menu_pointer)
        elif game_phase == 2:

            # Set Background
            game_display.blit(game_bg, (0, 0))
            font = pygame.font.Font(None, 40)
            game_display.blit(font.render('SCORE : ' + str(score), 3, white), (390, 5))
            game_display.blit(font.render('Pres SPACE to PAUSE/Cont.!', 3, white), (270, 605))

            if [current_x, current_y] in snake_movements[len(snake_movements) - snake_length:len(snake_movements) - 1] \
                    or current_x >= screen_width - 60 or current_x <= 20 or current_y >= screen_height - 60 or current_y <= 20:

                pygame.mixer.music.load('game_over.wav')
                pygame.mixer.music.play(0)
                game_phase = 3

            else:

                if (abs(apple_x - current_x) * abs(apple_x - current_x)) + (abs(apple_y - current_y)\
                                                                                * abs(apple_y - current_y)) <= 25 * 25:
                    visited += 1
                    if visited == 4:
                        visited = 0
                        score += 1
                        pygame.mixer.music.load('bite.mp3')
                        pygame.mixer.music.play(0)
                        apple_x = int(random.randrange(30, 800) / 10.0) * 10
                        apple_y = int(random.randrange(30, 500) / 10.0) * 10
                        snake_length += 1
                    else:
                        game_display.blit(apple, (apple_x, apple_y))

                else:
                    game_display.blit(apple, (apple_x, apple_y))

                current_x += delta_x
                current_y += delta_y
                snake_movements.append([current_x, current_y])
                draw_snake(snake_movements, snake_length)

        elif game_phase == 3:
            pygame.mixer.stop()
            pygame.mixer.Sound('3.wav').play(loops=-1)
            set_end_menu(menu_pointer, score)

        pygame.display.update()

        # Makes the game thread sleeps to slow the game
        clock.tick(frames_per_sec)
    pygame.quit()

    quit()

game()
