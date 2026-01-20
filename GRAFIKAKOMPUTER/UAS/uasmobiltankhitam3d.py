import pygame
import numpy as np
import math

# --- KONFIGURASI LAYAR ---
WIDTH, HEIGHT = 1200, 800
FPS = 60

def draw_spotlight_background(screen):
    """
    Menggambar sorot lampu putih yang sempit dan panjangnya 
    hanya sampai setengah layar.
    """
    # Isi background dengan hitam pekat
    screen.fill((5, 5, 5)) 
    
    # Parameter Cahaya
    beam_width = 100            # Lebar cahaya (sempit)
    beam_height = HEIGHT // 2   # Panjang hanya setengah layar
    center_x = (WIDTH // 2) - (beam_width // 2)
    
    # Buat surface transparan untuk efek gradasi (RGBA)
    beam_surface = pygame.Surface((beam_width, beam_height), pygame.SRCALPHA)

    # Gambar gradasi dari atas (terang) ke bawah (transparan)
    for y in range(beam_height):
        # Alpha 200 di atas, memudar ke 0 di tengah layar
        alpha = max(0, 200 - (y * 200 // beam_height))
        color = (255, 255, 255, alpha)
        pygame.draw.line(beam_surface, color, (0, y), (beam_width, y))

    # Tambahkan sedikit efek pendaran (glow) di inti cahaya
    core_width = beam_width // 3
    core_surface = pygame.Surface((core_width, beam_height), pygame.SRCALPHA)
    for y in range(beam_height):
        alpha = max(0, 150 - (y * 150 // beam_height))
        pygame.draw.line(core_surface, (255, 255, 255, alpha), (0, y), (core_width, y))

    # Gambar ke screen utama
    screen.blit(beam_surface, (center_x, 0))
    screen.blit(core_surface, (WIDTH // 2 - core_width // 2, 0))

class ModernTank3D:
    def __init__(self):
        self.vertices = []
        self.faces = []
        
        # Warna
        self.TANK_GREEN = (70, 85, 60)
        self.BLACK_TRACK = (30, 30, 30)
        
        # --- REPRESENTASI OBJEK 3D ---
        self.add_hull_body()
        self.add_fenders()
        # Roda & Track
        for side in [-2.5, 2.5]:
            for i in range(7):
                z_pos = -2.8 + (i * 0.9)
                self.add_cylinder(side, -0.6, z_pos, 0.45, 0.45, 12)
            self.add_track_shape(side)

        self.add_angular_turret()
        # Cannon
        for i in range(15):
            z = 1.8 + (i * 0.4)
            r = 0.18 if i < 14 else 0.35
            self.add_cylinder(0, 0.6, z, r, 0.4, 8, horizontal=True)

        self.base_v = np.array(self.vertices)
        
        # --- PARAMETER TRANSFORMASI ---
        self.angle_x, self.angle_y = 0.35, 0.7 
        self.pos = np.array([0.0, 0.0, 25.0]) 
        self.scale_val = 1.0
        self.reflect_y = 1.0 

    def add_hull_body(self):
        pts = [[2.0, 0.8, 3.0], [2.0, -0.6, 3.0], [-2.0, -0.6, 3.0], [-2.0, 0.8, 3.0], 
               [2.2, 0.9, -3.5], [2.2, -0.8, -3.5], [-2.2, -0.8, -3.5], [-2.2, 0.9, -3.5],
               [1.5, 1.2, 2.0], [-1.5, 1.2, 2.0], [1.8, 1.2, -2.5], [-1.8, 1.2, -2.5]]
        s = len(self.vertices)
        for p in pts: self.vertices.append([*p, 1])
        self.faces.extend([(s+0, s+1, s+2, s+3), (s+4, s+5, s+6, s+7), (s+0, s+4, s+5, s+1),
                           (s+3, s+7, s+6, s+2), (s+0, s+3, s+9, s+8), (s+4, s+7, s+11, s+10),
                           (s+8, s+9, s+11, s+10), (s+1, s+2, s+6, s+5)])

    def add_fenders(self):
        self.add_box(2.2, 0.0, 0, 0.8, 0.15, 6.5)
        self.add_box(-2.2, 0.0, 0, 0.8, 0.15, 6.5)

    def add_track_shape(self, x_offset):
        s = len(self.vertices)
        for y, z in [(-0.2, 3.0), (-0.2, -3.0), (-1.0, 3.0), (-1.0, -3.0)]:
            self.vertices.append([x_offset - 0.25, y, z, 1])
            self.vertices.append([x_offset + 0.25, y, z, 1])
        self.faces.extend([(s+0, s+1, s+3, s+2), (s+4, s+5, s+7, s+6)])

    def add_box(self, x, y, z, w, h, d):
        s = len(self.vertices)
        for dx in [-w/2, w/2]:
            for dy in [-h/2, h/2]:
                for dz in [-d/2, d/2]:
                    self.vertices.append([x+dx, y+dy, z+dz, 1])
        f = [(0,1,3,2), (4,5,7,6), (0,1,5,4), (2,3,7,6), (0,2,6,4), (1,3,7,5)]
        for face in f: self.faces.append([i + s for i in face])

    def add_cylinder(self, cx, cy, cz, r, l, seg, horizontal=False):
        s = len(self.vertices)
        for i in range(seg):
            a = 2 * math.pi * i / seg
            if not horizontal:
                self.vertices.append([cx - l/2, cy + math.cos(a)*r, cz + math.sin(a)*r, 1])
                self.vertices.append([cx + l/2, cy + math.cos(a)*r, cz + math.sin(a)*r, 1])
            else:
                self.vertices.append([cx + math.cos(a)*r, cy + math.sin(a)*r, cz, 1])
                self.vertices.append([cx + math.cos(a)*r, cy + math.sin(a)*r, cz + l, 1])
            c, n = s + i*2, s + ((i+1)%seg)*2
            self.faces.append((c, n, n+1, c+1))

    def add_angular_turret(self):
        s = len(self.vertices)
        pts = [[1.2, 1.0, 1.5], [1.2, 1.0, -1.5], [-1.2, 1.0, -1.5], [-1.2, 1.0, 1.5],
               [1.0, 1.5, 1.2], [1.0, 1.5, -1.2], [-1.0, 1.5, -1.2], [-1.0, 1.5, 1.2],
               [0.8, 1.8, 1.0], [0.8, 1.8, -1.0], [-0.8, 1.8, -1.0], [-0.8, 1.8, 1.0]]
        for p in pts: self.vertices.append([*p, 1])
        self.faces.extend([(s+0, s+1, s+2, s+3), (s+8, s+9, s+10, s+11), (s+0, s+4, s+7, s+3)])

    def draw(self, screen):
        # --- TRANSFORMASI GEOMETRIS 3D ---
        rx = np.array([[1,0,0,0],[0,math.cos(self.angle_x),-math.sin(self.angle_x),0],[0,math.sin(self.angle_x),math.cos(self.angle_x),0],[0,0,0,1]])
        ry = np.array([[math.cos(self.angle_y),0,math.sin(self.angle_y),0],[0,1,0,0],[-math.sin(self.angle_y),0,math.cos(self.angle_y),0],[0,0,0,1]])
        sc = np.array([[self.scale_val,0,0,0],[0,self.scale_val,0,0],[0,0,self.scale_val,0],[0,0,0,1]])
        rf = np.array([[1,0,0,0],[0,self.reflect_y,0,0],[0,0,1,0],[0,0,0,1]])
        tr = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[self.pos[0], self.pos[1], self.pos[2], 1]])
        
        view_v = self.base_v @ sc @ rf @ rx @ ry @ tr
        sorted_faces = sorted(self.faces, key=lambda f: np.mean([view_v[i][2] for i in f]), reverse=True)
        
        # --- PROYEKSI PERSPEKTIF ---
        fov = 1 / math.tan(math.radians(60) / 2)
        proj = np.array([[fov*(HEIGHT/WIDTH),0,0,0],[0,fov,0,0],[0,0,1,1],[0,0,0,0]])
        final_v = view_v @ proj
        
        pts = []
        for v in final_v:
            if v[3] > 0.1:
                pts.append((int(v[0]/v[3]*WIDTH/2+WIDTH/2), int(v[1]/v[3]*HEIGHT/2+HEIGHT/2)))
            else: pts.append(None)

        for f in sorted_faces:
            if all(pts[i] is not None for i in f):
                v1 = view_v[f[1]][:3] - view_v[f[0]][:3]
                v2 = view_v[f[2]][:3] - view_v[f[0]][:3]
                normal = np.cross(v1, v2)
                mag = np.linalg.norm(normal)
                lum = np.dot(normal/mag, [0.5, -1, 0.2]) if mag != 0 else 0
                
                # Warna objek dengan pencahayaan sederhana
                color = [max(0, min(255, int(c * (0.7 + 0.3 * lum)))) for c in self.TANK_GREEN]
                pygame.draw.polygon(screen, color, [pts[i] for i in f])
                pygame.draw.polygon(screen, (30, 40, 25), [pts[i] for i in f], 1)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("3D Tank - Vertical Spotlight Beam")
    clock, tank = pygame.time.Clock(), ModernTank3D()
    
    while True:
        draw_spotlight_background(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    tank.reflect_y *= -1

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]: tank.pos[0] -= 0.4
        if keys[pygame.K_d]: tank.pos[0] += 0.4
        if keys[pygame.K_w]: tank.scale_val += 0.02
        if keys[pygame.K_s]: tank.scale_val -= 0.02
        if keys[pygame.K_LEFT]:  tank.angle_y -= 0.05
        if keys[pygame.K_RIGHT]: tank.angle_y += 0.05
        if keys[pygame.K_UP]:    tank.angle_x -= 0.05
        if keys[pygame.K_DOWN]:  tank.angle_x += 0.05

        tank.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__": 
    main()