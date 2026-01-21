import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

class Cube3DTransform:
    def __init__(self):
        # Definisi titik-titik kubus (vertices)
        self.original_vertices = np.array([
            [-1, -1, -1], [1, -1, -1], [1, 1, -1], [-1, 1, -1],  # Sisi belakang
            [-1, -1, 1], [1, -1, 1], [1, 1, 1], [-1, 1, 1]       # Sisi depan
        ])
        
        # Sisi-sisi kubus (faces)
        self.faces = [
            [0, 1, 2, 3],  # Belakang
            [4, 5, 6, 7],  # Depan
            [0, 1, 5, 4],  # Bawah
            [2, 3, 7, 6],  # Atas
            [0, 3, 7, 4],  # Kiri
            [1, 2, 6, 5]   # Kanan
        ]
        
        self.vertices = self.original_vertices.copy()
        self.setup_plot()
        
    def setup_plot(self):
        """Setup plot dan kontrol interaktif"""
        self.fig = plt.figure(figsize=(14, 8))
        self.fig.suptitle('Transformasi 3D: Kubus Interaktif', fontsize=16, fontweight='bold')
        
        # Plot utama
        self.ax = self.fig.add_subplot(111, projection='3d')
        plt.subplots_adjust(left=0.05, bottom=0.35, right=0.95, top=0.95)
        
        # === TRANSLASI ===
        ax_tx = plt.axes([0.15, 0.25, 0.3, 0.02])
        ax_ty = plt.axes([0.15, 0.22, 0.3, 0.02])
        ax_tz = plt.axes([0.15, 0.19, 0.3, 0.02])
        
        self.slider_tx = Slider(ax_tx, 'Trans X', -5, 5, valinit=0, color='#ff6b6b')
        self.slider_ty = Slider(ax_ty, 'Trans Y', -5, 5, valinit=0, color='#4ecdc4')
        self.slider_tz = Slider(ax_tz, 'Trans Z', -5, 5, valinit=0, color='#45b7d1')
        
        # === ROTASI ===
        ax_rx = plt.axes([0.60, 0.25, 0.3, 0.02])
        ax_ry = plt.axes([0.60, 0.22, 0.3, 0.02])
        ax_rz = plt.axes([0.60, 0.19, 0.3, 0.02])
        
        self.slider_rx = Slider(ax_rx, 'Rotasi X', 0, 360, valinit=0, color='#ff6b6b')
        self.slider_ry = Slider(ax_ry, 'Rotasi Y', 0, 360, valinit=0, color='#4ecdc4')
        self.slider_rz = Slider(ax_rz, 'Rotasi Z', 0, 360, valinit=0, color='#45b7d1')
        
        # === SKALA ===
        ax_scale = plt.axes([0.15, 0.14, 0.3, 0.02])
        self.slider_scale = Slider(ax_scale, 'Skala', 0.1, 3, valinit=1, color='#95e1d3')
        
        # === REFLEKSI ===
        ax_ref_x = plt.axes([0.60, 0.14, 0.08, 0.04])
        ax_ref_y = plt.axes([0.70, 0.14, 0.08, 0.04])
        ax_ref_z = plt.axes([0.80, 0.14, 0.08, 0.04])
        
        self.btn_ref_x = Button(ax_ref_x, 'Refleksi X', color='#ff6b6b', hovercolor='#ff8787')
        self.btn_ref_y = Button(ax_ref_y, 'Refleksi Y', color='#4ecdc4', hovercolor='#6ed9d0')
        self.btn_ref_z = Button(ax_ref_z, 'Refleksi Z', color='#45b7d1', hovercolor='#6bc5db')
        
        # Tombol Reset
        ax_reset = plt.axes([0.15, 0.08, 0.15, 0.04])
        self.btn_reset = Button(ax_reset, 'Reset Semua', color='#f39c12', hovercolor='#f5b041')
        
        # Status refleksi
        self.reflect_x = False
        self.reflect_y = False
        self.reflect_z = False
        
        # Event handlers
        self.slider_tx.on_changed(self.update)
        self.slider_ty.on_changed(self.update)
        self.slider_tz.on_changed(self.update)
        self.slider_rx.on_changed(self.update)
        self.slider_ry.on_changed(self.update)
        self.slider_rz.on_changed(self.update)
        self.slider_scale.on_changed(self.update)
        
        self.btn_ref_x.on_clicked(self.toggle_reflect_x)
        self.btn_ref_y.on_clicked(self.toggle_reflect_y)
        self.btn_ref_z.on_clicked(self.toggle_reflect_z)
        self.btn_reset.on_clicked(self.reset_all)
        
        self.draw_cube()
        
    def translate(self, vertices, tx, ty, tz):
        """TRANSLASI 3D: Menggeser objek ke posisi lain"""
        translation_matrix = np.array([tx, ty, tz])
        return vertices + translation_matrix
    
    def rotate_x(self, vertices, angle):
        """ROTASI 3D: Rotasi terhadap sumbu X"""
        rad = np.radians(angle)
        rotation_matrix = np.array([
            [1, 0, 0],
            [0, np.cos(rad), -np.sin(rad)],
            [0, np.sin(rad), np.cos(rad)]
        ])
        return np.dot(vertices, rotation_matrix.T)
    
    def rotate_y(self, vertices, angle):
        """ROTASI 3D: Rotasi terhadap sumbu Y"""
        rad = np.radians(angle)
        rotation_matrix = np.array([
            [np.cos(rad), 0, np.sin(rad)],
            [0, 1, 0],
            [-np.sin(rad), 0, np.cos(rad)]
        ])
        return np.dot(vertices, rotation_matrix.T)
    
    def rotate_z(self, vertices, angle):
        """ROTASI 3D: Rotasi terhadap sumbu Z"""
        rad = np.radians(angle)
        rotation_matrix = np.array([
            [np.cos(rad), -np.sin(rad), 0],
            [np.sin(rad), np.cos(rad), 0],
            [0, 0, 1]
        ])
        return np.dot(vertices, rotation_matrix.T)
    
    def scale(self, vertices, factor):
        """SKALA 3D: Mengubah ukuran objek"""
        scale_matrix = np.array([
            [factor, 0, 0],
            [0, factor, 0],
            [0, 0, factor]
        ])
        return np.dot(vertices, scale_matrix.T)
    
    def reflect(self, vertices, axis):
        """REFLEKSI 3D: Mencerminkan objek terhadap sumbu"""
        reflection_matrix = np.eye(3)
        if axis == 'x':
            reflection_matrix[0, 0] = -1
        elif axis == 'y':
            reflection_matrix[1, 1] = -1
        elif axis == 'z':
            reflection_matrix[2, 2] = -1
        return np.dot(vertices, reflection_matrix.T)
    
    def apply_transformations(self):
        """Menerapkan semua transformasi secara berurutan"""
        vertices = self.original_vertices.copy()
        
        # 1. SKALA
        scale_factor = self.slider_scale.val
        vertices = self.scale(vertices, scale_factor)
        
        # 2. ROTASI (X -> Y -> Z)
        vertices = self.rotate_x(vertices, self.slider_rx.val)
        vertices = self.rotate_y(vertices, self.slider_ry.val)
        vertices = self.rotate_z(vertices, self.slider_rz.val)
        
        # 3. REFLEKSI
        if self.reflect_x:
            vertices = self.reflect(vertices, 'x')
        if self.reflect_y:
            vertices = self.reflect(vertices, 'y')
        if self.reflect_z:
            vertices = self.reflect(vertices, 'z')
        
        # 4. TRANSLASI (terakhir)
        vertices = self.translate(vertices, 
                                 self.slider_tx.val,
                                 self.slider_ty.val,
                                 self.slider_tz.val)
        
        return vertices
    
    def draw_cube(self):
        """Menggambar kubus dengan transformasi"""
        self.ax.clear()
        
        # Terapkan transformasi
        self.vertices = self.apply_transformations()
        
        # Buat faces untuk ditampilkan
        face_vertices = []
        for face in self.faces:
            face_vertices.append([self.vertices[i] for i in face])
        
        # Warna gradient untuk setiap sisi
        colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#f39c12', '#9b59b6', '#1abc9c']
        
        # Gambar kubus
        poly = Poly3DCollection(face_vertices, alpha=0.8, linewidths=2, edgecolors='black')
        poly.set_facecolor(colors)
        self.ax.add_collection3d(poly)
        
        # Gambar titik-titik vertices
        self.ax.scatter(self.vertices[:, 0], self.vertices[:, 1], self.vertices[:, 2],
                       c='red', s=100, marker='o', edgecolors='black', linewidths=2)
        
        # Gambar sumbu koordinat
        axis_length = 6
        self.ax.plot([0, axis_length], [0, 0], [0, 0], 'r-', linewidth=2, label='X')
        self.ax.plot([0, 0], [0, axis_length], [0, 0], 'g-', linewidth=2, label='Y')
        self.ax.plot([0, 0], [0, 0], [0, axis_length], 'b-', linewidth=2, label='Z')
        
        # Setting plot
        self.ax.set_xlabel('X', fontsize=12, fontweight='bold')
        self.ax.set_ylabel('Y', fontsize=12, fontweight='bold')
        self.ax.set_zlabel('Z', fontsize=12, fontweight='bold')
        
        limit = 8
        self.ax.set_xlim([-limit, limit])
        self.ax.set_ylim([-limit, limit])
        self.ax.set_zlim([-limit, limit])
        
        # Info transformasi
        info_text = f'Transformasi Aktif:\n'
        info_text += f'Translasi: ({self.slider_tx.val:.1f}, {self.slider_ty.val:.1f}, {self.slider_tz.val:.1f})\n'
        info_text += f'Rotasi: X={self.slider_rx.val:.0f}° Y={self.slider_ry.val:.0f}° Z={self.slider_rz.val:.0f}°\n'
        info_text += f'Skala: {self.slider_scale.val:.2f}\n'
        info_text += f'Refleksi: X={self.reflect_x} Y={self.reflect_y} Z={self.reflect_z}'
        
        self.ax.text2D(0.02, 0.98, info_text, transform=self.ax.transAxes,
                      fontsize=9, verticalalignment='top',
                      bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
        
        self.ax.legend(loc='upper right')
        self.ax.grid(True, alpha=0.3)
        
    def update(self, val):
        """Update gambar saat slider berubah"""
        self.draw_cube()
        plt.draw()
    
    def toggle_reflect_x(self, event):
        """Toggle refleksi sumbu X"""
        self.reflect_x = not self.reflect_x
        self.update(None)
    
    def toggle_reflect_y(self, event):
        """Toggle refleksi sumbu Y"""
        self.reflect_y = not self.reflect_y
        self.update(None)
    
    def toggle_reflect_z(self, event):
        """Toggle refleksi sumbu Z"""
        self.reflect_z = not self.reflect_z
        self.update(None)
    
    def reset_all(self, event):
        """Reset semua transformasi"""
        self.slider_tx.reset()
        self.slider_ty.reset()
        self.slider_tz.reset()
        self.slider_rx.reset()
        self.slider_ry.reset()
        self.slider_rz.reset()
        self.slider_scale.reset()
        self.reflect_x = False
        self.reflect_y = False
        self.reflect_z = False
        self.update(None)
    
    def show(self):
        """Tampilkan plot"""
        plt.show()

# Jalankan program
if __name__ == "__main__":
    
    cube = Cube3DTransform()
    cube.show()