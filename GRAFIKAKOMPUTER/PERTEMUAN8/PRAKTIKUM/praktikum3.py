import pygame
import numpy as np
import math

# Konfigurasi Layar
WIDTH, HEIGHT = 800, 600
FPS = 60

class Object3D:
    def __init__(self):
        # 1. SKALA & TITIK (Vertices) - Menentukan bentuk objek
        # Homogeneous coordinates (x, y, z, 1)
        self.vertices = np.array([
            [-1, -1, 1, 1], [1, -1, 1, 1], [1, 1, 1, 1], [-1, 1, 1, 1],
            [-1, -1, -1, 1], [1, -1, -1, 1], [1, 1, -1, 1], [-1, 1, -1, 1]
        ])
        
        # Menghubungkan titik menjadi sisi (Faces)
        self.faces = [
            (0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4),
            (2, 3, 7, 6), (1, 2, 6, 5), (0, 3, 7, 4)
        ]
        self.angle = 0

    def draw(self, screen):
        # 2. MATRIKS ROTASI (X, Y, Z) - Sesuai menit [00:02:34]
        a = self.angle
        rotation_x = np.array([[1, 0, 0, 0], [0, math.cos(a), -math.sin(a), 0], [0, math.sin(a), math.cos(a), 0], [0, 0, 0, 1]])
        rotation_y = np.array([[math.cos(a), 0, math.sin(a), 0], [0, 1, 0, 0], [-math.sin(a), 0, math.cos(a), 0], [0, 0, 0, 1]])
        rotation_z = np.array([[math.cos(a), -math.sin(a), 0, 0], [math.sin(a), math.cos(a), 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])

        # 3. MATRIKS TRANSLASI - Memindahkan objek ke tengah layar [00:02:16]
        translation = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 4, 1]]) # Z=4 agar menjauh dari kamera

        # Gabungkan Transformasi
        matrix = rotation_x @ rotation_y @ rotation_z @ translation

        # 4. MATRIKS PROYEKSI - Mengubah 3D ke 2D Layar [00:06:30]
        fobe = 1 / math.tan(math.radians(45) / 2)
        projection = np.array([
            [fobe * (HEIGHT/WIDTH), 0, 0, 0],
            [0, fobe, 0, 0],
            [0, 0, 1, 1],
            [0, 0, 0, 0]
        ])

        # Hitung posisi titik akhir
        transformed_vertices = self.vertices @ matrix @ projection
        
        # Normalisasi (Divide by W) - Sesuai menit [00:07:20]
        points_2d = []
        for v in transformed_vertices:
            if v[3] != 0:
                x = (v[0] / v[3] * WIDTH // 2) + WIDTH // 2
                y = (v[1] / v[3] * HEIGHT // 2) + HEIGHT // 2
                points_2d.append((int(x), int(y)))

        # Gambar Sisi-Sisi Objek
        for face in self.faces:
            polygon = [points_2d[i] for i in face]
            pygame.draw.polygon(screen, (255, 0, 0), polygon, 2)
        
        self.angle += 0.02

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    cube = Object3D()

    while True:
        screen.fill((20, 20, 20))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        cube.draw(screen)
        
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()