import sys
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import Qt, QTimer
import time
from PyQt5.QtWidgets import QMessageBox
import math as m
import CG_5_alg as alg
import keyboard
from PyQt5.QtGui import QPixmap

eps = 0.0001
nano = 1000000000.0


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
        self.msg.setFont(QtGui.QFont("Times", 12))

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update)

        self.setStyleSheet("QLabel {font-size: 10pt}")
        self.setStyleSheet("QPushButton {font-size: 10pt}")
        self.setStyleSheet("QTableWidget {font-size: 10pt}")

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
        self.canvas.w = 1300
        self.canvas.h = 1300
        #self.canvas.adjustSize()
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
        self.fill_color.currentIndexChanged.connect(self.on_combobox_changed)

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
        self.input = QtWidgets.QPushButton()
        self.input.setText("Ввести")
        self.input.clicked.connect(self.manual_input)
        
        self.last_point = point(None, None)
        self.first_point = point(None, None)
        self.pnt_amount = 0

        w = QtWidgets.QWidget()
        w.setFont(QtGui.QFont("Times", 12))
        horiz = QtWidgets.QHBoxLayout()
        w.setLayout(horiz)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.table)
        layout.addWidget(self.label)
        layout.addWidget(self.x_label)
        layout.addWidget(self.x)
        layout.addWidget(self.y_label)
        layout.addWidget(self.y)
        layout.addWidget(self.input)
        layout.addWidget(self.clear_btn)
        layout.addWidget(self.fill_label)
        layout.addWidget(self.fill_color)
        layout.addWidget(self.close_btn)
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

    def get_color(self):
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
        self.pnt_amount = 0

    # Функция заливки холста
    def fill_canvas(self):
        self.pixmap = QtGui.QPixmap(self.canvas.w, self.canvas.h)
        self.pixmap.fill(inverted_color(QtGui.QColor(self.get_color())))
        self.canvas.setPixmap(self.pixmap)
        self.canvas.setStyleSheet("border: 1px solid black;")
        self.draw_by_table()

    def mousePressEvent(self, a0):
        # По непонятным причинам не регистрируется первое нажатие, работает только так
        keyboard.is_pressed("v")
        painter = QtGui.QPainter(self.canvas.pixmap())
        pen = painter.pen()
        pen.setWidth(1)
        pen.setColor(QtGui.QColor(self.get_color()))
        painter.setPen(pen)
        x0 = a0.x() - 530
        y0 = a0.y() - 20
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
        self.pixmap = self.canvas.pixmap()
        self.canvas.setPixmap(self.pixmap)

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
        pen.setColor(QtGui.QColor(self.get_color()))
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
        pen.setColor(QtGui.QColor(self.get_color()))
        painter.setPen(pen)
        try:
            for i in range(self.table.rowCount()):
                x0 = int(self.table.item(i, 0).text())
                y0 = int(self.table.item(i, 1).text())
                x1 = int(self.table.item(i, 2).text())
                y1 = int(self.table.item(i, 3).text())
                #painter.drawLine(x0, y0, x1, y1)
                self.draw_bres(x0, y0, x1, y1, painter)
            self.update()
        except ValueError:
            self.show_message("Ошибка в таблице")
            return
        except Exception:
            self.show_message("Неизвестная ошибка")
            return

    def on_combobox_changed(self):
        self.fill_canvas()

    def manual_input(self):
        painter = QtGui.QPainter(self.canvas.pixmap())
        pen = painter.pen()
        pen.setWidth(1)
        pen.setColor(QtGui.QColor(self.get_color()))
        painter.setPen(pen)
        try:
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
            self.pixmap = self.canvas.pixmap()
            self.canvas.setPixmap(self.pixmap)
        except ValueError:
            self.show_message("Ошибка ввода координат")
        except Exception:
            self.show_message("Неизвестная ошибка")

    def main_process(self):
        whole_start = time.perf_counter_ns()
        alg_time = 0.0
        whole_time = 0.0
        draw_time = 0.0

        painter = QtGui.QPainter(self.canvas.pixmap())
        pen = painter.pen()
        pen.setWidth(1)
        pen.setColor(QtGui.QColor(self.get_color()))
        painter.setPen(pen)
        x_max = -1
        try:
            start = time.perf_counter_ns()
            for i in range(self.table.rowCount()):
                x0 = int(self.table.item(i, 0).text())
                x1 = int(self.table.item(i, 2).text())
                if x0 > x_max:
                    x_max = x0
                if x1 > x_max:
                    x_max = x1
            alg_time += time.perf_counter_ns() - start
            # Цикл по всем ребрам в таблице
            for i in range(self.table.rowCount()):
                draw_time = 0.0
                start = time.perf_counter_ns()
                img = self.pixmap.toImage()
                x0 = int(self.table.item(i, 0).text())
                y0 = int(self.table.item(i, 1).text())
                x1 = int(self.table.item(i, 2).text())
                y1 = int(self.table.item(i, 3).text())
                if y0 == y1:
                    continue
                # dx - инкрементирующий шаг для поиска пересечения новой сканирующей строки с ребром
                if y0 > y1:
                    dx = 1.0 * (x0 - x1) / abs(y0 - y1)
                    y = y1
                    x = x1
                else:
                    dx = 1.0 * (x1 - x0) / abs(y0 - y1)
                    x = x0
                    y = y0
                alg_time += time.perf_counter_ns() - start
                # Цикл по сканирующим строкам
                start = time.perf_counter_ns()
                for j in range(abs(y0 - y1)):
                    x_start = m.ceil(x)
                    # Цикл по одной строке до ее конца
                    while x_start < x_max:
                        color = img.pixelColor(x_start, y)
                        draw_start = time.perf_counter_ns()
                        pen.setColor(inverted_color(color))
                        painter.setPen(pen)
                        painter.drawPoint(x_start, y)
                        draw_time += time.perf_counter_ns() - draw_start
                        x_start += 1
                    y += 1
                    x += dx
                alg_time += time.perf_counter_ns() - start - draw_time
            pen.setColor(QtGui.QColor(self.get_color()))
            painter.setPen(pen)
            for i in range(self.table.rowCount()):
                x0 = int(self.table.item(i, 0).text())
                y0 = int(self.table.item(i, 1).text())
                x1 = int(self.table.item(i, 2).text())
                y1 = int(self.table.item(i, 3).text())
                #painter.drawLine(x0, y0, x1, y1)
                self.draw_bres(x0, y0, x1, y1, painter)
            self.update()
            whole_time = time.perf_counter_ns() - whole_start
            self.alg_time.setText(f"{alg_time / nano} с.")
            self.whole_time.setText(f"{whole_time / nano} с.")
        except ValueError:
            self.show_message("Ошибка в таблице")
            return
        except Exception:
            self.show_message("Неизвестная ошибка")
            return


    def step_process(self):
        painter = QtGui.QPainter(self.canvas.pixmap())
        pen = painter.pen()
        pen.setWidth(1)
        pen.setColor(QtGui.QColor(self.get_color()))
        painter.setPen(pen)
        x_max = -1
        try:
            for i in range(self.table.rowCount()):
                x0 = int(self.table.item(i, 0).text())
                x1 = int(self.table.item(i, 2).text())
                if x0 > x_max:
                    x_max = x0
                if x1 > x_max:
                    x_max = x1
            # Цикл по всем ребрам в таблице
            for i in range(self.table.rowCount()):
                img = self.pixmap.toImage()
                x0 = int(self.table.item(i, 0).text())
                y0 = int(self.table.item(i, 1).text())
                x1 = int(self.table.item(i, 2).text())
                y1 = int(self.table.item(i, 3).text())
                if y0 == y1:
                    continue
                # dx - инкрементирующий шаг для поиска пересечения новой сканирующей строки с ребром
                if y0 > y1:
                    dx = 1.0 * (x0 - x1) / abs(y0 - y1)
                    y = y1
                    x = x1
                else:
                    dx = 1.0 * (x1 - x0) / abs(y0 - y1)
                    x = x0
                    y = y0

                # Цикл по сканирующим строкам
                for j in range(abs(y0 - y1)):
                    x_start = m.ceil(x)
                    # Цикл по одной строке до ее конца
                    while x_start < x_max:
                        color = img.pixelColor(x_start, y)
                        pen.setColor(inverted_color(color))
                        painter.setPen(pen)
                        painter.drawPoint(x_start, y)
                        x_start += 1
                    self.update()
                    QtCore.QCoreApplication.processEvents()
                    time.sleep(0.01)
                    y += 1
                    x += dx
            self.update()
            pen.setColor(QtGui.QColor(self.get_color()))
            painter.setPen(pen)
            for i in range(self.table.rowCount()):
                x0 = int(self.table.item(i, 0).text())
                y0 = int(self.table.item(i, 1).text())
                x1 = int(self.table.item(i, 2).text())
                y1 = int(self.table.item(i, 3).text())
                #painter.drawLine(x0, y0, x1, y1)
                self.draw_bres(x0, y0, x1, y1, painter)
            self.pixmap = self.canvas.pixmap()
            self.canvas.setPixmap(self.pixmap)

        except ValueError:
            self.show_message("Ошибка в таблице")
            return
        except Exception:
            self.show_message("Неизвестная ошибка")
            return

    def update(self):
        self.pixmap = self.canvas.pixmap()
        self.canvas.setPixmap(self.pixmap)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
