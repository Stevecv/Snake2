# import the pygame module
import random
import pygame
import time

# Define the background colour
# using RGB color coding.
background_colour = (0, 0, 0)

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

def draw_snake(snake):
    #(snake)
    for segment in snake:
        draw_tile(segment[0], segment[1], (0, 255, 0))

apple = (13, 8)
snake = [(4, 8)]
snake_dir = "r"
apple_count = 0
extend = False

last_snake_move = time.time()
# game loop
while running:
    refresh_screen()
    draw_apple(apple[0], apple[1])
    draw_snake(snake)
    extend = True

    if snake[0][0] == apple[0] and snake[0][1] == apple[1]:
        apple_count += 1
        apple = (random.randint(0, grid_cols - 1), random.randint(0, grid_rows - 1))



    pygame.display.flip()


    # Move snake
    if time.time() - last_snake_move > 0.35:
        for snake_piece in range(len(snake)):
            if snake_dir == "r":
                print(snake_piece)
                snake[snake_piece] = (snake[snake_piece][0] + 1, snake[snake_piece][1])
                if extend:
                    snake.append((snake[snake_piece][0], snake[snake_piece][1]))
                    extend = False
                last_snake_move = time.time()



    # for loop through the event queue
    for event in pygame.event.get():

        # Check for QUIT event
        if event.type == pygame.QUIT:
            running = False
