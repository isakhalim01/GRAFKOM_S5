tinggi = 10
lebar = 10
grid = [['.' for _ in range(lebar)] for _ in range(tinggi)]

# Menempatkan X di posisi (4,6)
# Catatan: koordinat (x,y) dimana x=kolom, y=baris
x_pos = 4
y_pos = 6

# Validasi posisi
if 0 <= x_pos < lebar and 0 <= y_pos < tinggi:
    grid[y_pos][x_pos] = 'X'
    print(f"\nPiksel 'X' ditempatkan pada posisi ({x_pos}, {y_pos})\n")
else:
    print(f"\nPosisi ({x_pos}, {y_pos}) di luar batas grid!\n")

# Tampilkan grid dengan nomor koordinat
print("  ", end="")
for i in range(lebar):
    print(i, end=" ")
print()

for idx, baris in enumerate(grid):
    print(f"{idx} ", end="")
    print(' '.join(baris))