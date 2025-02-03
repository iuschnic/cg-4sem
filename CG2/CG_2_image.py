import math as m

class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.x += int(dx)
        self.y += int(dy)

    def scale(self, x0, y0, kx, ky):
        x1 = kx * self.x + x0 * (1 - kx)
        y1 = ky * self.y + y0 * (1 - ky)
        self.x = x1
        self.y = y1

    def rotate(self, x0, y0, phi_rad):
        x1 = x0 + (self.x - x0) * m.cos(phi_rad) + (self.y - y0) * m.sin(phi_rad)
        y1 = y0 - (self.x - x0) * m.sin(phi_rad) + (self.y - y0) * m.cos(phi_rad)
        self.x = x1
        self.y = y1

class line:
    def __init__(self, x1, y1, x2, y2):
        self.p1 = point(x1, y1)
        self.p2 = point(x2, y2)

    def move(self, dx, dy):
        self.p1.move(dx, dy)
        self.p2.move(dx, dy)

    def scale(self, x0, y0, kx, ky):
        self.p1.scale(x0, y0, kx, ky)
        self.p2.scale(x0, y0, kx, ky)

    def rotate(self, x0, y0, phi_rad):
        self.p1.rotate(x0, y0, phi_rad)
        self.p2.rotate(x0, y0, phi_rad)

'''class circle:
    def __init__(self, x, y, r):
        self.center = point(x, y)
        self.r = r

    def move(self, dx, dy):
        self.center.move(dx, dy)

    def scale(self, x0, y0, k):
        self.center.scale(x0, y0, k)
        self.r *= k

    def rotate(self, x0, y0, phi_rad):
        self.center.rotate(x0, y0, phi_rad)'''

class ellipse:
    def __init__(self, x, y, a, b):
        # центр эллипса
        self.center = point(x, y)
        # длины двух полуосей
        self.major_axis = a
        self.minor_axis = b
        # массив точек эллипса
        self.arr = []
        start = 0
        stop = m.pi * 2
        step = (stop - start) / 360
        # координаты центра эллипса
        x0 = self.center.x
        y0 = self.center.y
        while stop > start:
            # из уравнения эллипса в сферических координатах получаем новую точку эллипса
            x1 = self.major_axis * m.cos(start) + x0
            y1 = self.minor_axis * m.sin(start) + y0
            self.arr.append(point(x1, y1))
            start += step

    def move(self, dx, dy):
        self.center.move(dx, dy)
        for point in self.arr:
            point.move(dx, dy)

    def rotate(self, x0, y0, phi_rad):
        for point in self.arr:
            point.rotate(x0, y0, phi_rad)

    def scale(self, x0, y0, kx, ky):
        self.center.scale(x0, y0, kx, ky)
        for point in self.arr:
            point.scale(x0, y0, kx, ky)

# класс для отрисовки полуокружностей-крыльев
class half_ellipse:
    def __init__(self, x, y, a, b):
        # центр эллипса
        self.center = point(x, y)
        # длины двух полуосей
        self.major_axis = a
        self.minor_axis = b
        # массивы точек крыльев
        self.right_arr = []
        self.left_arr = []

        start = - m.pi / 2
        stop = m.pi / 2
        step = (stop - start) / 180
        # координаты центра эллипса
        x0 = self.center.x + 160
        y0 = self.center.y
        while stop > start:
            # из уравнения эллипса в сферических координатах получаем новую точку эллипса
            x1 = self.major_axis * m.cos(start) + x0
            y1 = self.minor_axis * m.sin(start) + y0
            self.right_arr.append(point(x1, y1))
            start += step

        start = m.pi / 2
        stop = 3 * m.pi / 2
        step = (stop - start) / 180
        # координаты центра эллипса
        x0 = self.center.x - 160
        y0 = self.center.y
        while stop > start:
            # из уравнения эллипса в сферических координатах получаем новую точку эллипса
            x1 = self.major_axis * m.cos(start) + x0
            y1 = self.minor_axis * m.sin(start) + y0
            self.left_arr.append(point(x1, y1))
            start += step

    def move(self, dx, dy):
        self.center.move(dx, dy)
        for point in self.left_arr:
            point.move(dx, dy)
        for point in self.right_arr:
            point.move(dx, dy)

    def rotate(self, x0, y0, phi_rad):
        self.center.rotate(x0, y0, phi_rad)
        for point in self.left_arr:
            point.rotate(x0, y0, phi_rad)
        for point in self.right_arr:
            point.rotate(x0, y0, phi_rad)

    def scale(self, x0, y0, kx, ky):
        self.center.scale(x0, y0, kx, ky)
        for point in self.left_arr:
            point.scale(x0, y0, kx, ky)
        for point in self.right_arr:
            point.scale(x0, y0, kx, ky)

class four_polygon:
    def __init__(self, x1, y1, x2, y2, x3, y3, x4, y4):
        self.p1 = point(x1, y1)
        self.p2 = point(x2, y2)
        self.p3 = point(x3, y3)
        self.p4 = point(x4, y4)

    def move(self, dx, dy):
        self.p1.move(dx, dy)
        self.p2.move(dx, dy)
        self.p3.move(dx, dy)
        self.p4.move(dx, dy)

    def scale(self, x0, y0, kx, ky):
        self.p1.scale(x0, y0, kx, ky)
        self.p2.scale(x0, y0, kx, ky)
        self.p3.scale(x0, y0, kx, ky)
        self.p4.scale(x0, y0, kx, ky)

    def rotate(self, x0, y0, phi_rad):
        self.p1.rotate(x0, y0, phi_rad)
        self.p2.rotate(x0, y0, phi_rad)
        self.p3.rotate(x0, y0, phi_rad)
        self.p4.rotate(x0, y0, phi_rad)


class image:
    def __init__(self, x, y):
        x = int(x)
        y = int(y)
        self.center = point(x, y)
        self.ellipse = ellipse(x, y, 40, 40)
        self.line1 = line(x, y - 40, x, y + 40)
        self.line2 = line(x - 40, y, x + 40, y)
        self.romb = four_polygon(x - 160, y, x, y + 80, x + 160, y, x, y - 80)
        self.square = four_polygon(x - 160, y + 80, x + 160, y + 80, x + 160, y - 80, x - 160, y - 80)
        self.wings = half_ellipse(x, y, 80, 80)

    def move(self, dx, dy):
        self.center.move(dx, dy)
        self.ellipse.move(dx, dy)
        self.line1.move(dx, dy)
        self.line2.move(dx, dy)
        self.romb.move(dx, dy)
        self.square.move(dx, dy)
        self.wings.move(dx, dy)

    def rotate(self, x0, y0, phi_rad):
        self.center.rotate(x0, y0, phi_rad)
        self.ellipse.rotate(x0, y0, phi_rad)
        self.line1.rotate(x0, y0, phi_rad)
        self.line2.rotate(x0, y0, phi_rad)
        self.romb.rotate(x0, y0, phi_rad)
        self.square.rotate(x0, y0, phi_rad)
        self.wings.rotate(x0, y0, phi_rad)
        
    def scale(self, x0, y0, kx, ky):
        self.center.scale(x0, y0, kx, ky)
        self.ellipse.scale(x0, y0, kx, ky)
        self.line1.scale(x0, y0, kx, ky)
        self.line2.scale(x0, y0, kx, ky)
        self.romb.scale(x0, y0, kx, ky)
        self.square.scale(x0, y0, kx, ky)
        self.wings.scale(x0, y0, kx, ky)
