import turtle

# ======================
# SETUP TURTLE WINDOW
# ======================
wn = turtle.Screen()
wn.title("Algoritma Garis, Lingkaran dan Poligon")
wn.bgcolor("green")

pen = turtle.Turtle()
pen.speed(0)
pen.hideturtle()
pen.penup()

turtle.tracer(5)  # Disable animation

# Fungsi menggambar titik
def plot(x, y):
    pen.goto(x, y)
    pen.dot(3, "black")

# Fungsi menulis teks
def write_text(x, y, text):
    pen.goto(x, y)
    pen.write(text, align="center", font=("Arial", 14, "bold"))

# ======================
# ALGORITMA GARIS DDA
# ======================
def line_dda(x1, y1, x2, y2):
    
## MENGHITUNG dx dan dy DARI NILAI SELISIH
    dx = x2 - x1
    dy = y2 - y1
## MENGHITUNG JUMLAH LANGKAH/STEP DARI NILAI MAX ANTARA dx dan dy 
    steps = int(max(abs(dx), abs(dy)))
## MENGHITUNG NILAI INCREMENT PERLANGKAH UNTUK x DAN y
    x_inc = dx / steps
    y_inc = dy / steps
## MENENTUKAN POSISI AWAL
    x = x1
    y = y1
## LOOP HASIL INCREMENT x,y SAMPAI KE STEP YANG TELAH DITENTUKAN
    for _ in range(steps + 1):
        plot(round(x), round(y))
        x += x_inc
        y += y_inc

# ======================
# ALGORITMA GARIS BRESENHAM
# ======================
def line_bresenham(x1, y1, x2, y2):

## Inisialisasi titik awal
    x, y = x1, y1
## Hitung dx dan dy
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
## Menentukan arah gerak (sx & sy)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1

    if dx > dy:  				#Garis lebih mendatar 
        p = 2*dy - dx 			#Hitung nilai p awal
        for _ in range(dx):		#Perulangan sebanyak dx langkah
            plot(x, y)			#Gambar titik saat ini
            x += sx				#Geser x sesuai arah (sx)
            if p < 0:			#Pengambilan keputusan berdasarkan p
                p += 2*dy
            else:
                y += sy
                p += 2*(dy - dx)
    else:
        p = 2*dx - dy			#Garis lebih curam, p awal
        for _ in range(dy):		#Perulangan sebanyak dy langkah
            plot(x, y)			#Gambar titik saat ini
            y += sy				#Geser y sesuai arah (sy)
            if p < 0:			#Keputusan berdasarkan p
                p += 2*dx
            else:
                x += sx
                p += 2*(dx - dy)

# ======================
# MIDPOINT CIRCLE
# ======================
def circle_midpoint(xc, yc, r):
    x = 0
    y = r
    p = 1 - r

    def plot_circle(x, y):
        plot(xc + x, yc + y)
        plot(xc - x, yc + y)
        plot(xc + x, yc - y)
        plot(xc - x, yc - y)
        plot(xc + y, yc + x)
        plot(xc - y, yc + x)
        plot(xc + y, yc - x)
        plot(xc - y, yc - x)

    while x <= y:
        plot_circle(x, y)
        x += 1
        if p < 0:
            p += 2*x + 1
        else:
            y -= 1
            p += 2*(x - y) + 1

# ======================
# POLIGON
# ======================
def draw_polygon(points, algorithm="dda"):
    n = len(points)
    for i in range(n):
        x1, y1 = points[i]
        x2, y2 = points[(i+1) % n]
        if algorithm == "dda":
            line_dda(x1, y1, x2, y2)
        else:
            line_bresenham(x1, y1, x2, y2)

# ======================
# GAMBAR DITEMPATKAN TERPISAH + JUDUL
# ======================

# Garis DDA (kiri atas)
write_text(-180, 230, "Garis DDA")
line_dda(-300, 200, -50, 150)

# Garis Bresenham (kiri bawah)
write_text(-180, -120, "Garis Bresenham")
line_bresenham(-300, -200, -50, -150)

# Lingkaran midpoint (kanan atas)
write_text(180, 230, "Lingkaran (Midpoint Circle)")
circle_midpoint(180, 150, 80)

# Poligon segilima (kanan bawah)
write_text(180, -20, "Poligon (Bresenham)")
polygon_points = [
    (180, -50),
    (260, -120),
    (220, -200),
    (140, -200),
    (100, -120)
]
draw_polygon(polygon_points, algorithm="bresenham")

# Update layar setelah semua selesai
turtle.update()
turtle.done()
