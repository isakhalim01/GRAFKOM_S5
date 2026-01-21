
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

class Camera:
    def __init__(self):
        self.rotation_x = 25
        self.rotation_y = -45
        self.distance = 22
        self.pos_x = 0
        self.pos_y = -1
        
    def apply(self):
        glTranslatef(self.pos_x, self.pos_y, -self.distance)
        glRotatef(self.rotation_x, 1, 0, 0)
        glRotatef(self.rotation_y, 0, 1, 0)

def setup_lighting():
    """Setup pencahayaan untuk efek 3D yang lebih realistis"""
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    
    light_position = [2, 8, 3, 1]
    light_ambient = [0.4, 0.4, 0.4, 1]
    light_diffuse = [1, 1, 1, 1]
    light_specular = [0.8, 0.8, 0.8, 1]
    
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)

def draw_cube(width, height, depth, color):
    """Menggambar kubus dengan lighting"""
    w, h, d = width/2, height/2, depth/2
    glColor3fv(color)
    
    faces = [
        ([(-w,-h,d), (w,-h,d), (w,h,d), (-w,h,d)], (0,0,1)),      # Depan
        ([(-w,-h,-d), (-w,h,-d), (w,h,-d), (w,-h,-d)], (0,0,-1)), # Belakang
        ([(-w,h,-d), (-w,h,d), (w,h,d), (w,h,-d)], (0,1,0)),      # Atas
        ([(-w,-h,-d), (w,-h,-d), (w,-h,d), (-w,-h,d)], (0,-1,0)), # Bawah
        ([(-w,-h,-d), (-w,-h,d), (-w,h,d), (-w,h,-d)], (-1,0,0)), # Kiri
        ([(w,-h,-d), (w,h,-d), (w,h,d), (w,-h,d)], (1,0,0))       # Kanan
    ]
    
    for vertices, normal in faces:
        glBegin(GL_QUADS)
        glNormal3fv(normal)
        for vertex in vertices:
            glVertex3fv(vertex)
        glEnd()

def draw_sphere(radius, slices=20, stacks=20):
    """Menggambar bola dengan GLU"""
    quad = gluNewQuadric()
    gluSphere(quad, radius, slices, stacks)

def draw_cylinder(radius, height, slices=20):
    """Menggambar silinder"""
    glBegin(GL_QUAD_STRIP)
    for i in range(slices + 1):
        angle = 2 * math.pi * i / slices
        x = radius * math.cos(angle)
        z = radius * math.sin(angle)
        glNormal3f(x/radius, 0, z/radius)
        glVertex3f(x, height/2, z)
        glVertex3f(x, -height/2, z)
    glEnd()
    
    # Tutup atas dan bawah
    for y_pos, normal_y in [(height/2, 1), (-height/2, -1)]:
        glBegin(GL_TRIANGLE_FAN)
        glNormal3f(0, normal_y, 0)
        glVertex3f(0, y_pos, 0)
        for i in range(slices + 1):
            angle = 2 * math.pi * i / slices
            x = radius * math.cos(angle)
            z = radius * math.sin(angle)
            glVertex3f(x, y_pos, z)
        glEnd()

