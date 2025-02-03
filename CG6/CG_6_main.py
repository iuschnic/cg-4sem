import sys
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import Qt, QTimer
import time
from PyQt5.QtWidgets import QMessageBox
import math as m
import CG_6_alg as alg
import keyboard
from PyQt5.QtGui import QPixmap

eps = 0.0001
nano = 1000000000.0

shift_x = 565
shift_y = 20


def sign(x):
    if x < 0:
        return -1
    return 1


class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def inverted_color(color: QtGui.QColor):
    return QtGui.QColor(255 - color.red(), 255 - color.green(), 255 - color.blue())


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Алгоритмы заполнения")

        self.msg = QtWidgets.QMessageBox()
        self.msg.setFont(QtGui.QFont("Times", 10))

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update)

        self.setStyleSheet("QLabel {font-size: 10pt}")
        self.setStyleSheet("QPushButton {font-size: 10pt}")
        self.setStyleSheet("QTableWidget {font-size: 10pt}")

        self.squares = QtWidgets.QRadioButton()
        self.squares.setText("Рисование многоугольников")
        self.pixels = QtWidgets.QRadioButton()
        self.pixels.setText("Рисование произвольных кривых")
        self.seed = QtWidgets.QRadioButton()
        self.seed.setText("Установка затравки")

        self.group = QtWidgets.QButtonGroup()
        self.group.addButton(self.squares, 1)
        self.group.addButton(self.pixels, 2)
        self.group.addButton(self.seed, 3)
        self.squares.setChecked(True)

        self.last_x = None
        self.last_y = None

        self.seed_pnt = point(None, None)

        self.seed_label = QtWidgets.QLabel()
        self.seed_label.setText("Координаты затравки: --- ---")

        self.table = QtWidgets.QTableWidget(self)
        self.table.setFont(QtGui.QFont("Times", 10))
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            ["x0", "y0", "x1", "y1"])
        self.table.resizeColumnsToContents()

        self.alg_time_label = QtWidgets.QLabel()
        self.alg_time_label.setText("Чистое время работы алгоритма:")
        self.alg_time = QtWidgets.QLabel()
        self.alg_time.setText("--------")

        self.whole_time_label = QtWidgets.QLabel()
        self.whole_time_label.setText("Время работы с отрисовкой:")
        self.whole_time = QtWidgets.QLabel()
        self.whole_time.setText("--------")

        self.main_process_btn = QtWidgets.QPushButton()
        self.main_process_btn.setFixedWidth(500)
        self.main_process_btn.setText("Заполнить область")
        self.main_process_btn.clicked.connect(lambda: self.main_process())

        self.main_wait_btn = QtWidgets.QPushButton()
        self.main_wait_btn.setFixedWidth(500)
        self.main_wait_btn.setText("Заполнить область пошагово")
        self.main_wait_btn.clicked.connect(lambda: self.step_process())

        self.close_btn = QtWidgets.QPushButton()
        self.close_btn.setFixedWidth(500)
        self.close_btn.setText("Замкнуть")
        self.close_btn.clicked.connect(self.close)

        self.canvas = QtWidgets.QLabel()
        #self.canvas.move(0, 0)
        self.canvas.w = 1600
        self.canvas.h = 1500
        # self.canvas.adjustSize()
        self.pixmap = QtGui.QPixmap(self.canvas.w, self.canvas.h)
        self.pixmap.fill(Qt.white)
        self.canvas.setPixmap(self.pixmap)
        self.canvas.setStyleSheet("border: 1px solid black;")

        self.fill_label = QtWidgets.QLabel()
        self.fill_label.setText("Цвет заполнения:")

        self.fill_color = QtWidgets.QComboBox()
        self.fill_color.addItem("Черный")
        self.fill_color.addItem("Красный")
        self.fill_color.addItem("Синий")

        self.border_label = QtWidgets.QLabel()
        self.border_label.setText("Цвет границы:")

        self.border_color = QtWidgets.QComboBox()
        self.border_color.addItem("Черный")
        self.border_color.addItem("Красный")
        self.border_color.addItem("Синий")

        self.clear_btn = QtWidgets.QPushButton()
        self.clear_btn.setText("Очистить холст")
        self.clear_btn.clicked.connect(self.clear_all)

        self.label = QtWidgets.QLabel()
        self.label.setText("Введите точку:")
        self.x_label = QtWidgets.QLabel()
        self.x_label.setText("x:")
        self.y_label = QtWidgets.QLabel()
        self.y_label.setText("y:")
        self.x = QtWidgets.QLineEdit()
        self.y = QtWidgets.QLineEdit()
        self.input_node = QtWidgets.QPushButton()
        self.input_node.setText("Ввести вершину (x, y)")
        self.input_node.clicked.connect(lambda: self.manual_input(0))
        self.input_seed = QtWidgets.QPushButton()
        self.input_seed.setText("Ввести затравку(x, y)")
        self.input_seed.clicked.connect(lambda: self.manual_input(1))

        self.last_point = point(None, None)
        self.first_point = point(None, None)
        self.pnt_amount = 0

        w = QtWidgets.QWidget()
        w.setFont(QtGui.QFont("Times", 12))
        horiz = QtWidgets.QHBoxLayout()
        w.setLayout(horiz)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.table)
        layout.addWidget(self.seed_label)
        layout.addWidget(self.label)
        layout.addWidget(self.x_label)
        layout.addWidget(self.x)
        layout.addWidget(self.y_label)
        layout.addWidget(self.y)
        layout.addWidget(self.input_node)
        layout.addWidget(self.input_seed)
        layout.addWidget(self.clear_btn)
        layout.addWidget(self.fill_label)
        layout.addWidget(self.fill_color)
        layout.addWidget(self.border_label)
        layout.addWidget(self.border_color)
        layout.addWidget(self.close_btn)
        layout.addWidget(self.squares)
        layout.addWidget(self.pixels)
        layout.addWidget(self.seed)
        layout.addWidget(self.main_process_btn)
        layout.addWidget(self.main_wait_btn)
        layout.addWidget(self.alg_time_label)
        layout.addWidget(self.alg_time)
        layout.addWidget(self.whole_time_label)
        layout.addWidget(self.whole_time)
        horiz.addLayout(layout)
        horiz.addWidget(self.canvas)
        self.setCentralWidget(w)
        QTimer.singleShot(10, self.center_window)

    def center_window(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def get_border_color(self):
        if self.border_color.currentIndex() == 0:
            return 'black'
        elif self.border_color.currentIndex() == 1:
            return 'red'
        elif self.border_color.currentIndex() == 2:
            return 'blue'

    def get_fill_color(self):
        if self.fill_color.currentIndex() == 0:
            return 'black'
        elif self.fill_color.currentIndex() == 1:
            return 'red'
        elif self.fill_color.currentIndex() == 2:
            return 'blue'

    def set_color(self, color):
        self.colors.setCurrentIndex(color)

    def show_message(self, error):
        self.msg.setIcon(QMessageBox.Warning)
        self.msg.setText(error)
        self.msg.setWindowTitle("Info")
        retval = self.msg.exec_()

    # Функция очистки таблицы и холста
    def clear_all(self):
        self.table.clearContents()
        while self.table.rowCount() > 0:
            self.table.removeRow(self.table.rowCount() - 1)
        self.fill_canvas()
        self.first_point = point(None, None)
        self.last_point = point(None, None)
        self.seed_pnt = point(None, None)
        self.seed_label.setText("Координаты затравки: --- ---")
        self.pnt_amount = 0

    # Функция заливки холста
    def fill_canvas(self):
        self.pixmap = QtGui.QPixmap(self.canvas.w, self.canvas.h)
        self.pixmap.fill(QtGui.QColor('white'))
        self.canvas.setPixmap(self.pixmap)
        self.canvas.setStyleSheet("border: 1px solid black;")
        self.draw_by_table()

    def mouseMoveEvent(self, a0):
        if self.group.checkedId() != 2:
            return
        if not self.last_x:
            self.last_x = a0.x() - shift_x
            self.last_y = a0.y() - shift_y
            return
        painter = QtGui.QPainter(self.canvas.pixmap())
        pen = painter.pen()
        pen.setWidth(1)
        pen.setColor(QtGui.QColor(self.get_border_color()))
        painter.setPen(pen)
        painter.drawLine(self.last_x, self.last_y, a0.x() - shift_x, a0.y() - shift_y)
        painter.end()
        self.update()
        self.last_x = a0.x() - shift_x
        self.last_y = a0.y() - shift_y

    def mouseReleaseEvent(self, a0):
        self.last_x = None
        self.last_y = None

    def mousePressEvent(self, a0):
        if self.group.checkedId() == 1:
            # По непонятным причинам не регистрируется первое нажатие, работает только так
            keyboard.is_pressed("v")
            x0 = a0.x() - shift_x
            y0 = a0.y() - shift_y
            painter = QtGui.QPainter(self.canvas.pixmap())
            pen = painter.pen()
            pen.setWidth(1)
            pen.setColor(QtGui.QColor(self.get_border_color()))
            painter.setPen(pen)
            if x0 < 0 or y0 < 0:
                return
            if x0 > self.canvas.w or y0 > self.canvas.height():
                return
            if not self.last_point.x:
                painter.drawPoint(x0, y0)
                self.last_point = point(x0, y0)
                self.first_point = point(x0, y0)
            else:
                if keyboard.is_pressed("v"):
                    '''painter.drawLine(self.last_point.x, self.last_point.y,
                                     self.last_point.x, y0)'''
                    self.draw_bres(self.last_point.x, self.last_point.y,
                                   self.last_point.x, y0, painter)
                    self.add_data(self.last_point.x, self.last_point.y,
                                  self.last_point.x, y0)
                    self.last_point = point(self.last_point.x, y0)
                elif keyboard.is_pressed("h"):
                    '''painter.drawLine(self.last_point.x, self.last_point.y,
                                     x0, self.last_point.y)'''
                    self.draw_bres(self.last_point.x, self.last_point.y,
                                   x0, self.last_point.y, painter)
                    self.add_data(self.last_point.x, self.last_point.y,
                                  x0, self.last_point.y)
                    self.last_point = point(x0, self.last_point.y)
                else:
                    '''painter.drawLine(self.last_point.x, self.last_point.y,
                                     x0, y0)'''
                    self.draw_bres(self.last_point.x, self.last_point.y,
                                   x0, y0, painter)
                    self.add_data(self.last_point.x, self.last_point.y,
                                  x0, y0)
                    self.last_point = point(x0, y0)
            self.pnt_amount += 1
            self.update()

        elif self.group.checkedId() == 3:
            x0 = a0.x() - shift_x
            y0 = a0.y() - shift_y
            if x0 < 0 or y0 < 0:
                self.show_message("Точка выходит за границы холста")
                return
            if x0 > self.canvas.w or y0 > self.canvas.height():
                self.show_message("Точка выходит за границы холста")
                return
            painter = QtGui.QPainter(self.canvas.pixmap())
            pen = painter.pen()
            pen.setWidth(1)
            pen.setColor(QtGui.QColor(self.get_fill_color()))
            painter.setPen(pen)
            self.seed_pnt = point(x0, y0)
            painter.drawPoint(x0, y0)
            self.seed_label.setText(f"Координаты затравки: {x0} {y0}")
            self.update()

    def add_data(self, x0, y0, x1, y1):
        pos = self.table.rowCount()
        self.table.insertRow(pos)
        item = QtWidgets.QTableWidgetItem(f"{x0}")
        item.setFlags(item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
        self.table.setItem(pos, 0, item)
        item = QtWidgets.QTableWidgetItem(f"{y0}")
        item.setFlags(item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
        self.table.setItem(pos, 1, item)
        item = QtWidgets.QTableWidgetItem(f"{x1}")
        item.setFlags(item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
        self.table.setItem(pos, 2, item)
        item = QtWidgets.QTableWidgetItem(f"{y1}")
        item.setFlags(item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
        self.table.setItem(pos, 3, item)

    def draw_bres(self, x0, y0, x1, y1, painter):
        array = alg.bresenham_integers([x0, y0, x1, y1])
        if not array:
            return -1
        for elem in array:
            painter.drawPoint(elem[0], elem[1])
        self.update()

    def close(self):
        if self.pnt_amount < 3:
            self.show_message("Введите минимум три точки для замыкания текущей фигуры")
            return
        painter = QtGui.QPainter(self.canvas.pixmap())
        pen = painter.pen()
        pen.setWidth(1)
        pen.setColor(QtGui.QColor(self.get_border_color()))
        painter.setPen(pen)
        '''painter.drawLine(self.last_point.x, self.last_point.y, 
                         self.first_point.x, self.first_point.y)'''
        self.draw_bres(self.last_point.x, self.last_point.y,
                       self.first_point.x, self.first_point.y, painter)
        self.add_data(self.last_point.x, self.last_point.y,
                      self.first_point.x, self.first_point.y)
        self.pixmap = self.canvas.pixmap()
        self.canvas.setPixmap(self.pixmap)
        self.last_point = point(None, None)
        self.first_point = point(None, None)
        self.pnt_amount = 0

    def draw_by_table(self):
        painter = QtGui.QPainter(self.canvas.pixmap())
        pen = painter.pen()
        pen.setWidth(1)
        pen.setColor(QtGui.QColor(self.get_border_color()))
        painter.setPen(pen)
        try:
            for i in range(self.table.rowCount()):
                x0 = int(self.table.item(i, 0).text())
                y0 = int(self.table.item(i, 1).text())
                x1 = int(self.table.item(i, 2).text())
                y1 = int(self.table.item(i, 3).text())
                # painter.drawLine(x0, y0, x1, y1)
                self.draw_bres(x0, y0, x1, y1, painter)
            self.update()
        except ValueError:
            self.show_message("Ошибка в таблице")
            return
        except Exception:
            self.show_message("Неизвестная ошибка")
            return

    def manual_input(self, opt):
        try:
            if opt == 0:
                painter = QtGui.QPainter(self.canvas.pixmap())
                pen = painter.pen()
                pen.setWidth(1)
                pen.setColor(QtGui.QColor(self.get_border_color()))
                painter.setPen(pen)
                x0 = float(self.x.text())
                y0 = float(self.y.text())
                if x0 < 0 or y0 < 0:
                    self.show_message("Точка выходит за границы холста")
                    return
                if x0 > self.canvas.w or y0 > self.canvas.height():
                    self.show_message("Точка выходит за границы холста")
                    return
                x0 = int(x0)
                y0 = int(y0)
                if not self.last_point.x:
                    painter.drawPoint(x0, y0)
                    self.last_point = point(x0, y0)
                    self.first_point = point(x0, y0)
                else:
                    if keyboard.is_pressed("v"):
                        '''painter.drawLine(self.last_point.x, self.last_point.y,
                                         self.last_point.x, y0)'''
                        self.draw_bres(self.last_point.x, self.last_point.y,
                                       self.last_point.x, y0, painter)
                        self.add_data(self.last_point.x, self.last_point.y,
                                      self.last_point.x, y0)
                        self.last_point = point(self.last_point.x, y0)
                    elif keyboard.is_pressed("h"):
                        '''painter.drawLine(self.last_point.x, self.last_point.y,
                                         x0, self.last_point.y)'''
                        self.draw_bres(self.last_point.x, self.last_point.y,
                                       x0, self.last_point.y, painter)
                        self.add_data(self.last_point.x, self.last_point.y,
                                      x0, self.last_point.y)
                        self.last_point = point(x0, self.last_point.y)
                    else:
                        '''painter.drawLine(self.last_point.x, self.last_point.y,
                                         x0, y0)'''
                        self.draw_bres(self.last_point.x, self.last_point.y,
                                       x0, y0, painter)
                        self.add_data(self.last_point.x, self.last_point.y,
                                      x0, y0)
                        self.last_point = point(x0, y0)
                self.pnt_amount += 1
                self.update()
            elif opt == 1:
                painter = QtGui.QPainter(self.canvas.pixmap())
                pen = painter.pen()
                pen.setWidth(1)
                pen.setColor(QtGui.QColor(self.get_fill_color()))
                painter.setPen(pen)
                x0 = float(self.x.text())
                y0 = float(self.y.text())
                if x0 < 0 or y0 < 0:
                    self.show_message("Точка выходит за границы холста")
                    return
                if x0 > self.canvas.w or y0 > self.canvas.height():
                    self.show_message("Точка выходит за границы холста")
                    return
                x0 = int(x0)
                y0 = int(y0)
                self.seed_pnt = point(x0, y0)
                painter.drawPoint(x0, y0)
                self.seed_label.setText(f"Координаты затравки: {x0} {y0}")
                self.update()


        except ValueError:
            self.show_message("Ошибка ввода координат")
        except Exception:
            self.show_message("Неизвестная ошибка")

    def main_process(self):
        draw_time = 0.0
        whole_time = time.perf_counter_ns()
        draw_start = time.perf_counter_ns()
        if not self.seed_pnt.x:
            self.show_message("Требуется ввод затравочного пикселя")
            return
        painter = QtGui.QPainter(self.canvas.pixmap())
        pen = painter.pen()
        pen.setWidth(1)
        pen.setColor(QtGui.QColor(self.get_fill_color()))
        painter.setPen(pen)
        draw_time += time.perf_counter_ns() - draw_start
        alg_time = time.perf_counter_ns()
        stack = []
        stack.append(self.seed_pnt)
        draw_start = time.perf_counter_ns()
        border_color = QtGui.QColor(self.get_border_color())
        fill_color = QtGui.QColor(self.get_fill_color())
        draw_time += time.perf_counter_ns() - draw_start
        y = 1
        while len(stack) > 0 and 0 < y < self.canvas.h:
            cur = stack.pop()
            draw_start = time.perf_counter_ns()
            img = self.pixmap.toImage()
            painter.drawPoint(cur.x, cur.y)
            draw_time += time.perf_counter_ns() - draw_start
            x = cur.x
            y = cur.y
            x_temp = x
            x = x - 1
            # Для начала ищем самый левый и самый правый пиксель очередной заполняемой строки
            while img.pixelColor(x, y) != border_color and x > 0:
                draw_start = time.perf_counter_ns()
                painter.drawPoint(x, y)
                draw_time += time.perf_counter_ns() - draw_start
                x -= 1
            x_left = x + 1
            x = x_temp + 1
            while img.pixelColor(x, y) != border_color and x < self.canvas.w:
                draw_start = time.perf_counter_ns()
                painter.drawPoint(x, y)
                draw_time += time.perf_counter_ns() - draw_start
                x += 1
            x_right = x - 1
            if x_right == x_left:
                if img.pixelColor(x_right, y + 1) != border_color and img.pixelColor(x_right, y + 1) != fill_color:
                    stack.append(point(x_right, y + 1))
                if img.pixelColor(x_right, y - 1) != border_color and img.pixelColor(x_right, y - 1) != fill_color:
                    stack.append(point(x_right, y - 1))
                continue
            # x_left, x_right - крайние заполненные пиксели
            # Теперь проверим верхнюю и нижнюю строки на заполненность, попробуем там найти еще затравки
            x = x_left
            y = y - 1

            while x <= x_right:
                flag = 0
                cur_color = img.pixelColor(x, y)
                # Пробегаем все доступные пустые пиксели
                while cur_color != border_color and cur_color != fill_color and x < x_right:
                    if flag == 0:
                        flag = 1
                    x += 1
                    cur_color = img.pixelColor(x, y)
                cur_color = img.pixelColor(x, y)
                # Если флаг == 0, то мы еще не заполняли пиксели -> не находили затравочный
                # Заносим найденный затравочный пиксель в стек
                if flag == 1:
                    if x == x_right and cur_color != border_color and cur_color != fill_color:
                        stack.append(point(x, y))
                    else:
                        stack.append(point(x - 1, y))
                # Если пиксель с x_left на следующей строке попадает в границу фигуры, пробегаем эту границу
                x_last = x
                cur_color = img.pixelColor(x, y)
                while (cur_color == border_color or cur_color == fill_color) and x < x_right:
                    x += 1
                    cur_color = img.pixelColor(x, y)
                if x_last == x:
                    x += 1
            x = x_left
            # Этот if нужен для корректного заполнения всего холста, без него заполняется только нижняя половина
            if y < self.canvas.h - 2:
                y = y + 2
                while x <= x_right:
                    flag = 0
                    cur_color = img.pixelColor(x, y)
                    # Пробегаем все доступные пустые пиксели и заполняем их
                    while cur_color != border_color and cur_color != fill_color and x < x_right:
                        if flag == 0:
                            flag = 1
                        x += 1
                        cur_color = img.pixelColor(x, y)
                    cur_color = img.pixelColor(x, y)
                    # Если флаг == 0, то мы еще не заполняли пиксели -> не находили затравочный
                    # Заносим найденный затравочный пиксель в стек
                    if flag == 1:
                        if x == x_right and cur_color != border_color and cur_color != fill_color:
                            stack.append(point(x, y))
                        else:
                            stack.append(point(x - 1, y))
                    # Если пиксель с x_left на следующей строке попадает в границу фигуры, пробегаем эту границу
                    x_last = x
                    cur_color = img.pixelColor(x, y)
                    while (cur_color == border_color or cur_color == fill_color) and x < x_right:
                        x += 1
                        cur_color = img.pixelColor(x, y)
                    if x_last == x:
                        x += 1
        self.alg_time.setText(f"{(time.perf_counter_ns() - alg_time - draw_time) / nano} с.")
        self.update()
        self.whole_time.setText(f"{(time.perf_counter_ns() - whole_time) / nano} с.")

    def step_process(self):
        if not self.seed_pnt.x:
            self.show_message("Требуется ввод затравочного пикселя")
            return
        painter = QtGui.QPainter(self.canvas.pixmap())
        pen = painter.pen()
        pen.setWidth(1)
        pen.setColor(QtGui.QColor(self.get_fill_color()))
        painter.setPen(pen)
        stack = []
        stack.append(self.seed_pnt)
        border_color = QtGui.QColor(self.get_border_color())
        fill_color = QtGui.QColor(self.get_fill_color())
        y = 1
        while len(stack) > 0 and 0 < y < self.canvas.h:
            img = self.pixmap.toImage()
            cur = stack.pop()
            painter.drawPoint(cur.x, cur.y)
            x = cur.x
            y = cur.y
            x_temp = x
            x = x - 1
            # Для начала ищем самый левый и самый правый пиксель очередной заполняемой строки
            while img.pixelColor(x, y) != border_color and x > 0:
                painter.drawPoint(x, y)
                x -= 1
            x_left = x + 1
            x = x_temp
            x = x + 1
            while img.pixelColor(x, y) != border_color and x < self.canvas.w:
                painter.drawPoint(x, y)
                x += 1
            x_right = x - 1
            if x_right == x_left:
                if img.pixelColor(x_right, y + 1) != border_color and img.pixelColor(x_right, y + 1) != fill_color:
                    stack.append(point(x_right, y + 1))
                if img.pixelColor(x_right, y - 1) != border_color and img.pixelColor(x_right, y - 1) != fill_color:
                    stack.append(point(x_right, y - 1))
                self.update()
                QtCore.QCoreApplication.processEvents()
                continue
            # x_left, x_right - крайние заполненные пиксели
            # Теперь проверим верхнюю и нижнюю строки на заполненность, попробуем там найти еще затравки
            x = x_left
            y = y - 1

            while x <= x_right:
                flag = 0
                cur_color = img.pixelColor(x, y)
                # Пробегаем все доступные пустые пиксели
                while cur_color != border_color and cur_color != fill_color and x < x_right:
                    if flag == 0:
                        flag = 1
                    x += 1
                    cur_color = img.pixelColor(x, y)
                cur_color = img.pixelColor(x, y)
                # Если флаг == 0, то мы еще не заполняли пиксели -> не находили затравочный
                # Заносим найденный затравочный пиксель в стек
                if flag == 1:
                    if x == x_right and cur_color != border_color and cur_color != fill_color:
                        stack.append(point(x, y))
                    else:
                        stack.append(point(x - 1, y))
                # Если пиксель с x_left на следующей строке попадает в границу фигуры, пробегаем эту границу
                x_last = x
                cur_color = img.pixelColor(x, y)
                while (cur_color == border_color or cur_color == fill_color) and x < x_right:
                    x += 1
                    cur_color = img.pixelColor(x, y)
                if x_last == x:
                    x += 1
            x = x_left
            # Этот if нужен для корректного заполнения всего холста, без него заполняется только нижняя половина
            if y < self.canvas.h - 2:
                y = y + 2
                while x <= x_right:
                    flag = 0
                    cur_color = img.pixelColor(x, y)
                    # Пробегаем все доступные пустые пиксели и заполняем их
                    while cur_color != border_color and cur_color != fill_color and x < x_right:
                        if flag == 0:
                            flag = 1
                        x += 1
                        cur_color = img.pixelColor(x, y)
                    cur_color = img.pixelColor(x, y)
                    # Если флаг == 0, то мы еще не заполняли пиксели -> не находили затравочный
                    # Заносим найденный затравочный пиксель в стек
                    if flag == 1:
                        if x == x_right and cur_color != border_color and cur_color != fill_color:
                            stack.append(point(x, y))
                        else:
                            stack.append(point(x - 1, y))
                    # Если пиксель с x_left на следующей строке попадает в границу фигуры, пробегаем эту границу
                    x_last = x
                    cur_color = img.pixelColor(x, y)
                    while (cur_color == border_color or cur_color == fill_color) and x < x_right:
                        x += 1
                        cur_color = img.pixelColor(x, y)
                    if x_last == x:
                        x += 1
            self.update()
            QtCore.QCoreApplication.processEvents()

    def update(self):
        self.pixmap = self.canvas.pixmap()
        self.canvas.setPixmap(self.pixmap)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
