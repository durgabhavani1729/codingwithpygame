import pygame
import random
import sys

# Initialize
pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Debugger Game with Music")

# 🎵 Music setup
try:
    pygame.mixer.music.load("music.mp3")  # background music file
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.5)
except:
    print("⚠ Background music not found!")

try:
    shoot_sound = pygame.mixer.Sound("laser.wav")  # shooting sound
except:
    shoot_sound = None
    print("⚠ Shooting sound not found!")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (255, 0, 0)

# Fonts
font = pygame.font.SysFont(None, 40)

# Player setup
player_x, player_y = WIDTH // 2, HEIGHT - 50
player_speed = 7

# Bullet setup
bullet = None
bullet_speed = -10

# Falling codes setup
codes = ["pritn('Hi')", "print('Hi')", "2++2",
         "prit()", "print(5)", "if True print('ok')", "if True: print('ok')"]
falling = []
fall_speed = 3

# Score and game state
score = 0
game_over = False

clock = pygame.time.Clock()

def draw_text(text, x, y, color=BLACK):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not game_over:
        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - 50:
            player_x += player_speed
        if keys[pygame.K_SPACE] and bullet is None:
            bullet = [player_x + 22, player_y]
            if shoot_sound:
                shoot_sound.play()

        # Bullet movement
        if bullet:
            bullet[1] += bullet_speed
            if bullet[1] < 0:
                bullet = None

        # Spawn new code
        if random.randint(1, 40) == 1:
            text = random.choice(codes)
            is_bug = "pritn" in text or "++" in text or "prit()" in text or "if True print" in text
            falling.append([random.randint(50, WIDTH - 150), 0, text, is_bug])  # added is_bug flag

        # Move falling codes
        for item in falling[:]:
            item[1] += fall_speed

            # Only bug reaching bottom ends game
            if item[3] and item[1] + 40 >= HEIGHT:
                game_over = True

            # Bullet collision
            if bullet:
                bug_rect = pygame.Rect(item[0], item[1], 120, 40)
                bullet_rect = pygame.Rect(bullet[0], bullet[1], 5, 10)
                if bug_rect.colliderect(bullet_rect):
                    if item[3]:  # it is a bug
                        score += 10
                    else:        # correct code
                        score -= 5
                    falling.remove(item)
                    bullet = None
                    break

        # Remove off-screen codes
        falling = [item for item in falling if item[1] < HEIGHT]

    # Drawing
    screen.fill((200, 255, 200))  # background
    pygame.draw.rect(screen, GREEN, (player_x, player_y, 50, 30))  # player box

    # Draw bullet
    if bullet:
        pygame.draw.rect(screen, RED, (bullet[0], bullet[1], 5, 10))

    # Draw falling codes
    for item in falling:
        draw_text(item[2], item[0], item[1])

    # Draw score
    draw_text(f"Score: {score}", 10, 10)

    # Game over display
    if game_over:
        draw_text("GAME OVER", WIDTH // 2 - 100, HEIGHT // 2 - 20, RED)
        draw_text(f"Final Score: {score}", WIDTH // 2 - 100, HEIGHT // 2 + 20, RED)

    pygame.display.flip()
    clock.tick(60)
