<h1 align="center">
LAPORAN UAS
</h1>

## Judul Proyek
----------------------------------------------------------
<b>Pemodelan Kendaraan Tempur Taktis</b>
----------------------------------------------------------


## Konsep Grafika
Proyek ini mengaplikasikan konsep grafika komputer dasar untuk menciptakan adegan kendaraan tempur dalam ruang tiga dimensi:

    1. Representasi Objek 3D (Vertex, Edge, Polygon):
    Objek utama (tank) dikonstruksi secara manual melalui daftar koordinat titik (vertex) yang saling terhubung membentuk kerangka (edge)     dan bidang permukaan (polygon/faces). Ini memungkinkan pembuatan struktur kompleks seperti body, turret, dan roda tank.

    2.Transformasi Geometris 3D: Menggunakan matematika matriks untuk memanipulasi objek dalam scene:
    Translasi: Menggeser posisi tank secara horizontal (Sumbu X).
    Rotasi: Memutar tank pada sumbu X dan Y untuk melihat dari berbagai sudut.
    Skala: Menyesuaikan besar kecilnya objek (Zoom).
    Refleksi: Mengimplementasikan pencerminan objek terhadap bidang lantai (glossy floor) untuk meningkatkan realisme visual.

    3.Viewing & Proyeksi 3D:
    Implementasi sistem kamera yang mendukung dua mode pandang:
        -Perspektif: Memberikan kedalaman visual di mana garis sejajar tampak bertemu di satu titik hilang.
        -Ortogonal: Menampilkan objek tanpa distorsi jarak, sering digunakan dalam pemodelan teknis.
    Warna & Ilusi Kedalaman:
    Pencahayaan (Lambertian Shading): Menghitung intensitas warna poligon berdasarkan orientasi bidang terhadap sumber cahaya pusat           (spotlight).
    Z-Sorting (Overlapping): Memastikan poligon yang lebih dekat dengan kamera digambar terakhir agar tidak tertutup oleh bagian belakang     objek.
    Depth Cueing (Fog Effect): Gradasi warna yang menggelap seiring bertambahnya jarak objek pada sumbu Z untuk mempertegas dimensi ruang.

----------------------------------------------------------

## Cara Menjalankan Program
Prasyarat (Requirements)
Aplikasi ini membutuhkan Python dan beberapa library tambahan. Instalasi dapat dilakukan dengan perintah:

    pip install pygame numpy

Langkah-langkah
1. Simpan seluruh kode program ke dalam satu file Python (contoh: uasmobiltank2_3d.py).
Jalankan file tersebut melalui terminal atau IDE pilihan Anda:

        python uasmobiltank2_3d.py
   
----------------------------------------------------------

##Kontrol Navigasi

Panah Atas / Bawah :Rotasi Objek pada Sumbu X
Panah Kiri / Kanan :Rotasi Objek pada Sumbu Y
W / S              :Skala(Perbesar / Perkecil)
A / D              :Translasi (Geser Kiri / Kanan)
P                  :Switch Mode Proyeksi (Perspektif / Ortogonal)
R                  :Toggle Refleksi Lantai (On / Off)

----------------------------------------------------------


