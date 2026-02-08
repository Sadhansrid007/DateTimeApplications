import pygame
import random

pygame.init()

# Screen setup
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird with Restart")

clock = pygame.time.Clock()
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (200, 0, 0)
GREEN = (0, 200, 0)

# Bird settings
BIRD_WIDTH, BIRD_HEIGHT = 34, 24
GRAVITY = 0.5
FLAP_STRENGTH = -10

# Pipe settings
PIPE_WIDTH = 70
PIPE_GAP = 150
PIPE_SPEED = 3

font = pygame.font.SysFont("Arial", 32)

class Bird:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = 50
        self.y = HEIGHT // 2
        self.vel = 0
        self.rect = pygame.Rect(self.x, self.y, BIRD_WIDTH, BIRD_HEIGHT)

    def update(self):
        self.vel += GRAVITY
        self.y += self.vel
        self.rect.y = int(self.y)

    def flap(self):
        self.vel = FLAP_STRENGTH

    def draw(self):
        pygame.draw.rect(screen, BLACK, self.rect)

class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(100, HEIGHT - PIPE_GAP - 100)
        self.top_rect = pygame.Rect(self.x, 0, PIPE_WIDTH, self.height)
        self.bottom_rect = pygame.Rect(self.x, self.height + PIPE_GAP, PIPE_WIDTH, HEIGHT - (self.height + PIPE_GAP))

    def update(self):
        self.x -= PIPE_SPEED
        self.top_rect.x = int(self.x)
        self.bottom_rect.x = int(self.x)

    def draw(self):
        pygame.draw.rect(screen, BLACK, self.top_rect)
        pygame.draw.rect(screen, BLACK, self.bottom_rect)

    def off_screen(self):
        return self.x + PIPE_WIDTH < 0


def draw_text(text, x, y, color=BLACK):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def draw_button(text, rect):
    pygame.draw.rect(screen, GREEN, rect)
    txt = font.render(text, True, BLACK)
    screen.blit(txt, (rect.x + 10, rect.y + 5))


def run_game():
    bird = Bird()
    pipes = []
    spawn_timer = 0
    score = 0
    game_over = False

    # Button for retry
    button_rect = pygame.Rect(WIDTH//2 - 75, HEIGHT//2, 150, 50)

    running = True
    while running:
        clock.tick(FPS)
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if not game_over:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    bird.flap()
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_rect.collidepoint(event.pos):
                        run_game()  # restart game

        # Update & draw game when not over
        if not game_over:
            bird.update()
            bird.draw()

            spawn_timer += 1
            if spawn_timer > 90:
                pipes.append(Pipe(WIDTH))
                spawn_timer = 0

            for pipe in list(pipes):
                pipe.update()
                pipe.draw()
                if pipe.off_screen():
                    pipes.remove(pipe)
                    score += 1
                if bird.rect.colliderect(pipe.top_rect) or bird.rect.colliderect(pipe.bottom_rect):
                    game_over = True

            # boundary collision
            if bird.y < 0 or bird.y + BIRD_HEIGHT >= HEIGHT:
                game_over = True

            draw_text(f"Score: {score}", 10, 10)

        else:
            draw_text("GAME OVER", WIDTH//2 - 90, HEIGHT//2 - 80, RED)
            draw_button("Try Again", button_rect)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    run_game()

