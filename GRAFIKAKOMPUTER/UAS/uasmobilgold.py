import pygame
import numpy as np
import math
import sys

# --- KONFIGURASI LAYAR ---
WIDTH, HEIGHT = 1000, 800
FPS = 60

class SpotlightTankUAS:
    def __init__(self):
        self.vertices = []
        self.faces = []
        self.face_colors = [] # Menyimpan warna per face untuk jendela
        self.GOLD_SOLID = (120, 95, 30)
        self.GOLD_WIRE = (255, 215, 100)
        self.DARK_WINDOW = (20, 20, 20) # Warna jendela gelap
        
        # --- MODELING DETAIL ---
        
        # 1. Body Utama Tank (Lambung)
        for i in range(8):
            z_offset = -3.5 + (i * 0.875)
            self.add_detailed_box(0, 0, z_offset, 4.2, 0.9, 0.875, self.GOLD_SOLID)
            
        # 2. Side Skirts Full & Melengkung
        for s in [-2.5, 2.5]: 
            self.add_detailed_box(s, 0.3, -0.2, 0.3, 1.4, 6.0, self.GOLD_SOLID)
            self.add_detailed_box(s, 0.5, 3.2, 0.3, 1.0, 1.0, self.GOLD_SOLID)
            self.add_detailed_box(s, 0.5, -3.5, 0.3, 1.0, 1.0, self.GOLD_SOLID)
            
        # 3. Kubah (Turret Utama)
        self.add_turret_v4()
        
        # 4. Jendela Depan Kubah (Permintaan 1)
        self.add_detailed_box(0, -1.5, 1.9, 1.4, 0.6, 0.1, self.DARK_WINDOW)
        
        # 5. Detail Garis-Garis Samping Kubah
        for side in [-1.8, 1.8]:
            self.add_detailed_box(side, -1.2, -0.5, 0.4, 0.8, 2.5, self.GOLD_SOLID)
            self.add_detailed_box(side, -1.2, 1.0, 0.3, 0.6, 0.5, self.GOLD_SOLID)
            
        # 6. Detail Atas Kubah (Palka/Hatch)
        self.add_detailed_box(0.6, -2.4, -0.2, 0.8, 0.1, 0.8, self.GOLD_SOLID)
        self.add_detailed_box(-0.6, -2.4, -0.2, 0.8, 0.1, 0.8, self.GOLD_SOLID)

        # 7. Laras Meriam
        for i in range(25):
            z_pos = 2.0 + (i * 0.25)
            r = 0.45 if i >= 23 else (0.35 if i == 10 else 0.2)
            self.add_cyl(0, -1.3, z_pos, r, 0.25, 16, hor=True)
            
        # 8. Roda
        for s in [-2.4, 2.4]:
            for i in range(7):
                self.add_cyl(s, 0.7, -2.8 + (i * 0.95), 0.6, 0.4, 20)

        self.base_v = np.array(self.vertices, dtype=float)
        self.angle = [0.4, 0.6]
        self.pos = np.array([0.0, 0.0, 26.0])
        self.scale = 1.0
        self.show_reflection = True 

    def add_detailed_box(self, x, y, z, w, h, d, color=None):
        if color is None: color = self.GOLD_SOLID
        s = len(self.vertices)
        for dx in [-w/2, w/2]:
            for dy in [-h/2, h/2]:
                for dz in [-d/2, d/2]: self.vertices.append([x+dx, y+dy, z+dz, 1])
        for f in [(0,1,3,2), (4,5,7,6), (0,1,5,4), (2,3,7,6), (0,2,6,4), (1,3,7,5)]:
            self.faces.append([i + s for i in f])
            self.face_colors.append(color)

    def add_cyl(self, cx, cy, cz, r, l, seg, hor=False):
        s = len(self.vertices)
        for i in range(seg):
            a = 2 * math.pi * i / seg
            if hor: 
                self.vertices.extend([[cx+math.cos(a)*r, cy+math.sin(a)*r, cz, 1], [cx+math.cos(a)*r, cy+math.sin(a)*r, cz+l, 1]])
            else: 
                self.vertices.extend([[cx-l/2, cy+math.cos(a)*r, cz+math.sin(a)*r, 1], [cx+l/2, cy+math.cos(a)*r, cz+math.sin(a)*r, 1]])
            c, n = s+i*2, s+((i+1)%seg)*2
            self.faces.append((c, n, n+1, c+1))
            self.face_colors.append(self.GOLD_SOLID)

    def add_turret_v4(self):
        s = len(self.vertices)
        pts = [[2.2, 1.0, 2.0], [2.2, 1.0, -3.0], [-2.2, 1.0, -3.0], [-2.2, 1.0, 2.0],
               [1.5, -0.6, 1.6], [1.5, -0.6, -2.5], [-1.5, -0.6, -2.5], [-1.5, -0.6, 1.6],
               [0, -1.2, 0.2]] 
        for p in pts: self.vertices.append([p[0], p[1]-1.6, p[2], 1])
        f_list = [[s,s+1,s+5,s+4], [s+1,s+2,s+6,s+5], [s+2,s+3,s+7,s+6], [s+3,s,s+4,s+7], 
                  [s+4,s+5,s+8], [s+5,s+6,s+8], [s+6,s+7,s+8], [s+7,s+4,s+8]]
        self.faces.extend(f_list)
        for _ in f_list: self.face_colors.append(self.GOLD_SOLID)

    def draw_spotlight_background(self, screen):
        screen.fill((0, 0, 0)) 
        spot_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        center_x, top_y = WIDTH // 2, -100 
        for r in range(WIDTH // 2, 0, -8):
            ratio = (r / (WIDTH // 2)) ** 0.8
            alpha = max(0, min(150, 150 - int(ratio * 150)))
            if alpha > 0:
                color = (alpha, alpha, alpha, alpha)
                width_narrow, height_long = r * 0.8, r * 3.0
                rect = pygame.Rect(center_x - width_narrow//2, top_y, width_narrow, height_long)
                pygame.draw.ellipse(spot_surf, color, rect)
        screen.blit(spot_surf, (0, 0))

    def draw_floor(self, screen, proj_mat):
        color = (40, 40, 40) 
        limit = 10
        spacing = 4
        y_pos = 5.5 
        static_view = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[0, -2.0, 20, 1]], dtype=float)
        
        for i in range(-limit, limit + 1):
            # Garis Horizontal & Vertikal membentuk kotak-kotak (Permintaan 3)
            p1 = np.array([i*spacing, y_pos, -limit*spacing, 1]) @ static_view @ proj_mat
            p2 = np.array([i*spacing, y_pos, limit*spacing, 1]) @ static_view @ proj_mat
            if p1[3] > 0.1 and p2[3] > 0.1:
                pygame.draw.line(screen, color, (int(p1[0]/p1[3]*WIDTH/2+WIDTH/2), int(p1[1]/p1[3]*HEIGHT/2+HEIGHT/2)),
                                 (int(p2[0]/p2[3]*WIDTH/2+WIDTH/2), int(p2[1]/p2[3]*HEIGHT/2+HEIGHT/2)), 1)
            
            p3 = np.array([-limit*spacing, y_pos, i*spacing, 1]) @ static_view @ proj_mat
            p4 = np.array([limit*spacing, y_pos, i*spacing, 1]) @ static_view @ proj_mat
            if p3[3] > 0.1 and p4[3] > 0.1:
                pygame.draw.line(screen, color, (int(p3[0]/p3[3]*WIDTH/2+WIDTH/2), int(p3[1]/p3[3]*HEIGHT/2+HEIGHT/2)),
                                 (int(p4[0]/p4[3]*WIDTH/2+WIDTH/2), int(p4[1]/p4[3]*HEIGHT/2+HEIGHT/2)), 1)

    def render_engine(self, screen, matrix, proj_mat, is_refl=False):
        world_v = self.base_v @ matrix
        indexed_faces = list(enumerate(self.faces))
        sorted_faces = sorted(indexed_faces, key=lambda f: np.mean([world_v[i][2] for i in f[1]]), reverse=True)
        final_v = world_v @ proj_mat
        
        pts = []
        for v in final_v:
            if v[3] > 0.1:
                pts.append((int(v[0]/v[3]*WIDTH/2+WIDTH/2), int(v[1]/v[3]*HEIGHT/2+HEIGHT/2)))
            else: pts.append(None)
            
        for idx, f in sorted_faces:
            if all(pts[i] is not None for i in f):
                # Hitung normal sederhana untuk gradasi senter dari atas (Permintaan 4)
                v0, v1, v2 = world_v[f[0]][:3], world_v[f[1]][:3], world_v[f[2]][:3]
                normal = np.cross(v1 - v0, v2 - v0)
                norm = np.linalg.norm(normal)
                
                # Gradasi berdasarkan arah atas (y-axis)
                light_intensity = 1.0
                if norm > 0:
                    normal /= norm
                    # Semakin menghadap ke atas (normal[1] negatif di ruang layar), semakin terang
                    light_intensity = max(0.4, 0.7 - normal[1] * 0.5) 
                
                dist = np.mean([world_v[i][2] for i in f])
                shade = max(0.2, min(1.0, 1.8 - dist/45)) * light_intensity
                
                base_color = self.face_colors[idx]
                if is_refl:
                    # Refleksi Glossy (Permintaan 2)
                    c = [int(x * shade * 0.4) for x in base_color]
                    pygame.draw.polygon(screen, c, [pts[i] for i in f])
                else:
                    c = [int(x * shade) for x in base_color]
                    pygame.draw.polygon(screen, c, [pts[i] for i in f])
                    pygame.draw.polygon(screen, self.GOLD_WIRE, [pts[i] for i in f], 1)

    def draw(self, screen):
        self.draw_spotlight_background(screen)
        fov = 1 / math.tan(math.radians(60)/2)
        proj_mat = np.array([[fov*(HEIGHT/WIDTH),0,0,0],[0,fov,0,0],[0,0,1,1],[0,0,0,0]], dtype=float)
        self.draw_floor(screen, proj_mat)
        
        ax, ay = self.angle
        rx = np.array([[1,0,0,0],[0,math.cos(ax),-math.sin(ax),0],[0,math.sin(ax),math.cos(ax),0],[0,0,0,1]])
        ry = np.array([[math.cos(ay),0,math.sin(ay),0],[0,1,0,0],[-math.sin(ay),0,math.cos(ay),0],[0,0,0,1]])
        sc = np.array([[self.scale,0,0,0],[0,self.scale,0,0],[0,0,self.scale,0],[0,0,0,1]])
        tr = np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[self.pos[0], self.pos[1], self.pos[2], 1]])
        view_mat = sc @ rx @ ry @ tr

        if self.show_reflection:
            # Posisi refleksi agar lebih menempel ke lantai (Glossy)
            refl_mat = np.array([[1,0,0,0],[0,-1,0,0],[0,0,1,0],[0, 5.2, 0, 1]], dtype=float)
            self.render_engine(screen, refl_mat @ view_mat, proj_mat, True)
            
        self.render_engine(screen, view_mat, proj_mat)

def main():
    pygame.init()
    try:
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Final UAS - Glossy Gradient Tank")
        clock = pygame.time.Clock()
        tank = SpotlightTankUAS()

        running = True
        while running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT: running = False
                if e.type == pygame.KEYDOWN and e.key == pygame.K_r:
                    tank.show_reflection = not tank.show_reflection

            k = pygame.key.get_pressed()
            if k[pygame.K_LEFT]:  tank.angle[1] -= 0.05
            if k[pygame.K_RIGHT]: tank.angle[1] += 0.05
            if k[pygame.K_UP]:    tank.angle[0] -= 0.05
            if k[pygame.K_DOWN]:  tank.angle[0] += 0.05
            if k[pygame.K_a]:     tank.pos[0] -= 0.3
            if k[pygame.K_d]:     tank.pos[0] += 0.3
            if k[pygame.K_w]:     tank.scale += 0.02
            if k[pygame.K_s]:     tank.scale -= 0.02

            tank.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()