import sys
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QMessageBox
import keyboard
from CG_8_alg import point, cut, check_convex, inside_normal

eps = 0.0001
nano = 1000000000.0

shift_x = 660
shift_y = 20

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Алгоритм отсечения выпуклым отсекателем")

        self.msg = QtWidgets.QMessageBox()
        self.msg.setFont(QtGui.QFont("Times", 10))

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update)

        self.setStyleSheet("QLabel {font-size: 10pt}")
        self.setStyleSheet("QPushButton {font-size: 10pt}")
        self.setStyleSheet("QTableWidget {font-size: 10pt}")

        self.clipper = QtWidgets.QRadioButton()
        self.clipper.setText("Рисование отсекателя")
        self.lines = QtWidgets.QRadioButton()
        self.lines.setText("Рисование отрезков")

        self.close_btn = QtWidgets.QPushButton()
        self.close_btn.setFixedWidth(500)
        self.close_btn.setText("Замкнуть отсекатель")
        self.close_btn.clicked.connect(self.close)
        self.closed = 0

        self.group = QtWidgets.QButtonGroup()
        self.group.addButton(self.lines, 1)
        self.group.addButton(self.clipper, 2)
        self.lines.setChecked(True)
        self.lines.clicked.connect(lambda: self.clear_first_point())
        self.clipper.clicked.connect(lambda: self.clear_first_point())

        self.first_point = point(None, None)

        self.last_point = point(None, None)
        self.last_point_clipper = point(None, None)
        self.first_point_clipper = point(None, None)

        self.clipper_coords = QtWidgets.QLabel()
        self.clipper_coords.setText("Координаты отсекателя:")

        self.lines_coords = QtWidgets.QLabel()
        self.lines_coords.setText("Координаты отрезков:")

        self.table = QtWidgets.QTableWidget(self)
        self.table.setFont(QtGui.QFont("Times", 10))
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["x0", "y0", "x1", "y1"])
        self.table.resizeColumnsToContents()

        self.clipper_table = QtWidgets.QTableWidget(self)
        self.clipper_table.setFont(QtGui.QFont("Times", 10))
        self.clipper_table.setColumnCount(4)
        self.clipper_table.setHorizontalHeaderLabels(["x0", "y0", "x1", "y1"])
        self.clipper_table.resizeColumnsToContents()

        self.main_process_btn = QtWidgets.QPushButton()
        self.main_process_btn.setFixedWidth(500)
        self.main_process_btn.setText("Произвести отсечение")
        self.main_process_btn.clicked.connect(lambda: self.main_process())

        self.canvas = QtWidgets.QLabel()
        #self.canvas.move(0, 0)
        self.canvas.w = 1600
        self.canvas.h = 1600
        # self.canvas.adjustSize()
        self.pixmap = QtGui.QPixmap(self.canvas.w, self.canvas.h)
        self.pixmap.fill(Qt.white)
        self.canvas.setPixmap(self.pixmap)
        self.canvas.setStyleSheet("border: 1px solid black;")

        self.clipper_label = QtWidgets.QLabel()
        self.clipper_label.setText("Цвет границы отсекателя:")
        self.clipper_color = QtWidgets.QComboBox()
        self.clipper_color.addItem("Черный")
        self.clipper_color.addItem("Красный")
        self.clipper_color.addItem("Синий")

        self.line_label = QtWidgets.QLabel()
        self.line_label.setText("Цвет отрезков:")
        self.line_color = QtWidgets.QComboBox()
        self.line_color.addItem("Черный")
        self.line_color.addItem("Красный")
        self.line_color.addItem("Синий")

        self.result_label = QtWidgets.QLabel()
        self.result_label.setText("Цвет результата:")
        self.result_color = QtWidgets.QComboBox()
        self.result_color.addItem("Черный")
        self.result_color.addItem("Красный")
        self.result_color.addItem("Синий")

        self.clear_btn = QtWidgets.QPushButton()
        self.clear_btn.setText("Очистить холст")
        self.clear_btn.clicked.connect(self.clear_all)

        self.label = QtWidgets.QLabel()
        self.label.setText("Введите точку отрезка:")
        self.x_label = QtWidgets.QLabel()
        self.x_label.setText("x:")
        self.y_label = QtWidgets.QLabel()
        self.y_label.setText("y:")
        self.x = QtWidgets.QLineEdit()
        self.y = QtWidgets.QLineEdit()
        self.input_node = QtWidgets.QPushButton()
        self.input_node.setText("Ввести вершину отрезка/отсекателя(x, y)")
        self.input_node.clicked.connect(self.manual_input)

        self.last_point = point(None, None)
        self.first_point = point(None, None)
        self.pnt_amount = 0

        w = QtWidgets.QWidget()
        w.setFont(QtGui.QFont("Times", 12))
        horiz = QtWidgets.QHBoxLayout()
        w.setLayout(horiz)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.lines_coords)
        layout.addWidget(self.table)
        layout.addWidget(self.clipper_coords)
        layout.addWidget(self.clipper_table)
        layout.addWidget(self.label)
        layout.addWidget(self.x_label)
        layout.addWidget(self.x)
        layout.addWidget(self.y_label)
        layout.addWidget(self.y)
        layout.addWidget(self.input_node)
        layout.addWidget(self.clear_btn)
        layout.addWidget(self.clipper_label)
        layout.addWidget(self.clipper_color)
        layout.addWidget(self.line_label)
        layout.addWidget(self.line_color)
        layout.addWidget(self.result_label)
        layout.addWidget(self.result_color)
        layout.addWidget(self.lines)
        layout.addWidget(self.clipper)
        layout.addWidget(self.close_btn)
        layout.addWidget(self.main_process_btn)
        horiz.addLayout(layout)
        horiz.addWidget(self.canvas)
        self.setCentralWidget(w)
        QTimer.singleShot(10, self.center_window)

    def close(self):
        if self.closed == 1:
            self.show_message("Отсекатель уже замкнут")
            return
        if self.clipper_table.rowCount() < 2:
            self.show_message("Для замыкания отсекателя требуется ввести хотя бы три его вершины")
            return
        painter = QtGui.QPainter(self.canvas.pixmap())
        pen = painter.pen()
        pen.setWidth(1)
        pen.setColor(QtGui.QColor(self.get_clipper_color()))
        painter.setPen(pen)
        painter.drawLine(self.last_point_clipper.x, self.last_point_clipper.y,
                         self.first_point_clipper.x, self.first_point_clipper.y)
        self.add_data(self.last_point_clipper.x, self.last_point_clipper.y,
                      self.first_point_clipper.x, self.first_point_clipper.y, 1)
        self.update()
        self.last_point_clipper = point(None, None)
        self.first_point_clipper = point(None, None)
        self.closed = 1

    def clear_first_point(self):
        self.first_point = point(None, None)

    def draw_by_table(self, painter):
        pen = painter.pen()
        pen.setWidth(1)
        pen.setColor(QtGui.QColor(self.get_line_color()))
        painter.setPen(pen)
        try:
            for i in range(self.table.rowCount()):
                x0 = int(self.table.item(i, 0).text())
                y0 = int(self.table.item(i, 1).text())
                x1 = int(self.table.item(i, 2).text())
                y1 = int(self.table.item(i, 3).text())
                painter.drawLine(x0, y0, x1, y1)
            self.update()
        except ValueError:
            self.show_message("Ошибка в таблице")
            return
        except Exception:
            self.show_message("Неизвестная ошибка")
            return

    def center_window(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def get_clipper_color(self):
        if self.clipper_color.currentIndex() == 0:
            return 'black'
        elif self.clipper_color.currentIndex() == 1:
            return 'red'
        elif self.clipper_color.currentIndex() == 2:
            return 'blue'

    def get_line_color(self):
        if self.line_color.currentIndex() == 0:
            return 'black'
        elif self.line_color.currentIndex() == 1:
            return 'red'
        elif self.line_color.currentIndex() == 2:
            return 'blue'

    def get_result_color(self):
        if self.result_color.currentIndex() == 0:
            return 'black'
        elif self.result_color.currentIndex() == 1:
            return 'red'
        elif self.result_color.currentIndex() == 2:
            return 'blue'

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
        self.clipper_table.clearContents()
        while self.clipper_table.rowCount() > 0:
            self.clipper_table.removeRow(self.clipper_table.rowCount() - 1)
        self.fill_canvas()
        self.last_point = point(None, None)
        self.first_point_clipper = point(None, None)
        self.last_point_clipper = point(None, None)
        self.closed = 0

    # Функция заливки холста
    def fill_canvas(self):
        self.pixmap = QtGui.QPixmap(self.canvas.w, self.canvas.h)
        self.pixmap.fill(QtGui.QColor('white'))
        self.canvas.setPixmap(self.pixmap)
        self.canvas.setStyleSheet("border: 1px solid black;")

    def mousePressEvent(self, a0):
        if self.group.checkedId() == 1:
            # По непонятным причинам не регистрируется первое нажатие, работает только так
            keyboard.is_pressed("v")
            x0 = a0.x() - shift_x
            y0 = a0.y() - shift_y
            painter = QtGui.QPainter(self.canvas.pixmap())
            pen = painter.pen()
            pen.setWidth(1)
            pen.setColor(QtGui.QColor(self.get_line_color()))
            painter.setPen(pen)
            if x0 < 0 or y0 < 0:
                return
            if x0 > self.canvas.w or y0 > self.canvas.height():
                return
            if not self.first_point.x:
                painter.drawPoint(x0, y0)
                self.first_point.x = x0
                self.first_point.y = y0
                return
            else:
                if keyboard.is_pressed("v"):
                    painter.drawLine(self.first_point.x, self.first_point.y,
                                     self.first_point.x, y0)
                    self.add_data(self.first_point.x, self.first_point.y,
                                  self.first_point.x, y0, 0)
                elif keyboard.is_pressed("h"):
                    painter.drawLine(self.first_point.x, self.first_point.y,
                                     x0, self.first_point.y)
                    self.add_data(self.first_point.x, self.first_point.y,
                                  x0, self.first_point.y, 0)
                else:
                    painter.drawLine(self.first_point.x, self.first_point.y,
                                     x0, y0)
                    self.add_data(self.first_point.x, self.first_point.y,
                                  x0, y0, 0)
            self.first_point.x = None
            self.first_point.y = None
            self.update()

        elif self.group.checkedId() == 2:
            # По непонятным причинам не регистрируется первое нажатие, работает только так
            keyboard.is_pressed("v")
            x0 = a0.x() - shift_x
            y0 = a0.y() - shift_y
            painter = QtGui.QPainter(self.canvas.pixmap())
            pen = painter.pen()
            pen.setWidth(1)
            pen.setColor(QtGui.QColor(self.get_clipper_color()))
            painter.setPen(pen)
            if x0 < 0 or y0 < 0:
                return
            if x0 > self.canvas.w or y0 > self.canvas.height():
                return
            if self.closed == 1:
                self.show_message("На холсте должен быть один отсекатель")
                return
            if not self.last_point_clipper.x:
                painter.drawPoint(x0, y0)
                self.last_point_clipper = point(x0, y0)
                self.first_point_clipper = point(x0, y0)
            else:
                if keyboard.is_pressed("v"):
                    painter.drawLine(self.last_point_clipper.x, self.last_point_clipper.y,
                                     self.last_point_clipper.x, y0)
                    '''self.draw_bres(self.last_point.x, self.last_point.y,
                                   self.last_point.x, y0, painter)'''
                    self.add_data(self.last_point_clipper.x, self.last_point_clipper.y,
                                  self.last_point_clipper.x, y0, 1)
                    self.last_point_clipper = point(self.last_point_clipper.x, y0)
                elif keyboard.is_pressed("h"):
                    painter.drawLine(self.last_point_clipper.x, self.last_point_clipper.y,
                                     x0, self.last_point_clipper.y)
                    '''self.draw_bres(self.last_point.x, self.last_point.y,
                                   x0, self.last_point.y, painter)'''
                    self.add_data(self.last_point_clipper.x, self.last_point_clipper.y,
                                  x0, self.last_point_clipper.y, 1)
                    self.last_point_clipper = point(x0, self.last_point_clipper.y)
                else:
                    painter.drawLine(self.last_point_clipper.x, self.last_point_clipper.y,
                                     x0, y0)
                    '''self.draw_bres(self.last_point.x, self.last_point.y,
                                   x0, y0, painter)'''
                    self.add_data(self.last_point_clipper.x, self.last_point_clipper.y,
                                  x0, y0, 1)
                    self.last_point_clipper = point(x0, y0)
            #self.first_point_clipper = point(None, None)
            self.update()

    def add_data(self, x0, y0, x1, y1, flag):
        if flag == 0:
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
        elif flag == 1:
            pos = self.clipper_table.rowCount()
            self.clipper_table.insertRow(pos)
            item = QtWidgets.QTableWidgetItem(f"{x0}")
            item.setFlags(item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            self.clipper_table.setItem(pos, 0, item)
            item = QtWidgets.QTableWidgetItem(f"{y0}")
            item.setFlags(item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            self.clipper_table.setItem(pos, 1, item)
            item = QtWidgets.QTableWidgetItem(f"{x1}")
            item.setFlags(item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            self.clipper_table.setItem(pos, 2, item)
            item = QtWidgets.QTableWidgetItem(f"{y1}")
            item.setFlags(item.flags() & ~QtCore.Qt.ItemFlag.ItemIsEditable)
            self.clipper_table.setItem(pos, 3, item)

    def manual_input(self):
        try:
            if self.group.checkedId() == 1:
                x0 = float(self.x.text())
                y0 = float(self.y.text())
                x0 = round(x0)
                y0 = round(y0)
                painter = QtGui.QPainter(self.canvas.pixmap())
                pen = painter.pen()
                pen.setWidth(1)
                pen.setColor(QtGui.QColor(self.get_line_color()))
                painter.setPen(pen)
                if x0 < 0 or y0 < 0:
                    return
                if x0 > self.canvas.w or y0 > self.canvas.height():
                    return
                if not self.first_point.x:
                    painter.drawPoint(x0, y0)
                    self.first_point.x = x0
                    self.first_point.y = y0
                    return
                else:
                    painter.drawLine(self.first_point.x, self.first_point.y,
                                     x0, y0)
                    self.add_data(self.first_point.x, self.first_point.y,
                                  x0, y0, 0)
                self.first_point.x = None
                self.first_point.y = None
                self.update()

            elif self.group.checkedId() == 2:
                # По непонятным причинам не регистрируется первое нажатие, работает только так
                keyboard.is_pressed("v")
                x0 = float(self.x.text())
                y0 = float(self.y.text())
                x0 = round(x0)
                y0 = round(y0)
                painter = QtGui.QPainter(self.canvas.pixmap())
                pen = painter.pen()
                pen.setWidth(1)
                pen.setColor(QtGui.QColor(self.get_clipper_color()))
                painter.setPen(pen)
                if x0 < 0 or y0 < 0:
                    return
                if x0 > self.canvas.w or y0 > self.canvas.height():
                    return
                if self.closed == 1:
                    self.show_message("На холсте должен быть один отсекатель")
                    return
                if not self.last_point_clipper.x:
                    painter.drawPoint(x0, y0)
                    self.last_point_clipper = point(x0, y0)
                    self.first_point_clipper = point(x0, y0)
                else:
                    painter.drawLine(self.last_point_clipper.x, self.last_point_clipper.y,
                                     x0, y0)
                    '''self.draw_bres(self.last_point.x, self.last_point.y,
                                   x0, y0, painter)'''
                    self.add_data(self.last_point_clipper.x, self.last_point_clipper.y,
                                  x0, y0, 1)
                    self.last_point_clipper = point(x0, y0)
                # self.first_point_clipper = point(None, None)
                self.update()
        except ValueError:
            self.show_message("Ошибка ввода координат")
        except Exception:
            self.show_message("Неизвестная ошибка")

    def main_process(self):
        # ДОБАВИТЬ ПРОВЕРКИ
        painter = QtGui.QPainter(self.canvas.pixmap())
        pen = painter.pen()
        pen.setWidth(3)
        pen.setColor(QtGui.QColor(self.get_result_color()))
        painter.setPen(pen)
        arr = []
        x0 = int(self.clipper_table.item(0, 0).text())
        y0 = int(self.clipper_table.item(0, 1).text())
        x1 = int(self.clipper_table.item(0, 2).text())
        y1 = int(self.clipper_table.item(0, 3).text())
        p0 = point(x0, y0)
        p1 = point(x1, y1)
        arr.append(p0)
        arr.append(p1)
        for i in range(1, self.clipper_table.rowCount() - 1):
            x1 = int(self.clipper_table.item(i, 2).text())
            y1 = int(self.clipper_table.item(i, 3).text())
            p1 = point(x1, y1)
            arr.append(p1)
        if check_convex(arr) == 1:
            self.show_message("Отсекатель должен быть выпуклым")
            return
        for i in range(self.table.rowCount()):
            x0 = int(self.table.item(i, 0).text())
            y0 = int(self.table.item(i, 1).text())
            x1 = int(self.table.item(i, 2).text())
            y1 = int(self.table.item(i, 3).text())
            p0 = point(x0, y0)
            p1 = point(x1, y1)
            p2, p3 = cut(p0, p1, arr)
            if p2:
                painter.drawLine(p2.x, p2.y, p3.x, p3.y)
        self.update()



        '''if self.clipper_table.rowCount() == 0:
            self.show_message("Требуется ввести отсекатель!")
            return
        if self.table.rowCount() == 0:
            self.show_message("Требуется ввести хотя бы один отрезок!")
            return
        xl = min(self.clipper_obj[0].x, self.clipper_obj[1].x)
        xr = max(self.clipper_obj[0].x, self.clipper_obj[1].x)
        ylow = min(self.clipper_obj[0].y, self.clipper_obj[1].y)
        yup = max(self.clipper_obj[0].y, self.clipper_obj[1].y)

        painter = QtGui.QPainter(self.canvas.pixmap())
        pen = painter.pen()
        pen.setWidth(3)
        pen.setColor(QtGui.QColor('red'))
        painter.setPen(pen)
        for i in range(self.table.rowCount()):
            x0 = int(self.table.item(i, 0).text())
            y0 = int(self.table.item(i, 1).text())
            x1 = int(self.table.item(i, 2).text())
            y1 = int(self.table.item(i, 3).text())
            p0 = point(x0, y0)
            p1 = point(x1, y1)
            p2, p3 = cut(p0, p1, xl, xr, ylow, yup)
            if p2:
                painter.drawLine(p2.x, p2.y, p3.x, p3.y)
        self.update()'''

    def update(self):
        self.pixmap = self.canvas.pixmap()
        self.canvas.setPixmap(self.pixmap)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
