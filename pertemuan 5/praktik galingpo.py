import turtle

# Setup Window
turtle.title("Computer Graphics: Line, Circle & Polygon Algorithms")
turtle.speed(0)
turtle.penup()

# --------------------- #
#   Algoritma Garis DDA #
# --------------------- #
def draw_line_DDA(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    steps = abs(dx) if abs(dx) > abs(dy) else abs(dy)

    x_inc = dx / steps
    y_inc = dy / steps

    x = x1
    y = y1

    for _ in range(int(steps) + 1):
        turtle.goto(round(x), round(y))
        turtle.dot(3, "black")
        x += x_inc
        y += y_inc


# ------------------------------------------------ #
#   Algoritma Midpoint Circle (8-way symmetry)     #
# ------------------------------------------------ #
def draw_circle_midpoint(xc, yc, r):
    x = 0
    y = r
    p = 1 - r

    plot_circle_points(xc, yc, x, y)

    while x < y:
        x += 1
        if p < 0:
            p += 2 * x + 1
        else:
            y -= 1
            p += 2 * (x - y) + 1

        plot_circle_points(xc, yc, x, y)


def plot_circle_points(xc, yc, x, y):
    points = [
        (xc + x, yc + y), (xc - x, yc + y),
        (xc + x, yc - y), (xc - x, yc - y),
        (xc + y, yc + x), (xc - y, yc + x),
        (xc + y, yc - x), (xc - y, yc - x)
    ]
    for px, py in points:
        turtle.goto(px, py)
        turtle.dot(3, "red")


# -------------------------------- #
#   Menggambar Poligon (DDA)       #
# -------------------------------- #
def draw_polygon(points):
    for i in range(len(points)):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % len(points)]
        draw_line_DDA(x1, y1, x2, y2)


# -------------------------------- #
#   Judul untuk setiap bagian      #
# -------------------------------- #
def draw_title(text, x, y):
    turtle.goto(x, y)
    turtle.write(text, align="center", font=("Arial", 14, "bold"))


# -------------------------------- #
#   DRAW AREA                      #
# -------------------------------- #

# Judul Garis
draw_title("GAMBAR GARIS (DDA)", 0, 250)
draw_line_DDA(-200, 200, 200, 200)

# Judul Lingkaran
draw_title("GAMBAR LINGKARAN (Midpoint Circle)", 0, 50)
draw_circle_midpoint(0, -50, 80)

# Judul Poligon
draw_title("GAMBAR POLIGON (Menggunakan DDA)", 0, -200)
polygon_points = [
    (-60, -250), (60, -250),
    (100, -300), (0, -350),
    (-100, -300)
]
draw_polygon(polygon_points)

turtle.hideturtle()
turtle.done()
