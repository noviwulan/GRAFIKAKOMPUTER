# Titik awal dan akhir
x1, y1 = 0, 0
x2, y2 = 5, 3

# Menghitung delta
dx = x2 - x1
dy = y2 - y1

# Banyak langkah (mengikuti nilai dx)
steps = dx

print("Titik-titik koordinat garis dari (0,0) ke (5,3):")

# Loop untuk menghitung titik
for i in range(steps + 1):
    x = x1 + (dx / steps) * i
    y = y1 + (dy / steps) * i
    print(f"({round(x, 2)}, {round(y, 2)})")
