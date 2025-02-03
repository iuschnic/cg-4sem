import sys
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QMessageBox
import keyboard
from CG_7_alg import point, cut

eps = 0.0001
nano = 1000000000.0

shift_x = 660
shift_y = 20


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Алгоритм отсечения Сазерна-Коэна")

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

        self.group = QtWidgets.QButtonGroup()
        self.group.addButton(self.lines, 1)
        self.group.addButton(self.clipper, 2)
        self.lines.setChecked(True)
        self.lines.clicked.connect(lambda: self.clear_first_point())
        self.clipper.clicked.connect(lambda: self.clear_first_point())
        #self.group.buttonClicked.connect(lambda: self.clear_first_point)

        self.first_point = point(None, None)

        self.clipper_obj = [point(None, None), point(None, None)]

        self.clipper_coords = QtWidgets.QLabel()
        self.clipper_coords.setText("Координаты отсекателя: \n"
                                    "(----, ----)(----, ----)\n"
                                    "(----, ----)(----, ----)")

        self.table = QtWidgets.QTableWidget(self)
        self.table.setFont(QtGui.QFont("Times", 10))
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["x0", "y0", "x1", "y1"])
        self.table.resizeColumnsToContents()

        self.main_process_btn = QtWidgets.QPushButton()
        self.main_process_btn.setText("Произвести отсечение")
        self.main_process_btn.clicked.connect(lambda: self.main_process())

        self.canvas = QtWidgets.QLabel()
        #self.canvas.move(0, 0)
        self.canvas.w = 1600
        self.canvas.h = 1500
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
        layout.addWidget(self.table)
        layout.addWidget(self.clipper_coords)
        layout.addWidget(self.label)
        layout.addWidget(self.x_label)
        layout.addWidget(self.x)
        layout.addWidget(self.y_label)
        layout.addWidget(self.y)
        layout.addWidget(self.input_node)
        #layout.addWidget(self.input_seed)
        layout.addWidget(self.clipper_label)
        layout.addWidget(self.clipper_color)
        layout.addWidget(self.line_label)
        layout.addWidget(self.line_color)
        layout.addWidget(self.result_label)
        layout.addWidget(self.result_color)
        layout.addWidget(self.lines)
        layout.addWidget(self.clipper)
        layout.addWidget(self.main_process_btn)
        layout.addWidget(self.clear_btn)
        horiz.addLayout(layout)
        horiz.addWidget(self.canvas)
        self.setCentralWidget(w)
        QTimer.singleShot(10, self.center_window)

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
                #self.draw_bres(x0, y0, x1, y1, painter)
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
        self.fill_canvas()
        self.first_point = point(None, None)
        self.clipper_obj[0] = point(None, None)
        self.clipper_obj[1] = point(None, None)
        self.clipper_coords.setText("Координаты отсекателя: \n"
                                    "(----, ----)(----, ----)\n"
                                    "(----, ----)(----, ----)")

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
                                  self.first_point.x, y0)
                elif keyboard.is_pressed("h"):
                    painter.drawLine(self.first_point.x, self.first_point.y,
                                     x0, self.first_point.y)
                    self.add_data(self.first_point.x, self.first_point.y,
                                  x0, self.first_point.y)
                else:
                    painter.drawLine(self.first_point.x, self.first_point.y,
                                     x0, y0)
                    self.add_data(self.first_point.x, self.first_point.y,
                                  x0, y0)
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
            if not self.first_point.x:
                painter.drawPoint(x0, y0)
                self.first_point.x = x0
                self.first_point.y = y0
                return
            else:
                painter.drawRect(self.first_point.x, self.first_point.y,
                                 x0 - self.first_point.x, y0 - self.first_point.y)
                if self.clipper_obj[0].x:
                    # Затирание предыдущего отсекателя
                    pen.setColor(QtGui.QColor('white'))
                    painter.setPen(pen)
                    painter.drawRect(self.clipper_obj[0].x, self.clipper_obj[0].y,
                                     self.clipper_obj[1].x - self.clipper_obj[0].x,
                                     self.clipper_obj[1].y - self.clipper_obj[0].y)
                    # Чтобы не затереть пиксели отрезков, пересекающих отсекатель
                    self.draw_by_table(painter)
                self.clipper_obj[0] = point(self.first_point.x, self.first_point.y)
                self.clipper_obj[1] = point(x0, y0)
                self.clipper_coords.setText("Координаты отсекателя: \n"
                                            f"({self.clipper_obj[0].x}, {self.clipper_obj[0].y})"
                                            f"({self.clipper_obj[1].x}, {self.clipper_obj[0].y})\n"
                                            f"({self.clipper_obj[1].x}, {self.clipper_obj[1].y})"
                                            f"({self.clipper_obj[0].x}, {self.clipper_obj[1].y})")

            self.first_point.x = None
            self.first_point.y = None
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

    def manual_input(self):
        try:
            if self.group.checkedId() == 1:
                x0 = float(self.x.text())
                y0 = float(self.y.text())
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
                    painter.drawPoint(int(x0), int(y0))
                    self.first_point.x = int(x0)
                    self.first_point.y = int(y0)
                    return
                else:
                    painter.drawLine(self.first_point.x, self.first_point.y,
                                     int(x0), int(y0))
                    self.add_data(self.first_point.x, self.first_point.y,
                                  int(x0), int(y0))
                self.first_point.x = None
                self.first_point.y = None
                self.update()
            else:
                x0 = float(self.x.text())
                y0 = float(self.y.text())
                x0 = int(x0)
                y0 = int(y0)
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
                    painter.drawPoint(int(x0), int(y0))
                    self.first_point.x = int(x0)
                    self.first_point.y = int(y0)
                    return
                else:
                    painter.drawRect(self.first_point.x, self.first_point.y,
                                     x0 - self.first_point.x, y0 - self.first_point.y)
                    if self.clipper_obj[0].x:
                        pen.setColor(QtGui.QColor('white'))
                        painter.setPen(pen)
                        painter.drawRect(self.clipper_obj[0].x, self.clipper_obj[0].y,
                                         self.clipper_obj[1].x - self.clipper_obj[0].x,
                                         self.clipper_obj[1].y - self.clipper_obj[0].y)
                    self.clipper_obj[0] = point(self.first_point.x, self.first_point.y)
                    self.clipper_obj[1] = point(x0, y0)
                    self.clipper_coords.setText("Координаты отсекателя: \n"
                                                f"({self.clipper_obj[0].x}, {self.clipper_obj[0].y})"
                                                f"({self.clipper_obj[1].x}, {self.clipper_obj[0].y})\n"
                                                f"({self.clipper_obj[1].x}, {self.clipper_obj[1].y})"
                                                f"({self.clipper_obj[0].x}, {self.clipper_obj[1].y})")
                self.first_point.x = None
                self.first_point.y = None
                self.update()


        except ValueError:
            self.show_message("Ошибка ввода координат")
        except Exception:
            self.show_message("Неизвестная ошибка")

    def main_process(self):
        if not self.clipper_obj[0].x:
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
        pen.setColor(QtGui.QColor(self.get_result_color()))
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
        self.update()

    def update(self):
        self.pixmap = self.canvas.pixmap()
        self.canvas.setPixmap(self.pixmap)


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
