import tkinter as tk
import math

class BeachBoatAnimation:
    def __init__(self, root):
        self.root = root
        self.root.title("Animasi Pantai dengan Perahu - Grafika 2D")
        
        # Canvas setup
        self.width = 1200
        self.height = 800
        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg='#87CEEB')
        self.canvas.pack()
        
        # Animation variables
        self.boat_x = 100
        self.boat_direction = 1
        self.boat_scale = 1.0
        self.scale_direction = 1
        self.sail_angle = 0
        self.wave_offset = 0
        self.sun_y = 100
        self.sun_direction = 1
        
        # Windmill rotation (ROTASI yang jelas terlihat)
        self.windmill_angle = 0
        
        # Seagull animation (ROTASI burung)
        self.bird_angle = 0
        self.bird_x = 200
        
        self.draw_scene()
        self.animate()
    
    # ========== ALGORITMA DDA (Digital Differential Analyzer) ==========
    def dda_line(self, x1, y1, x2, y2, color='black', width=2):
        """Menggambar garis menggunakan algoritma DDA"""
        dx = x2 - x1
        dy = y2 - y1
        steps = max(abs(dx), abs(dy))
        
        if steps == 0:
            return
        
        x_inc = dx / steps
        y_inc = dy / steps
        
        x, y = x1, y1
        points = []
        for _ in range(int(steps) + 1):
            points.append((round(x), round(y)))
            x += x_inc
            y += y_inc
        
        for i in range(len(points) - 1):
            self.canvas.create_line(points[i][0], points[i][1], 
                                   points[i+1][0], points[i+1][1], 
                                   fill=color, width=width)
    
    # ========== ALGORITMA BRESENHAM ==========
    def bresenham_line(self, x1, y1, x2, y2, color='black', width=2):
        """Menggambar garis menggunakan algoritma Bresenham"""
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy
        
        points = []
        x, y = x1, y1
        
        while True:
            points.append((x, y))
            if x == x2 and y == y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x += sx
            if e2 < dx:
                err += dx
                y += sy
        
        for i in range(len(points) - 1):
            self.canvas.create_line(points[i][0], points[i][1], 
                                   points[i+1][0], points[i+1][1], 
                                   fill=color, width=width)
    
    # ========== ALGORITMA MIDPOINT CIRCLE ==========
    def midpoint_circle(self, xc, yc, r, color='black', fill=''):
        """Menggambar lingkaran menggunakan algoritma Midpoint Circle"""
        x = 0
        y = r
        d = 1 - r
        points = []
        
        while x <= y:
            points.extend([
                (xc + x, yc + y), (xc - x, yc + y),
                (xc + x, yc - y), (xc - x, yc - y),
                (xc + y, yc + x), (xc - y, yc + x),
                (xc + y, yc - x), (xc - y, yc - x)
            ])
            
            if d < 0:
                d += 2 * x + 3
            else:
                d += 2 * (x - y) + 5
                y -= 1
            x += 1
        
        if fill:
            self.canvas.create_oval(xc-r, yc-r, xc+r, yc+r, outline=color, fill=fill, width=2)
        else:
            for point in points:
                self.canvas.create_oval(point[0]-1, point[1]-1, 
                                       point[0]+1, point[1]+1, 
                                       outline=color, fill=color)
    
    # ========== ALGORITMA POLYGON ==========
    def draw_polygon(self, points, color='black', fill=''):
        """Menggambar polygon menggunakan titik-titik"""
        if fill:
            self.canvas.create_polygon(points, outline=color, fill=fill, width=2)
        else:
            for i in range(len(points)):
                x1, y1 = points[i]
                x2, y2 = points[(i + 1) % len(points)]
                self.bresenham_line(x1, y1, x2, y2, color, 2)
    
    # ========== TRANSFORMASI GEOMETRIS 2D ==========
    
    def translate(self, points, tx, ty):
        """TRANSLASI: Menggeser objek"""
        return [(x + tx, y + ty) for x, y in points]
    
    def rotate(self, points, angle, cx, cy):
        """ROTASI: Memutar objek terhadap titik pusat"""
        rad = math.radians(angle)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)
        
        rotated = []
        for x, y in points:
            x_new = x - cx
            y_new = y - cy
            x_rot = x_new * cos_a - y_new * sin_a
            y_rot = x_new * sin_a + y_new * cos_a
            rotated.append((x_rot + cx, y_rot + cy))
        return rotated
    
    def scale(self, points, sx, sy, cx, cy):
        """SKALA: Memperbesar/memperkecil objek"""
        scaled = []
        for x, y in points:
            x_new = cx + (x - cx) * sx
            y_new = cy + (y - cy) * sy
            scaled.append((x_new, y_new))
        return scaled
    
    def reflect_y(self, points, axis_y):
        """REFLEKSI: Mencerminkan objek terhadap sumbu Y"""
        return [(x, 2 * axis_y - y) for x, y in points]
    
    # ========== MENGGAMBAR SCENE ==========
    
    def draw_scene(self):
        self.canvas.delete('all')
        
        # Background gradient (langit)
        for i in range(400):
            color_val = int(135 + (i / 400) * 80)
            color = f'#{color_val:02x}{int(206 + (i/400)*30):02x}{int(235 - (i/400)*30):02x}'
            self.canvas.create_line(0, i, self.width, i, fill=color)
        
        # Laut dengan gradient
        for i in range(400, self.height):
            progress = (i - 400) / (self.height - 400)
            r = int(30 + progress * 20)
            g = int(144 - progress * 30)
            b = int(255 - progress * 40)
            color = f'#{r:02x}{g:02x}{b:02x}'
            self.canvas.create_line(0, i, self.width, i, fill=color)
        
        # MATAHARI (Midpoint Circle + Translasi)
        self.midpoint_circle(950, int(self.sun_y), 60, '#FF8C00', '#FFD700')
        # Sinar matahari (garis)
        for angle in range(0, 360, 30):
            rad = math.radians(angle)
            x1 = 950 + 70 * math.cos(rad)
            y1 = int(self.sun_y) + 70 * math.sin(rad)
            x2 = 950 + 90 * math.cos(rad)
            y2 = int(self.sun_y) + 90 * math.sin(rad)
            self.dda_line(int(x1), int(y1), int(x2), int(y2), '#FFD700', 3)
        
        # AWAN (Midpoint Circle)
        self.draw_cloud(200, 100, 1.0)
        self.draw_cloud(500, 80, 0.9)
        self.draw_cloud(800, 120, 1.1)
        
        # BURUNG TERBANG (ROTASI) - Burung berbentuk V
        self.draw_bird(self.bird_x, 150, self.bird_angle)
        self.draw_bird(self.bird_x + 100, 180, self.bird_angle)
        
        # OMBAK bergerak
        self.draw_waves()
        
        # Garis horizon (Bresenham)
        self.bresenham_line(0, 400, self.width, 400, '#1E90FF', 3)
        
        # PULAU dengan GUNUNG yang detail (Polygon)
        self.draw_island()
        
        # KINCIR ANGIN di pulau (ROTASI JELAS)
        self.draw_windmill(900, 320, self.windmill_angle)
        
        # PERAHU dengan detail (Translasi + Skala + Refleksi)
        self.draw_boat()
        
        # Box info kiri atas dengan background
        box_x = 10
        box_y = 10
        box_width = 260
        box_height = 110
        
        # Background box dengan shadow
        self.canvas.create_rectangle(box_x + 2, box_y + 2, 
                                     box_x + box_width + 2, box_y + box_height + 2,
                                     fill='#000000', outline='')
        self.canvas.create_rectangle(box_x, box_y, 
                                     box_x + box_width, box_y + box_height,
                                     fill='#2C3E50', outline='#34495E', width=2)
        
        # Label transformasi dengan detail lengkap
        y_offset = box_y + 12
        self.canvas.create_text(box_x + 8, y_offset, 
                               text="⚙ TRANSFORMASI GEOMETRIS 2D", 
                               font=("Arial", 9, "bold"), fill='#ECF0F1', anchor='w')
        
        y_offset += 20
        self.canvas.create_text(box_x + 8, y_offset, 
                               text=f"→ Translasi: Perahu bergerak X={int(self.boat_x)}px", 
                               font=("Arial", 8), fill='#3498DB', anchor='w')
        
        y_offset += 18
        self.canvas.create_text(box_x + 8, y_offset, 
                               text=f"↻ Rotasi: Kincir angin putar {int(self.windmill_angle)}°", 
                               font=("Arial", 8), fill='#E74C3C', anchor='w')
        
        y_offset += 18
        self.canvas.create_text(box_x + 8, y_offset, 
                               text=f"⇄ Skala: Perahu zoom {self.boat_scale:.2f}x (0.7-1.5)", 
                               font=("Arial", 8), fill='#F39C12', anchor='w')
        
        y_offset += 18
        self.canvas.create_text(box_x + 8, y_offset, 
                               text="⬇ Refleksi: Cermin bayangan di air", 
                               font=("Arial", 8), fill='#1ABC9C', anchor='w')
    
    def draw_cloud(self, x, y, scale):
        """Menggambar awan detail"""
        circles = [
            (0, 0, 30), (-25, 5, 25), (25, 5, 25), 
            (-15, -12, 22), (15, -12, 22), (0, -20, 18)
        ]
        for cx, cy, r in circles:
            scaled_r = int(r * scale)
            self.midpoint_circle(int(x + cx), int(y + cy), scaled_r, 
                               '#FFFFFF', '#FFFFFF')
    
    def draw_bird(self, x, y, angle):
        """Menggambar burung dengan rotasi"""
        # Bentuk V untuk burung
        bird_points = [(x-15, y), (x, y-10), (x+15, y)]
        rotated_bird = self.rotate(bird_points, angle, x, y-5)
        
        for i in range(len(rotated_bird) - 1):
            x1, y1 = rotated_bird[i]
            x2, y2 = rotated_bird[i + 1]
            self.dda_line(int(x1), int(y1), int(x2), int(y2), '#000000', 2)
    
    def draw_waves(self):
        """Menggambar ombak bergerak"""
        for i in range(0, self.width + 100, 100):
            x = i + self.wave_offset
            for angle in range(0, 180, 5):
                rad = math.radians(angle)
                x1 = x + 40 * math.cos(rad)
                y1 = 420 + 20 * math.sin(rad)
                x2 = x + 40 * math.cos(math.radians(angle + 5))
                y2 = 420 + 20 * math.sin(math.radians(angle + 5))
                self.canvas.create_line(x1, y1, x2, y2, fill='#ADD8E6', width=2)
    
    def draw_island(self):
        """Menggambar pulau dengan gunung detail"""
        # Gunung besar (Polygon)
        mountain1 = [(750, 400), (820, 280), (890, 400)]
        self.draw_polygon(mountain1, '#654321', '#8B7355')
        
        # Puncak salju
        snow_peak = [(820, 280), (800, 310), (840, 310)]
        self.draw_polygon(snow_peak, '#FFFFFF', '#FFFFFF')
        
        # Gunung kecil
        mountain2 = [(850, 400), (900, 320), (950, 400)]
        self.draw_polygon(mountain2, '#654321', '#A0826D')
        
        # Pantai pulau
        beach = [(700, 400), (750, 380), (950, 380), (1000, 400)]
        self.draw_polygon(beach, '#C2B280', '#D2B48C')
        
        # Pohon kelapa detail
        self.draw_detailed_palm(760, 370)
        self.draw_detailed_palm(850, 365)
        self.draw_detailed_palm(920, 368)
        
        # Batu-batu pantai (circle)
        self.midpoint_circle(720, 395, 8, '#696969', '#808080')
        self.midpoint_circle(740, 392, 6, '#696969', '#808080')
        self.midpoint_circle(965, 393, 7, '#696969', '#808080')
    
    def draw_detailed_palm(self, x, y):
        """Menggambar pohon kelapa yang detail"""
        # Batang berlekuk (DDA lines)
        segments = 5
        for i in range(segments):
            y_start = y + (i * 15)
            y_end = y + ((i + 1) * 15)
            x_offset = 3 * math.sin(i * 0.5)
            self.dda_line(int(x + x_offset), int(y_start), 
                         int(x + x_offset), int(y_end), '#8B4513', 5)
        
        # Tekstur batang
        for i in range(5):
            y_line = y + (i * 15) + 7
            self.dda_line(int(x - 3), int(y_line), int(x + 3), int(y_line), 
                         '#654321', 2)
        
        # Daun kelapa (8 arah)
        leaf_angles = [0, 45, 90, 135, 180, 225, 270, 315]
        for angle in leaf_angles:
            rad = math.radians(angle)
            for j in range(5):
                length = 40 - j * 5
                x_end = x + length * math.cos(rad)
                y_end = y + length * math.sin(rad)
                width = 5 - j
                self.dda_line(x, y, int(x_end), int(y_end), '#228B22', width)
        
        # Kelapa (cluster)
        coconut_positions = [(-8, 15), (0, 18), (8, 15)]
        for cx, cy in coconut_positions:
            self.midpoint_circle(x + cx, y + cy, 6, '#8B4513', '#CD853F')
    
    def draw_windmill(self, x, y, angle):
        """Menggambar kincir angin dengan ROTASI nyata"""
        # Tower kincir (Polygon)
        tower = [(x-15, y+80), (x+15, y+80), (x+10, y), (x-10, y)]
        self.draw_polygon(tower, '#8B4513', '#A0826D')
        
        # Pusat kincir (circle)
        self.midpoint_circle(x, y, 12, '#654321', '#8B4513')
        
        # Baling-baling kincir (4 blade) - INI YANG BERPUTAR
        blade_length = 45
        for i in range(4):
            blade_angle = angle + (i * 90)
            rad = math.radians(blade_angle)
            
            # Titik blade
            x_end = x + blade_length * math.cos(rad)
            y_end = y + blade_length * math.sin(rad)
            
            # Blade shape (polygon segitiga)
            blade_points = [
                (x, y),
                (x_end - 8 * math.sin(rad), y_end + 8 * math.cos(rad)),
                (x_end + 8 * math.sin(rad), y_end - 8 * math.cos(rad))
            ]
            self.draw_polygon(blade_points, '#FFFFFF', '#F5F5F5')
            
            # Garis tengah blade
            self.dda_line(x, y, int(x_end), int(y_end), '#654321', 3)
    
    def draw_boat(self):
        """Menggambar perahu DETAIL dengan semua transformasi"""
        # Base boat body (trapezoid)
        boat_body = [
            (0, 25), (70, 25), (65, 50), (5, 50)
        ]
        
        # TRANSLASI: Geser perahu
        boat_body = self.translate(boat_body, self.boat_x, 520)
        
        # SKALA: Perbesar/perkecil (ANIMASI SCALING JELAS)
        center_x = self.boat_x + 35
        center_y = 545
        boat_body = self.scale(boat_body, self.boat_scale, self.boat_scale, 
                              center_x, center_y)
        
        # Gambar badan perahu
        self.draw_polygon(boat_body, '#8B4513', '#A0522D')
        
        # Detail papan kayu (horizontal lines)
        for i in range(3):
            y_offset = 530 + i * 8
            scaled_y = center_y + (y_offset - 545) * self.boat_scale
            x_left = center_x + (5 - 35) * self.boat_scale
            x_right = center_x + (65 - 35) * self.boat_scale
            self.dda_line(int(x_left), int(scaled_y), 
                         int(x_right), int(scaled_y), '#654321', 2)
        
        # Tiang perahu (Bresenham) - scale sensitive
        mast_x = center_x
        mast_base_y = center_y + (525 - 545) * self.boat_scale
        mast_top_y = mast_base_y - 100 * self.boat_scale
        self.bresenham_line(int(mast_x), int(mast_base_y), 
                           int(mast_x), int(mast_top_y), '#654321', 5)
        
        # LAYAR (Polygon dengan rotasi)
        sail_base = [
            (mast_x, mast_top_y),
            (mast_x + 50 * self.boat_scale, mast_top_y + 25 * self.boat_scale),
            (mast_x + 45 * self.boat_scale, mast_base_y - 20 * self.boat_scale),
            (mast_x, mast_base_y - 30 * self.boat_scale)
        ]
        
        # Rotasi layar (efek angin)
        sail_rotated = self.rotate(sail_base, self.sail_angle, mast_x, 
                                   (mast_top_y + mast_base_y) / 2)
        self.draw_polygon(sail_rotated, '#FFFFFF', '#F8F8FF')
        
        # Garis layar
        for i in range(4):
            offset = 20 + i * 20
            y_line = mast_top_y + offset * self.boat_scale
            self.dda_line(int(mast_x), int(y_line), 
                         int(mast_x + 45 * self.boat_scale), int(y_line), 
                         '#D3D3D3', 1)
        
        # Bendera di puncak
        flag = [
            (mast_x, mast_top_y),
            (mast_x + 15, mast_top_y + 5),
            (mast_x, mast_top_y + 10)
        ]
        self.draw_polygon(flag, '#FF0000', '#FF0000')
        
        # REFLEKSI: Bayangan perahu di air (JELAS TERLIHAT)
        water_level = 580
        reflection_body = [(x, 2 * water_level - y) for x, y in boat_body]
        self.draw_polygon(reflection_body, '#6495ED', '#87CEEB')
        
        # Refleksi tiang
        reflect_mast_base = 2 * water_level - mast_base_y
        reflect_mast_top = 2 * water_level - mast_top_y
        self.bresenham_line(int(mast_x), int(reflect_mast_base),
                           int(mast_x), int(reflect_mast_top), 
                           '#6495ED', 3)
    
    # ========== ANIMASI ==========
    def animate(self):
        # 1. TRANSLASI: Perahu bergerak horizontal
        self.boat_x += 2 * self.boat_direction
        if self.boat_x > 700:
            self.boat_direction = -1
        elif self.boat_x < 100:
            self.boat_direction = 1
        
        # 2. SKALA: Perahu membesar-mengecil (JELAS)
        self.boat_scale += 0.01 * self.scale_direction
        if self.boat_scale > 1.5:
            self.scale_direction = -1
        elif self.boat_scale < 0.7:
            self.scale_direction = 1
        
        # 3. ROTASI: Kincir angin berputar terus (JELAS)
        self.windmill_angle += 3
        if self.windmill_angle >= 360:
            self.windmill_angle = 0
        
        # Rotasi layar (efek angin kecil)
        self.sail_angle = 8 * math.sin(self.wave_offset / 10)
        
        # Rotasi burung
        self.bird_angle = 15 * math.sin(self.wave_offset / 15)
        self.bird_x += 1
        if self.bird_x > self.width:
            self.bird_x = -50
        
        # Ombak bergerak
        self.wave_offset = (self.wave_offset + 3) % 100
        
        # Matahari naik-turun
        self.sun_y += 0.4 * self.sun_direction
        if self.sun_y > 160 or self.sun_y < 80:
            self.sun_direction *= -1
        
        # Redraw
        self.draw_scene()
        self.root.after(30, self.animate)


# ========== MAIN PROGRAM ==========
root = tk.Tk()
app = BeachBoatAnimation(root)
root.mainloop()