def draw_floor():
    """Lantai kayu parquet"""
    tile_size = 1.5
    tiles = 12
    
    for i in range(-tiles//2, tiles//2):
        for j in range(-tiles//2, tiles//2):
            if (i + j) % 2 == 0:
                color = (0.65, 0.45, 0.3)
            else:
                color = (0.6, 0.4, 0.25)
            
            glPushMatrix()
            glTranslatef(i * tile_size + tile_size/2, -3, j * tile_size + tile_size/2)
            draw_cube(tile_size, 0.08, tile_size, color)
            glPopMatrix()

def draw_walls():
    """Dinding ruang tamu"""
    # Dinding belakang - Krem
    glPushMatrix()
    glTranslatef(0, 2, -9)
    draw_cube(18, 10, 0.2, (0.92, 0.88, 0.82))
    glPopMatrix()
    
    # Dinding kiri - Abu-abu muda
    glPushMatrix()
    glTranslatef(-9, 2, 0)
    draw_cube(0.2, 10, 18, (0.88, 0.88, 0.88))
    glPopMatrix()
    
    # Dinding kanan - Putih
    glPushMatrix()
    glTranslatef(9, 2, 0)
    draw_cube(0.2, 10, 18, (0.95, 0.95, 0.95))
    glPopMatrix()
    
    # Plafon - Putih
    glPushMatrix()
    glTranslatef(0, 7, 0)
    draw_cube(18, 0.2, 18, (0.98, 0.98, 0.98))
    glPopMatrix()

def draw_coffee_table():
    """Meja kopi di tengah"""
    # Top meja - kaca (biru transparan)
    glPushMatrix()
    glTranslatef(0, -1.2, 0)
    draw_cube(2.5, 0.15, 1.5, (0.7, 0.85, 0.95))
    glPopMatrix()
    
    # Frame meja - hitam
    glPushMatrix()
    glTranslatef(0, -1.3, 0)
    draw_cube(2.6, 0.08, 1.6, (0.2, 0.2, 0.2))
    glPopMatrix()
    
    # Kaki meja modern (4 kaki silinder)
    leg_positions = [(-1, -2.1, -0.6), (1, -2.1, -0.6), (-1, -2.1, 0.6), (1, -2.1, 0.6)]
    for x, y, z in leg_positions:
        glPushMatrix()
        glTranslatef(x, y, z)
        glColor3f(0.15, 0.15, 0.15)
        draw_cylinder(0.08, 1.6, 12)
        glPopMatrix()

def draw_sofa(x, z, rotation, color=(0.3, 0.4, 0.6)):
    """Sofa modern 3 dudukan"""
    glPushMatrix()
    glTranslatef(x, 0, z)
    glRotatef(rotation, 0, 1, 0)
    
    # Dudukan utama
    glPushMatrix()
    glTranslatef(0, -1.8, 0)
    draw_cube(3, 0.6, 1.2, color)
    glPopMatrix()
    
    # Bantalan dudukan (cushion)
    for cx in [-0.9, 0, 0.9]:
        glPushMatrix()
        glTranslatef(cx, -1.45, 0)
        lighter_color = (color[0]*1.2, color[1]*1.2, color[2]*1.2)
        draw_cube(0.85, 0.3, 1.1, lighter_color)
        glPopMatrix()
    
    # Sandaran
    glPushMatrix()
    glTranslatef(0, -0.8, -0.55)
    draw_cube(3, 1.4, 0.3, color)
    glPopMatrix()
    
    # Bantalan sandaran
    for cx in [-0.9, 0, 0.9]:
        glPushMatrix()
        glTranslatef(cx, -0.8, -0.45)
        lighter_color = (color[0]*1.15, color[1]*1.15, color[2]*1.15)
        draw_cube(0.8, 1.2, 0.2, lighter_color)
        glPopMatrix()
    
    # Armrest kiri
    glPushMatrix()
    glTranslatef(-1.6, -1.2, 0)
    draw_cube(0.35, 1, 1.2, (color[0]*0.9, color[1]*0.9, color[2]*0.9))
    glPopMatrix()
    
    # Armrest kanan
    glPushMatrix()
    glTranslatef(1.6, -1.2, 0)
    draw_cube(0.35, 1, 1.2, (color[0]*0.9, color[1]*0.9, color[2]*0.9))
    glPopMatrix()
    
    # Kaki sofa
    for kx in [-1.3, -0.4, 0.4, 1.3]:
        for kz in [-0.5, 0.5]:
            glPushMatrix()
            glTranslatef(kx, -2.4, kz)
            glColor3f(0.2, 0.15, 0.1)
            draw_cylinder(0.06, 0.4, 8)
            glPopMatrix()
    
    glPopMatrix()

def draw_person_sitting(x, z, rotation):
    """Orang duduk di sofa"""
    glPushMatrix()
    glTranslatef(x, 0, z)
    glRotatef(rotation, 0, 1, 0)
    
    # Kepala
    glPushMatrix()
    glTranslatef(0, -0.3, 0.1)
    glColor3f(0.95, 0.8, 0.7)
    draw_sphere(0.35, 16, 16)
    glPopMatrix()
    
    # Rambut
    glPushMatrix()
    glTranslatef(0, -0.15, 0.1)
    draw_cube(0.5, 0.35, 0.5, (0.1, 0.05, 0.02))
    glPopMatrix()
    
    # Badan
    glPushMatrix()
    glTranslatef(0, -1.1, 0.15)
    draw_cube(0.8, 1.1, 0.45, (0.8, 0.3, 0.3))  # Baju merah
    glPopMatrix()
    
    # Lengan kiri
    glPushMatrix()
    glTranslatef(-0.55, -1.0, 0.15)
    glRotatef(20, 0, 0, 1)
    draw_cube(0.22, 0.9, 0.22, (0.75, 0.25, 0.25))
    glPopMatrix()
    
    # Lengan kanan
    glPushMatrix()
    glTranslatef(0.55, -1.0, 0.15)
    glRotatef(-20, 0, 0, 1)
    draw_cube(0.22, 0.9, 0.22, (0.75, 0.25, 0.25))
    glPopMatrix()
    
    # Tangan kiri
    glPushMatrix()
    glTranslatef(-0.7, -1.5, 0.15)
    glColor3f(0.9, 0.75, 0.65)
    draw_sphere(0.14, 12, 12)
    glPopMatrix()
    
    # Tangan kanan
    glPushMatrix()
    glTranslatef(0.7, -1.5, 0.15)
    glColor3f(0.9, 0.75, 0.65)
    draw_sphere(0.14, 12, 12)
    glPopMatrix()
    
    # Paha kiri
    glPushMatrix()
    glTranslatef(-0.3, -1.85, 0.3)
    draw_cube(0.32, 0.7, 0.32, (0.2, 0.2, 0.4))  # Celana biru
    glPopMatrix()
    
    # Paha kanan
    glPushMatrix()
    glTranslatef(0.3, -1.85, 0.3)
    draw_cube(0.32, 0.7, 0.32, (0.2, 0.2, 0.4))
    glPopMatrix()
    
    glPopMatrix()

def draw_person_standing(x, z, rotation):
    """Orang berdiri"""
    glPushMatrix()
    glTranslatef(x, 0, z)
    glRotatef(rotation, 0, 1, 0)
    
    # Kepala
    glPushMatrix()
    glTranslatef(0, 0.7, 0)
    glColor3f(0.92, 0.78, 0.68)
    draw_sphere(0.32, 16, 16)
    glPopMatrix()
    
    # Rambut
    glPushMatrix()
    glTranslatef(0, 0.85, 0)
    draw_cube(0.48, 0.3, 0.48, (0.15, 0.1, 0.05))
    glPopMatrix()
    
    # Badan
    glPushMatrix()
    glTranslatef(0, -0.2, 0)
    draw_cube(0.75, 1.4, 0.4, (0.3, 0.5, 0.7))  # Baju biru
    glPopMatrix()
    
    # Lengan kiri
    glPushMatrix()
    glTranslatef(-0.52, -0.1, 0)
    glRotatef(15, 0, 0, 1)
    draw_cube(0.22, 1.1, 0.22, (0.25, 0.45, 0.65))
    glPopMatrix()
    
    # Lengan kanan
    glPushMatrix()
    glTranslatef(0.52, -0.1, 0)
    glRotatef(-15, 0, 0, 1)
    draw_cube(0.22, 1.1, 0.22, (0.25, 0.45, 0.65))
    glPopMatrix()
    
    # Tangan kiri
    glPushMatrix()
    glTranslatef(-0.65, -0.7, 0)
    glColor3f(0.88, 0.72, 0.62)
    draw_sphere(0.13, 12, 12)
    glPopMatrix()
    
    # Tangan kanan
    glPushMatrix()
    glTranslatef(0.65, -0.7, 0)
    glColor3f(0.88, 0.72, 0.62)
    draw_sphere(0.13, 12, 12)
    glPopMatrix()
    
    # Celana kiri
    glPushMatrix()
    glTranslatef(-0.22, -1.5, 0)
    draw_cube(0.32, 1.3, 0.32, (0.15, 0.15, 0.2))
    glPopMatrix()
    
    # Celana kanan
    glPushMatrix()
    glTranslatef(0.22, -1.5, 0)
    draw_cube(0.32, 1.3, 0.32, (0.15, 0.15, 0.2))
    glPopMatrix()
    
    # Sepatu kiri
    glPushMatrix()
    glTranslatef(-0.22, -2.3, 0.1)
    draw_cube(0.35, 0.2, 0.5, (0.1, 0.1, 0.1))
    glPopMatrix()
    
    # Sepatu kanan
    glPushMatrix()
    glTranslatef(0.22, -2.3, 0.1)
    draw_cube(0.35, 0.2, 0.5, (0.1, 0.1, 0.1))
    glPopMatrix()
    
    glPopMatrix()

def draw_tv_stand():
    """Meja TV dengan TV"""
    glPushMatrix()
    glTranslatef(0, -1.5, -8)
    
    # Meja TV - coklat gelap
    draw_cube(4, 0.7, 1.2, (0.35, 0.25, 0.18))
    
    # TV Screen - hitam
    glPushMatrix()
    glTranslatef(0, 1.5, -0.3)
    draw_cube(3, 2, 0.15, (0.05, 0.05, 0.05))
    glPopMatrix()
    
    # TV Screen aktif - biru
    glPushMatrix()
    glTranslatef(0, 1.5, -0.22)
    draw_cube(2.8, 1.8, 0.05, (0.2, 0.3, 0.5))
    glPopMatrix()
    
    # Stand TV
    glPushMatrix()
    glTranslatef(0, 0.5, 0)
    draw_cube(0.8, 0.3, 0.8, (0.3, 0.3, 0.3))
    glPopMatrix()
    
    glPopMatrix()

def draw_ceiling_lamp():
    """Lampu gantung kristal"""
    glPushMatrix()
    glTranslatef(0, 6, 0)
    
    # Kabel
    glPushMatrix()
    glColor3f(0.15, 0.15, 0.15)
    draw_cylinder(0.04, 1.5, 10)
    glPopMatrix()
    
    # Holder atas
    glPushMatrix()
    glTranslatef(0, -1, 0)
    draw_cube(0.6, 0.3, 0.6, (0.8, 0.8, 0.8))
    glPopMatrix()
    
    # Lampu utama - kuning terang
    glPushMatrix()
    glTranslatef(0, -1.6, 0)
    glColor3f(1, 0.95, 0.7)
    draw_sphere(0.4, 16, 16)
    glPopMatrix()
    
    # Kristal menggantung
    for angle in [0, 90, 180, 270]:
        glPushMatrix()
        glRotatef(angle, 0, 1, 0)
        glTranslatef(0.35, -2, 0)
        glColor3f(0.9, 0.9, 1)
        draw_cylinder(0.05, 0.5, 8)
        glPopMatrix()
    
    glPopMatrix()

def draw_picture_frame(x, y, z, width, height):
    """Bingkai foto di dinding"""
    glPushMatrix()
    glTranslatef(x, y, z)
    
    # Frame - emas
    draw_cube(width + 0.2, height + 0.2, 0.08, (0.8, 0.7, 0.3))
    
    # Gambar - landscape
    glPushMatrix()
    glTranslatef(0, 0, 0.05)
    draw_cube(width, height, 0.02, (0.4, 0.6, 0.5))
    glPopMatrix()
    
    glPopMatrix()

def draw_plant():
    """Tanaman hias di pot"""
    glPushMatrix()
    glTranslatef(-6.5, -2, 6)
    
    # Pot - terakota
    glPushMatrix()
    glColor3f(0.7, 0.4, 0.3)
    draw_cylinder(0.35, 0.6, 16)
    glPopMatrix()
    
    # Tanah
    glPushMatrix()
    glTranslatef(0, 0.3, 0)
    draw_cube(0.6, 0.1, 0.6, (0.3, 0.2, 0.1))
    glPopMatrix()
    
    # Batang
    glPushMatrix()
    glTranslatef(0, 0.8, 0)
    glColor3f(0.2, 0.4, 0.1)
    draw_cylinder(0.08, 0.8, 8)
    glPopMatrix()
    
    # Daun (3 buah)
    for i, angle in enumerate([0, 120, 240]):
        glPushMatrix()
        glRotatef(angle, 0, 1, 0)
        glTranslatef(0.2, 1.2 + i*0.15, 0)
        glRotatef(45, 0, 0, 1)
        draw_cube(0.5, 0.05, 0.3, (0.3, 0.7, 0.2))
        glPopMatrix()
    
    glPopMatrix()

def draw_rug():
    """Karpet besar di tengah ruangan"""
    glPushMatrix()
    glTranslatef(0, -2.93, 0)
    draw_cube(6, 0.05, 4.5, (0.6, 0.25, 0.25))
    
    # Border karpet
    glTranslatef(0, 0.03, 0)
    draw_cube(5.7, 0.03, 4.2, (0.5, 0.2, 0.2))
    glPopMatrix()

def main():
    pygame.init()
    
    window_width = 1200
    window_height = 800
    display = (window_width, window_height)
    
    screen = pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Ruang Tamu 3D - Grafika Komputer [Drag: Rotate | Scroll: Zoom]")
    
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (display[0]/display[1]), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    
    setup_lighting()
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glClearColor(0.92, 0.92, 0.95, 1)
    
    camera = Camera()
    clock = pygame.time.Clock()
    
    mouse_down = False
    last_mouse_pos = (0, 0)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    camera = Camera()
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_down = True
                    last_mouse_pos = pygame.mouse.get_pos()
                elif event.button == 4:
                    camera.distance = max(10, camera.distance - 1)
                elif event.button == 5:
                    camera.distance = min(50, camera.distance + 1)
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_down = False
            
            elif event.type == pygame.MOUSEMOTION:
                if mouse_down:
                    current_pos = pygame.mouse.get_pos()
                    dx = current_pos[0] - last_mouse_pos[0]
                    dy = current_pos[1] - last_mouse_pos[1]
                    
                    camera.rotation_y += dx * 0.5
                    camera.rotation_x += dy * 0.5
                    camera.rotation_x = max(-89, min(89, camera.rotation_x))
                    
                    last_mouse_pos = current_pos
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: camera.pos_x += 0.15
        if keys[pygame.K_RIGHT]: camera.pos_x -= 0.15
        if keys[pygame.K_UP]: camera.pos_y -= 0.15
        if keys[pygame.K_DOWN]: camera.pos_y += 0.15
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        
        camera.apply()
        
        # Gambar ruangan
        draw_floor()
        draw_walls()
        draw_rug()
        draw_coffee_table()
        
        # Sofa menghadap meja (L-Shape arrangement)
        draw_sofa(0, 3.5, 180, (0.35, 0.45, 0.65))    # Depan (hadap ke TV)
        draw_sofa(-4, 0, 90, (0.4, 0.5, 0.7))         # Kiri
        draw_sofa(4, 0, -90, (0.38, 0.48, 0.68))      # Kanan
        draw_sofa(0, -3.5, 0, (0.37, 0.47, 0.67))     # Belakang
        
        # Orang duduk di sofa
        draw_person_sitting(-0.8, 3.5, 180)  # Depan kiri
        draw_person_sitting(0.8, 3.5, 180)   # Depan kanan
        draw_person_sitting(-4, 0, 90)        # Kiri
        
        # Orang berdiri dekat tanaman
        draw_person_standing(-5.5, 5, -135)
        
        # Furniture tambahan
        draw_tv_stand()
        draw_ceiling_lamp()
        draw_plant()
        
        # Dekorasi dinding
        draw_picture_frame(-6, 2, -8.8, 1.2, 0.9)
        draw_picture_frame(4, 2.5, -8.8, 1, 1.3)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()