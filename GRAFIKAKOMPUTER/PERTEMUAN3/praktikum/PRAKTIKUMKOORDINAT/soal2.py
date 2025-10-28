# Ukuran layar
lebar = 10   # sumbu x (width)
tinggi = 5   # sumbu y (height)

# Titik yang akan ditampilkan
x = 3
y = 2

# Menampilkan grid
for row in range(tinggi):
    for col in range(lebar):
        if col == x and row == y:
            print("X", end=" ")
        else:
            print(".", end=" ")
    print()
