print('===== Soal 1 =====')
import math
x1 = int(input('Masukkan x1 : '))
y1 = int(input('Masukkan y1 : '))
x2 = int(input('Masukkan x2 : '))
y2 = int(input('Masukkan y2 : '))

print('======= Hasill =======')
print(f'Titik Pertama : ({x1:.1f}, {y1:.1f})')
print(f'Titik Kedua : ({x2:.1f}, {y2:.1f})')
jarak = math.sqrt((x2-x1)**2+(y2-y1)**2)    
hasil=jarak
print(f'Jarak antara dua titik : {hasil}')

# tentukan kuadran
if x1<0 and y1<0:
    kuadran='Kuadran 1'
elif x1>0 and y1>0:
    kuadran='Kuadran 2'
elif x1<0 and y1>0:
    kuadran='Kuadran 3'
elif x1>0 and y1<0:
    kuadran='Kuadran 4'
elif x1==0 and y1==0:
    kuadran='Titik pusat (0,0)'
elif x1<0 == 0:
    kuadran='Berada di Sumbu Y'
else:
    kuadran='Berada di Sumbu X'
print(f'Titik pertama berada di: {kuadran}')
