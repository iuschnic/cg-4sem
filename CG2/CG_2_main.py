import sys
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QMessageBox
import CG_2_image as imgs
import math as m

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Преобразования на плоскости")

        self.setStyleSheet("QLabel {font-size: 10pt}")
        self.setStyleSheet("QPushButton {font-size: 10pt}")
        self.setStyleSheet("QTableWidget {font-size: 10pt}")

        self.info = QtWidgets.QLabel()
        self.info.setText("Дана картинка из примитивов, реализовать ее смещение на заданное количество пикселей\n"
                          "реализовать ее масштабирование и поворот относительно произвольной точки")
        self.info.adjustSize()

        self.offset_button = QtWidgets.QPushButton()
        self.offset_button.setFixedWidth(400)
        self.offset_button.setText("Сдвиг (на dx, dy)")
        self.offset_button.clicked.connect(self.move_image)
        self.offset_button.setFont(QtGui.QFont("Times", 10))

        self.center_turn_button = QtWidgets.QPushButton()
        self.center_turn_button.setFixedWidth(400)
        self.center_turn_button.setText("Поворот (центр)")
        self.center_turn_button.clicked.connect(lambda: self.rotate_image(self.img.center.x, self.img.center.y))
        self.center_turn_button.setFont(QtGui.QFont("Times", 10))

        self.center_scale_button = QtWidgets.QPushButton()
        self.center_scale_button.setFixedWidth(400)
        self.center_scale_button.setText("Масштабирование (центр)")
        self.center_scale_button.clicked.connect(lambda: self.scale_image(self.img.center.x, self.img.center.y))
        self.center_scale_button.setFont(QtGui.QFont("Times", 10))

        self.dx_label = QtWidgets.QLabel()
        self.dx_label.setText("dx (смещение по х): ")
        self.dx_label.setFont(QtGui.QFont("Times", 10))

        self.dy_label = QtWidgets.QLabel()
        self.dy_label.setText("dy (смещение по у): ")
        self.dy_label.setFont(QtGui.QFont("Times", 10))

        self.dx = QtWidgets.QLineEdit()
        self.dx.setFont(QtGui.QFont("Times", 10))

        self.dy = QtWidgets.QLineEdit()
        self.dy.setFont(QtGui.QFont("Times", 10))

        self.x_label = QtWidgets.QLabel()
        self.x_label.setText("x (центр по х): ")
        self.x_label.setFont(QtGui.QFont("Times", 10))

        self.y_label = QtWidgets.QLabel()
        self.y_label.setText("y (центр по у): ")
        self.y_label.setFont(QtGui.QFont("Times", 10))

        self.x = QtWidgets.QLineEdit()
        self.x.setFont(QtGui.QFont("Times", 10))

        self.y = QtWidgets.QLineEdit()
        self.y.setFont(QtGui.QFont("Times", 10))

        self.angle_label = QtWidgets.QLabel()
        self.angle_label.setText("Угол поворота(градусы): ")
        self.angle_label.setFont(QtGui.QFont("Times", 10))

        self.angle = QtWidgets.QLineEdit()
        self.angle.setFont(QtGui.QFont("Times", 10))

        self.koef_x_label = QtWidgets.QLabel()
        self.koef_x_label.setText("Коэфициент масштабирования kx: ")
        self.koef_x_label.setFont(QtGui.QFont("Times", 10))

        self.koef_x = QtWidgets.QLineEdit()
        self.koef_x.setFont(QtGui.QFont("Times", 10))

        self.koef_y_label = QtWidgets.QLabel()
        self.koef_y_label.setText("Коэфициент масштабирования ky: ")
        self.koef_y_label.setFont(QtGui.QFont("Times", 10))

        self.koef_y = QtWidgets.QLineEdit()
        self.koef_y.setFont(QtGui.QFont("Times", 10))

        self.center_coords_label = QtWidgets.QLabel()
        self.center_coords_label.setText("Координаты центра:")
        self.center_coords_label.setFont(QtGui.QFont("Times", 10))

        self.center_coords = QtWidgets.QLabel()
        self.center_coords.setText("100 100")
        self.center_coords.setFont(QtGui.QFont("Times", 10))

        self.turn_button = QtWidgets.QPushButton()
        self.turn_button.setFixedWidth(400)
        self.turn_button.setText("Поворот (x, y)")
        self.turn_button.clicked.connect(lambda: self.rotate_image(None, None))
        self.turn_button.setFont(QtGui.QFont("Times", 10))

        self.scale_button = QtWidgets.QPushButton()
        self.scale_button.setFixedWidth(400)
        self.scale_button.setText("Масштабирование (x, y)")
        self.scale_button.clicked.connect(lambda: self.scale_image(None, None))
        self.scale_button.setFont(QtGui.QFont("Times", 10))

        self.center_button = QtWidgets.QPushButton()
        #self.center_button.setFixedWidth(400)
        self.center_button.setText("Центрировать изображение")
        self.center_button.adjustSize()
        self.center_button.clicked.connect(self.center_image)
        self.center_button.setFont(QtGui.QFont("Times", 10))
        
        self.cancel_op_button = QtWidgets.QPushButton()
        #self.cancel_op_button.setFixedWidth(400)
        self.cancel_op_button.setText("Отмена предыдущей операции")
        self.cancel_op_button.adjustSize()
        self.cancel_op_button.clicked.connect(self.return_op)
        self.cancel_op_button.setFont(QtGui.QFont("Times", 10))

        self.return_image_button = QtWidgets.QPushButton()
        self.return_image_button.setText("Вернуться к исходному")
        self.return_image_button.adjustSize()
        self.return_image_button.clicked.connect(self.return_image)
        self.return_image_button.setFont(QtGui.QFont("Times", 10))

        self.msg = QtWidgets.QMessageBox()
        self.msg.setFont(QtGui.QFont("Times", 10))

        self.canvas = QtWidgets.QLabel()
        self.canvas.move(0, 0)
        self.canvas.w = 1200
        self.canvas.h = 1000
        self.canvas.adjustSize()
        pixmap = QtGui.QPixmap(self.canvas.w, self.canvas.h)
        pixmap.fill(Qt.white)
        self.canvas.setPixmap(pixmap)
        self.canvas.setStyleSheet("border: 1px solid black;")

        self.img = imgs.image(self.canvas.w // 2, self.canvas.h // 2)
        self.last_op = ""

        w = QtWidgets.QWidget()
        start = QtWidgets.QVBoxLayout()
        start.addWidget(self.info)
        data = QtWidgets.QGridLayout()
        buttons1 = QtWidgets.QGridLayout()
        buttons2 = QtWidgets.QGridLayout()
        w.setLayout(start)

        data.addWidget(self.dx_label, 1, 0)
        data.addWidget(self.dx, 1, 1)
        data.addWidget(self.dy_label, 1, 2)
        data.addWidget(self.dy, 1, 3)

        data.addWidget(self.x_label, 2, 0)
        data.addWidget(self.x, 2, 1)
        data.addWidget(self.y_label, 2, 2)
        data.addWidget(self.y, 2, 3)

        data.addWidget(self.angle_label, 3, 0)
        data.addWidget(self.angle, 3, 1)

        data.addWidget(self.koef_x_label, 4, 0)
        data.addWidget(self.koef_x, 4, 1)

        data.addWidget(self.koef_y_label, 5, 0)
        data.addWidget(self.koef_y, 5, 1)

        data.addWidget(self.center_coords_label, 3, 2)
        data.addWidget(self.center_coords, 3, 3)

        buttons2.addWidget(self.cancel_op_button, 0, 0)
        buttons2.addWidget(self.return_image_button, 0, 1)
        buttons2.addWidget(self.center_button, 1, 0)
        buttons2.addWidget(self.offset_button, 1, 1)
        buttons2.addWidget(self.scale_button, 2, 0)
        buttons2.addWidget(self.turn_button, 2, 1)
        buttons2.addWidget(self.center_scale_button, 3, 0)
        buttons2.addWidget(self.center_turn_button, 3, 1)

        start.addLayout(data)
        start.addLayout(buttons1)
        start.addLayout(buttons2)
        start.addWidget(self.canvas)
        self.setCentralWidget(w)
        QTimer.singleShot(10, self.center_window)
        self.draw_img()


    def center_window(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def draw_img(self):
        pixmap = QtGui.QPixmap(self.canvas.w + 60, self.canvas.h)
        pixmap.fill(Qt.white)
        self.canvas.setPixmap(pixmap)
        painter = QtGui.QPainter(self.canvas.pixmap())
        pen = painter.pen()
        try:
            x = int(self.x.text())
            y = int(self.y.text())
            pen.setWidth(4)
            pen.setColor(QtGui.QColor('black'))
            painter.setPen(pen)
            painter.drawPoint(x, self.canvas.h - y)
            pen.setWidth(1)
            painter.drawText(x + 10, self.canvas.h - y - 10, "Центр")
        except ValueError:
            pass
        except Exception:
            pass
        self.center_coords.setText(f"[{int(self.img.center.x)}, {int(self.img.center.y)}]")
        pen.setWidth(1)
        pen.setColor(QtGui.QColor('black'))
        painter.setPen(pen)
        painter.drawLine(m.ceil(self.img.line1.p1.x), m.ceil(self.canvas.h - self.img.line1.p1.y),
                         m.ceil(self.img.line1.p2.x), m.ceil(self.canvas.h - self.img.line1.p2.y))
        painter.drawLine(m.ceil(self.img.line2.p1.x), m.ceil(self.canvas.h - self.img.line2.p1.y),
                         m.ceil(self.img.line2.p2.x), m.ceil(self.canvas.h - self.img.line2.p2.y))

        for i in range(0, len(self.img.ellipse.arr)):
            painter.drawLine(m.ceil(self.img.ellipse.arr[i].x), m.ceil(self.canvas.h - self.img.ellipse.arr[i].y),
                             m.ceil(self.img.ellipse.arr[i - 1].x), m.ceil(self.canvas.h - self.img.ellipse.arr[i - 1].y))

        painter.drawLine(m.ceil(self.img.square.p1.x), m.ceil(self.canvas.h - self.img.square.p1.y),
                         m.ceil(self.img.square.p2.x), m.ceil(self.canvas.h - self.img.square.p2.y))
        painter.drawLine(m.ceil(self.img.square.p2.x), m.ceil(self.canvas.h - self.img.square.p2.y),
                         m.ceil(self.img.square.p3.x), m.ceil(self.canvas.h - self.img.square.p3.y))
        painter.drawLine(m.ceil(self.img.square.p3.x), m.ceil(self.canvas.h - self.img.square.p3.y),
                         m.ceil(self.img.square.p4.x), m.ceil(self.canvas.h - self.img.square.p4.y))
        painter.drawLine(m.ceil(self.img.square.p4.x), m.ceil(self.canvas.h - self.img.square.p4.y),
                         m.ceil(self.img.square.p1.x), m.ceil(self.canvas.h - self.img.square.p1.y))

        painter.drawLine(m.ceil(self.img.romb.p1.x), m.ceil(self.canvas.h - self.img.romb.p1.y),
                         m.ceil(self.img.romb.p2.x), m.ceil(self.canvas.h - self.img.romb.p2.y))
        painter.drawLine(m.ceil(self.img.romb.p2.x), m.ceil(self.canvas.h - self.img.romb.p2.y),
                         m.ceil(self.img.romb.p3.x), m.ceil(self.canvas.h - self.img.romb.p3.y))
        painter.drawLine(m.ceil(self.img.romb.p3.x), m.ceil(self.canvas.h - self.img.romb.p3.y),
                         m.ceil(self.img.romb.p4.x), m.ceil(self.canvas.h - self.img.romb.p4.y))
        painter.drawLine(m.ceil(self.img.romb.p4.x), m.ceil(self.canvas.h - self.img.romb.p4.y),
                         m.ceil(self.img.romb.p1.x), m.ceil(self.canvas.h - self.img.romb.p1.y))

        # Отрисовка правого круглого крыла
        for i in range(1, len(self.img.wings.left_arr)):
            painter.drawLine(m.ceil(self.img.wings.left_arr[i].x), m.ceil(self.canvas.h - self.img.wings.left_arr[i].y),
                             m.ceil(self.img.wings.left_arr[i - 1].x), m.ceil(self.canvas.h - self.img.wings.left_arr[i - 1].y))
        # Отрисовка левого круглого крыла
        for i in range(1, len(self.img.wings.right_arr)):
            painter.drawLine(m.ceil(self.img.wings.right_arr[i].x), m.ceil(self.canvas.h - self.img.wings.right_arr[i].y),
                             m.ceil(self.img.wings.right_arr[i - 1].x), m.ceil(self.canvas.h - self.img.wings.right_arr[i - 1].y))

    # Функция вывода сообщения об ошибке
    def show_message(self, error):
        self.msg.setIcon(QMessageBox.Warning)
        self.msg.setText(error)
        self.msg.setWindowTitle("Info")
        retval = self.msg.exec_()

    def move_image(self):
        try:
            dx = int(self.dx.text())
            dy = int(self.dy.text())
            self.last_op = f"m,{-dx},{-dy}"
            self.img.move(dx, dy)
            self.draw_img()
        except ValueError:
            self.show_message("Ошибка ввода dx или dy")
            return -1
        except Exception:
            self.show_message("Неизвестная ошибка")
            return -2

    def rotate_image(self, x0, y0):
        try:
            if x0 == None:
                x0 = int(self.x.text())
                y0 = int(self.y.text())
            phi = float(self.angle.text())
            phi_rad = m.pi * (phi / 180)
            self.last_op = f"r,{int(x0)},{int(y0)},{-phi_rad}"
            self.img.rotate(int(x0), int(y0), phi_rad)
            self.draw_img()
            #print(f"{self.img.center.x}  {self.img.center.y}")
        except ValueError:
            self.show_message("Ошибка ввода угла или координат x, y")
            return -1
        except Exception:
            self.show_message("Неизвестная ошибка")
            return -2

    def scale_image(self, x0, y0):
        try:
            if x0 == None:
                x0 = int(self.x.text())
                y0 = int(self.y.text())
            kx = float(self.koef_x.text())
            ky = float(self.koef_y.text())
            self.last_op = f"s,{int(x0)},{int(y0)},{1 / kx},{1 / ky}"
            self.img.scale(int(x0), int(y0), kx, ky)
            self.draw_img()
        except ValueError:
            self.show_message("Ошибка ввода коэфициента или координат x, y")
            return -1
        except Exception:
            self.show_message("Неизвестная ошибка")
            return -2

    def center_image(self):
        dx = self.canvas.w // 2 - int(self.img.center.x)
        dy = self.canvas.h // 2 - int(self.img.center.y)
        self.img.move(dx, dy)
        self.draw_img()
        self.last_op = f"m,{-dx},{-dy}"

    def return_op(self):
        if self.last_op == "":
            self.show_message("Возможен возврат только на одну операцию")
            return
        params = self.last_op.split(',')
        #print(params)
        if params[0] == 'm':
            self.img.move(int(params[1]), int(params[2]))
        elif params[0] == 'r':
            self.img.rotate(int(params[1]), int(params[2]), float(params[3]))
        elif params[0] == 's':
            self.img.scale(int(params[1]), int(params[2]), float(params[3]), float(params[4]))
        self.draw_img()
        self.last_op = ""
        
    def return_image(self):
        self.img = imgs.image(self.canvas.w // 2, self.canvas.h // 2)
        self.draw_img()
        self.last_op = ""


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()