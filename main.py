import pygame
import random
import sys

# Initialize
pygame.init()
pygame.mixer.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Racing Game")

# Load assets
road_img = pygame.image.load("assets/road.png")
player_car = pygame.image.load("assets/player_car.png")
enemy_car = pygame.image.load("assets/enemy_car.png")
coin_img = pygame.image.load("assets/coin.png")
crash_sound = pygame.mixer.Sound("assets/crash.wav")
bg_music = pygame.mixer.Sound("assets/bg_music.mp3")

# Resize
player_car = pygame.transform.scale(player_car, (60, 120))
enemy_car = pygame.transform.scale(enemy_car, (60, 120))
coin_img = pygame.transform.scale(coin_img, (40, 40))
road_img = pygame.transform.scale(road_img, (WIDTH, HEIGHT))

# Font
font = pygame.font.SysFont("Arial", 30)
big_font = pygame.font.SysFont("Arial", 50)

# Road limits
ROAD_LEFT = 250
ROAD_RIGHT = 550
coin_width, coin_height = coin_img.get_width(), coin_img.get_height()

clock = pygame.time.Clock()

# Spawn Coin
def spawn_coin():
    coin_x = random.randint(ROAD_LEFT, ROAD_RIGHT - coin_width)
    coin_y = -coin_height
    return coin_x, coin_y

# Collision Detection with padding
def check_collision(x1, y1, w1, h1, x2, y2, w2, h2, padding=15):
    return (
        x1 + padding < x2 + w2 - padding and
        x1 + w1 - padding > x2 + padding and
        y1 + padding < y2 + h2 - padding and
        y1 + h1 - padding > y2 + padding
    )

# Draw Game Window
def draw_window(player_x, player_y, enemy_x, enemy_y, coin_x, coin_y, score):
    win.fill((0, 0, 0))
    win.blit(road_img, (0, 0))
    win.blit(player_car, (player_x, player_y))
    win.blit(enemy_car, (enemy_x, enemy_y))
    win.blit(coin_img, (coin_x, coin_y))
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    win.blit(score_text, (10, 10))
    pygame.display.update()

# Show message on screen
def show_message(text, subtext=""):
    win.fill((0, 0, 0))
    line1 = big_font.render(text, True, (255, 255, 255))
    line2 = font.render(subtext, True, (200, 200, 200))
    win.blit(line1, (WIDTH//2 - line1.get_width()//2, HEIGHT//2 - 50))
    win.blit(line2, (WIDTH//2 - line2.get_width()//2, HEIGHT//2 + 20))
    pygame.display.update()

# Wait for key press to continue
def wait_for_key():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

# Main game loop
def main_game():
    # Play music
    bg_music.play(-1)

    # Game variables
    player_x = WIDTH // 2 - 30
    player_y = HEIGHT - 140
    player_speed = 5

    enemy_x = random.randint(ROAD_LEFT, ROAD_RIGHT - 60)
    enemy_y = -120
    enemy_speed = 6

    coin_x, coin_y = spawn_coin()
    coin_speed = 4

    score = 0
    run = True

    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Player input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_x += player_speed

        # Clamp player
        player_x = max(ROAD_LEFT, min(player_x, ROAD_RIGHT - 60))

        # Move enemy
        enemy_y += enemy_speed
        if enemy_y > HEIGHT:
            enemy_y = -120
            enemy_x = random.randint(ROAD_LEFT, ROAD_RIGHT - 60)

        # Move coin
        coin_y += coin_speed
        if coin_y > HEIGHT:
            coin_x, coin_y = spawn_coin()

        # Collision checks
        if check_collision(player_x, player_y, 60, 120, enemy_x, enemy_y, 60, 120):
            crash_sound.play()
            pygame.time.delay(1000)
            return score  # Game over

        if check_collision(player_x, player_y, 60, 120, coin_x, coin_y, 40, 40):
            score += 1
            coin_x, coin_y = spawn_coin()

        draw_window(player_x, player_y, enemy_x, enemy_y, coin_x, coin_y, score)

# -------------------- Main Program Flow --------------------

while True:
    show_message("Press Any Key to Start", "Arrow keys to move. Collect coins. Avoid cars.")
    wait_for_key()

    final_score = main_game()

    show_message("Game Over", f"Your Score: {final_score} | Press R to Retry or Q to Quit")

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False  # Restart loop
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
