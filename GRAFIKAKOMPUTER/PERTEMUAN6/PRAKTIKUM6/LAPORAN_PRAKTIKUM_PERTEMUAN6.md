<h1 align="center">
LAPORAN PRAKTIKUM PADA PERTEMUAN 6
</h1>

##  PRAKTIKUM GAME SEDERHANA BERTEMA 'PETANI MENJAGA KEBUN PISANG DARI PENCURIAN MONYET'

## CODE 1

KODE PROGRAM :

    ```python
    pygame.init()
    WIDTH, HEIGHT = 800, 500
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Petani Menjaga Kebun Pisang - Transformasi 2D")
    ```

HASIL OUTPUT :
<p align="center"><img width="300" height="200" alt="image" src="GRAFIKAKOMPUTER/PERTEMUAN6/SS_TUGAS/ss1.PNG" /></p>

PENJELASAN :
Inisialisasi Pygame dan Layar
- pygame.init() menginisialisasi semua modul pygame.  
- set_mode() membuat jendela game.  
- set_caption() memberi judul pada window.

----------------------------------------------------------

## CODE 2

KODE PROGRAM :

    ```python
def draw_background(surface):
    surface.fill(BLUE)
    pygame.draw.rect(surface, GREEN, (0, 350, WIDTH, 200))
```


HASIL OUTPUT :
<p align="center"><img width="400" height="200" alt="image" src="GRAFIKAKOMPUTER/PERTEMUAN6/SS_TUGAS/ss2.PNG" /></p>

PENJELASAN :
Background Kebun Pisang
Membuat latar langit dan tanah, serta pohon pisang menggunakan bentuk dasar rect dan ellipse.

----------------------------------------------------------

## code 3

KODE PROGRAM :
      
    ```
    draw_farmer()
    ```

HASIL OUTPUT :
<p align="center"><img width="350" height="350" alt="image" src="GRAFIKAKOMPUTER/PERTEMUAN6/SS_TUGAS/ss3.PNG" /></p>

PENJELASAN :
Karakter Petani
Fungsi draw_farmer() menggambar kepala, badan, kaki, lengan, dan cangkul petani.

----------------------------------------------------------

## CODE 4

KODE PROGRAM :

     ```python
    rotated_arm = pygame.transform.rotate(arm, arm_angle if attacking else 0)
    ```
    
HASIL OUTPUT :
<p align="center"><img width="300" height="300" alt="image" src="GRAFIKAKOMPUTER/PERTEMUAN6/SS_TUGAS/ss4.PNG" /></p>

PENJELASAN :
Transformasi Rotasi
Lengan petani berputar saat tombol SPACE ditekan.

----------------------------------------------------------

## CODE 5

KODE PROGRAM :
 
   ```python
    farmer = pygame.transform.scale(farmer, (int(200*scale), int(200*scale)))
    ```

HASIL OUTPUT :
<p align="center"><img width="500" height="500" alt="image" src="GRAFIKAKOMPUTER/PERTEMUAN6/SS_TUGAS/ss5.PNG" /></p>
    
PENJELASAN :
Transformasi Scaling
Karakter petani membesar saat monyet tinggi muncul. memperbesar dengan menekan tombol S

----------------------------------------------------------

## CODE 6

KODE PROGRAM :

    ```python
    scene = pygame.transform.flip(scene, True, False)
    ```

HASIL OUTPUT :
<p align="center"><img width="500" height="500" alt="image" src="GRAFIKAKOMPUTER/PERTEMUAN6/SS_TUGAS/ss6.PNG" /></p>
    
PENJELASAN :
Transformasi Refleksi
Tampilan layar dicerminkan secara horizontal. dicerminkan dengan menekan tombol M/N

----------------------------------------------------------

## CODE 7

KODE PROGRAM :

    ```python
    is_tall = random.choice([True, False])
    monkeys.append([WIDTH + 40, 260, True])
    ```

HASIL OUTPUT :
<p align="center"><img width="500" height="500" alt="image" src="GRAFIKAKOMPUTER/PERTEMUAN6/SS_TUGAS/ss7.PNG" /></p>
    
PENJELASAN :
Spawn dan Gerakan Monyet
Monyet muncul secara acak dan bergerak dari kanan ke kiri. Dengan menekan tombol panah kanan / kiri

----------------------------------------------------------

## CODE 8

KODE PROGRAM :

    ```python
    dist = math.hypot(farmer_x - m[0], farmer_y - m[1])
    if dist < 60:
        monkeys.remove(m)
        score += 1
    ```

HASIL OUTPUT :
<p align="center"><img width="500" height="500" alt="image" src="GRAFIKAKOMPUTER/PERTEMUAN6/SS_TUGAS/ss8.PNG" /></p>
    
PENJELASAN :
Collision Detection
Jika jarak dekat, monyet dikalahkan dan skor bertambah.

----------------------------------------------------------

## CODE 9

KODE PROGRAM :

    ```python
    if m[0] < -10:
        game_over = True
    ```


HASIL OUTPUT :
<p align="center"><img width="500" height="500" alt="image" src="GRAFIKAKOMPUTER/PERTEMUAN6/SS_TUGAS/ss9.PNG" /></p>
    
PENJELASAN :
Game Over
Jika monyet lolos melewati layar → Game Over.

----------------------------------------------------------
----------------------------------------------------------
## Kontrol Game

← → : Gerak kiri kanan  
D : Dash cepat  
SPACE : Serang  
S : Scaling  
M : Mirror ON  
N : Mirror OFF  

HASIL OUTPUT :
<p align="center"><img width="500" height="500" alt="image" src="GRAFIKAKOMPUTER/PERTEMUAN6/SS_TUGAS/ss10.PNG" /></p>
----------------------------------------------------------
----------------------------------------------------------