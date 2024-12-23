# import the pygame module
import random
import pygame
import time

challenge_mode = False

# Define the background colour
# using RGB color coding.
background_colour = (0, 0, 0)

pygame.init()
width = 1000
height = 1000
screen = pygame.display.set_mode((width, height))

# Set the caption of the screen
pygame.display.set_caption('Snake')

# Fill the background colour to the screen
screen.fill(background_colour)

# Variable to keep our game loop running
running = True


# Game
#grid_cols = 17
#grid_rows = 17
grid_cols = 17
grid_rows = 17

wall_locations = []
def generate_apple():
    apple_loc = (random.randint(0, grid_cols - 1), random.randint(0, grid_rows - 1))
    if apple_loc in snake_locations or apple_loc in wall_locations:
        return generate_apple()
    return apple_loc


def generate_wall():
    wall_loc = (random.randint(0, grid_cols - 1), random.randint(0, grid_rows - 1))
    if wall_loc in snake_locations or wall_loc in wall_locations:
        return generate_wall()
    wall_locations.append(wall_loc)
    return wall_loc


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


def draw_walls(wall_locs):
    for location in wall_locs:
        draw_tile(location[0], location[1], (225, 225, 225))


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

def pause_screen():
    global playing
    game_over_screen_fade = pygame.Surface((width, height))
    game_over_screen_fade.fill((0, 0, 0))
    game_over_screen_fade.set_alpha(160)
    screen.blit(game_over_screen_fade, (0, 0))

    font = pygame.font.Font(None, 75)
    text = font.render("PAUSED", True, (255,255,255))
    text_rect = text.get_rect(center=(width/2, height/2))
    screen.blit(text, text_rect)
    pygame.display.update()


apple = (13, 8)
snake_head = (4,8)
snake_locations = [(4, 8)]
snake_length = 1
snake_dir = "r"
apple_count = 0
extend = False
move_queue = []

last_snake_move = time.time()
# game loop
while running:
    refresh_screen()
    draw_apple(apple[0], apple[1])
    draw_snake(snake_length, snake_locations)
    draw_walls(wall_locations)

    font = pygame.font.Font(None, 40)
    text = font.render(str(apple_count), True, (255,255,255))
    screen.blit(text, (10,10))

    if playing:
        if snake_head[0] == apple[0] and snake_head[1] == apple[1]:
            apple_count += 1
            snake_length += 1
            apple = generate_apple()

            if challenge_mode:
                generate_wall()

        pygame.display.flip()

        # Move snake
        if time.time() - last_snake_move > 0.15:
            if len(move_queue) > 0:
                snake_dir = move_queue.pop(0)

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

            if snake_head in wall_locations:
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
                move_queue.append("r")
            if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and snake_dir != "r":
                move_queue.append("l")
            if (event.key == pygame.K_UP or event.key == pygame.K_w) and snake_dir != "d":
                move_queue.append("u")
            if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and snake_dir != "u":
                move_queue.append("d")

            if event.key == pygame.K_ESCAPE:
                playing = not playing
                if not playing:
                    pause_screen()
