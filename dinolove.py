import pygame
import random

pygame.init()
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Runner — With Love!")

clock = pygame.time.Clock()
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
GREEN = (0, 200, 0)

font = pygame.font.SysFont(None, 36)
DINO_WIDTH, DINO_HEIGHT = 50, 50
GRAVITY = 1
JUMP_VEL = -18
OB_SPEED = 8

class Dino:
    def __init__(self):
        self.reset()
    def reset(self):
        self.x = 50
        self.y = HEIGHT - DINO_HEIGHT - 10
        self.vel_y = 0
        self.jump = False
        self.rect = pygame.Rect(self.x, self.y, DINO_WIDTH, DINO_HEIGHT)
    def update(self):
        if self.jump:
            self.vel_y = JUMP_VEL
            self.jump = False
        self.vel_y += GRAVITY
        self.y += self.vel_y
        if self.y >= HEIGHT - DINO_HEIGHT - 10:
            self.y = HEIGHT - DINO_HEIGHT - 10
            self.vel_y = 0
        self.rect.y = int(self.y)
    def draw(self):
        pygame.draw.rect(screen, BLACK, self.rect)

class Cactus:
    def __init__(self):
        self.x = WIDTH
        self.rect = pygame.Rect(self.x, HEIGHT - 50 - 10, 30, 50)
    def update(self):
        self.x -= OB_SPEED
        self.rect.x = int(self.x)
    def draw(self):
        pygame.draw.rect(screen, BLACK, self.rect)
    def off_screen(self):
        return self.x + 30 < 0

class Bird:
    def __init__(self):
        self.x = WIDTH
        self.y = random.choice([HEIGHT - 120, HEIGHT - 180, HEIGHT - 240])
        self.rect = pygame.Rect(self.x, self.y, 40, 30)
    def update(self):
        self.x -= OB_SPEED
        self.rect.x = int(self.x)
    def draw(self):
        pygame.draw.rect(screen, RED, self.rect)
    def off_screen(self):
        return self.x + 40 < 0

def show_love():
    screen.fill(WHITE)
    t1 = font.render("❤️ LOVE MOMENT! ❤️", True, RED)
    t2 = font.render("You met your love with a bouquet!", True, BLACK)
    screen.blit(t1, (180, 120))
    screen.blit(t2, (120, 160))
    pygame.display.update()
    pygame.time.delay(3000)

def draw_text(txt, x, y, col=BLACK):
    surf = font.render(txt, True, col)
    screen.blit(surf, (x, y))

def draw_button(txt, rect):
    pygame.draw.rect(screen, GREEN, rect)
    label = font.render(txt, True, BLACK)
    screen.blit(label, (rect.x + 10, rect.y + 5))

def run_game():
    dino = Dino()
    obstacles = []
    score = 0
    game_over = False
    love_shown = False

    next_spawn_time = pygame.time.get_ticks() + random.randint(1000, 2500)
    retry_button = pygame.Rect(WIDTH//2 - 75, HEIGHT//2, 150, 50)

    running = True
    while running:
        clock.tick(FPS)
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if not game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    dino.jump = True
            if game_over and event.type == pygame.MOUSEBUTTONDOWN:
                if retry_button.collidepoint(event.pos):
                    run_game()

        now = pygame.time.get_ticks()
        if not game_over and now >= next_spawn_time:
            if random.randint(0, 4) < 3:
                obstacles.append(Cactus())
            else:
                obstacles.append(Bird())
            next_spawn_time = now + random.randint(800, 2300)

        if not game_over:
            dino.update()
            dino.draw()

            for obs in list(obstacles):
                obs.update()
                obs.draw()
                if obs.off_screen():
                    obstacles.remove(obs)
                    score += 1
                if dino.rect.colliderect(obs.rect):
                    game_over = True

            draw_text(f"Score: {score}", 10, 10)

            if score >= 10 and not love_shown:  # Love at 10
                show_love()
                love_shown = True

        else:
            draw_text("GAME OVER!", WIDTH//2 - 80, HEIGHT//2 - 80, RED)
            draw_button("Try Again", retry_button)

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    run_game()

