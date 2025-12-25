x = int(input("Masukkan nilai x: "))
if x > 0:
    print("Titik di Kanan layar")
elif x == 0:
    print("Titik di Tengah")
else:
    print("Titik di Kiri Layar")
print("==============")
print("Perulangan 1-5")
print("--------------")
for i in range(1,6):
    print(f"Titik ke-{i}")