import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Initialize the mixer for sound
pygame.mixer.init()

# Screen dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Blossom Blast")

# Load and scale the image
image_path = r"C:\rithika\pygame install\stars.png"
image = pygame.image.load(image_path)
width = int(image.get_width() * 0.1)
height = int(image.get_height() * 0.1)
image = pygame.transform.scale(image, (width, height))

# Load the sound for collecting small red squares
collect_sound_path = r"C:\rithika\pygame install\square.wav"
collect_sound = pygame.mixer.Sound(collect_sound_path)
circle_sound_path = r"C:\rithika\pygame install\circle.wav"
circle_sound = pygame.mixer.Sound(circle_sound_path)
triangle_sound_path = r"C:\rithika\pygame install\triangle1.wav"
triangle_sound = pygame.mixer.Sound(triangle_sound_path)

# Load and play the background music
background_music_path = r"C:\rithika\pygame install\yumi-remy-158395.mp3"
pygame.mixer.music.load(background_music_path)
pygame.mixer.music.play(-1)  # Loop indefinitely

# Player properties
player_x = 600
player_y = 600
player_vel = 10

# Collectible properties
collectible_sizes = [20, 30, 40]  # Sizes of the collectibles
collectible_points = {20: 2, 30: 3, 40: 5}  # Points for each size
circle_size = 30
circle_speed_boost = 10  # Speed increase
boost_duration = 20  # Duration of the speed boost in seconds
triangle_size = 30
triangle_time_increase = 5  # Time increase in seconds
triangle_max_count = 3  # Max number of triangles to collect
triangle_spawn_interval = 20  # Interval to spawn triangles in seconds

def draw_triangle(surface, color, position, size):
    x, y = position
    half_size = size // 2
    points = [(x, y - half_size), (x - half_size, y + half_size), (x + half_size, y + half_size)]
    pygame.draw.polygon(surface, color, points)

