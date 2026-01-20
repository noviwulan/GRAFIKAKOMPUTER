import pygame, math
pygame.init()

# ==== LOAD BACKGROUND EXTERNAL ====
bg = pygame.image.load("bg.jpg")          # nama file bisa diganti
bg = pygame.transform.scale(bg, (900,300)) # dibuat setengah tinggi window (600/2 = 300)


screen = pygame.display.set_mode((900,600))
pygame.display.set_caption("Rumah 2D Transformasi | DDA-Midpoint-Polygon")
clock=pygame.time.Clock()

WHITE=(255,255,255); GREEN=(0,128,0)
BROWN=(150,75,0); BLUE=(0,200,255)
YELLOW=(255,255,0); RED=(255,0,0)
GRAY=(180,180,180) ; BLACK=(0,0,0)

# ==================== ALGORITMA DDA =====================
def lineDDA(x1,y1,x2,y2,color=WHITE):
    dx=x2-x1; dy=y2-y1
    steps=int(max(abs(dx),abs(dy)))

    if steps == 0:  # <--- FIX ERROR ZeroDivision
        pygame.draw.circle(screen,color,(int(x1),int(y1)),1)
        return

    x_inc=dx/steps; y_inc=dy/steps
    x,y=x1,y1
    for i in range(steps):
        pygame.draw.circle(screen,color,(int(x),int(y)),1)
        x+=x_inc; y+=y_inc


# ==================== POLIGON =====================
def polygon(points,color=WHITE):
    for i in range(len(points)):
        lineDDA(points[i][0],points[i][1],points[(i+1)%len(points)][0],points[(i+1)%len(points)][1],color)

def fill_polygon(points, fill_color):
    # dapatkan bounding box
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    ymin, ymax = min(ys), max(ys)

    for y in range(ymin, ymax):
        intersections = []
        for i in range(len(points)):
            x1, y1 = points[i]
            x2, y2 = points[(i+1) % len(points)]
            if y1 == y2: 
                continue
            if min(y1,y2) <= y <= max(y1,y2):
                x = x1 + (y-y1)*(x2-x1)/(y2-y1)
                intersections.append(x)
        intersections.sort()

        for i in range(0,len(intersections),2):
            if i+1 < len(intersections):
                lineDDA(int(intersections[i]), y, int(intersections[i+1]), y, fill_color)


# ==================== MIDPOINT CIRCLE =====================
def circle_mid(xc,yc,r,color=YELLOW):
    x=0; y=r; p=1-r
    while x<=y:
        pts=[(xc+x,yc+y),(xc+y,yc+x),(xc-x,yc+y),(xc-y,yc+x),
             (xc+x,yc-y),(xc+y,yc-x),(xc-x,yc-y),(xc-y,yc-x)]
        for ptx,pty in pts: pygame.draw.circle(screen,color,(ptx,pty),1)
        x+=1
        if p<0: p+=2*x+1
        else: y-=1; p+=2*(x-y)+1

# ==================== TRANSFORMASI =====================
def refleksi_y(points,xc): # mirror secara horizontal
    return [(2*xc-x,y) for x,y in points]

def rotasi(points,deg,origin):
    rad=math.radians(deg)
    ox,oy=origin
    res=[]
    for x,y in points:
        x-=ox; y-=oy
        xr=x*math.cos(rad)-y*math.sin(rad)
        yr=x*math.sin(rad)+y*math.cos(rad)
        res.append((xr+ox,yr+oy))
    return res

def skala(points,s,cx,cy):
    return [((x-cx)*s+cx,(y-cy)*s+cy) for x,y in points]

# ====================== DATA OBJEK =========================

# Rumah
tembok=[(300,350),(300,250),(500,250),(500,350)]
atap=[(280,250),(400,180),(520,250)]
pintu_closed=[(360,350),(360,300),(420,300),(420,350)]
pintu_open=[(360,350),(360,300),(330,300),(330,350)]  # pintu terbuka (refleksi arah kiri)

# Jendela (2 berjajar)
winL_closed=[(310,310),(310,280),(340,280),(340,310)]
winL_open=refleksi_y(winL_closed,310)  # refleksi membuka ke kiri
winR_closed=[(460,310),(460,280),(490,280),(490,310)]
winR_open=refleksi_y(winR_closed,490)  # refleksi membuka ke kanan

# Pagar besi
pagar=[]
start=250
for i in range(18):              # <-- jumlah pagar diperbanyak jadi 30 tiang
    pagar += [(start,400),(start,350),(start+5,350),(start+5,400)]
    start+=15
pagar_shift=0       # <<< tambahkan ini
rot_sun=0
scale_sun=1

# Status jendela & pintu
open_state=False

# ---- Awan bergerak ----
cloud_x = 0
# ---- Mode Siang/Malam ----
is_night = False
brightness = 255          # intensitas cahaya (siang = terang)




