import pygame
import numpy as np
import math

# Konfigurasi Layar
WIDTH, HEIGHT = 800, 600
FPS = 60

class Engine3D:
    def __init__(self):
        # 1. SKALA & TITIK (Vertices Kubus)
        self.vertices = np.array([
            [-1, -1, 1, 1], [1, -1, 1, 1], [1, 1, 1, 1], [-1, 1, 1, 1],
            [-1, -1, -1, 1], [1, -1, -1, 1], [1, 1, -1, 1], [-1, 1, -1, 1]
        ])
        
        self.faces = [
            (0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4),
            (2, 3, 7, 6), (1, 2, 6, 5), (0, 3, 7, 4)
        ]
        
        # Variabel Transformasi
        self.angle_x = 0
        self.angle_y = 0
        self.pos_z = 6
        self.pos_x = 0
        self.show_reflection = False # Status Refleksi

    def get_projection_matrix(self):
        fov = 1 / math.tan(math.radians(60) / 2)
        return np.array([
            [fov * (HEIGHT/WIDTH), 0, 0, 0],
            [0, fov, 0, 0],
            [0, 0, 1, 1],
            [0, 0, 0, 0]
        ])

    def transform_and_draw(self, screen, matrix, color):
        projection = self.get_projection_matrix()
        full_matrix = matrix @ projection
        transformed = self.vertices @ full_matrix
        
        points_2d = []
        for v in transformed:
            w = v[3]
            if w > 0.1:
                x = (v[0] / w * WIDTH // 2) + WIDTH // 2
                y = (v[1] / w * HEIGHT // 2) + HEIGHT // 2
                points_2d.append((int(x), int(y)))
            else: points_2d.append(None)

        for face in self.faces:
            pts = [points_2d[i] for i in face if points_2d[i] is not None]
            if len(pts) == 4:
                pygame.draw.polygon(screen, color, pts, 2)

    def draw(self, screen):
        # 2. MATRIKS ROTASI & TRANSLASI UTAMA
        ax, ay = self.angle_x, self.angle_y
        rot_x = np.array([[1,0,0,0],[0,math.cos(ax),-math.sin(ax),0],[0,math.sin(ax),math.cos(ax),0],[0,0,0,1]])
        rot_y = np.array([[math.cos(ay),0,math.sin(ay),0],[0,1,0,0],[-math.sin(ay),0,math.cos(ay),0],[0,0,0,1]])
        
        translation = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[self.pos_x, 0, self.pos_z, 1]])
        
        main_matrix = rot_x @ rot_y @ translation
        
        # Gambar Objek Asli (Hijau)
        self.transform_and_draw(screen, main_matrix, (0, 255, 0))

        # 3. MATRIKS REFLEKSI (Terhadap Sumbu Y / Lantai)
        if self.show_reflection:
            # Matriks Refleksi: Membalikkan nilai Y (baris kedua, kolom kedua jadi -1)
            reflection_mat = np.array([
                [1,  0, 0, 0],
                [0, -1, 0, 0], # <--- Nilai Y dibalik
                [0,  0, 1, 0],
                [0,  0, 0, 1]
            ])
            
            # Geser refleksi sedikit ke bawah agar tidak tumpang tindih tepat di tengah
            reflect_translation = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0, 2.5, 0, 1]])
            
            # Gabungkan: Rotasi -> Refleksi -> Geser Bawah -> Posisi Dunia
            reflected_matrix = rot_x @ rot_y @ reflection_mat @ reflect_translation @ translation
            
            # Gambar Refleksi (Warna Abu-abu/Transparan)
            self.transform_and_draw(screen, reflected_matrix, (100, 100, 100))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    engine = Engine3D()

    print("KONTROL BARU:")
    print("- R : Toggle REFLEKSI (ON/OFF)")
    print("- W/S : Maju/Mundur | A/D : Kiri/Kanan")
    print("- Panah : Rotasi X & Y")

    while True:
        screen.fill((15, 15, 15))
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: # Tombol Refleksi
                    engine.show_reflection = not engine.show_reflection

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:  engine.angle_y -= 0.05
        if keys[pygame.K_RIGHT]: engine.angle_y += 0.05
        if keys[pygame.K_UP]:    engine.angle_x -= 0.05
        if keys[pygame.K_DOWN]:  engine.angle_x += 0.05
        if keys[pygame.K_w]:     engine.pos_z -= 0.1
        if keys[pygame.K_s]:     engine.pos_z += 0.1
        if keys[pygame.K_a]:     engine.pos_x -= 0.1
        if keys[pygame.K_d]:     engine.pos_x += 0.1

        # Gambar lantai sederhana sebagai referensi refleksi
        pygame.draw.line(screen, (50, 50, 50), (0, HEIGHT//2 + 50), (WIDTH, HEIGHT//2 + 50), 1)

        engine.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()