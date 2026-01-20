import pygame
import numpy as np
import math

# --- KONFIGURASI LAYAR ---
WIDTH, HEIGHT = 1000, 750
FPS = 60

class UltraTankFinal:
    def __init__(self):
        self.vertices = []
        self.faces = []
        self.GOLD_SOLID = (130, 100, 30)
        self.GOLD_WIRE = (255, 220, 100)
        
        # 1. GEOMETRI DETAIL (Vertex, Edge, Polygon)
        # Hull Utama (Bodi)
        self.add_box(0, 0, 0, 3.8, 0.7, 6.5)
        # Side Skirts berlapis (Pelindung Roda)
        self.add_box(2.3, -0.2, 0, 0.6, 0.8, 6.8)
        self.add_box(-2.3, -0.2, 0, 0.6, 0.8, 6.8)
        
        # 14 Roda Utama & Rantai (Tracks)
        for side in [-2.2, 2.2]:
            for i in range(7):
                self.add_cylinder(side, 0.6, -2.5 + (i * 0.85), 0.5, 0.45, 12)
        
        # Turret Angular Kompleks (Sesuai Gambar)
        self.add_complex_turret()
        
        # Laras Meriam dengan Chamber & Muzzle Brake
        for i in range(16):
            z_pos = 2.0 + (i * 0.35)
            r = 0.3 if i >= 14 else (0.25 if i == 5 else 0.18)
            self.add_cylinder(0, -1.0, z_pos, r, 0.35, 12, horizontal=True)

        self.base_v = np.array(self.vertices)
        
        # Status Transformasi
        self.angle = [0.4, 0.6]
        self.pos = np.array([0.0, 0.0, 22.0])
        self.scale = 1.0
        self.show_reflection = False

    def add_box(self, x, y, z, w, h, d):
        s = len(self.vertices)
        for dx in [-w/2, w/2]:
            for dy in [-h/2, h/2]:
                for dz in [-d/2, d/2]: self.vertices.append([x+dx, y+dy, z+dz, 1])
        f = [(0,1,3,2), (4,5,7,6), (0,1,5,4), (2,3,7,6), (0,2,6,4), (1,3,7,5)]
        for face in f: self.faces.append([i + s for i in face])

    def add_cylinder(self, cx, cy, cz, r, l, seg, horizontal=False):
        s = len(self.vertices)
        for i in range(seg):
            a = 2 * math.pi * i / seg
            if not horizontal:
                self.vertices.extend([[cx-l/2, cy+math.cos(a)*r, cz+math.sin(a)*r, 1], [cx+l/2, cy+math.cos(a)*r, cz+math.sin(a)*r, 1]])
            else:
                self.vertices.extend([[cx+math.cos(a)*r, cy+math.sin(a)*r, cz, 1], [cx+math.cos(a)*r, cy+math.sin(a)*r, cz+l, 1]])
            c, n = s+i*2, s+((i+1)%seg)*2
            self.faces.append((c, n, n+1, c+1))

    def add_complex_turret(self):
        s = len(self.vertices)
        # Titik Turret yang lebih tajam dan miring (Sloped Armor)
        pts = [[1.9, 0.8, 1.5], [1.9, 0.8, -2.5], [-1.9, 0.8, -2.5], [-1.9, 0.8, 1.5], # Bawah
               [1.2, -0.6, 1.2], [1.2, -0.6, -2.0], [-1.2, -0.6, -2.0], [-1.2, -0.6, 1.2], # Atas
               [0, -1.0, 0.8]] # Puncak antena/sensor
        for p in pts: self.vertices.append([p[0], p[1]-1.2, p[2], 1])
        self.faces.extend([[s,s+1,s+5,s+4], [s+1,s+2,s+6,s+5], [s+2,s+3,s+7,s+6], [s+3,s,s+4,s+7], 
                           [s+4,s+5,s+8], [s+5,s+6,s+8], [s+6,s+7,s+8], [s+7,s+4,s+8]])

    def draw_background(self, screen):
        # 5. GRADASI CAHAYA PUSAT (Hitam ke Terang di Tengah)
        center_x, center_y = WIDTH // 2, HEIGHT // 2
        for r in range(WIDTH, 0, -20):
            color_val = max(0, min(40, 40 - int(r/WIDTH * 40)))
            pygame.draw.circle(screen, (color_val, color_val, color_val), (center_x, center_y), r)

    def draw_floor(self, screen, view_mat, proj_mat):
        # LANTAI TIPIS (Grid Biru Redup)
        color = (0, 40, 80)
        grid_size = 8
        spacing = 1.5
        for i in range(-grid_size, grid_size + 1):
            p1 = np.array([i*spacing, 1.2, -grid_size*spacing, 1]) @ view_mat @ proj_mat
            p2 = np.array([i*spacing, 1.2, grid_size*spacing, 1]) @ view_mat @ proj_mat
            if p1[3] > 0.1 and p2[3] > 0.1:
                pygame.draw.line(screen, color, (int(p1[0]/p1[3]*WIDTH/2+WIDTH/2), int(p1[1]/p1[3]*HEIGHT/2+HEIGHT/2)),
                                 (int(p2[0]/p2[3]*WIDTH/2+WIDTH/2), int(p2[1]/p2[3]*HEIGHT/2+HEIGHT/2)), 1)
            p3 = np.array([-grid_size*spacing, 1.2, i*spacing, 1]) @ view_mat @ proj_mat
            p4 = np.array([grid_size*spacing, 1.2, i*spacing, 1]) @ view_mat @ proj_mat
            if p3[3] > 0.1 and p4[3] > 0.1:
                pygame.draw.line(screen, color, (int(p3[0]/p3[3]*WIDTH/2+WIDTH/2), int(p3[1]/p3[3]*HEIGHT/2+HEIGHT/2)),
                                 (int(p4[0]/p4[3]*WIDTH/2+WIDTH/2), int(p4[1]/p4[3]*HEIGHT/2+HEIGHT/2)), 1)

    def render_object(self, screen, matrix, proj_mat, is_reflection=False):
        world_v = self.base_v @ matrix
        sorted_faces = sorted(self.faces, key=lambda f: np.mean([world_v[i][2] for i in f]), reverse=True)
        final_v = world_v @ proj_mat
        
        pts = [(int(v[0]/v[3]*WIDTH/2+WIDTH/2), int(v[1]/v[3]*HEIGHT/2+HEIGHT/2)) if v[3]>0.1 else None for v in final_v]

        for f in sorted_faces:
            if all(pts[i] for i in f):
                # Ilusi Kedalaman & Cahaya
                dist = np.mean([world_v[i][2] for i in f])
                lum = max(0.1, min(1.0, 1.5 - dist/40))
                
                base_c = self.GOLD_SOLID
                if is_reflection: # Warna bayangan lebih gelap dan transparan (simulasi)
                    color = [int(c * lum * 0.3) for c in base_c]
                else:
                    color = [int(c * lum) for c in base_c]
                
                pygame.draw.polygon(screen, color, [pts[i] for i in f])
                if not is_reflection:
                    pygame.draw.polygon(screen, self.GOLD_WIRE, [pts[i] for i in f], 1)

    def draw(self, screen):
        self.draw_background(screen)
        
        # Matriks Dasar
        ax, ay = self.angle
        rx = np.array([[1,0,0,0],[0,math.cos(ax),-math.sin(ax),0],[0,math.sin(ax),math.cos(ax),0],[0,0,0,1]])
        ry = np.array([[math.cos(ay),0,math.sin(ay),0],[0,1,0,0],[-math.sin(ay),0,math.cos(ay),0],[0,0,0,1]])
        sc = np.array([[self.scale,0,0,0],[0,self.scale,0,0],[0,0,self.scale,0],[0,0,0,1]])
        tr = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[self.pos[0], self.pos[1], self.pos[2], 1]])
        
        view_mat = sc @ rx @ ry @ tr
        fov = 1 / math.tan(math.radians(60)/2)
        proj_mat = np.array([[fov*(HEIGHT/WIDTH),0,0,0],[0,fov,0,0],[0,0,1,1],[0,0,0,0]])
        
        self.draw_floor(screen, view_mat, proj_mat)

        # 2. REFLEKSI (Tombol R)
        if self.show_reflection:
            # Matriks Refleksi terhadap bidang lantai (Y)
            ref_mat = np.array([[1,0,0,0],[0,-1,0,0],[0,0,1,0],[0, 2.4, 0, 1]])
            self.render_object(screen, ref_mat @ view_mat, proj_mat, True)
            
        # Render Tank Utama
        self.render_object(screen, view_mat, proj_mat)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock, tank = pygame.time.Clock(), UltraTankFinal()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                tank.show_reflection = not tank.show_reflection

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:  tank.angle[1] -= 0.04
        if keys[pygame.K_RIGHT]: tank.angle[1] += 0.04
        if keys[pygame.K_UP]:    tank.angle[0] -= 0.04
        if keys[pygame.K_DOWN]:  tank.angle[0] += 0.04
        if keys[pygame.K_a]:     tank.pos[0] -= 0.2
        if keys[pygame.K_d]:     tank.pos[0] += 0.2
        if keys[pygame.K_w]:     tank.scale += 0.01
        if keys[pygame.K_s]:     tank.scale -= 0.01

        tank.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__": main()