# ====================== MAIN LOOP =======================
running=True
while running:
    screen.fill(GREEN)

    # Perintah Keyboard
    keys=pygame.key.get_pressed()
    if keys[pygame.K_g]: pagar_shift+=2     # pagar bergeser kanan
    if keys[pygame.K_b]: pagar_shift-=2     # pagar bergeser kiri
    if keys[pygame.K_o]: open_state=True    # buka pintu+window
    if keys[pygame.K_c]: open_state=False   # tutup pintu+window
    if keys[pygame.K_s]: scale_sun+=0.02    # perbesar matahari
    if keys[pygame.K_x]: scale_sun-=0.02    # perkecil matahari



    # Tentukan kondisi buka/tutup
    pintu=pintu_open if open_state else pintu_closed
    winL=winL_open if open_state else winL_closed
    winR=winR_open if open_state else winR_closed

    # ========== GAMBAR RUMAH ==========
    
    # ==== BRIGHTNESS BERDASARKAN BESAR MATAHARI ====
    brightness = int(150 + scale_sun*120)   # nilai dasar + dipengaruhi skala

    # batas agar tidak terlalu terang/gelap
    brightness = max(50, min(brightness, 255))
    
    # ==== TAMPILKAN BACKGROUND & EFEK SIANG-MALAM ====
    screen.blit(bg,(0,0))  # tampilkan gambar asli
    

    # buat layer gelap/terang
    overlay = pygame.Surface((900,600))
    overlay.set_alpha(255-brightness)    # semakin malam semakin gelap
    overlay.fill((0,0,0))                # warna gelap dominan malam

    screen.blit(overlay,(0,0))


    # TEMBOK = Fill coklat muda + outline putih
    fill_polygon(tembok,(210,160,100))   # coklat muda
    polygon(tembok,WHITE)                # outline putih

    # ATAP = Fill coklat tua + outline hitam
    fill_polygon(atap,(120,60,20))       # coklat tua
    polygon(atap,BLACK)                  # outline hitam

    # ========== PINTU DAN JENDELA ==========
    fill_polygon(pintu, WHITE)      # pintu warna putih
    polygon(pintu, BLACK)           # outline pintu hitam biar terlihat

    fill_polygon(winL, WHITE)       # jendela kiri putih
    polygon(winL, BLACK)

    fill_polygon(winR, WHITE)       # jendela kanan putih
    polygon(winR, BLACK)

    # --- Tambahkan gagang pintu (lingkaran kecil) ---
    # posisi tengah kanan pintu
    door_handle_x = (pintu[2][0] + pintu[3][0])//2 - 5
    door_handle_y = (pintu[1][1] + pintu[2][1]) // 2 + 30

    pygame.draw.circle(screen, (200,150,50), (door_handle_x, door_handle_y), 6) # warna emas
    
    # ========== JALAN ASPAL MIRING DARI KIRI BAWAH ==========
    jalan_aspal = [
        (0,600),      # pojok kiri bawah layar
        (260,400),    # mendekati pagar bagian kiri
        (330,400),    # tepat depan pagar kiri
        (100,600)     # kembali ke bawah sebagai bidang trapezoid miring
    ]

    fill_polygon(jalan_aspal,(50,50,50))  # warna abu gelap aspal
    polygon(jalan_aspal,WHITE)            # outline putih

    # Marka jalan putus-putus
    for i in range(8):
        x1 = 50 + i*30
        y1 = 600 - i*25
        x2 = x1 + 15
        y2 = y1 - 15
        lineDDA(x1,y1,x2,y2,(230,230,230))
   

    # ========== PAGAR (dapat digeser) ==========
    poly_pagar=[(x+pagar_shift,y) for x,y in pagar]
    polygon(poly_pagar,GRAY)
    

    # ========== MATAHARI DETAIL + ROTASI + SKALA ==========
    rot_sun += 1        # matahari berputar otomatis setiap frame
    sun_center=(100,100)
    circle_mid(sun_center[0],sun_center[1],int(40*scale_sun),YELLOW)

    # Sinar Matahari
    rays=[]
    for angle in range(0,360,30):
        x1=sun_center[0]+math.cos(math.radians(angle+rot_sun))*50*scale_sun
        y1=sun_center[1]+math.sin(math.radians(angle+rot_sun))*50*scale_sun
        x2=sun_center[0]+math.cos(math.radians(angle+rot_sun))*70*scale_sun
        y2=sun_center[1]+math.sin(math.radians(angle+rot_sun))*70*scale_sun
        lineDDA(x1,y1,x2,y2,YELLOW)
        
    # AWAN BERGERAK 
    cloud_x += 3
    if cloud_x > 950: cloud_x = -200  # reset ulang agar mengulang bergerak

    # Awan = beberapa lingkaran putih
    for cx, cy in [(cloud_x,120),(cloud_x+40,130),(cloud_x+80,120),(cloud_x+30,110)]:
        pygame.draw.circle(screen, (255,255,255), (cx,cy), 30)


    # Text
    font=pygame.font.SysFont("Arial",20)
    screen.blit(font.render("O = buka | C = tutup | G/B = geser pagar | S/X = skala matahari",True,WHITE),(10,10))

    pygame.display.update()
    clock.tick(60)

    for event in pygame.event.get():
        if event.type==pygame.QUIT: running=False

pygame.quit()
