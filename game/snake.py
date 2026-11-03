import pygame
import time
import random
import math

# Initialize Pygame
pygame.init()

# Define colors
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (255, 215, 0)  # Gold color
blue = (50, 153, 213)

# Screen dimensions
dis_width = 1000
dis_height = 700

# Set up the display
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game by Whimsickel wonders')

# Set up the clock
clock = pygame.time.Clock()

# Snake properties
snake_block = 20
snake_speed = 12

# Font styles
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Load sound
collect_sound_path = r"C:\rithika\pygame install\snake.wav"
collect_sound = pygame.mixer.Sound(collect_sound_path)

# Load background image
background_image_path = r"C:\rithika\pygame install\47774339.jpg"
background_image = pygame.image.load(background_image_path)
background_image = pygame.transform.scale(background_image, (dis_width, dis_height))  # Scale the image to fit the screen

# Define food properties
food_radius = 15  # Radius of the food circle

def Your_score(score):
    value = score_font.render("Your Score: " + str(score), True, yellow)
    dis.blit(value, [0, 0])

def our_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])

def draw_food(x, y, radius):
    pygame.draw.circle(dis, green, (int(x), int(y)), radius)

def distance(x1, y1, x2, y2):
    return math.hypot(x2 - x1, y2 - y1)

def gameLoop():
    game_over = False
    game_close = False

    # Initial snake position and movement
    x1 = dis_width / 2
    y1 = dis_height / 2
    x1_change = 0
    y1_change = 0

    # Snake properties
    snake_List = []
    Length_of_snake = 1

    # Initial food position
    foodx = round(random.randrange(food_radius, dis_width - food_radius))
    foody = round(random.randrange(food_radius, dis_height - food_radius))

    while not game_over:
        while game_close == True:
            dis.blit(background_image, (0, 0))  # Draw the background image
            message("You Lost! Press C-Play Again or Q-Quit", red)
            Your_score(Length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.blit(background_image, (0, 0))  # Draw the background image
        draw_food(foodx, foody, food_radius)  # Draw the food circle
        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        Your_score(Length_of_snake - 1)

        pygame.display.update()

        # Check collision with food circle
        if distance(x1, y1, foodx, foody) < food_radius:
            foodx = round(random.randrange(food_radius, dis_width - food_radius))
            foody = round(random.randrange(food_radius, dis_height - food_radius))
            Length_of_snake += 1
            # Play sound for collecting the food
            collect_sound.play()

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()
