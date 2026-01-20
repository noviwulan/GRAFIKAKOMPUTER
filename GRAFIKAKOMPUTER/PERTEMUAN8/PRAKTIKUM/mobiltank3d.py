import pygame
import numpy as np
import math

# Konfigurasi Layar
WIDTH, HEIGHT = 800, 600
FPS = 60

class UltraExtremeTank3D:
    def __init__(self):
        self.base_vertices = []
        self.edges = []
        
        # --- DEFINISI WARNA EMAS ---
        self.GOLD_COLOR = (255, 215, 0)      # Emas Terang
        self.GOLD_SHADOW = (100, 85, 0)     # Emas Gelap untuk refleksi
        
        # --- 1. BODY/HULL ULTRA DETAIL (Subdivisi Ganda) ---
        hull_idx = len(self.base_vertices)
        z_segments = 10 
        for i in range(z_segments + 1):
            z = 2.5 - (i * 5.0 / z_segments)
            self.base_vertices.extend([
                [1.5, 0.5, z, 1], [1.5, -0.5, z, 1], 
                [-1.5, -0.5, z, 1], [-1.5, 0.5, z, 1]
            ])
            ring_start = hull_idx + i * 4
            for j in range(4):
                self.edges.append((ring_start + j, ring_start + (j + 1) % 4))
            
            if i > 0:
                prev = ring_start - 4
                for j in range(4):
                    self.edges.extend([
                        (prev + j, ring_start + j),           
                        (prev + j, ring_start + (j + 1) % 4), 
                        (prev + (j + 1) % 4, ring_start + j)  
                    ])

        # --- 2. EXTREME TRACKS (RODA RANTAI) ---
        for side in [1.9, -1.9]: 
            track_start = len(self.base_vertices)
            t_segments = 15 
            for i in range(t_segments + 1):
                z = 2.8 - (i * 5.6 / t_segments)
                self.base_vertices.extend([[side, 0.6, z, 1], [side, -0.3, z, 1]])
                if i > 0:
                    curr = track_start + i * 2
                    prev = curr - 2
                    self.edges.extend([(prev, curr), (prev+1, curr+1), (prev, curr+1), (prev+1, curr)])

        # --- 3. KUBAH GEODESIC (TURRET) ---
        turret_idx = len(self.base_vertices)
        t_segments = 18 
        for h, r in [(-0.5, 1.0), (-0.8, 1.2), (-1.2, 0.9), (-1.5, 0.4)]:
            start_ring = len(self.base_vertices)
            for i in range(t_segments):
                a = 2 * math.pi * i / t_segments
                self.base_vertices.append([math.cos(a)*r, h, math.sin(a)*r, 1])
            if start_ring > turret_idx:
                p_ring = start_ring - t_segments
                for i in range(t_segments):
                    n = (i + 1) % t_segments
                    self.edges.extend([(start_ring+i, start_ring+n), (start_ring+i, p_ring+i), (start_ring+i, p_ring+n)])

        # --- 4. CANNON (LARAS MERIAM) ---
        cannon_idx = len(self.base_vertices)
        for i in range(8):
            a = 2 * math.pi * i / 8
            self.base_vertices.extend([[math.cos(a)*0.15, -1.0, 1.0 + math.sin(a)*0.15, 1],
                                      [math.cos(a)*0.15, -1.0, 5.0 + math.sin(a)*0.15, 1]])
            curr = cannon_idx + i * 2
            nxt = cannon_idx + ((i+1)%8) * 2
            self.edges.extend([(curr, curr+1), (curr, nxt), (curr+1, nxt+1)])

        self.vertices = np.array(self.base_vertices)
        self.angle_x = self.angle_y = 0
        self.pos_z = 15
        self.pos_x = 0 
        self.show_reflection = False

    def draw(self, screen):
        ax, ay = self.angle_x, self.angle_y
        rx = np.array([[1,0,0,0],[0,math.cos(ax),-math.sin(ax),0],[0,math.sin(ax),math.cos(ax),0],[0,0,0,1]])
        ry = np.array([[math.cos(ay),0,math.sin(ay),0],[0,1,0,0],[-math.sin(ay),0,math.cos(ay),0],[0,0,0,1]])
        tr = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[self.pos_x, 0, self.pos_z, 1]])
        
        main_mat = rx @ ry @ tr
        
        # MENGGUNAKAN WARNA EMAS (GOLD)
        self.render(screen, main_mat, self.GOLD_COLOR)
        
        if self.show_reflection:
            refl = np.array([[1,0,0,0],[0,-1,0,0],[0,0,1,0],[0, 4, 0, 1]])
            # MENGGUNAKAN WARNA EMAS GELAP UNTUK BAYANGAN
            self.render(screen, main_mat @ refl, self.GOLD_SHADOW)

    def render(self, screen, matrix, color):
        fov = 1 / math.tan(math.radians(60) / 2)
        proj = np.array([[fov*(HEIGHT/WIDTH),0,0,0],[0,fov,0,0],[0,0,1,1],[0,0,0,0]])
        trans = self.vertices @ matrix @ proj
        pts = []
        for v in trans:
            if v[3] > 0.1:
                pts.append((int((v[0]/v[3]*WIDTH/2)+WIDTH/2), int((v[1]/v[3]*HEIGHT/2)+HEIGHT/2)))
            else: pts.append(None)
        for e in self.edges:
            if pts[e[0]] and pts[e[1]]:
                pygame.draw.line(screen, color, pts[e[0]], pts[e[1]], 1)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Golden Ultra Extreme Tank 3D")
    clock = pygame.time.Clock()
    tank = UltraExtremeTank3D()
    while True:
        # Background dibuat agak abu-abu sangat gelap agar warna gold menyala
        screen.fill((15, 15, 15))
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r: tank.show_reflection = not tank.show_reflection
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:  tank.angle_y -= 0.04
        if keys[pygame.K_RIGHT]: tank.angle_y += 0.04
        if keys[pygame.K_UP]:    tank.angle_x -= 0.04
        if keys[pygame.K_DOWN]:  tank.angle_x += 0.04
        
        if keys[pygame.K_w]: tank.pos_z -= 0.15 
        if keys[pygame.K_s]: tank.pos_z += 0.15 
        if keys[pygame.K_a]: tank.pos_x -= 0.15 
        if keys[pygame.K_d]: tank.pos_x += 0.15 
        
        tank.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()