import pygame
import numpy as np
import math

# Konfigurasi Layar
WIDTH, HEIGHT = 800, 600
FPS = 60

class UltraPlane3D:
    def __init__(self):
        # 1. VERTICES (Titik-titik detail: Total 34 Titik)
        self.base_vertices = [
            [0, 0, 3.5, 1],    # 0: Ujung Hidung (Propeller Hub)
            # Ring Kokpit (Titik 1-4)
            [0.3, 0.5, 2, 1], [0.3, -0.3, 2, 1], [-0.3, -0.3, 2, 1], [-0.3, 0.5, 2, 1],
            # Ring Badan Depan (Titik 5-8)
            [0.7, 0.7, 0.5, 1], [0.7, -0.7, 0.5, 1], [-0.7, -0.7, 0.5, 1], [-0.7, 0.7, 0.5, 1],
            # Ring Badan Belakang (Titik 9-12)
            [0.4, 0.4, -2.5, 1], [0.4, -0.4, -2.5, 1], [-0.4, -0.4, -2.5, 1], [-0.4, 0.4, -2.5, 1],
            [0, 0, -4, 1],     # 13: Ujung Ekor Belakang
            # Sayap (Wing Nodes)
            [5, 0, 0.8, 1], [5, 0, -0.5, 1],    # 14, 15: Kanan
            [-5, 0, 0.8, 1], [-5, 0, -0.5, 1],  # 16, 17: Kiri
            # Ekor (Stabilizer)
            [1.8, 0, -3.2, 1], [-1.8, 0, -3.2, 1], # 18, 19
            [0, -1.8, -3.8, 1], # 20: Fin Atas
            # Baling-baling (Propeller Animasi)
            [0, 1.8, 3.5, 1], [0, -1.8, 3.5, 1], # 21, 22
            # Roda Pendaratan (Landing Gear)
            [0.5, 1.2, 1, 1], [-0.5, 1.2, 1, 1], # 23, 24: Roda Depan Kiri/Kanan
            [0, 1, -2, 1]      # 25: Roda Belakang
        ]
        self.vertices = np.array(self.base_vertices)
        
        # 2. EDGES (Koneksi Rangka Detail)
        self.edges = [
            (0,1), (0,2), (0,3), (0,4), # Hidung ke Kokpit
            (1,5), (2,6), (3,7), (4,8), (1,2), (2,3), (3,4), (4,1), # Ring 1 ke 2
            (5,9), (6,10), (7,11), (8,12), (5,6), (6,7), (7,8), (8,5), # Ring 2 ke 3
            (9,13), (10,13), (11,13), (12,13), (9,10), (10,11), (11,12), (12,9), # Ring 3 ke Ekor
            (5,14), (6,14), (14,15), (5,15), # Sayap Kanan
            (8,16), (7,16), (16,17), (8,17), # Sayap Kiri
            (13,18), (9,18), (13,19), (12,19), (13,20), (9,20), # Ekor & Fin
            (0,21), (0,22), # Baling-baling
            (5,23), (8,24), (10,25), (11,25) # Roda Pendaratan
        ]
        
        # Parameter Transformasi
        self.angle_x = self.angle_y = self.angle_z = 0
        self.pos_z = 12
        self.pos_x = 0
        self.prop_rot = 0
        self.show_reflection = False

    def get_matrices(self):
        # --- TRANSFORMASI 3D: ROTASI ---
        ax, ay, az = self.angle_x, self.angle_y, self.angle_z
        rx = np.array([[1,0,0,0],[0,math.cos(ax),-math.sin(ax),0],[0,math.sin(ax),math.cos(ax),0],[0,0,0,1]])
        ry = np.array([[math.cos(ay),0,math.sin(ay),0],[0,1,0,0],[-math.sin(ay),0,math.cos(ay),0],[0,0,0,1]])
        rz = np.array([[math.cos(az),-math.sin(az),0,0],[math.sin(az),math.cos(az),0,0],[0,0,1,0],[0,0,0,1]])
        
        # --- TRANSFORMASI 3D: TRANSLASI ---
        tr = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[self.pos_x, 0, self.pos_z, 1]])
        
        return rx @ ry @ rz @ tr

    def draw(self, screen):
        # Animasi Baling-baling (Update Vertices 21 & 22)
        self.prop_rot += 0.8
        s, c = math.sin(self.prop_rot), math.cos(self.prop_rot)
        self.vertices[21][:2] = [s * 2, c * 2]
        self.vertices[22][:2] = [-s * 2, -c * 2]

        main_matrix = self.get_matrices()
        
        # Render Pesawat Utama
        self.render_mesh(screen, main_matrix, (0, 255, 150))

        # --- TRANSFORMASI 3D: REFLEKSI ---
        if self.show_reflection:
            # Matriks Refleksi terhadap sumbu Y
            reflect_mat = np.array([[1,0,0,0],[0,-1,0,0],[0,0,1,0],[0,0,0,1]])
            # Geser refleksi ke bawah lantai (Translasi Y)
            floor_offset = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0, 6, 0, 1]])
            
            reflected_matrix = main_matrix @ reflect_mat @ floor_offset
            self.render_mesh(screen, reflected_matrix, (60, 60, 90))

    def render_mesh(self, screen, matrix, color):
        # --- TRANSFORMASI 3D: SKALA (Via Proyeksi Perspektif) ---
        fov = 1 / math.tan(math.radians(60) / 2)
        proj = np.array([[fov*(HEIGHT/WIDTH),0,0,0],[0,fov,0,0],[0,0,1,1],[0,0,0,0]])
        
        full_mat = matrix @ proj
        transformed = self.vertices @ full_mat
        
        pts = []
        for v in transformed:
            if v[3] > 0.1:
                # Proyeksi ke layar 2D
                x = int((v[0]/v[3] * WIDTH/2) + WIDTH/2)
                y = int((v[1]/v[3] * HEIGHT/2) + HEIGHT/2)
                pts.append((x, y))
            else: pts.append(None)

        for e in self.edges:
            if pts[e[0]] and pts[e[1]]:
                pygame.draw.line(screen, color, pts[e[0]], pts[e[1]], 2)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    plane = UltraPlane3D()

    while True:
        screen.fill((5, 5, 10))
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                plane.show_reflection = not plane.show_reflection

        keys = pygame.key.get_pressed()
        # Kontrol Rotasi (Panah)
        if keys[pygame.K_LEFT]:  plane.angle_y -= 0.05
        if keys[pygame.K_RIGHT]: plane.angle_y += 0.05
        if keys[pygame.K_UP]:    plane.angle_x -= 0.05
        if keys[pygame.K_DOWN]:  plane.angle_x += 0.05
        # Kontrol Translasi (W/S/A/D)
        if keys[pygame.K_w]: plane.pos_z -= 0.15
        if keys[pygame.K_s]: plane.pos_z += 0.15
        if keys[pygame.K_a]: plane.pos_x -= 0.15
        if keys[pygame.K_d]: plane.pos_x += 0.15

        # Garis bantu lantai
        pygame.draw.line(screen, (30, 30, 50), (0, HEIGHT//2 + 150), (WIDTH, HEIGHT//2 + 150), 1)

        plane.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()