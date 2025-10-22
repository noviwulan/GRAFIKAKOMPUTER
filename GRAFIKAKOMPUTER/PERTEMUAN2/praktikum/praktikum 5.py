# ==========================
# Praktikum: Struktur Data Titik
# ==========================

# a. List berisi tiga pasangan titik dan tampilkan dengan for
titik_list = [(0, 0), (50, 50), (100, 0)]
print("Daftar Titik dalam List:")
for titik in titik_list:
    print(titik)

print()  # baris kosong

# b. Tuple berisi satu titik
pusat = (0, 0)
print(f"Titik pusat adalah: {pusat}")

print()  # baris kosong

# c. Dictionary berisi atribut titik
titik_dict = {"x": 10, "y": 20, "warna": "biru"}
print(f"Titik ({titik_dict['x']},{titik_dict['y']}) berwarna {titik_dict['warna']}.")
