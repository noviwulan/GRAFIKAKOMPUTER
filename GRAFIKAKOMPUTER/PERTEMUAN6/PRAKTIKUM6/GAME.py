import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Petani Menjaga Kebun Pisang - Transformasi 2D")

clock = pygame.time.Clock()

# COLORS
GREEN = (80, 200, 120)
LIGHT_GREEN = (120, 240, 150)
BROWN = (150, 75, 0)
BLUE = (140, 180, 255)
BLACK = (0,0,0)
WHITE = (255,255,255)

# SCALE FACTOR
scale_factor = 1.0

# MIRROR MODE
mirror_world = False

# GAME OVER FLAG
game_over = False

# =======================================================================
# DRAW FUNCTIONS
# =======================================================================

def draw_background(surface):
    surface.fill(BLUE)
    pygame.draw.rect(surface, GREEN, (0, 350, WIDTH, 200))

    for x in [100, 300, 500, 700]:
        pygame.draw.rect(surface, BROWN, (x-10, 250, 20, 120))
        pygame.draw.ellipse(surface, LIGHT_GREEN, (x-40, 190, 80, 80))
        pygame.draw.ellipse(surface, LIGHT_GREEN, (x-50, 230, 100, 60))


def draw_farmer(surface, x, y, attacking, arm_angle, scale):
    farmer = pygame.Surface((200, 200), pygame.SRCALPHA)

    # Kepala
    pygame.draw.circle(farmer, (255, 220, 180), (100, 50), 20)

    # Badan
    pygame.draw.rect(farmer, (200, 100, 50), (85, 70, 30, 60))

    # Kaki
    pygame.draw.rect(farmer, (80, 40, 0), (85, 130, 10, 40))
    pygame.draw.rect(farmer, (80, 40, 0), (105, 130, 10, 40))

    # Lengan + Cangkul
    arm = pygame.Surface((80, 20), pygame.SRCALPHA)
    pygame.draw.rect(arm, (255,220,180), (0, 5, 50, 10))
    pygame.draw.rect(arm, (120,120,120), (45,0,30,10))
    pygame.draw.rect(arm, BLACK, (70,-5,20,20))

    rotated_arm = pygame.transform.rotate(arm, arm_angle if attacking else 0)
    farmer.blit(rotated_arm, (100, 60))

    # SCALE
    if scale != 1.0:
        farmer = pygame.transform.scale(farmer, (int(200*scale), int(200*scale)))

    surface.blit(farmer, (x - 100, y - 80))


def draw_monkey(surface, mx, my, is_tall):
    color_body = (150, 80, 30)

    if is_tall:
        # MONYET TINGGI
        pygame.draw.circle(surface, color_body, (mx, my - 40), 18)
        pygame.draw.rect(surface, color_body, (mx-12, my-25, 24, 50))
        pygame.draw.rect(surface, color_body, (mx-18, my, 36, 10))
    else:
        # MONYET RENDAH
        pygame.draw.circle(surface, color_body, (mx, my - 10), 15)
        pygame.draw.rect(surface, color_body, (mx-10, my, 20, 25))


# =======================================================================
# GAME VARIABLES
# =======================================================================

farmer_x = 100
farmer_y = 260
attacking = False
arm_angle = -30

monkeys = []  # [x, y, is_tall]
spawn_time = 0
score = 0


# =======================================================================
# MAIN LOOP
# =======================================================================
running = True
while running:
    clock.tick(60)

    if game_over:
        screen.fill(BLACK)
        font = pygame.font.SysFont("Arial", 60)
        text = font.render("GAME OVER", True, WHITE)
        screen.blit(text, (WIDTH//2 - 150, HEIGHT//2 - 30))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        continue

    # ---------------------------------------------------------
    # EVENT
    # ---------------------------------------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Dash
    if keys[pygame.K_d]:
        farmer_x += 20

    # Move
    if keys[pygame.K_LEFT]:
        farmer_x -= 5
    if keys[pygame.K_RIGHT]:
        farmer_x += 5

    # Attack
    attacking = keys[pygame.K_SPACE]

    # Mirror
    if keys[pygame.K_m]:
        mirror_world = True
    if keys[pygame.K_n]:
        mirror_world = False

    # ===================================================
    # S → SCALING HANYA JIKA ADA MONYET TINGGI
    # ===================================================
    if keys[pygame.K_s]:
        monkey_higher = any(m[2] == True for m in monkeys)
        scale_factor = 1.5 if monkey_higher else 1.0
    else:
        scale_factor = 1.0

    farmer_x = max(50, min(farmer_x, WIDTH - 50))

    # Spawn monyet
    spawn_time += 1
    if spawn_time > 70:
        spawn_time = 0

        is_tall = random.choice([True, False])

        if is_tall:
            monkeys.append([WIDTH + 40, 260, True])   # tinggi
        else:
            monkeys.append([WIDTH + 40, 330, False])  # rendah

    # Gerak monyet
    for m in monkeys[:]:
        m[0] -= 4

        # HIT detection
        if attacking:
            dist = math.hypot(farmer_x - m[0], farmer_y - m[1])
            if dist < 60:
                monkeys.remove(m)
                score += 1

        # ❌ MONYET LOLOS → GAME OVER
        if m[0] < -10:
            game_over = True

    # RENDER
    scene = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    draw_background(scene)
    draw_farmer(scene, farmer_x, farmer_y, attacking, arm_angle, scale_factor)

    for m in monkeys:
        draw_monkey(scene, m[0], m[1], m[2])

    if mirror_world:
        scene = pygame.transform.flip(scene, True, False)

    screen.blit(scene, (0, 0))

    font = pygame.font.SysFont("Comic Sans MS", 30)
    screen.blit(font.render(f"Skor: {score}", True, WHITE), (10, 10))

    pygame.display.update()

pygame.quit()
