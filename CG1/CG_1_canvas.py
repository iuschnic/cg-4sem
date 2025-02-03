import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox
import math as m

class CanvasWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Решение в геометрическом виде")
        self.canvas = QtWidgets.QLabel()
        self.canvas.move(0, 0)
        self.canvas.w = 650
        self.canvas.h = 650
        self.borders = 40
        pixmap = QtGui.QPixmap(self.canvas.w + 60, self.canvas.h)
        pixmap.fill(Qt.white)
        self.canvas.setPixmap(pixmap)
        self.canvas.setStyleSheet("border: 1px solid black;")

        self.answer = QtWidgets.QLabel()
        self.answer.setFont(QtGui.QFont("Times", 10))

        w = QtWidgets.QWidget()
        l = QtWidgets.QHBoxLayout()
        w.setLayout(l)
        l.addWidget(self.canvas)
        l.addWidget(self.answer)

        self.setCentralWidget(w)

    # Функция отрисовки координатных прямых
    def draw_coord_lines(self, left, right, up, down):
        pixmap = QtGui.QPixmap(self.canvas.w + 60, self.canvas.h)
        pixmap.fill(Qt.white)
        self.canvas.setPixmap(pixmap)
        painter = QtGui.QPainter(self.canvas.pixmap())
        pen = painter.pen()
        pen.setWidth(1)
        pen.setColor(QtGui.QColor('black'))
        painter.setPen(pen)
        start = (self.borders, self.canvas.h - self.borders)
        endx = (self.canvas.w - 10, self.canvas.h - self.borders)
        endy = (self.borders, 10)
        painter.drawLine(start[0], start[1], endx[0], endx[1])
        painter.drawLine(start[0], start[1], endy[0], endy[1])

        painter.drawLine(endx[0], endx[1], endx[0] - 10, endx[1] - 3)
        painter.drawLine(endx[0], endx[1], endx[0] - 10, endx[1] + 3)

        painter.drawLine(endy[0], endy[1], endy[0] + 3, endy[1] + 10)
        painter.drawLine(endy[0], endy[1], endy[0] - 3, endy[1] + 10)

        painter.drawText(endx[0], endx[1] + 15, "x")
        painter.drawText(endy[0] - 15, endy[1], "y")

        step = (self.canvas.w - self.borders - 10) // 6
        step_x = (right - left) / (self.canvas.w - self.borders)
        coordx = left
        summ_step = 0
        for i in range(0, 6):
            painter.drawLine(summ_step + self.borders, self.canvas.h - (self.borders - 15),
                             summ_step + self.borders, self.canvas.h - (self.borders + 5))
            painter.drawText(summ_step + self.borders + 4, self.canvas.h - (self.borders - 15), f"{coordx:5.2f}")
            summ_step += step
            coordx += step_x * step

        step = (self.canvas.h - self.borders - 10) // 6
        step_y = (up - down) / (self.canvas.h - self.borders)
        coordy = down
        summ_step = 0
        for i in range(0, 6):
            painter.drawLine(self.borders - 15, self.canvas.h - (summ_step + self.borders),
                             self.borders + 5, self.canvas.h - (summ_step + self.borders))
            painter.drawText(self.borders - 35, self.canvas.h - (summ_step + self.borders + 4), f"{coordy:5.2f}")
            summ_step += step
            coordy += step_y * step

    def convert_coords(self, left, right, up, down, x, y):
        dx = x - left
        dy = y - down
        # сколько единиц измерения укладывается в пикселе
        per_pixel = (right - left) / (self.canvas.w - self.borders)
        pix_x = int(m.floor(dx / per_pixel)) + self.borders
        pix_y = self.canvas.h - (int(m.floor(dy / per_pixel)) + self.borders)
        return pix_x, pix_y

    def draw_point(self, left, right, up, down, x, y, pntnum, color):
        painter = QtGui.QPainter(self.canvas.pixmap())
        pen = painter.pen()
        pen.setWidth(5)
        pen.setColor(QtGui.QColor(color))
        painter.setPen(pen)
        pix_x, pix_y = self.convert_coords(left, right, up, down, x, y)
        painter.drawPoint(pix_x, pix_y)
        painter.drawText(pix_x + 3, pix_y - 5, f"{pntnum}: [{x:5.2f}, {y:5.2f}]")

    def draw_circle(self, left, right, up, down, x, y, r, color):
        painter = QtGui.QPainter(self.canvas.pixmap())
        pen = painter.pen()
        pen.setWidth(5)
        pen.setColor(QtGui.QColor(color))
        painter.setPen(pen)
        pix_x, pix_y = self.convert_coords(left, right, up, down, x, y)
        per_pixel = (right - left) / (self.canvas.w - self.borders)
        pix_r = r // per_pixel
        painter.drawPoint(pix_x, pix_y)
        pen.setWidth(1)
        painter.setPen(pen)
        painter.drawEllipse(pix_x - pix_r, pix_y - pix_r, pix_r * 2, pix_r * 2)

    def draw_line(self, left, right, up, down, pnt1, pnt2, color):
        x1 = pnt1[0]
        y1 = pnt1[1]
        x2 = pnt2[0]
        y2 = pnt2[1]
        painter = QtGui.QPainter(self.canvas.pixmap())
        pen = painter.pen()
        pen.setWidth(1)
        pen.setColor(QtGui.QColor(color))
        painter.setPen(pen)
        pix_x1, pix_y1 = self.convert_coords(left, right, up, down, x1, y1)
        pix_x2, pix_y2 = self.convert_coords(left, right, up, down, x2, y2)
        painter.drawLine(pix_x1, pix_y1, pix_x2, pix_y2)

