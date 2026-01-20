import pygame
import numpy as np
import math

# --- KONFIGURASI SISTEM ---
WIDTH, HEIGHT = 1000, 750
FPS = 60

class UltraTankFinal:
    def __init__(self):
        # [POIN 1: REPRESENTASI OBJEK 3D]
        # Menggunakan Vertex (titik), Edge (garis), dan Polygon (bidang/faces)
        # untuk membentuk geometri Tank secara prosedural.
        self.vertices, self.faces = [], []
        self.base_color = np.array([130, 100, 30]) 
        self.GOLD_WIRE = (255, 220, 100)
        
        # Geometri dibentuk dari gabungan Polygon
        self.add_box(0, 0, 0, 3.8, 0.7, 6.5) 
        self.add_box(2.3, -0.2, 0, 0.6, 0.8, 6.8) 
        self.add_box(-2.3, -0.2, 0, 0.6, 0.8, 6.8)
        for side in [-2.2, 2.2]:
            for i in range(7): self.add_cylinder(side, 0.6, -2.5+(i*0.85), 0.5, 0.45, 12)
        self.add_complex_turret()
        for i in range(16):
            z = 2.0+(i*0.35); r = 0.3 if i>=14 else (0.25 if i==5 else 0.18)
            self.add_cylinder(0, -1.0, z, r, 0.35, 12, horizontal=True)

        self.base_v = np.array(self.vertices)
        
        # State awal untuk Transformasi
        self.angle = [0.4, 0.6]
        self.pos = np.array([0.0, 0.0, 22.0])
        self.scale = 1.0
        self.show_reflection = True
        self.projection_mode = "PERSPECTIVE"
        
        # Buffer untuk optimasi background
        self.bg_surface = pygame.Surface((WIDTH, HEIGHT))
        self.pre_render_bg()

    def add_box(self, x, y, z, w, h, d):
        s = len(self.vertices)
        for dx in [-w/2, w/2]:
            for dy in [-h/2, h/2]:
                for dz in [-d/2, d/2]: self.vertices.append([x+dx, y+dy, z+dz, 1])
        for f in [(0,1,3,2), (4,5,7,6), (0,1,5,4), (2,3,7,6), (0,2,6,4), (1,3,7,5)]:
            self.faces.append([i + s for i in f])

    def add_cylinder(self, cx, cy, cz, r, l, seg, horizontal=False):
        s = len(self.vertices)
        for i in range(seg):
            a = 2 * math.pi * i / seg
            if not horizontal: self.vertices.extend([[cx-l/2, cy+math.cos(a)*r, cz+math.sin(a)*r, 1], [cx+l/2, cy+math.cos(a)*r, cz+math.sin(a)*r, 1]])
            else: self.vertices.extend([[cx+math.cos(a)*r, cy+math.sin(a)*r, cz, 1], [cx+math.cos(a)*r, cy+math.sin(a)*r, cz+l, 1]])
            c, n = s+i*2, s+((i+1)%seg)*2
            self.faces.append((c, n, n+1, c+1))

    def add_complex_turret(self):
        s = len(self.vertices)
        pts = [[1.9, 0.8, 1.5], [1.9, 0.8, -2.5], [-1.9, 0.8, -2.5], [-1.9, 0.8, 1.5],
               [1.2, -0.6, 1.2], [1.2, -0.6, -2.0], [-1.2, -0.6, -2.0], [-1.2, -0.6, 1.2], [0, -1.0, 0.8]]
        for p in pts: self.vertices.append([p[0], p[1]-1.2, p[2], 1])
        self.faces.extend([[s,s+1,s+5,s+4], [s+1,s+2,s+6,s+5], [s+2,s+3,s+7,s+6], [s+3,s,s+4,s+7], [s+4,s+5,s+8], [s+5,s+6,s+8], [s+6,s+7,s+8], [s+7,s+4,s+8]])

    def pre_render_bg(self):
        self.bg_surface.fill((0, 0, 0))
        for r in range(900, 0, -5):
            c = int(255 * (1 - r/900)**4)
            if c > 2: pygame.draw.circle(self.bg_surface, (c, c, c), (WIDTH//2, -100), r)

    def draw_floor(self, screen, proj_mat):
        grid_count, spacing = 4, 6.0
        floor_view = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0, 3.8, 20.0, 1]])
        for iz in range(-grid_count, grid_count):
            for ix in range(-grid_count, grid_count):
                pts = []
                for dx, dz in [(0,0), (1,0), (1,1), (0,1)]:
                    v = np.array([(ix+dx)*spacing, 0, (iz+dz)*spacing, 1]) @ floor_view @ proj_mat
                    w = v[3] if self.projection_mode == "PERSPECTIVE" else 1.0
                    if w > 0.1: pts.append((int(v[0]/w*WIDTH/2+WIDTH/2), int(v[1]/w*HEIGHT/2+HEIGHT/2)))
                if len(pts) == 4:
                    col = 25 if (ix+iz)%2==0 else 15
                    pygame.draw.polygon(screen, (col, col, col), pts)

    def render_object(self, screen, matrix, proj_mat, is_reflection=False):
        # [POIN 2: TRANSFORMASI GEOMETRIS 3D]
        # Proses perkalian matriks (dot product) untuk posisi (translasi), 
        # rotasi, dan skala objek ke koordinat dunia.
        world_v = self.base_v @ matrix
        
        # [POIN 3: VIEWING & PROYEKSI 3D]
        # Mengubah koordinat 3D menjadi 2D menggunakan matriks proyeksi.
        final_v = world_v @ proj_mat
        
        pts = []
        for v in final_v:
            w = v[3] if self.projection_mode == "PERSPECTIVE" else 1.0
            pts.append((int(v[0]/w*WIDTH/2+WIDTH/2), int(v[1]/w*HEIGHT/2+HEIGHT/2)) if w > 0.1 else None)

        # [POIN 4: WARNA & ILUSI KEDALAMAN (Overlapping)]
        # Mengurutkan poligon (Z-sorting) agar yang di depan menutupi yang di belakang (overlapping)
        sorted_faces = sorted(self.faces, key=lambda f: np.mean([world_v[i][2] for i in f]), reverse=True)
        
        # [POIN 4: WARNA & ILUSI KEDALAMAN (Cahaya Dasar)]
        # Menghitung intensitas cahaya berdasarkan Normal vektor permukaan (Lambertian Shading sederhana)
        l_dir = np.array([0, -1, -0.5]); l_dir /= np.linalg.norm(l_dir)

        for f in sorted_faces:
            poly = [pts[i] for i in f if pts[i] is not None]
            if len(poly) == len(f):
                v1, v2, v3 = world_v[f[0]][:3], world_v[f[1]][:3], world_v[f[2]][:3]
                norm = np.cross(v2 - v1, v3 - v1)
                n_len = np.linalg.norm(norm)
                if n_len == 0: continue
                norm /= n_len
                if np.dot(norm, v1) > 0: norm = -norm
                
                dot = np.dot(norm, l_dir)
                
                if is_reflection:
                    # [POIN 2: REFLEKSI]
                    # Rendering objek kedua dengan matriks refleksi terhadap sumbu Y (lantai)
                    fade = max(0, min(1.0, 1.2 - np.mean([world_v[i][2] for i in f])/35))
                    col = (self.base_color * (0.1 + 0.3 * max(0, dot)) * fade).astype(int)
                    pygame.draw.polygon(screen, col, poly)
                else:
                    intensity = 0.2 + 0.8 * max(0, dot)
                    # [POIN 4: PERSPEKTIF WARNA (FOG)]
                    # Semakin jauh objek (Z besar), warna semakin pudar ke arah background (hitam)
                    fog = max(0.1, min(1.0, 1.6 - np.mean([world_v[i][2] for i in f])/40))
                    col = np.clip((self.base_color * intensity + (70 if dot > 0.8 else 0)) * fog, 0, 255).astype(int)
                    pygame.draw.polygon(screen, col, poly)
                    pygame.draw.polygon(screen, (np.array(self.GOLD_WIRE)*intensity*fog).astype(int), poly, 1)

    def draw(self, screen):
        screen.blit(self.bg_surface, (0,0))
        
        # [POIN 3: PROYEKSI (Ortogonal atau Perspektif)]
        # Switch matriks proyeksi berdasarkan input user (Tombol P)
        if self.projection_mode == "PERSPECTIVE":
            fov = 1 / math.tan(math.radians(60)/2)
            proj_mat = np.array([[fov*(HEIGHT/WIDTH),0,0,0],[0,fov,0,0],[0,0,1,1],[0,0,0,0]])
        else:
            s = 0.06 * self.scale
            proj_mat = np.array([[s*(HEIGHT/WIDTH),0,0,0],[0,s,0,0],[0,0,0.01,0],[0,0,0,1]])

        self.draw_floor(screen, proj_mat)

        # [POIN 2: TRANSFORMASI (Rotasi, Skala, Translasi)]
        ax, ay = self.angle
        rx = np.array([[1,0,0,0],[0,math.cos(ax),-math.sin(ax),0],[0,math.sin(ax),math.cos(ax),0],[0,0,0,1]])
        ry = np.array([[math.cos(ay),0,math.sin(ay),0],[0,1,0,0],[-math.sin(ay),0,math.cos(ay),0],[0,0,0,1]])
        view_mat = np.diag([self.scale, self.scale, self.scale, 1]) @ rx @ ry
        view_mat[3, :3] = self.pos
        
        if self.show_reflection:
            # [POIN 2: REFLEKSI] Matriks cermin terhadap bidang lantai
            ref_mat = np.array([[1,0,0,0],[0,-1,0,0],[0,0,1,0],[0, 3.2, 0, 1]])
            self.render_object(screen, ref_mat @ view_mat, proj_mat, True)
            
        self.render_object(screen, view_mat, proj_mat)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tugas Proyek Grafkom 3D")
    clock, tank = pygame.time.Clock(), UltraTankFinal()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return
            if event.type == pygame.KEYDOWN:
                # [POIN 3] Interaksi untuk ganti mode proyeksi
                if event.key == pygame.K_p: tank.projection_mode = "ORTHOGONAL" if tank.projection_mode == "PERSPECTIVE" else "PERSPECTIVE"
                # [POIN 2] Interaksi aktifkan/nonaktifkan refleksi
                if event.key == pygame.K_r: tank.show_reflection = not tank.show_reflection
        
        # [KONTROL TRANSFORMASI INTERAKTIF]
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:  tank.angle[1] -= 0.05 # Rotasi Y
        if keys[pygame.K_RIGHT]: tank.angle[1] += 0.05
        if keys[pygame.K_UP]:    tank.angle[0] -= 0.05 # Rotasi X
        if keys[pygame.K_DOWN]:  tank.angle[0] += 0.05
        if keys[pygame.K_w]:     tank.scale += 0.02    # Skala (Zoom In)
        if keys[pygame.K_s]:     tank.scale -= 0.02    # Skala (Zoom Out)
        if keys[pygame.K_a]:     tank.pos[0] -= 0.2    # Translasi X
        if keys[pygame.K_d]:     tank.pos[0] += 0.2

        tank.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__": main()