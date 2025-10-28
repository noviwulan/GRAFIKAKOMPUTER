# Ukuran grid
lebar = 10   # sumbu x
tinggi = 10  # sumbu y

# Titik yang akan diganti
x = 4
y = 6

# Tampilkan grid
for row in range(tinggi):
    for col in range(lebar):
        if col == x and row == y:
            print("X", end=" ")
        else:
            print(".", end=" ")
    print()
