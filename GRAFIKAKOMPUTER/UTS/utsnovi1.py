import pygame
import math

pygame.init()
screen = pygame.display.set_mode((900, 600))
pygame.display.set_caption("Rumah 2D Animasi Lengkap")
clock = pygame.time.Clock()

WHITE = (255,255,255)
BLACK = (0,0,0)
BROWN = (150,75,0)
YELLOW = (255,255,0)
GRAY = (180,180,180)
GREEN = (0,255,0)
BLUE = (135,206,250)

# ===== DDA =====
def lineDDA(x1,y1,x2,y2,color=WHITE):
    dx, dy = x2-x1, y2-y1
    steps = int(max(abs(dx),abs(dy)))
    x, y = x1, y1
    for _ in range(steps):
        pygame.draw.circle(screen, color,(int(x),int(y)),1)
        x+=dx/steps; y+=dy/steps

def draw_polygon(points,color=WHITE):
    for i in range(len(points)):
        lineDDA(*points[i],*points[(i+1)%len(points)],color)

# ===== Midpoint Circle =====
def circle_mid(xc,yc,r,color=YELLOW):
    x,y,p=0,r,1-r
    while x<=y:
        for px,py in [(xc+x,yc+y),(xc+y,yc+x),(xc-x,yc+y),(xc-y,yc+x),
                      (xc+x,yc-y),(xc+y,yc-x),(xc-x,yc-y),(xc-y,yc-x)]:
            pygame.draw.circle(screen,color,(px,py),1)
        x+=1
        if p<0: p+=2*x+1
        else: y-=1; p+=2*(x-y)+1

# ==================================================
door_offset = 0
window_offset = 0
gate_shift = 0
target_door = 0
target_window = 0

sun_angle = 0
sun_scale = 40
scale_dir = 1

cloud_x = 0
grass_wave = 0

running=True
while running:
    screen.fill(BLUE)

    # Awan bergerak
    cloud_x = (cloud_x+1) % 1000
    pygame.draw.circle(screen, WHITE,(100+cloud_x,100),25)
    pygame.draw.circle(screen, WHITE,(130+cloud_x,110),30)
    pygame.draw.circle(screen, WHITE,(160+cloud_x,100),25)

    pygame.draw.circle(screen, WHITE,(600+cloud_x,120),25)
    pygame.draw.circle(screen, WHITE,(630+cloud_x,130),30)
    pygame.draw.circle(screen, WHITE,(660+cloud_x,120),25)

    # Rumput goyang
    grass_wave = (grass_wave+0.1)
    for i in range(0,900,10):
        h = 10+math.sin(i*0.2+grass_wave)*3
        lineDDA(i,580,i,580-h,GREEN)

    # Rumah
    draw_polygon([(300,350),(300,250),(500,250),(500,350)],WHITE) # tembok
    draw_polygon([(280,250),(400,180),(520,250)],BROWN) # atap

    # Animasi pintu/jendela halus
    if door_offset < target_door: door_offset += 1
    if door_offset > target_door: door_offset -= 1
    if window_offset < target_window: window_offset += 1
    if window_offset > target_window: window_offset -= 1

    # pintu
    draw_polygon([(360-door_offset,350),(360-door_offset,300),
                  (420-door_offset,300),(420-door_offset,350)],BROWN)

    # jendela kiri-kanan
    draw_polygon([(310-window_offset,310),(310-window_offset,280),
                  (340-window_offset,280),(340-window_offset,310)],BROWN)
    draw_polygon([(460+window_offset,310),(460+window_offset,280),
                  (490+window_offset,280),(490+window_offset,310)],BROWN)

    # pagar geser
    draw_polygon([(260+gate_shift,350),(260+gate_shift,330),
                  (540+gate_shift,330),(540+gate_shift,350)],GRAY)

    # Matahari animasi
    sun_angle+=0.02
    sun_scale+=scale_dir
    if sun_scale>=50 or sun_scale<=30: scale_dir*=-1

    cx,cy=100,100
    circle_mid(cx,cy,int(sun_scale),YELLOW)

    # sinar rotasi
    for i in range(8):
        ang=sun_angle+i*(math.pi/4)
        x1=cx+math.cos(ang)*(sun_scale+5)
        y1=cy+math.sin(ang)*(sun_scale+5)
        x2=cx+math.cos(ang)*(sun_scale+25)
        y2=cy+math.sin(ang)*(sun_scale+25)
        lineDDA(x1,y1,x2,y2,YELLOW)

    font=pygame.font.SysFont("Arial",22)
    screen.blit(font.render("[O] Buka | [C] Tutup | [G] Geser pagar",1,BLACK),(20,20))

    pygame.display.update()
    clock.tick(60)

    for e in pygame.event.get():
        if e.type==pygame.QUIT: running=False
        if e.type==pygame.KEYDOWN:
            if e.key==pygame.K_o: target_window,target_door = 20,25
            if e.key==pygame.K_c: target_window,target_door = 0,0
            if e.key==pygame.K_g: gate_shift = 80 if gate_shift==0 else 0

pygame.quit()
