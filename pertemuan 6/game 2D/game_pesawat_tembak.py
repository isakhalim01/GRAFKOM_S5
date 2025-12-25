import tkinter as tk
import math
import random

class SpaceShooterGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Space Shooter 2D - Game Grafika")
        
        # Canvas setup
        self.width = 800
        self.height = 600
        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg='#000000')
        self.canvas.pack()
        
        # Game state
        self.game_over = False
        self.score = 0
        self.lives = 3
        
        # Player variables
        self.player_x = self.width // 2
        self.player_y = self.height - 80
        self.player_angle = 0
        self.player_scale = 1.0
        self.scale_direction = 1
        
        # Movement
        self.move_left = False
        self.move_right = False
        self.move_up = False
        self.move_down = False
        
        # Bullets
        self.bullets = []
        
        # Enemies
        self.enemies = []
        self.enemy_spawn_timer = 0
        
        # Explosions
        self.explosions = []
        
        # Power-ups
        self.powerups = []
        self.powerup_timer = 0
        
        # Stars (background)
        self.stars = []
        for _ in range(50):
            self.stars.append({
                'x': random.randint(0, self.width),
                'y': random.randint(0, self.height),
                'speed': random.uniform(0.5, 2)
            })
        
        # Shield (refleksi)
        self.shield_active = False
        self.shield_timer = 0
        
        # Bind keys
        self.root.bind('<KeyPress>', self.key_press)
        self.root.bind('<KeyRelease>', self.key_release)
        
        self.game_loop()
    
    # ========== ALGORITMA DDA ==========
    def dda_line(self, x1, y1, x2, y2, color='white', width=2):
        """Menggambar garis menggunakan algoritma DDA"""
        dx = x2 - x1
        dy = y2 - y1
        steps = max(abs(dx), abs(dy))
        
        if steps == 0:
            return
        
        x_inc = dx / steps
        y_inc = dy / steps
        
        x, y = x1, y1
        for _ in range(int(steps) + 1):
            self.canvas.create_oval(round(x)-1, round(y)-1, 
                                   round(x)+1, round(y)+1, 
                                   fill=color, outline=color)
            x += x_inc
            y += y_inc
    
    # ========== ALGORITMA BRESENHAM ==========
    def bresenham_line(self, x1, y1, x2, y2, color='white', width=2):
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
        
        for px, py in points:
            self.canvas.create_oval(px-width, py-width, px+width, py+width, 
                                   fill=color, outline=color)
    
    # ========== ALGORITMA MIDPOINT CIRCLE ==========
    def midpoint_circle(self, xc, yc, r, color='white', fill=''):
        """Menggambar lingkaran menggunakan algoritma Midpoint Circle"""
        if fill:
            self.canvas.create_oval(xc-r, yc-r, xc+r, yc+r, 
                                   outline=color, fill=fill, width=2)
        else:
            x = 0
            y = r
            d = 1 - r
            
            while x <= y:
                points = [
                    (xc + x, yc + y), (xc - x, yc + y),
                    (xc + x, yc - y), (xc - x, yc - y),
                    (xc + y, yc + x), (xc - y, yc + x),
                    (xc + y, yc - x), (xc - y, yc - x)
                ]
                
                for px, py in points:
                    self.canvas.create_oval(px-1, py-1, px+1, py+1, 
                                           fill=color, outline=color)
                
                if d < 0:
                    d += 2 * x + 3
                else:
                    d += 2 * (x - y) + 5
                    y -= 1
                x += 1
    
    # ========== ALGORITMA POLYGON ==========
    def draw_polygon(self, points, color='white', fill=''):
        """Menggambar polygon"""
        if fill:
            self.canvas.create_polygon(points, outline=color, fill=fill, width=2)
        else:
            for i in range(len(points)):
                x1, y1 = points[i]
                x2, y2 = points[(i + 1) % len(points)]
                self.bresenham_line(int(x1), int(y1), int(x2), int(y2), color, 2)
    
    # ========== TRANSFORMASI GEOMETRIS 2D ==========
    
    def translate(self, points, tx, ty):
        """TRANSLASI: Menggeser objek"""
        return [(x + tx, y + ty) for x, y in points]
    
    def rotate(self, points, angle, cx, cy):
        """ROTASI: Memutar objek"""
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
        """REFLEKSI: Mencerminkan objek"""
        return [(x, 2 * axis_y - y) for x, y in points]
    
    # ========== KEYBOARD CONTROLS ==========
    
    def key_press(self, event):
        if event.keysym == 'Left':
            self.move_left = True
        elif event.keysym == 'Right':
            self.move_right = True
        elif event.keysym == 'Up':
            self.move_up = True
        elif event.keysym == 'Down':
            self.move_down = True
        elif event.keysym == 'space':
            self.shoot()
        elif event.keysym == 'r' and self.game_over:
            self.restart_game()
    
    def key_release(self, event):
        if event.keysym == 'Left':
            self.move_left = False
        elif event.keysym == 'Right':
            self.move_right = False
        elif event.keysym == 'Up':
            self.move_up = False
        elif event.keysym == 'Down':
            self.move_down = False
    
    # ========== GAME OBJECTS ==========
    
    def draw_player(self):
        """Menggambar pesawat player dengan ROTASI dan SKALA"""
        # Base spaceship shape (segitiga)
        ship = [
            (0, -20),   # Nose
            (-15, 15),  # Left wing
            (0, 10),    # Center
            (15, 15)    # Right wing
        ]
        
        # SKALA: Pulse effect
        ship = self.scale(ship, self.player_scale, self.player_scale, 0, 0)
        
        # ROTASI: Rotate based on angle
        ship = self.rotate(ship, self.player_angle, 0, 0)
        
        # TRANSLASI: Move to player position
        ship = self.translate(ship, self.player_x, self.player_y)
        
        # Draw ship
        self.draw_polygon(ship, '#00FFFF', '#0080FF')
        
        # Cockpit window
        self.midpoint_circle(int(self.player_x), int(self.player_y), 
                           int(5 * self.player_scale), '#FFFFFF', '#80FFFF')
        
        # Engine flames (DDA lines)
        flame_len = 10 + random.randint(0, 5)
        self.dda_line(self.player_x - 8, self.player_y + 12, 
                     self.player_x - 8, self.player_y + 12 + flame_len, '#FF6600', 3)
        self.dda_line(self.player_x + 8, self.player_y + 12, 
                     self.player_x + 8, self.player_y + 12 + flame_len, '#FF6600', 3)
        
        # REFLEKSI: Shield (mirror effect)
        if self.shield_active:
            for offset in range(3):
                radius = 35 + offset * 5
                self.midpoint_circle(int(self.player_x), int(self.player_y), 
                                   radius, '#00FFFF')
    
    def shoot(self):
        """Menembak peluru (TRANSLASI)"""
        if not self.game_over:
            bullet = {
                'x': self.player_x,
                'y': self.player_y - 20,
                'speed': 10
            }
            self.bullets.append(bullet)
    
    def draw_bullet(self, bullet):
        """Menggambar peluru dengan Bresenham"""
        x, y = bullet['x'], bullet['y']
        self.bresenham_line(int(x), int(y), int(x), int(y - 15), '#FFFF00', 3)
        # Glow effect
        self.midpoint_circle(int(x), int(y), 3, '#FFFF00', '#FFFF00')
    
    def spawn_enemy(self):
        """Spawn musuh (TRANSLASI dari atas)"""
        enemy_type = random.choice(['circle', 'polygon'])
        enemy = {
            'x': random.randint(30, self.width - 30),
            'y': -30,
            'speed': random.uniform(1, 3),
            'type': enemy_type,
            'angle': 0,
            'health': 1
        }
        self.enemies.append(enemy)
    
    def draw_enemy(self, enemy):
        """Menggambar musuh dengan ROTASI"""
        x, y = enemy['x'], enemy['y']
        
        if enemy['type'] == 'circle':
            # Alien bulat dengan animasi rotasi
            self.midpoint_circle(int(x), int(y), 15, '#FF0000', '#FF6666')
            # Eyes
            eye_offset = 5
            self.midpoint_circle(int(x - eye_offset), int(y - 3), 3, '#000000', '#FFFFFF')
            self.midpoint_circle(int(x + eye_offset), int(y - 3), 3, '#000000', '#FFFFFF')
            
        else:
            # Alien polygon (pentagon) dengan ROTASI
            pentagon = []
            sides = 6
            radius = 18
            for i in range(sides):
                angle = (360 / sides) * i + enemy['angle']
                rad = math.radians(angle)
                px = x + radius * math.cos(rad)
                py = y + radius * math.sin(rad)
                pentagon.append((px, py))
            
            self.draw_polygon(pentagon, '#00FF00', '#66FF66')
    
    def create_explosion(self, x, y):
        """Buat ledakan dengan SKALA (membesar)"""
        explosion = {
            'x': x,
            'y': y,
            'radius': 5,
            'max_radius': 40,
            'speed': 3
        }
        self.explosions.append(explosion)
    
    def draw_explosion(self, explosion):
        """Gambar ledakan dengan circle yang membesar (SKALA)"""
        x, y = explosion['x'], explosion['y']
        r = int(explosion['radius'])
        
        # Multi-layer explosion
        colors = ['#FF0000', '#FF6600', '#FFFF00']
        for i, color in enumerate(colors):
            radius = r - i * 5
            if radius > 0:
                self.midpoint_circle(int(x), int(y), radius, color, '')
        
        # Particles
        for i in range(8):
            angle = (360 / 8) * i
            rad = math.radians(angle)
            px = x + r * math.cos(rad)
            py = y + r * math.sin(rad)
            self.dda_line(int(x), int(y), int(px), int(py), '#FFAA00', 2)
    
    def spawn_powerup(self):
        """Spawn power-up dengan SKALA pulse"""
        powerup = {
            'x': random.randint(30, self.width - 30),
            'y': -20,
            'speed': 2,
            'scale': 1.0,
            'scale_dir': 1
        }
        self.powerups.append(powerup)
    
    def draw_powerup(self, powerup):
        """Gambar power-up dengan SKALA animasi"""
        x, y = powerup['x'], powerup['y']
        scale = powerup['scale']
        
        # Star shape (polygon)
        star = []
        for i in range(10):
            angle = (360 / 10) * i
            rad = math.radians(angle)
            r = 15 * scale if i % 2 == 0 else 7 * scale
            px = x + r * math.cos(rad)
            py = y + r * math.sin(rad)
            star.append((px, py))
        
        self.draw_polygon(star, '#FFD700', '#FFFF00')
        self.midpoint_circle(int(x), int(y), int(5 * scale), '#FFFFFF', '#FFFF00')
    
    def draw_stars(self):
        """Gambar bintang latar (TRANSLASI)"""
        for star in self.stars:
            self.canvas.create_oval(star['x']-1, star['y']-1, 
                                   star['x']+1, star['y']+1, 
                                   fill='#FFFFFF', outline='#FFFFFF')
    
    def draw_ui(self):
        """Gambar UI dan info box"""
        # Score
        self.canvas.create_text(self.width - 100, 30, 
                               text=f"SCORE: {self.score}", 
                               font=("Arial", 16, "bold"), fill='#FFFF00')
        
        # Lives
        for i in range(self.lives):
            heart_x = 30 + i * 35
            self.midpoint_circle(heart_x, 30, 10, '#FF0000', '#FF0000')
        
        # Info box transformasi (kiri atas)
        box_x = 10
        box_y = 60
        box_width = 280
        box_height = 110
        
        # Background
        self.canvas.create_rectangle(box_x + 2, box_y + 2, 
                                     box_x + box_width + 2, box_y + box_height + 2,
                                     fill='#000000', outline='')
        self.canvas.create_rectangle(box_x, box_y, 
                                     box_x + box_width, box_y + box_height,
                                     fill='#1A1A2E', outline='#0F3460', width=2)
        
        y_offset = box_y + 12
        self.canvas.create_text(box_x + 8, y_offset, 
                               text="⚙ TRANSFORMASI GEOMETRIS 2D", 
                               font=("Arial", 9, "bold"), fill='#EAEAEA', anchor='w')
        
        y_offset += 20
        self.canvas.create_text(box_x + 8, y_offset, 
                               text=f"→ Translasi: Pesawat X={int(self.player_x)}", 
                               font=("Arial", 8), fill='#00D9FF', anchor='w')
        
        y_offset += 18
        self.canvas.create_text(box_x + 8, y_offset, 
                               text=f"↻ Rotasi: Musuh berputar {int(self.player_angle)}°", 
                               font=("Arial", 8), fill='#FF6B6B', anchor='w')
        
        y_offset += 18
        self.canvas.create_text(box_x + 8, y_offset, 
                               text=f"⇄ Skala: Power-up pulse {self.player_scale:.2f}x", 
                               font=("Arial", 8), fill='#FFD93D', anchor='w')
        
        y_offset += 18
        shield_status = "AKTIF!" if self.shield_active else "non-aktif"
        self.canvas.create_text(box_x + 8, y_offset, 
                               text=f"⬇ Refleksi: Shield {shield_status}", 
                               font=("Arial", 8), fill='#6BCB77', anchor='w')
        
        # Controls hint
        self.canvas.create_text(self.width // 2, self.height - 20, 
                               text="Arrow Keys: Move | Space: Shoot", 
                               font=("Arial", 10), fill='#888888')
    
    def draw_game_over(self):
        """Tampilkan game over screen"""
        self.canvas.create_rectangle(200, 200, 600, 400, 
                                     fill='#000000', outline='#FF0000', width=3)
        self.canvas.create_text(400, 250, text="GAME OVER!", 
                               font=("Arial", 32, "bold"), fill='#FF0000')
        self.canvas.create_text(400, 300, text=f"Final Score: {self.score}", 
                               font=("Arial", 20), fill='#FFFFFF')
        self.canvas.create_text(400, 350, text="Press 'R' to Restart", 
                               font=("Arial", 16), fill='#00FF00')
    
    # ========== GAME LOGIC ==========
    
    def update_player(self):
        """Update posisi player (TRANSLASI)"""
        speed = 5
        
        if self.move_left and self.player_x > 30:
            self.player_x -= speed
        if self.move_right and self.player_x < self.width - 30:
            self.player_x += speed
        if self.move_up and self.player_y > 50:
            self.player_y -= speed
        if self.move_down and self.player_y < self.height - 50:
            self.player_y += speed
        
        # Subtle rotation animation
        self.player_angle = math.sin(self.enemy_spawn_timer / 10) * 5
        
        # Scale pulse animation (SKALA)
        self.player_scale += 0.01 * self.scale_direction
        if self.player_scale > 1.1:
            self.scale_direction = -1
        elif self.player_scale < 0.9:
            self.scale_direction = 1
        
        # Shield timer
        if self.shield_active:
            self.shield_timer -= 1
            if self.shield_timer <= 0:
                self.shield_active = False
    
    def update_bullets(self):
        """Update peluru (TRANSLASI ke atas)"""
        for bullet in self.bullets[:]:
            bullet['y'] -= bullet['speed']
            if bullet['y'] < -20:
                self.bullets.remove(bullet)
    
    def update_enemies(self):
        """Update musuh (TRANSLASI ke bawah + ROTASI)"""
        for enemy in self.enemies[:]:
            enemy['y'] += enemy['speed']
            enemy['angle'] += 2  # ROTASI kontinyu
            
            if enemy['y'] > self.height + 30:
                self.enemies.remove(enemy)
                if not self.shield_active:
                    self.lives -= 1
                    if self.lives <= 0:
                        self.game_over = True
    
    def update_explosions(self):
        """Update ledakan (SKALA membesar)"""
        for explosion in self.explosions[:]:
            explosion['radius'] += explosion['speed']
            if explosion['radius'] >= explosion['max_radius']:
                self.explosions.remove(explosion)
    
    def update_powerups(self):
        """Update power-ups (TRANSLASI + SKALA pulse)"""
        for powerup in self.powerups[:]:
            powerup['y'] += powerup['speed']
            
            # Scale animation (SKALA)
            powerup['scale'] += 0.05 * powerup['scale_dir']
            if powerup['scale'] > 1.3:
                powerup['scale_dir'] = -1
            elif powerup['scale'] < 0.8:
                powerup['scale_dir'] = 1
            
            if powerup['y'] > self.height + 30:
                self.powerups.remove(powerup)
    
    def update_stars(self):
        """Update bintang latar (TRANSLASI)"""
        for star in self.stars:
            star['y'] += star['speed']
            if star['y'] > self.height:
                star['y'] = 0
                star['x'] = random.randint(0, self.width)
    
    def check_collisions(self):
        """Cek collision antara objek"""
        # Bullet vs Enemy
        for bullet in self.bullets[:]:
            for enemy in self.enemies[:]:
                dx = bullet['x'] - enemy['x']
                dy = bullet['y'] - enemy['y']
                distance = math.sqrt(dx*dx + dy*dy)
                
                if distance < 20:
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    if enemy in self.enemies:
                        self.enemies.remove(enemy)
                    self.create_explosion(enemy['x'], enemy['y'])
                    self.score += 10
                    break
        
        # Player vs Enemy
        if not self.shield_active:
            for enemy in self.enemies[:]:
                dx = self.player_x - enemy['x']
                dy = self.player_y - enemy['y']
                distance = math.sqrt(dx*dx + dy*dy)
                
                if distance < 30:
                    self.enemies.remove(enemy)
                    self.create_explosion(self.player_x, self.player_y)
                    self.lives -= 1
                    if self.lives <= 0:
                        self.game_over = True
        
        # Player vs Powerup
        for powerup in self.powerups[:]:
            dx = self.player_x - powerup['x']
            dy = self.player_y - powerup['y']
            distance = math.sqrt(dx*dx + dy*dy)
            
            if distance < 30:
                self.powerups.remove(powerup)
                self.shield_active = True
                self.shield_timer = 180  # 6 seconds
                self.score += 50
    
    def restart_game(self):
        """Restart game"""
        self.game_over = False
        self.score = 0
        self.lives = 3
        self.player_x = self.width // 2
        self.player_y = self.height - 80
        self.bullets.clear()
        self.enemies.clear()
        self.explosions.clear()
        self.powerups.clear()
        self.shield_active = False
    
    # ========== MAIN GAME LOOP ==========
    
    def game_loop(self):
        """Main game loop"""
        self.canvas.delete('all')
        
        if not self.game_over:
            # Update background
            self.draw_stars()
            self.update_stars()
            
            # Update game objects
            self.update_player()
            self.update_bullets()
            self.update_enemies()
            self.update_explosions()
            self.update_powerups()
            self.check_collisions()
            
            # Spawn enemies
            self.enemy_spawn_timer += 1
            if self.enemy_spawn_timer > 60:  # Every 2 seconds
                self.spawn_enemy()
                self.enemy_spawn_timer = 0
            
            # Spawn power-ups
            self.powerup_timer += 1
            if self.powerup_timer > 300:  # Every 10 seconds
                self.spawn_powerup()
                self.powerup_timer = 0
            
            # Draw everything
            self.draw_player()
            
            for bullet in self.bullets:
                self.draw_bullet(bullet)
            
            for enemy in self.enemies:
                self.draw_enemy(enemy)
            
            for explosion in self.explosions:
                self.draw_explosion(explosion)
            
            for powerup in self.powerups:
                self.draw_powerup(powerup)
            
            self.draw_ui()
        else:
            self.draw_game_over()
        
        # Loop
        self.root.after(30, self.game_loop)


# ========== MAIN PROGRAM ==========
root = tk.Tk()
game = SpaceShooterGame(root)
root.mainloop()