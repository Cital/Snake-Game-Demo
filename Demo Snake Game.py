import pygame
import random

# COLORS
COLORS = {
    "BLACK": pygame.Color(0,0,0),
    "WHITE": pygame.Color(255,255,255),
    "RED": pygame.Color(255,0,0),
    "GREEN": pygame.Color(0,255,0),
    "BLUE": pygame.Color(0,0,255),
    "YELLOW": pygame.Color(255,255,0),
    "TEAL": pygame.Color(0,255,255),
    "PURPLE": pygame.Color(255,0,255)
}

SNAKE_COLORS = [COLORS['GREEN'], COLORS['RED'], COLORS['BLUE'], COLORS['YELLOW'], COLORS['TEAL']]
PICKUP_COLORS = [COLORS['PURPLE'], COLORS['WHITE'], COLORS['TEAL'], COLORS['YELLOW'], COLORS['GREEN']]

pygame.init()

# SCREEN VALUES
size = 10
width, height = 72, 48
pygame.display.set_caption('Demo Snake Game')
window = pygame.display.set_mode((width*size, height*size))

# SNAKE VALUES
directions = {
    pygame.K_UP: pygame.Vector2(0, -1),
    pygame.K_DOWN: pygame.Vector2(0, 1),
    pygame.K_LEFT: pygame.Vector2(-1, 0),
    pygame.K_RIGHT: pygame.Vector2(1, 0)
}

# SCORE DISPLAY
score = 0
font = pygame.font.Font(None, 50)
small_font = pygame.font.Font(None, 25)
fps = 60

def select_difficulty():
    global fps
    while True:
        window.fill(COLORS['BLACK'])
        text_surface = small_font.render('Press E for Easy Mode or H for Hard Mode', True, COLORS['GREEN'])
        window.blit(text_surface, (10, 10))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    fps = 30
                    return
                if event.key == pygame.K_h:
                    fps = 60
                    return

def reset_game():
    global snake, direction, score, pickup_position, snake_color, pickup_color
    snake = [pygame.Vector2(10, 5), pygame.Vector2(9, 5), pygame.Vector2(8, 5), pygame.Vector2(7, 5)]
    direction = directions[pygame.K_RIGHT]
    score = 0
    pickup_position = random_position()
    snake_color = SNAKE_COLORS[0]
    pickup_color = PICKUP_COLORS[0]

# GAME ENDING SCREEN
def end_game():
    text_surface = font.render(f'Final Score: {str(score)}', True, COLORS['YELLOW'])
    text_rect = text_surface.get_rect(center = (width*size//2, height*size//2))
    window.blit(text_surface, text_rect)
    pygame.display.flip()
    pygame.time.wait(2000)

def draw_rect(position, color):
    pygame.draw.rect(window, color, pygame.Rect(position.x*size, position.y*size, size, size))

def random_position():
    return pygame.Vector2(random.randrange(width), random.randrange(height))

pickup_position = random_position()

clock = pygame.time.Clock()

def game_loop():
    global running, direction, pickup_position, score, snake_color, pickup_color
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key in directions:
                    new_direction = directions[event.key]
                    if new_direction != direction and new_direction != -direction:
                        direction = new_direction

        snake.insert(0, snake[0] + direction)

        if snake[0] == pickup_position:
            score += 10
            pickup_position = random_position()
            if score % 50 == 0:
                color_index = (score // 50) % len(SNAKE_COLORS)
                snake_color = SNAKE_COLORS[color_index]
                pickup_color = PICKUP_COLORS[color_index]
        else:
            snake.pop()

        window.fill(COLORS['BLACK'])

        for segment in snake:
            draw_rect(segment, snake_color)
        draw_rect(pickup_position, pickup_color)

        text_surface = font.render(f'Points: {str(score)}', True, COLORS['GREEN'])
        window.blit(text_surface, (10, 10))

        if not (0 <= snake[0].x < width and 0 <= snake[0].y < height) or snake[0] in snake[1:]:
            end_game()
            reset_game()
            break

        pygame.display.flip()
        clock.tick(fps)

running = True
while running:
    select_difficulty()
    reset_game()
    game_loop()

pygame.quit()
