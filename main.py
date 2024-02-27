# import the pygame module
import random
import pygame
import time

# Define the background colour
# using RGB color coding.
background_colour = (0, 0, 0)

pygame.init()
width = 500
height = 500
screen = pygame.display.set_mode((width, height))

# Set the caption of the screen
pygame.display.set_caption('Snake')

# Fill the background colour to the screen
screen.fill(background_colour)

# Variable to keep our game loop running
running = True


# Game
grid_cols = 17
grid_rows = 17

def refresh_screen():
    screen.fill(background_colour)

def draw_tile(tile_x, tile_y, color):
    tile_width = width / grid_cols
    tile_height = height / grid_rows

    x = tile_x * tile_width
    y = tile_y * tile_height

    pygame.draw.rect(screen, color, pygame.Rect(x, y, tile_width, tile_height))


def draw_apple(apple_x, apple_y):
    draw_tile(apple_x, apple_y, (255, 0, 0))


def draw_snake(length, locations):
    for i in range(0, length):
        draw_tile(locations[len(locations)-(1+i)][0], locations[len(locations)-(1+i)][1], (0, 255, 0))


playing = True


def game_over():
    global playing
    game_over_screen_fade = pygame.Surface((width, height))
    game_over_screen_fade.fill((0, 0, 0))
    game_over_screen_fade.set_alpha(160)
    screen.blit(game_over_screen_fade, (0, 0))

    font = pygame.font.Font(None, 75)
    text = font.render("GAME OVER", True, (255,255,255))
    text_rect = text.get_rect(center=(width/2, height/2))
    screen.blit(text, text_rect)
    pygame.display.update()
    playing = False

apple = (13, 8)
snake_head = (4,8)
snake_locations = [(4, 8)]
snake_length = 1
snake_dir = "r"
apple_count = 0
extend = False

last_snake_move = time.time()
# game loop
while running:
    refresh_screen()
    draw_apple(apple[0], apple[1])
    draw_snake(snake_length, snake_locations)

    if playing:
        if snake_head[0] == apple[0] and snake_head[1] == apple[1]:
            apple_count += 1
            snake_length += 1
            apple = (random.randint(0, grid_cols - 1), random.randint(0, grid_rows - 1))

        pygame.display.flip()

        # Move snake
        if time.time() - last_snake_move > 0.25:
            if snake_dir == "r":
                snake_head = (snake_head[0] + 1, snake_head[1])
                last_snake_move = time.time()
            if snake_dir == "l":
                snake_head = (snake_head[0] - 1, snake_head[1])
                last_snake_move = time.time()
            if snake_dir == "u":
                snake_head = (snake_head[0], snake_head[1] - 1)
                last_snake_move = time.time()
            if snake_dir == "d":
                snake_head = (snake_head[0], snake_head[1] + 1)
                last_snake_move = time.time()

            snake_locations.append(snake_head)
            if len(snake_locations) > snake_length:
                snake_locations.pop(0)

            if snake_head in snake_locations[0:snake_length-1] and snake_length > 1:
                game_over()

            if snake_head[0] < 0 or snake_head[0] > grid_cols or snake_head[1] < 0 or snake_head[1] > grid_rows:
                game_over()


    # for loop through the event queue
    for event in pygame.event.get():
        # Check for QUIT event
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and snake_dir != "l":
                snake_dir = "r"
            if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and snake_dir != "r":
                snake_dir = "l"
            if (event.key == pygame.K_UP or event.key == pygame.K_w) and snake_dir != "d":
                snake_dir = "u"
            if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and snake_dir != "u":
                snake_dir = "d"
