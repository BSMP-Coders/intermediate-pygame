# Only needed if you're running in GitHub Codespaces
import os
os.environ["DISPLAY"] = ":1"

import pygame
import random
import sys
import time

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Healthy Snake Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
GRAY = (50, 50, 50)

# Fonts
font = pygame.font.SysFont("arial", 28, bold=True)
small_font = pygame.font.SysFont("arial", 18)

# Sounds (optional, comment out if no sound device)
try:
    eat_sound = pygame.mixer.Sound(pygame.mixer.Sound(file=None))
except:
    eat_sound = None

# Snake and food logic
def random_position():
    return (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

def draw_cell(pos, color):
    x, y = pos
    pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_snake(snake):
    for i, pos in enumerate(snake):
        color = YELLOW if i == 0 else BLUE
        draw_cell(pos, color)

def draw_food(pos, healthy=True):
    color = GREEN if healthy else RED
    pygame.draw.circle(screen, color, (pos[0] * CELL_SIZE + CELL_SIZE // 2, pos[1] * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 2)
    if healthy:
        pygame.draw.circle(screen, WHITE, (pos[0] * CELL_SIZE + CELL_SIZE // 2, pos[1] * CELL_SIZE + CELL_SIZE // 2), 3)

def show_countdown():
    for count in [3, 2, 1]:
        screen.fill(BLACK)
        text = font.render(f"{count}", True, WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()
        time.sleep(1)

def show_message(msg, color=WHITE):
    text = font.render(msg, True, color)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))

def main():
    clock = pygame.time.Clock()
    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    direction = (1, 0)
    score = 0
    healthy_food = random_position()
    unhealthy_food = random_position()
    while unhealthy_food == healthy_food:
        unhealthy_food = random_position()
    game_over = False

    show_countdown()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_w] and direction != (0, 1):
                    direction = (0, -1)
                elif event.key in [pygame.K_DOWN, pygame.K_s] and direction != (0, -1):
                    direction = (0, 1)
                elif event.key in [pygame.K_LEFT, pygame.K_a] and direction != (1, 0):
                    direction = (-1, 0)
                elif event.key in [pygame.K_RIGHT, pygame.K_d] and direction != (-1, 0):
                    direction = (1, 0)

        # Move snake
        new_head = ((snake[0][0] + direction[0]) % GRID_WIDTH, (snake[0][1] + direction[1]) % GRID_HEIGHT)
        if new_head in snake:
            game_over = True
            break
        snake.insert(0, new_head)

        # Check for healthy food
        if new_head == healthy_food:
            score += 1
            if eat_sound:
                eat_sound.play()
            healthy_food = random_position()
            while healthy_food in snake or healthy_food == unhealthy_food:
                healthy_food = random_position()
            # Unhealthy food moves too
            unhealthy_food = random_position()
            while unhealthy_food in snake or unhealthy_food == healthy_food:
                unhealthy_food = random_position()
        # Check for unhealthy food (snake ignores it)
        elif new_head == unhealthy_food:
            # Just move unhealthy food elsewhere
            unhealthy_food = random_position()
            while unhealthy_food in snake or unhealthy_food == healthy_food:
                unhealthy_food = random_position()
            snake.pop()
        else:
            snake.pop()

        # Draw everything
        screen.fill(GRAY)
        draw_snake(snake)
        draw_food(healthy_food, healthy=True)
        draw_food(unhealthy_food, healthy=False)
        score_text = small_font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Debug info
        debug_text = small_font.render(
            f"Head: {snake[0]}  Dir: {direction}", True, (255, 200, 0)
        )
        screen.blit(debug_text, (10, 30))

        pygame.display.flip()
        clock.tick(12 + score // 3)

    # Game Over
    screen.fill(BLACK)
    show_message(f"Game Over! Score: {score}", color=RED)
    pygame.display.flip()
    time.sleep(2)

if __name__ == "__main__":
    main()
