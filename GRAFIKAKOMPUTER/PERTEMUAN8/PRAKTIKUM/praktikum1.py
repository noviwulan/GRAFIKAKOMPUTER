import pygame
import math

pygame.init()

# =====================
# Setup Layar
# =====================
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Project Transformasi 3D - Sepeda Motor")

clock = pygame.time.Clock()

# =====================
# Load Aset Motor
# =====================
motor_img = pygame.image.load("motor2.png").convert_alpha()

# =====================
# Warna
# =====================
WHITE = (255,255,255)
BLACK = (0,0,0)

# =====================
# Variabel Transformasi 3D
# =====================
posX = WIDTH//2      # Translasi X
posY = HEIGHT//2     # Translasi Y
posZ = 0             # Translasi Z (untuk efek kedalaman)

angleZ = 0           # Rotasi
scale = 1.0          # Skala
reflect = 1          # Refleksi (1 normal, -1 mirror)

# =====================
# Main Loop
# =====================
running = True
while running:
    clock.tick(60)
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # =====================
    # TRANSLASI 3D
    # =====================

    # Kiri / Kanan (Sumbu X)
    if keys[pygame.K_LEFT]:
        posX -= 5
    if keys[pygame.K_RIGHT]:
        posX += 5

    # Atas / Bawah (Sumbu Y)
    if keys[pygame.K_UP]:
        posY -= 5
    if keys[pygame.K_DOWN]:
        posY += 5

    # Maju / Mundur (Sumbu Z → kedalaman / samping 3D)
    if keys[pygame.K_PAGEUP]:
        posZ += 10     # maju (motor makin besar)
    if keys[pygame.K_PAGEDOWN]:
        posZ -= 10     # mundur (motor makin kecil)


    # =====================
    # ROTASI 3D (sumbu Z)
    # =====================
    if keys[pygame.K_a]: angleZ += 3
    if keys[pygame.K_d]: angleZ -= 3

    # =====================
    # SKALA 3D
    # =====================
    if keys[pygame.K_w]: scale += 0.02
    if keys[pygame.K_s]: scale -= 0.02
    if scale < 0.2:
        scale = 0.2

    # =====================
    # REFLEKSI 3D
    # =====================
    if keys[pygame.K_r]: reflect = -1
    if keys[pygame.K_t]: reflect = 1

    # =====================
    # PROYEKSI SEDERHANA 3D → 2D
    # =====================
    # Efek kedalaman dari posZ
    depth = 500
    factor = depth / (depth + posZ)

    # Ukuran hasil skala + perspektif
    new_width = int(motor_img.get_width() * scale * factor)
    new_height = int(motor_img.get_height() * scale * factor)

    motor_scaled = pygame.transform.scale(motor_img, (new_width, new_height))

    # Rotasi
    motor_rotated = pygame.transform.rotate(motor_scaled, angleZ)

    # Refleksi
    if reflect == -1:
        motor_rotated = pygame.transform.flip(motor_rotated, True, False)

    # Posisi akhir di layar
    rect = motor_rotated.get_rect(center=(posX, posY))

    # Gambar ke layar
    screen.blit(motor_rotated, rect)

    # =====================
    # Info Kontrol di Layar
    # =====================
    font = pygame.font.SysFont("arial", 16)
    info = [
        "Arrow : Translasi X,Y",
        "O / P : Translasi Z (maju/mundur)",
        "A / D : Rotasi",
        "W / S : Skala",
        "R / T : Refleksi ON/OFF",
        "ESC : Quit"
    ]

    for i, text in enumerate(info):
        img = font.render(text, True, WHITE)
        screen.blit(img, (10, 10 + i*20))

    pygame.display.flip()

pygame.quit()
