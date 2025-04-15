import pygame
import time
import random
import os

# Initialize pygame
pygame.init()

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
bg_color = (0, 255, 0) 

# Set up the display
dis_width = 800
dis_height = 600
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game with Images')

# Game clock setup
clock = pygame.time.Clock()

snake_block = 30  # Size of snake segments (adjust to match images)
snake_speed = 20  # Slightly slower for better control

# Font setup
font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont(None, 30)

# 1.0 means exact match, lower values make collision detection more forgiving
collision_tolerance = 1

# Function to load or create game images
def create_game_images(block_size=30):
    images = {}
    
    # load background image
    try:
        bg_image = pygame.image.load('img/background.png')
        bg_image = pygame.transform.scale(bg_image, (dis_width, dis_height))
    except:
        bg_image = None

    images["background"] = bg_image

    try:
        welcome_img = pygame.image.load('img/welcome_screen.png')
        game_over_img = pygame.image.load('img/game_over_screen.png')
        # Scaleing
        welcome_img = pygame.transform.scale(welcome_img, (dis_width, dis_height))
        game_over_img = pygame.transform.scale(game_over_img, (dis_width, dis_height))
    except:
        welcome_img = None
        game_over_img = None

    images["welcome"] = welcome_img
    images["game_over"] = game_over_img

    # Load or create head image
    try:
        head_img = pygame.image.load('img/shiba_head.png')
        head_img = pygame.transform.scale(head_img, (block_size, block_size))
    except:
        print("Could not load head image. Creating a default one.")
        head_img = pygame.Surface((block_size, block_size), pygame.SRCALPHA)
        # Transparent background
        head_img.fill((0, 0, 0, 0))
        # Draw head
        radius = block_size // 2
        pygame.draw.circle(head_img, green, (radius, radius), radius)
        # Draw eyes
        eye_radius = block_size // 10
        pygame.draw.circle(head_img, white, (radius + radius//2, radius - radius//2), eye_radius * 2)
        pygame.draw.circle(head_img, black, (radius + radius//2, radius - radius//2), eye_radius)
        pygame.draw.circle(head_img, white, (radius - radius//2, radius - radius//2), eye_radius * 2)
        pygame.draw.circle(head_img, black, (radius - radius//2, radius - radius//2), eye_radius)
    
    # Load or create body image
    try:
        body_img = pygame.image.load('img/shiba_body.png')
        body_img = pygame.transform.scale(body_img, (block_size, block_size))
    except:
        print("Could not load body image. Creating a default one.")
        body_img = pygame.Surface((block_size, block_size), pygame.SRCALPHA)
        # Transparent background
        body_img.fill((0, 0, 0, 0))
        # Draw body (slightly smaller circle)
        padding = block_size // 10
        pygame.draw.circle(body_img, green, (block_size//2, block_size//2), (block_size//2) - padding)
    
    # Load or create food image
    try:
        food_img = pygame.image.load('img/food.png')
        food_img = pygame.transform.scale(food_img, (block_size, block_size))
    except:
        print("Could not load food image. Creating a default one.")
        food_img = pygame.Surface((block_size, block_size), pygame.SRCALPHA)
        # Transparent background
        food_img.fill((0, 0, 0, 0))
        # Draw apple-like shape
        pygame.draw.circle(food_img, red, (block_size//2, block_size//2), block_size//2 - 2)
        # Draw stem
        stem_color = (101, 67, 33)  # Brown
        pygame.draw.rect(food_img, stem_color, [block_size//2 - 2, 2, 4, 7])
        # Draw leaf
        leaf_color = (0, 180, 0)  # Green
        pygame.draw.ellipse(food_img, leaf_color, [block_size//2 + 2, 2, 7, 5])
    
    # Return images as a dictionary
    images["head"] = head_img
    images["body"] = body_img
    images["food"] = food_img
    
    # Create rotated versions of the head for each direction
    images["head_down"] = pygame.transform.rotate(head_img, 0)
    images["head_left"] = pygame.transform.rotate(head_img, 270)
    images["head_up"] = pygame.transform.rotate(head_img, 180)
    images["head_right"] = pygame.transform.rotate(head_img, 90)

    # Create rotated versions of the body for each direction
    images["body_right"] = pygame.transform.rotate(body_img, 90)
    images["body_left"] = pygame.transform.rotate(body_img, 270)
    images["body_down"] = pygame.transform.rotate(body_img, 0)
    images["body_top"] = pygame.transform.flip(images["body_down"], False, True)

    
    return images

# Load game images
game_images = create_game_images(snake_block)

# Function to display score
def show_score(score):
    value = score_font.render(f"Score: {score}", True, white)
    dis.blit(value, [10, 10])

# Function to draw snake using images
def draw_snake(snake_list, direction):
    # Initialized state. No key input
    if direction == "None" and len(snake_list) > 0:
        x, y = snake_list[0]
        dis.blit(game_images["head_down"], (x, y)) 
        return
    
    for i, pos in enumerate(snake_list):
        x, y = pos
        if i == len(snake_list) - 1:  # Head
            # Use appropriate head image based on direction
            if direction == "UP":
                dis.blit(game_images["head_up"], (x, y))
            elif direction == "DOWN":
                dis.blit(game_images["head_down"], (x, y))
            elif direction == "LEFT":
                dis.blit(game_images["head_left"], (x, y))
            else:  # "RIGHT"
                dis.blit(game_images["head_right"], (x, y))
        else:  # Body
            next_x, next_y  = snake_list[i+1]
            diff_x = next_x - x
            diff_y = next_y - y
            if diff_x > 0 :
                dis.blit(game_images["body_right"], (x, y))
            elif diff_x < 0 :
                dis.blit(game_images["body_left"], (x, y))    
            elif diff_y > 0 :
                dis.blit(game_images["body_down"], (x, y))   
            else:
                dis.blit(game_images["body_top"], (x, y))   


# Function to display messages
def message(msg, color, y_offset=0):
    rendered_msg = font_style.render(msg, True, color)
    text_rect = rendered_msg.get_rect(center=(dis_width/2, dis_height/2 + y_offset))
    dis.blit(rendered_msg, text_rect)

# Main game function
def game_loop():
    game_over = False
    game_close = False

    frame_counter = 0
    move_frames = 2

    # Initial snake position (center of screen)
    x1 = dis_width // 2
    y1 = dis_height // 2
    # Align to grid
    x1 = (x1 // snake_block) * snake_block
    y1 = (y1 // snake_block) * snake_block

    # Snake movement variables
    x1_change = 0
    y1_change = 0
    
    # Head direction
    direction = "None"

    # List to store snake body segments
    snake_list = []
    snake_length = 1

    # Initial food position
    foodx = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
    foody = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block

    while not game_over:

        # Game over state handling
        while game_close:
            if game_images["game_over"] is not None:
                dis.blit(game_images["game_over"], (0, 0))

            message("YOU LOSE!!", black, -150)
            message("Game Over! Haha!", black, -100)
            message("Press C to Play Again or Q to Quit", white, 250)

            show_score(snake_length - 1)
            pygame.display.update()

            # Handle key inputs during game over state
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        # Handle player inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and direction != "RIGHT":
                    x1_change = -snake_block
                    y1_change = 0
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    x1_change = snake_block
                    y1_change = 0
                    direction = "RIGHT"
                elif event.key == pygame.K_UP and direction != "DOWN":
                    y1_change = -snake_block
                    x1_change = 0
                    direction = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    y1_change = snake_block
                    x1_change = 0
                    direction = "DOWN"

        frame_counter += 1
        if frame_counter >= move_frames:
        # Check for collision with boundaries
            if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
                game_close = True

            # Update snake position
            x1 = (x1 + x1_change) % dis_width
            y1 = (y1 + y1_change) % dis_height
            

            
            # Update snake head position
            snake_head = [x1, y1]
            snake_list.append(snake_head)
            
            # Maintain snake length by removing oldest segment if needed
            if len(snake_list) > snake_length:
                del snake_list[0]

            # Check for collision with snake's own body
            for segment in snake_list[:-1]:
                if segment == snake_head:
                    game_close = True

            # Check if snake ate food
            if abs(x1 - foodx) < snake_block * collision_tolerance and abs(y1 - foody) < snake_block * collision_tolerance:
                # Generate new food position
                foodx = round(random.randrange(0, dis_width - snake_block) / snake_block) * snake_block
                foody = round(random.randrange(0, dis_height - snake_block) / snake_block) * snake_block
                # Increase snake length
                snake_length += 1

            frame_counter = 0

        # Draw background
        if game_images["background"] is not None:
            dis.blit(game_images["background"], (0, 0))
        else:
            dis.fill(bg_color)

        # Draw food
        dis.blit(game_images["food"], (foodx, foody))
        # Draw the snake
        draw_snake(snake_list, direction)
        # Display score
        show_score(snake_length - 1)
        # Update display
        pygame.display.update()

        # Control game speed
        clock.tick(snake_speed)

    # Quit game
    pygame.quit()
    quit()

# Welcome screen function
def welcome_screen():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN or \
                   event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    waiting = False
        
        
        if game_images["welcome"] is not None:
            # Background image
            dis.blit(game_images["welcome"], (0, 0))
        else:
            # default background
            dis.fill(bg_color) 

        message("Snake Game", white, -250)
        message("Press any arrow key to start", white, -200)
        message("Use arrow keys to move", white, -150)
        
        pygame.display.update()
        clock.tick(15)  

# Start the game
welcome_screen()
game_loop()