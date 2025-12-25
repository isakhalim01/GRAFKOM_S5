print('===== Soal 2 =====')

lebar = 10
tinggi = 5
for y in range (tinggi):
    for x in range (lebar):
        if x == 3 and y == 2:
            print('X', end='')
        else:
            print('.', end='')
    print()