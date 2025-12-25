x1,y1 = 0,0
x2,y2 = 5,3
n=5

points=[]
for i in range(n+1):
    x = x1+(x2-x1)*i/n
    y = y1+(y2-y1)*i/n
    points.append((round(x),round(y))) 
    print(f'Titik {i} : ({x:.1f},{y:.1f})') 
print('-------------------')
print('Garisnya')
lebar = x2+1 
tinggi = y2+1
for i in range(tinggi):
    for k in range(lebar):           
        if i == 0 and k == 0: #pusat
            print('0', end='')           
        elif (k, i) in points: #titik
            print('.', end='')
        elif i == 0:
            print('-', end='') #x          
        elif k == 0:
            print('|', end='')  #y      
        else:
            print(' ', end='')
    print()
print('')