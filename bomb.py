import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the window
window_width, window_height = 800, 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Jet Plane Bombing Animation")

# Load assets
jet_img = pygame.image.load("th.jpg")
bomb_img = pygame.image.load("bomb.jpg")
house_img = pygame.image.load("house.jpg")
explosion_img = pygame.image.load("explosion.jpg")

# Game variables
clock = pygame.time.Clock()
bombs_dropped = 0
houses_destroyed = 0
jet_x = 100
jet_y = window_height - jet_img.get_height() - 50
jet_speed = 50

# List to store active bombs
active_bombs = []

# Define colors
white = (255, 255, 255)
red = (255, 0, 0)

# Function to drop bombs from the plane
def drop_bomb():
    x = jet_x + jet_img.get_width() // 2 - bomb_img.get_width() // 2  # Align bomb with jet center
    y = jet_y
    active_bombs.append({'x': x, 'y': y})

# Function to check collision between bomb and house
def check_collision():
    for bomb in active_bombs:
        if (bomb['x'] > house_x - bomb_img.get_width() and
                bomb['x'] < house_x + house_img.get_width() and
                bomb['y'] > house_y - bomb_img.get_height() and
                bomb['y'] < house_y + house_img.get_height()):
            active_bombs.remove(bomb)
            return True
    return False

# Function to generate a new random position for the house
def generate_house_position():
    x = random.randint(0, window_width - house_img.get_width())
    y = random.randint(0, jet_y - house_img.get_height())  # Ensure house is above the plane
    return x, y

# Initialize the first house position
house_x, house_y = generate_house_position()

# Game loop
running = True
while running:
    window.fill(white)  # Clear the screen

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                jet_x -= jet_speed
            elif event.key == pygame.K_RIGHT:
                jet_x += jet_speed
            elif event.key == pygame.K_SPACE:
                drop_bomb()
                bombs_dropped += 1

    # Update game logic
    window.blit(jet_img, (jet_x, jet_y))

    # Update bomb positions
    for bomb in active_bombs:
        bomb['y'] -= 5  # Adjust bomb speed
        window.blit(bomb_img, (bomb['x'], bomb['y']))

    # Check for bomb impact on houses
    window.blit(house_img, (house_x, house_y))

    # Check collision and handle explosion
    if check_collision():
        houses_destroyed += 1
        window.blit(explosion_img, (house_x, house_y))
        house_x, house_y = generate_house_position()  # Generate new house position

    # Display score
    font = pygame.font.Font(None, 36)
    text = font.render(f"Bombs Dropped: {bombs_dropped}  Houses Destroyed: {houses_destroyed}", True, red)
    window.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(60)  # Cap the frame rate

pygame.quit()