def game_loop():
    global player_x, player_y, score, speed_boost_active, boost_start_time, collectibles, triangle_count, start_time, last_triangle_spawn_time
    num_collectibles = 5
    collectible_speed = 5
    collectibles = []
    speed_boost_active = False
    boost_start_time = 0
    triangle_count = 0
    last_triangle_spawn_time = time.time()

    # Initialize collectibles
    for _ in range(num_collectibles):
        size = random.choice(collectible_sizes)
        x = random.randint(0, SCREEN_WIDTH - size)
        y = random.randint(-SCREEN_HEIGHT, 0)  # Start above the screen
        collectibles.append([x, y, size, 'square'])

    # Add initial circle object
    circle_x = random.randint(0, SCREEN_WIDTH - circle_size)
    circle_y = random.randint(-SCREEN_HEIGHT, 0)  # Start above the screen
    collectibles.append([circle_x, circle_y, circle_size, 'circle'])

    # Game variables
    global score, start_time
    score = 0
    start_time = time.time()  # Record game start time
    time_limit = 60  # Game time limit in seconds

    # Create a clock object to control the frame rate
    clock = pygame.time.Clock()

    # Font for displaying score
    font = pygame.font.SysFont(None, 35)

    # Game loop
    running = True
    while running:
        pygame.time.delay(10)
        
        # Calculate elapsed time
        elapsed_time = time.time() - start_time
        
        # Check if time limit has been reached
        if elapsed_time >= time_limit:
            running = False  # End the game loop

        # Check if it's time to spawn a new triangle
        if triangle_count < triangle_max_count and (time.time() - last_triangle_spawn_time) >= triangle_spawn_interval:
            triangle_x = random.randint(0, SCREEN_WIDTH - triangle_size)
            triangle_y = random.randint(-SCREEN_HEIGHT, 0)
            collectibles.append([triangle_x, triangle_y, triangle_size, 'triangle'])
            triangle_count += 1
            last_triangle_spawn_time = time.time()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_vel
        if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - width:
            player_x += player_vel

        # Update collectible positions
        for collectible in collectibles:
            collectible[1] += collectible_speed if not speed_boost_active else collectible_speed + circle_speed_boost

        # Collision detection
        player_rect = pygame.Rect(player_x, player_y, width, height)
        
        for collectible in collectibles[:]:
            collectible_rect = pygame.Rect(collectible[0], collectible[1], collectible[2], collectible[2])
            if player_rect.colliderect(collectible_rect):
                if collectible[3] == 'square':
                    # Handle square collectible
                    score += collectible_points[collectible[2]]
                    collectibles.remove(collectible)  # Remove collected collectible
                    collect_sound.play()  # Play sound for collecting a small square
                    # Add a new square collectible at a random position at the top
                    new_size = random.choice(collectible_sizes)
                    new_collectible = [random.randint(0, SCREEN_WIDTH - new_size), 0, new_size, 'square']
                    collectibles.append(new_collectible)
                elif collectible[3] == 'circle':
                    # Handle circle collectible
                    collectibles.remove(collectible)  # Remove collected circle
                    # Add a new circle collectible at a random position at the top
                    circle_x = random.randint(0, SCREEN_WIDTH - circle_size)
                    circle_y = random.randint(-SCREEN_HEIGHT, 0)
                    collectibles.append([circle_x, circle_y, circle_size, 'circle'])
                    circle_sound.play()
                    # Activate speed boost
                    speed_boost_active = True
                    boost_start_time = time.time()
                elif collectible[3] == 'triangle':
                    # Handle triangle collectible
                    collectibles.remove(collectible)  # Remove collected triangle
                    triangle_sound.play()
                    # Extend the game time
                    time_limit += triangle_time_increase
                    triangle_sound.play()

        # Reset collectibles that go off screen
        for collectible in collectibles:
            if collectible[1] > SCREEN_HEIGHT:
                if collectible[3] == 'square':
                    size = random.choice(collectible_sizes)
                    collectible[0] = random.randint(0, SCREEN_WIDTH - size)
                    collectible[1] = 0
                    collectible[2] = size
                elif collectible[3] == 'circle':
                    collectible[0] = random.randint(0, SCREEN_WIDTH - circle_size)
                    collectible[1] = 0
                elif collectible[3] == 'triangle':
                    collectible[0] = random.randint(0, SCREEN_WIDTH - triangle_size)
                    collectible[1] = 0

        # Check if boost duration has ended
        if speed_boost_active and (time.time() - boost_start_time) > boost_duration:
            speed_boost_active = False

        # Fill the screen with black
        win.fill((0, 0, 0))

        # Draw the player image
        win.blit(image, (player_x, player_y))
        
        # Draw all collectibles
        for collectible in collectibles:
            if collectible[3] == 'square':
                pygame.draw.rect(win, (255, 0, 0), (collectible[0], collectible[1], collectible[2], collectible[2]))
            elif collectible[3] == 'circle':
                pygame.draw.circle(win, (0, 255, 0), (collectible[0] + circle_size // 2, collectible[1] + circle_size // 2), circle_size // 2)
            elif collectible[3] == 'triangle':
                draw_triangle(win, (0, 0, 255), (collectible[0] + triangle_size // 2, collectible[1] + triangle_size // 2), triangle_size)

        # Display the score and time remaining
        score_text = font.render(f'Score: {score}', True, (255, 255, 255))
        win.blit(score_text, (10, 10))
        
        time_remaining = max(0, int(time_limit - elapsed_time))
        time_text = font.render(f'Time: {time_remaining}s', True, (255, 255, 255))
        win.blit(time_text, (10, 50))

        # Update the display
        pygame.display.update()

        # Cap the frame rate
        clock.tick(30)

    # Stop the background music
    pygame.mixer.music.stop()

    # Display game over screen
    game_over_screen()

def game_over_screen():
    while True:
        win.fill((0, 0, 0))
        game_over_font = pygame.font.SysFont(None, 75)
        message_font = pygame.font.SysFont(None, 50)

        # Display final score
        score_text = game_over_font.render(f'Final Score: {score}', True, (255, 255, 255))
        win.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))

        # Display "Try Again" and "Quit" options
        try_again_text = message_font.render('Press T to Try Again', True, (255, 255, 255))
        quit_text = message_font.render('Press Q to Quit', True, (255, 255, 255))
        win.blit(try_again_text, (SCREEN_WIDTH // 2 - try_again_text.get_width() // 2, SCREEN_HEIGHT // 2))
        win.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    return  # Restart the game
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()

# Main loop
while True:
    game_loop()
