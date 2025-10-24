import pygame
import sys

# ---------- Settings ----------
WIDTH, HEIGHT = 800, 600
BLOCK = 20 
BG_COLOR = (10, 10, 10) # for balck color 
SNAKE_COLOR = (0, 200, 0) # for snake green color 
FOOD_COLOR = (255, 0, 0) # for food red color 
FPS = 10 # for speed of snake 

# ---------- Init ----------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# ---------- Font ----------
pygame.font.init()
font = pygame.font.SysFont('Arial', 30)
game_over_font = pygame.font.SysFont('Arial', 50, bold=True)

#-----------sound-----------
pygame.mixer.init()
eat_sound = pygame.mixer.Sound("eat.mp3")    
game_over_sound = pygame.mixer.Sound("game over.mp3")
# bacground music 
pygame.mixer.music.load("funny.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(loops=-1)  # loop indefinitely

# ---------- Snake ----------
x = WIDTH // 2
y = HEIGHT // 2
snake = [[x, y], [x - BLOCK, y], [x - 2*BLOCK, y]]
direction = "RIGHT"

# ---------- Food ----------
import random
food = [random.randrange(0, WIDTH, BLOCK), random.randrange(0, HEIGHT, BLOCK)]

score = 0
game_over = False

# ---------- Main loop ----------
running = True
while running: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if game_over == False:
                # movement controls
                if event.key == pygame.K_UP and direction != "DOWN":
                    direction = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    direction = "DOWN"
                elif event.key == pygame.K_LEFT and direction != "RIGHT":
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    direction = "RIGHT"
            else:
                # Restart the game if Enter is pressed
                if event.key == pygame.K_RETURN:  # Enter key
                    game_over_sound.stop() # stop game over sound 

                    # Reset snake
                    x = WIDTH // 2
                    y = HEIGHT // 2
                    snake = [[x, y], [x - BLOCK, y], [x - 2*BLOCK, y]]
                    direction = "RIGHT"

                    # Reset food
                    food = [random.randrange(0, WIDTH, BLOCK), random.randrange(0, HEIGHT, BLOCK)]

                    # Reset score
                    score = 0

                    # Reset game over flag
                    game_over = False

                    # Restart background music
                    pygame.mixer.music.play(loops=-1)

    if not game_over:
        # Move snake
        head_x, head_y = snake[0]
        if direction == "UP":
            head_y -= BLOCK
        elif direction == "DOWN":
            head_y += BLOCK
        elif direction == "LEFT":
            head_x -= BLOCK
        elif direction == "RIGHT":
            head_x += BLOCK

        new_head = [head_x, head_y]
        snake.insert(0, new_head)

        # Check food
        if snake[0] == food:
            score += 1
            eat_sound.play()
            food = [random.randrange(0, WIDTH, BLOCK), random.randrange(0, HEIGHT, BLOCK)]
        else:
            snake.pop()

        # Check collisions
        if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT or snake[0] in snake[1:]:
            pygame.mixer.music.stop() # stop baground music 
            game_over_sound.play() # run game over music 
            game_over = True
            
    # Draw everything
    screen.fill(BG_COLOR)

    for block in snake:
        pygame.draw.rect(screen, SNAKE_COLOR, pygame.Rect(block[0], block[1], BLOCK, BLOCK))

    pygame.draw.rect(screen, FOOD_COLOR, pygame.Rect(food[0], food[1], BLOCK, BLOCK))

    # Draw score
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Draw game over message
    if game_over:
        go_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(go_text, (WIDTH//2 - go_text.get_width()//2, HEIGHT//2 - go_text.get_height()//2))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
