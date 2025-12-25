<h1 align=center>⚙️ HASIL PRAKTIK DAN KODE</h1>
<h2 align=center>💻 Grafika Komputer</h2>

### 1. Variabel dan Tipe Data 

<p align=center>
  <img width="375" height="112" alt="image" src="https://github.com/user-attachments/assets/c8e9a247-6e31-47ad-a9f7-322fc67850c6" />
</p>

Untuk kodenya => [Variabel&TipeData.py](Variabel&TipeData.py)

### 2. Operasi Aritmatika

<p align=center>
  <img width="351" height="93" alt="image" src="https://github.com/user-attachments/assets/8352be4e-d5ec-462d-887b-3569cbcaf986" />
</p>

Untuk kodenya => [OperasiAritmatika.py](OperasiAritmatika.py)

### 3. Input Output

<p align=center>
  <img width="406" height="153" alt="image" src="https://github.com/user-attachments/assets/62f2d457-43b4-4e51-8d57-6b861f44c4f0" />
</p>

Untuk kodenya => [InputOutput.py](InputOutput.py)

### 4. Kondisi

<p align=center>
  <img width="388" height="115" alt="image" src="https://github.com/user-attachments/assets/fcdf61ed-56d8-4492-b948-8b243acf16a7" />
</p>

Untuk kodenya => [Kondisi.py](Kondisi.py)

### 5. Perulangan

<p align=center>
  <img width="285" height="263" alt="image" src="https://github.com/user-attachments/assets/fd28f959-478e-4fbf-bad2-f29db10e10bf" />
</p>

Untuk kodenya => [Perulangan.py](Perulangan.py)

### 6. Fungsi

<p align=center>
  <img width="518" height="123" alt="image" src="https://github.com/user-attachments/assets/16ba21cc-d163-4f3d-95ce-180636e93563" />
</p>

Untuk kodenya => [Fungsi.py](Fungsi.py)


--------------------------
<h1 align=center>📝 PRAKTIKUM/TUGAS 🧪</h1>

### 1. Praktikum 1

<p align=center>
  <img width="486" height="100" alt="image" src="https://github.com/user-attachments/assets/175f14e5-b73c-4435-ad77-658ed3d947d1" />
</p>

Untuk kodenya :

    x=50
    y=100
    merah="Merah"
    print(f"Koordinat titik ({x},{y}) dengan warna {merah}")

Penjelasan kode :

<p><i>
Kode tersebut menetapkan nilai pada variabel x = 50, y = 100, dan merah = "Merah", lalu menampilkan teks "Koordinat titik (50,100) dengan warna Merah" menggunakan print().
</i></p>

##

###  2. Praktikum 2 

<p align=center>
  <img width="483" height="173" alt="image" src="https://github.com/user-attachments/assets/cd610077-aaf4-41d3-a4d5-8ec74269ab7c" />
</p>

Untuk kodenya :

    x = int(input("Masukkan nilai x: "))
    y = int(input("Masukkan nilai y: "))
    warna = input("Masukkan warna titik : ")

    print(f"Titik berada di ({x},{y}) dan berwarna {warna}.")


Penjelasan kode :

<p><i>
Kode tersebut meminta pengguna memasukkan nilai untuk variabel x dan y dalam bentuk angka, serta warna dalam bentuk teks, lalu menampilkan hasilnya dalam kalimat "Titik berada di (x,y) dan berwarna warna" menggunakan print() dan f-string.
</i></p>

##

### 3. Praktikum 3

<p align=center>
  <img width="310" height="261" alt="image" src="https://github.com/user-attachments/assets/b166bf90-920c-44ed-9dd8-ae2c5dbe138f" />
</p>

Untuk kodenya :

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

Penjelasan kode :

<p><i>
Kode tersebut meminta pengguna memasukkan nilai untuk variabel x, lalu memeriksa posisinya dengan if, elif, dan else. Jika x > 0, program menampilkan "Titik di Kanan layar"; jika x == 0, menampilkan "Titik di Tengah"; dan jika x < 0, menampilkan "Titik di Kiri Layar".
Setelah itu, program menampilkan judul "Perulangan 1-5", lalu menggunakan perulangan for dengan range(1,6) untuk mencetak teks "Titik ke-1" hingga "Titik ke-5" secara berurutan.
</i></p>

##

### 4. Praktikum 4

<p align=center>
  <img width="328" height="96" alt="image" src="https://github.com/user-attachments/assets/0036ba34-3659-4e6c-951a-4c614b4835cd" />
</p>

Untuk kodenya :

    import math
    
    def hitung_jarak(x1, y1, x2, y2):
        jarak = math.sqrt((x2-x1)**2+(y2-y1)**2)
        return jarak
    
    hasil=hitung_jarak(0,0,3,4)
    print(f"Jarak antara dua titik : {hasil}")


Penjelasan kode :

<p><i>
Kode tersebut menggunakan modul math untuk menghitung jarak antara dua titik pada bidang koordinat. Fungsi hitung_jarak(x1, y1, x2, y2) menerima empat parameter, yaitu koordinat titik pertama (x1, y1) dan titik kedua (x2, y2).
Di dalam fungsi, rumus **math.sqrt((x2 - x1)**2 + (y2 - y1)2) digunakan untuk menghitung jarak antara kedua titik menggunakan rumus jarak Euclidean. Nilai hasil perhitungan tersebut kemudian dikembalikan dengan return jarak.
Selanjutnya, fungsi dipanggil dengan nilai (0, 0, 3, 4), dan hasilnya disimpan dalam variabel hasil. Program kemudian menampilkan output “Jarak antara dua titik : 5.0”, karena jarak antara titik (0,0) dan (3,4) adalah 5 satuan.
</i></p>

##

### 5. Praktikum 5

<p align=center>
  <img width="347" height="256" alt="image" src="https://github.com/user-attachments/assets/90f852d4-176f-4b73-a758-00ac2a2e3779" />
</p>

Untuk kodenya :

    print("1. List")
    titik_list = [(0,0),(50,50),(100,0)]
    for titik in titik_list:
        print(titik)
    print("-------------")
    print("2. Tuple")
    pusat=(0,0)
    print("Titik Pusat",pusat)
    print("-------------")
    print("3. Dictionary")
    objek = {"x":10,"y":20,"warna":"biru"}
    print(f"Titik ({objek['x']},{objek['y']}) berwarna {objek['warna']}.")

Penjelasan kode :

<p><i>
Kode tersebut menunjukkan tiga cara berbeda untuk menyimpan dan menampilkan data titik pada Python:

<ul>
  <li>
    List: Variabel titik_list berisi beberapa titik sebagai tuple, yaitu (0,0), (50,50), (100,0). Program kemudian menggunakan for loop untuk menampilkan tiap titik satu per satu.
  </li>
  <li>
    Tuple: Variabel pusat menyimpan satu titik (0,0). Program menampilkan titik pusat ini dengan menuliskannya langsung.
  </li>
  <li>
    Dictionary: Variabel objek menyimpan informasi titik dalam bentuk pasangan kunci-nilai (x, y, warna). Program menampilkan titik ini dengan f-string, menghasilkan teks “Titik (10,20) berwarna biru.”
  </li>
</ul>
</i></p>




