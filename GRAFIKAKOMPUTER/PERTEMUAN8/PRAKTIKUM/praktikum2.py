import pygame
import math

pygame.init()

# =====================
# SETUP LAYAR
# =====================
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GAME 3D - MOTOR KEREN")

clock = pygame.time.Clock()

# =====================
# LOAD GAMBAR MOTOR (ASET LUAR)
# =====================
motor_img = pygame.image.load("motor2.png").convert_alpha()

# =====================
# WARNA
# =====================
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# =====================
# BIDANG 3D TEMPAT GAMBAR MOTOR
# =====================
plane = [
    [-2, -1, 0],
    [ 2, -1, 0],
    [ 2,  1, 0],
    [-2,  1, 0]
]

# =====================
# VARIABEL TRANSFORMASI
# =====================
posX, posY, posZ = 0, 0, 6
rotX, rotY, rotZ = 0, 0, 0
scale = 1.5
reflect = 1   # 1 = normal, -1 = refleksi

# =====================
# FUNGSI ROTASI 3D
# =====================
def rotateX(p,a):
    x,y,z = p
    r = math.radians(a)
    y2 = y*math.cos(r) - z*math.sin(r)
    z2 = y*math.sin(r) + z*math.cos(r)
    return [x,y2,z2]

def rotateY(p,a):
    x,y,z = p
    r = math.radians(a)
    x2 = x*math.cos(r) + z*math.sin(r)
    z2 = -x*math.sin(r) + z*math.cos(r)
    return [x2,y,z2]

def rotateZ(p,a):
    x,y,z = p
    r = math.radians(a)
    x2 = x*math.cos(r) - y*math.sin(r)
    y2 = x*math.sin(r) + y*math.cos(r)
    return [x2,y2,z]

# =====================
# PROYEKSI 3D → 2D
# =====================
def project(p):
    x,y,z = p
    z += posZ
    fov = 400
    factor = fov / (fov + z)
    sx = int(x * factor * 120 + WIDTH/2)
    sy = int(-y * factor * 120 + HEIGHT/2)
    return (sx, sy)

# =====================
# MAIN LOOP GAME
# =====================
running = True
while running:
    clock.tick(60)
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # === TRANSLASI ===
    if keys[pygame.K_LEFT]: posX -= 0.1
    if keys[pygame.K_RIGHT]: posX += 0.1
    if keys[pygame.K_UP]: posY += 0.1
    if keys[pygame.K_DOWN]: posY -= 0.1
    if keys[pygame.K_PAGEUP]: posZ -= 0.1
    if keys[pygame.K_PAGEDOWN]: posZ += 0.1

    # === ROTASI ===
    if keys[pygame.K_w]: rotX += 2
    if keys[pygame.K_s]: rotX -= 2
    if keys[pygame.K_a]: rotY += 2
    if keys[pygame.K_d]: rotY -= 2
    if keys[pygame.K_q]: rotZ += 2
    if keys[pygame.K_e]: rotZ -= 2

    # === SKALA ===
    if keys[pygame.K_z]: scale += 0.05
    if keys[pygame.K_x]: scale -= 0.05
    if scale < 0.5: scale = 0.5

    # === REFLEKSI ===
    if keys[pygame.K_r]: reflect = -1
    if keys[pygame.K_t]: reflect = 1

    # =====================
    # HITUNG TRANSFORMASI
    # =====================
    projected = []
    for p in plane:
        p2 = [p[0]*scale, p[1]*scale, p[2]*scale]

        # refleksi sumbu X
        p2[0] *= reflect

        # rotasi
        p2 = rotateX(p2, rotX)
        p2 = rotateY(p2, rotY)
        p2 = rotateZ(p2, rotZ)

        # translasi
        p2[0] += posX
        p2[1] += posY

        # proyeksi layar
        projected.append(project(p2))

    # =====================
    # GAMBAR MOTOR
    # =====================
    xs = [p[0] for p in projected]
    ys = [p[1] for p in projected]

    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    w = max_x - min_x
    h = max_y - min_y

    if w > 20 and h > 20:
        motor_scaled = pygame.transform.scale(motor_img, (w, h))

        # refleksi gambar 2D agar terlihat nyata
        if reflect == -1:
            motor_scaled = pygame.transform.flip(motor_scaled, True, False)

        screen.blit(motor_scaled, (min_x, min_y))

    # =====================
    # INFO KONTROL
    # =====================
    font = pygame.font.SysFont("arial", 16)
    info = [
        "PANAH : Translasi X,Y",
        "PageUp/PageDown : Translasi Z",
        "W/S : Rotasi X",
        "A/D : Rotasi Y",
        "Q/E : Rotasi Z",
        "Z/X : Skala",
        "R : Refleksi",
        "T : Normal"
    ]

    for i, t in enumerate(info):
        screen.blit(font.render(t, True, WHITE), (10, 10 + i*20))

    pygame.display.flip()

pygame.quit()
