<h1 align="center">
LAPORAN PRAKTIKUM PADA PERTEMUAN 5
</h1>

## 1. PRAKTIKUM GAMBAR ALGORITMA GARIS DDA

KODE PROGRAM :

    
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

----------------------------------------------------------

## 2. PRAKTIKUM GAMBAR ALGORITMA GARIS BRESENHAM

KODE PROGRAM :

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

----------------------------------------------------------

## 3.  PRAKTIKUM GAMBAR MIDPOINT CIRCLE

KODE PROGRAM :
      
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


    
PENJELASAN :

1. Inisialisasi variabel
(xc, yc) = koordinat pusat lingkaran
r = jari-jari (radius)
x = 0, y = r
Artinya algoritma mulai dari titik paling atas lingkaran (0, r) dalam koordinat relatif.
p = 1 − r
Ini adalah keputusan awal (decision parameter):
Jika p < 0 → titik berikutnya berada di sebelah dalam lingkaran, jadi y tetap
Jika p ≥ 0 → titik berikutnya berada di luar lingkaran, jadi y harus diturunkan


2. FUNGSI PLOT 8 TITIK SIMETRIS

Mengapa 8 titik?
Lingkaran punya 8-banyak simetri (oktan), sehingga cukup hitung 1 oktan saja, lalu cerminkan titiknya.
Jika kita dapat 1 titik (x, y), maka:
empat titik di atas–bawah–kiri–kanan (kuadran),
empat titik lagi ditukar posisi x dan y.
Inilah yang membuat algoritma Midpoint Circle sangat cepat.

3. LOOP UTAMA
Mengapa kondisi x <= y?
Karena perhitungan dilakukan hanya dari 0° sampai 45°, yaitu 1/8 lingkaran, setelah itu semua titik tinggal dicerminkan.
Setelah menggambar satu set simetris:
x selalu bertambah 1 (berjalan ke kanan)
y bisa tetap atau turun (tergantung p)

4.PEMERIKSAAN PARAMETER 
Kasus 1: p < 0
Titik midpoint berada di dalam atau tepat pada lingkaran
Maka y tetap
Rumus pembaruan p:
p baru = p lama + (2x + 1)
Kenapa?
Karena kita hanya bergerak ke kanan (x bertambah 1).

Kasus 2: p ≥ 0
Titik midpoint berada di luar lingkaran
Maka y turun 1
Rumus pembaruan:
p baru = p lama + 2(x - y) + 1
Ini berasal dari evaluasi fungsi lingkaran ketika titik bergerak diagonal.

----------------------------------------------------------

## 4.  PRAKTIKUM GAMBAR POLIGON

KODE PROGRAM :

    def draw_polygon(points, algorithm="dda"):
    n = len(points)
    for i in range(n):
        x1, y1 = points[i]
        x2, y2 = points[(i+1) % n]
        if algorithm == "dda":
            line_dda(x1, y1, x2, y2)
        else:
            line_bresenham(x1, y1, x2, y2)

PENJELASAN : 
draw_polygon Fungsi ini digunakan untuk menggambar sebuah poligon (segi banyak),
points, algorithm="dda" ini adalah List berisi titik-titik poligon dan Anda dapat memilih algoritma garis: dda/bresenham
Menentukan jumlah titik  n = len(points)
Perulangan untuk menggambar setiap sisi poligon  for i in range(n):
Mengambil titik awal dan titik berikutnya:
     x1, y1 = points[i]
        x2, y2 = points[(i+1) % n]
Mengapa (i+1) % n?
Agar garis terakhir menghubungkan titik terakhir kembali ke titik awal.


----------------------------------------------------------
----------------------------------------------------------
HASIL OUTPUT :
    <p align="center"><img width="500" height="500" alt="image" src="GRAFIKAKOMPUTER/PERTEMUAN5/SS_TUGAS/capture1.PNG" /></p>
