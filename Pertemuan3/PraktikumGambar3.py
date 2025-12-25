print("\n" + "="*60)
print("SOAL 3: Tabel Perbandingan Representasi Raster dan Vektor")
print("="*60)

print("""
╔════════════════════╦═══════════════════════════╦═══════════════════════════╗
║     ASPEK          ║      RASTER (BITMAP)      ║         VEKTOR            ║
╠════════════════════╬═══════════════════════════╬═══════════════════════════╣
║ Representasi       ║ Kumpulan piksel/titik     ║ Persamaan matematika      ║
║                    ║ dalam grid                ║ (garis, kurva, bentuk)    ║
╠════════════════════╬═══════════════════════════╬═══════════════════════════╣
║ Contoh Soal        ║ SOAL 1: Grid 10×10        ║ SOAL 2: Garis (0,0)-(5,3) ║
║                    ║ dengan piksel diskrit     ║ dengan koordinat vektor   ║
╠════════════════════╬═══════════════════════════╬═══════════════════════════╣
║ Penyimpanan        ║ Menyimpan setiap piksel   ║ Menyimpan koordinat dan   ║
║                    ║ (besar untuk resolusi     ║ persamaan (lebih efisien) ║
║                    ║ tinggi)                   ║                           ║
╠════════════════════╬═══════════════════════════╬═══════════════════════════╣
║ Skalabilitas       ║ Kehilangan kualitas saat  ║ Tidak kehilangan kualitas ║
║                    ║ diperbesar (pixelated)    ║ saat diperbesar           ║
╠════════════════════╬═══════════════════════════╬═══════════════════════════╣
║ Ukuran File        ║ Bergantung pada resolusi  ║ Relatif kecil, tidak      ║
║                    ║ dan jumlah warna          ║ bergantung ukuran gambar  ║
╠════════════════════╬═══════════════════════════╬═══════════════════════════╣
║ Penggunaan         ║ Foto, gambar kompleks,    ║ Logo, ikon, ilustrasi,    ║
║                    ║ tekstur realistis         ║ diagram, desain grafis    ║
╠════════════════════╬═══════════════════════════╬═══════════════════════════╣
║ Format File        ║ JPG, PNG, BMP, GIF, TIFF  ║ SVG, AI, EPS, PDF         ║
╠════════════════════╬═══════════════════════════╬═══════════════════════════╣
║ Editing            ║ Edit per piksel           ║ Edit per objek/bentuk     ║
╠════════════════════╬═══════════════════════════╬═══════════════════════════╣
║ Kecepatan Render   ║ Cepat untuk tampilan      ║ Perlu kalkulasi untuk     ║
║                    ║ langsung                  ║ render                    ║
╚════════════════════╩═══════════════════════════╩═══════════════════════════╝
""")

print("\nKESIMPULAN:")
print("-" * 60)
print("• RASTER: Cocok untuk foto dan gambar dengan detail warna kompleks")
print("• VEKTOR: Cocok untuk logo, ilustrasi, dan desain yang perlu")
print("          diskalakan tanpa kehilangan kualitas")
print("-" * 60)