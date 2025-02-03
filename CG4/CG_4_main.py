import sys
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import Qt, QTimer
import time
from PyQt5.QtWidgets import QMessageBox
import math
import CG_4_alg as alg
import CG_4_plots as plot

eps = 0.0001


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Алгоритмы рисования окружностей и эллипсов")

        self.info = QtWidgets.QLabel()
        self.info.setText("Реализовать отрисовку окружностей и эллипсов попиксельно разными способами")
        self.info.adjustSize()

        self.msg = QtWidgets.QMessageBox()
        self.msg.setFont(QtGui.QFont("Times", 9))

        self.canvas = QtWidgets.QLabel()
        self.canvas.move(0, 0)
        self.canvas.w = 1300
        self.canvas.h = 1500
        self.canvas.adjustSize()
        self.pixmap = QtGui.QPixmap(self.canvas.w, self.canvas.h)
        self.pixmap.fill(Qt.white)
        self.canvas.setPixmap(self.pixmap)
        self.canvas.setStyleSheet("border: 1px solid black;")

        self.options = QtWidgets.QComboBox()
        self.options.addItem("Каноническое уравнение окружности")
        self.options.addItem("Параметрическое уравнение окружности")
        self.options.addItem("Брезенхем(окружность)")
        self.options.addItem("Алгоритм с центральной точкой(окружность)")
        self.options.addItem("Библиотечный(окружность)")
        self.options.addItem("Каноническое уравнение эллипса")
        self.options.addItem("Параметрическое уравнение эллипса")
        self.options.addItem("Брезенхем(эллипс)")
        self.options.addItem("Алгоритм с центральной точкой(эллипс)")
        self.options.addItem("Библиотечный(эллипс)")

        '''self.pixels = QtWidgets.QComboBox()
        self.pixels.addItem("Пиксели обычного размера")
        self.pixels.addItem("Крупные пиксели(кроме библиотечного алгоритма)")'''

        self.colors = QtWidgets.QComboBox()
        self.colors.addItem("Черный")
        self.colors.addItem("Красный")
        self.colors.addItem("Синий")
        self.colors.addItem("Цвет фона(Белый)")

        self.circle_label = QtWidgets.QLabel()
        self.circle_label.setText("Окружность:\n"
                                  "Каноническое уравнение:\n"
                                  "(x - x0)^2 + (y - y0)^2 = r^2\n"
                                  "Параметрические уравнения:\n"
                                  "x = x0 + r * cos(t)\n"
                                  "y = y0 + r * sin(t)\n"
                                  "0 <= t <= 2 * PI\n")

        self.ellypse_label = QtWidgets.QLabel()
        self.ellypse_label.setText("Эллипс:\n"
                                  "Каноническое уравнение:\n"
                                  "(x - x0)^2 / a^2 + (y - y0)^2 / b^2 = 1\n"
                                  "Параметрические уравнения:\n"
                                  "x = x0 + a * cos(t)\n"
                                  "y = y0 + b * sin(t)\n"
                                  "0 <= t <= 2 * PI\n")

        self.x0_label = QtWidgets.QLabel()
        self.x0_label.setText("x0:")
        self.y0_label = QtWidgets.QLabel()
        self.y0_label.setText("y0:")
        self.r_label = QtWidgets.QLabel()
        self.r_label.setText("r:")
        self.a_label = QtWidgets.QLabel()
        self.a_label.setText("a:")
        self.b_label = QtWidgets.QLabel()
        self.b_label.setText("b:")

        self.x0 = QtWidgets.QLineEdit()
        self.y0 = QtWidgets.QLineEdit()
        self.r = QtWidgets.QLineEdit()
        self.a = QtWidgets.QLineEdit()
        self.b = QtWidgets.QLineEdit()

        self.white_btn = QtWidgets.QPushButton()
        self.white_btn.setText("Цвет фона")
        self.white_btn.clicked.connect(lambda: self.set_color(3))

        self.black_btn = QtWidgets.QPushButton()
        self.black_btn.setText("Черный цвет")
        self.black_btn.clicked.connect(lambda: self.set_color(0))

        self.spectre_intro = QtWidgets.QLabel()
        self.spectre_intro.setText("Установите флаг в одну из четырех опций\n"
                                   "чтобы построить спектр по трем другим\n")

        self.r_start_label = QtWidgets.QRadioButton()
        self.r_start_label.setText("Начальный радиус: ")
        self.r_start = QtWidgets.QLineEdit()
        self.step_label = QtWidgets.QRadioButton()
        self.step_label.setText("Шаг увеличения радиуса: ")
        self.step = QtWidgets.QLineEdit()
        self.amount_label = QtWidgets.QRadioButton()
        self.amount_label.setText("Количество окружностей: ")
        self.amount = QtWidgets.QLineEdit()
        self.r_end_label = QtWidgets.QRadioButton()
        self.r_end_label.setText("Конечный радиус: ")
        self.r_end = QtWidgets.QLineEdit()

        self.circle_group = QtWidgets.QButtonGroup()
        self.circle_group.addButton(self.r_start_label, 1)
        self.circle_group.addButton(self.step_label, 2)
        self.circle_group.addButton(self.amount_label, 3)
        self.circle_group.addButton(self.r_end_label, 4)
        self.r_start_label.setChecked(True)

        self.ab_start_label = QtWidgets.QRadioButton()
        self.ab_start_label.setText("Начальные полуоси a и b: ")
        self.a_start = QtWidgets.QLineEdit()
        self.b_start = QtWidgets.QLineEdit()
        self.ab_step_label = QtWidgets.QRadioButton()
        self.ab_step_label.setText("Шаг увеличения полуосей a и b: ")
        self.step_a = QtWidgets.QLineEdit()
        self.step_b = QtWidgets.QLineEdit()
        self.ab_amount_label = QtWidgets.QRadioButton()
        self.ab_amount_label.setText("Количество эллипсов: ")
        self.ab_amount = QtWidgets.QLineEdit()
        self.ab_end_label = QtWidgets.QRadioButton()
        self.ab_end_label.setText("Конечные полуоси a и b: ")
        self.a_end = QtWidgets.QLineEdit()
        self.b_end = QtWidgets.QLineEdit()

        self.ellypse_group = QtWidgets.QButtonGroup()
        self.ellypse_group.addButton(self.ab_start_label, 1)
        self.ellypse_group.addButton(self.ab_step_label, 2)
        self.ellypse_group.addButton(self.ab_amount_label, 3)
        self.ellypse_group.addButton(self.ab_end_label, 4)
        self.ab_start_label.setChecked(True)

        self.spectre_btn = QtWidgets.QPushButton()
        self.spectre_btn.setText("Построить спектр")
        self.spectre_btn.clicked.connect(self.draw_spectre)

        self.times_circle_btn = QtWidgets.QPushButton()
        self.times_circle_btn.setText("Построить графики времени для окружностей")
        self.times_circle_btn.clicked.connect(self.circle_times)

        self.times_ellypse_btn = QtWidgets.QPushButton()
        self.times_ellypse_btn.setText("Построить графики времени для эллипсов")
        self.times_ellypse_btn.clicked.connect(self.ellypse_times)
        
        '''self.fir_btn = QtWidgets.QPushButton()
        self.fir_btn.setText("Начальному, конечному и количеству")
        self.sec_btn = QtWidgets.QPushButton()
        self.sec_btn.setText("Начальному, конечному и шагу")
        self.thi_btn = QtWidgets.QPushButton()
        self.thi_btn.setText("Начальному, количеству и шагу")
        self.fth_btn = QtWidgets.QPushButton()
        self.fth_btn.setText("Конечному, количеству и шагу")'''



        spectre_layout = QtWidgets.QVBoxLayout()

        spectre_layout.addWidget(self.spectre_intro)

        spectre_layout.addWidget(self.r_start_label)
        spectre_layout.addWidget(self.r_start)
        spectre_layout.addWidget(self.step_label)
        spectre_layout.addWidget(self.step)
        spectre_layout.addWidget(self.amount_label)
        spectre_layout.addWidget(self.amount)
        spectre_layout.addWidget(self.r_end_label)
        spectre_layout.addWidget(self.r_end)

        spectre_layout.addStretch()

        spectre_layout.addWidget(self.ab_start_label)
        spectre_layout.addWidget(self.a_start)
        spectre_layout.addWidget(self.b_start)
        spectre_layout.addWidget(self.ab_step_label)
        spectre_layout.addWidget(self.step_a)
        spectre_layout.addWidget(self.step_b)
        spectre_layout.addWidget(self.ab_amount_label)
        spectre_layout.addWidget(self.ab_amount)
        spectre_layout.addWidget(self.ab_end_label)
        spectre_layout.addWidget(self.a_end)
        spectre_layout.addWidget(self.b_end)

        spectre_layout.addStretch()
        spectre_layout.addWidget(self.spectre_btn)
        spectre_layout.addWidget(self.times_circle_btn)
        spectre_layout.addWidget(self.times_ellypse_btn)

        '''spectre_layout.addWidget(self.fir_btn)
        spectre_layout.addWidget(self.sec_btn)
        spectre_layout.addWidget(self.thi_btn)
        spectre_layout.addWidget(self.fth_btn)'''


        #spectre_layout.addStretch()

        '''self.steps_analysis_btn = QtWidgets.QPushButton()
        self.steps_analysis_btn.setText("Построить графики ступенек от угла наклона")
        self.steps_analysis_btn.clicked.connect(self.steps_analysis)

        self.times_analysis_btn = QtWidgets.QPushButton()
        self.times_analysis_btn.setText("Построить графики времени от угла наклона")
        self.times_analysis_btn.clicked.connect(self.times_analysis)

        self.average_times_btn = QtWidgets.QPushButton()
        self.average_times_btn.setText("Построить графики среднего времени по спектру")
        self.average_times_btn.clicked.connect(self.average_times)'''

        self.clear_btn = QtWidgets.QPushButton()
        self.clear_btn.setText("Очистить холст")
        self.clear_btn.clicked.connect(self.clear_canvas)

        self.btn = QtWidgets.QPushButton()
        self.btn.setText("Нарисовать")
        self.btn.clicked.connect(self.draw)

        w = QtWidgets.QWidget()
        horiz = QtWidgets.QHBoxLayout()
        start = QtWidgets.QVBoxLayout()
        horiz.addLayout(start)
        info = QtWidgets.QGridLayout()

        info.addWidget(self.x0_label, 0, 0)
        info.addWidget(self.y0_label, 1, 0)
        info.addWidget(self.r_label, 2, 0)
        info.addWidget(self.x0, 0, 1)
        info.addWidget(self.y0, 1, 1)
        info.addWidget(self.r, 2, 1)
        info.addWidget(self.a_label, 3, 0)
        info.addWidget(self.a, 3, 1)
        info.addWidget(self.b_label, 4, 0)
        info.addWidget(self.b, 4, 1)

        w.setFont(QtGui.QFont("Times", 12))
        w.setLayout(horiz)
        self.setCentralWidget(w)
        start.addWidget(self.options)
        start.addWidget(self.colors)
        #start.addWidget(self.pixels)
        start.addWidget(self.white_btn)
        start.addWidget(self.black_btn)
        start.addWidget(self.clear_btn)
        #start.addWidget(self.spectre_lable)
        start.addWidget(self.circle_label)
        start.addWidget(self.ellypse_label)
        start.addLayout(info)
        '''start.addLayout(spectre_layout)
        start.addWidget(self.spectre_btn)
        start.addWidget(self.steps_analysis_btn)
        start.addWidget(self.times_analysis_btn)
        start.addWidget(self.average_times_btn)
        start.addLayout(points)
        start.addLayout(coords)'''
        start.addWidget(self.btn)
        horiz.addLayout(spectre_layout)
        horiz.addWidget(self.canvas)
        QTimer.singleShot(10, self.center_window)

    def center_window(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def get_color(self):
        if self.colors.currentIndex() == 0:
            return 'black'
        elif self.colors.currentIndex() == 1:
            return 'red'
        elif self.colors.currentIndex() == 2:
            return 'blue'
        elif self.colors.currentIndex() == 3:
            return 'white'

    def set_color(self, color):
        self.colors.setCurrentIndex(color)

    def check_circle(self):
        try:
            x0 = float(self.x0.text())
            y0 = float(self.y0.text())
            r = float(self.r.text())
            if r <= 0:
                self.show_message("Радиус должен быть больше 0")
                return None
            return x0, y0, r
        except ValueError:
            self.show_message("Ошибка ввода параметров окружности")
            return None
        except Exception:
            self.show_message("Неизвестная ошибка")
            return None

    def check_ellypse(self):
        try:
            x0 = float(self.x0.text())
            y0 = float(self.y0.text())
            a = float(self.a.text())
            b = float(self.b.text())
            if a <= 0:
                self.show_message("Полуось a должна быть больше нуля")
                return None
            if b <= 0:
                self.show_message("Полуось b должна быть больше нуля")
                return None
            return x0, y0, a, b
        except ValueError:
            self.show_message("Ошибка ввода параметров эллипса")
            return None
        except Exception:
            self.show_message("Неизвестная ошибка")
            return None

    def show_message(self, error):
        self.msg.setIcon(QMessageBox.Warning)
        self.msg.setText(error)
        self.msg.setWindowTitle("Info")
        retval = self.msg.exec_()

    def draw(self):
        if self.options.currentIndex() == 0:
            ans = self.canonical_circle()
            if ans:
                self.draw_array(ans, self.get_color())
        elif self.options.currentIndex() == 1:
            ans = self.parametric_circle()
            if ans:
                self.draw_array(ans, self.get_color())
        elif self.options.currentIndex() == 2:
            ans = self.bres_circle()
            if ans:
                self.draw_array(ans, self.get_color())
        elif self.options.currentIndex() == 3:
            ans = self.central_point_circle()
            if ans:
                self.draw_array(ans, self.get_color())
        elif self.options.currentIndex() == 4:
            data = self.check_circle()
            if not data:
                return
            self.lib_draw_circle(data, self.get_color())
        elif self.options.currentIndex() == 5:
            ans = self.canonical_ellypse()
            if ans:
                self.draw_array(ans, self.get_color())
        elif self.options.currentIndex() == 6:
            ans = self.parametric_ellypse()
            if ans:
                self.draw_array(ans, self.get_color())
        elif self.options.currentIndex() == 7:
            ans = self.bres_ellypse()
            if ans:
                self.draw_array(ans, self.get_color())
        elif self.options.currentIndex() == 8:
            ans = self.central_point_ellypse()
            if ans:
                self.draw_array(ans, self.get_color())
        elif self.options.currentIndex() == 9:
            data = self.check_ellypse()
            if not data:
                return
            self.lib_draw_ellypse(data, self.get_color())

    def draw_array(self, array, color):
        painter = QtGui.QPainter(self.canvas.pixmap())
        pen = painter.pen()
        pen.setWidth(1)
        pen.setColor(QtGui.QColor(color))
        painter.setPen(pen)
        if not array:
            return -1
        dx = self.canvas.w // 2
        dy = self.canvas.h // 2
        for elem in array:
            painter.drawPoint(elem[0] + dx, dy - elem[1])
        pixmap = self.canvas.pixmap()
        self.canvas.setPixmap(pixmap)
        return 0

    def lib_draw_circle(self, data, color):
        painter = QtGui.QPainter(self.canvas.pixmap())
        pen = painter.pen()
        pen.setWidth(1)
        pen.setColor(QtGui.QColor(color))
        painter.setPen(pen)
        dx = self.canvas.w // 2
        dy = self.canvas.h // 2
        painter.drawEllipse(QtCore.QPoint(round(data[0]) + dx, dy - round(data[1])), round(data[2]), round(data[2]))
        pixmap = self.canvas.pixmap()
        self.canvas.setPixmap(pixmap)

    def lib_draw_ellypse(self, data, color):
        painter = QtGui.QPainter(self.canvas.pixmap())
        pen = painter.pen()
        pen.setWidth(1)
        pen.setColor(QtGui.QColor(color))
        painter.setPen(pen)
        dx = self.canvas.w // 2
        dy = self.canvas.h // 2
        painter.drawEllipse(QtCore.QPoint(round(data[0]) + dx, dy - round(data[1])), round(data[2]), round(data[3]))
        pixmap = self.canvas.pixmap()
        self.canvas.setPixmap(pixmap)

    def canonical_circle(self):
        data = self.check_circle()
        if not data:
            return None
        ans = alg.canonical_circle(data)
        return ans

    def parametric_circle(self):
        data = self.check_circle()
        if not data:
            return None
        ans = alg.parametr_circle(data)
        return ans

    def bres_circle(self):
        data = self.check_circle()
        if not data:
            return None
        ans = alg.bres_circle(data)
        return ans

    def central_point_circle(self):
        data = self.check_circle()
        if not data:
            return None
        ans = alg.central_point_circle(data)
        return ans

    def canonical_ellypse(self):
        data = self.check_ellypse()
        if not data:
            return None
        ans = alg.canonical_ellypse(data)
        return ans

    def parametric_ellypse(self):
        data = self.check_ellypse()
        if not data:
            return None
        ans = alg.parametr_ellypse(data)
        return ans

    def bres_ellypse(self):
        data = self.check_ellypse()
        if not data:
            return None
        ans = alg.bres_ellypse(data)
        return ans

    def central_point_ellypse(self):
        data = self.check_ellypse()
        if not data:
            return None
        ans = alg.central_point_ellypse(data)
        return ans

    def circle_get_spectre_data(self):
        id = self.circle_group.checkedId()
        # Шаг, количество, конечный радиус
        if id == 1:
            try:
                step = float(self.step.text())
                amount = int(self.amount.text())
                r_end = float(self.r_end.text())
                r_start = r_end - step * (amount - 1)
                if step <= 0:
                    self.show_message("Шаг должен быть больше 0")
                    return None
                if amount <= 0:
                    self.show_message("Количество окружностей должно быть больше 0")
                    return None
                if r_end <= 0:
                    self.show_message("Конечный радиус должен быть больше 0")
                    return None
                if r_start <= 0:
                    self.show_message("Начальный радиус при введенных параметрах меньше 0")
                    return None
                return r_start, step, amount
            except ValueError:
                self.show_message("Ошибка ввода параметров спектра окружности")
                return None
            except Exception:
                self.show_message("Неизвестная ошибка")
                return None
        # Начальный, количество, конечный
        elif id == 2:
            try:
                r_start = float(self.r_start.text())
                amount = int(self.amount.text())
                r_end = float(self.r_end.text())
                if amount <= 0:
                    self.show_message("Количество окружностей должно быть больше 0")
                    return None
                if r_start <= 0:
                    self.show_message("Начальный радиус должен быть больше 0")
                    return None
                if r_end <= 0:
                    self.show_message("Конечный радиус должен быть больше 0")
                    return None
                if r_end <= r_start:
                    self.show_message("Конечный радиус должен быть больше начального")
                    return None
                step = (r_end - r_start) / (amount - 1)
                return r_start, step, amount
            except ValueError:
                self.show_message("Ошибка ввода параметров спектра окружности")
                return None
            except Exception:
                self.show_message("Неизвестная ошибка")
                return None
        # Начальный, шаг, конечный
        elif id == 3:
            try:
                r_start = float(self.r_start.text())
                step = float(self.step.text())
                r_end = float(self.r_end.text())
                if step <= 0:
                    self.show_message("Шаг должен быть больше 0")
                    return None
                if r_start <= 0:
                    self.show_message("Начальный радиус должен быть больше 0")
                    return None
                if r_end <= 0:
                    self.show_message("Конечный радиус должен быть больше 0")
                    return None
                if r_end <= r_start:
                    self.show_message("Конечный радиус должен быть больше начального")
                    return None
                amount = round((r_end - r_start) / step) + 1
                return r_start, step, amount
            except ValueError:
                self.show_message("Ошибка ввода параметров спектра окружности")
                return None
            except Exception:
                self.show_message("Неизвестная ошибка")
                return None
        # Начальный, шаг, количество
        elif id == 4:
            try:
                r_start = float(self.r_start.text())
                step = float(self.step.text())
                amount = int(self.amount.text())
                if step <= 0:
                    self.show_message("Шаг должен быть больше 0")
                    return None
                if amount <= 0:
                    self.show_message("Количество окружностей должно быть больше 0")
                    return None
                if r_start <= 0:
                    self.show_message("Начальный радиус должен быть больше 0")
                    return None
                return r_start, step, amount
            except ValueError:
                self.show_message("Ошибка ввода параметров спектра окружности")
                return None
            except Exception:
                self.show_message("Неизвестная ошибка")
                return None

    def ellypse_get_spectre_data(self):
        id = self.ellypse_group.checkedId()
        # Шаг, количество, конечный радиус
        if id == 1:
            try:
                step_a = float(self.step_a.text())
                step_b = float(self.step_b.text())
                amount = int(self.ab_amount.text())
                a_end = float(self.a_end.text())
                b_end = float(self.b_end.text())
                if step_a <= 0:
                    self.show_message("Шаг увеличения полуоси a должен быть больше 0")
                    return None
                if step_b <= 0:
                    self.show_message("Шаг увеличения полуоси b должен быть больше 0")
                    return None
                if amount <= 0:
                    self.show_message("Количество эллипсов должно быть больше 0")
                    return None
                if a_end <= 0 or b_end <= 0:
                    self.show_message("Конечные полуоси должны быть больше 0")
                    return None
                a_start = a_end - step_a * (amount - 1)
                b_start = b_end - step_b * (amount - 1)
                if a_start <= 0:
                    self.show_message("Начальное значение полуоси a при введенных параметрах меньше 0")
                    return None
                if b_start <= 0:
                    self.show_message("Начальное значение полуоси b при введенных параметрах меньше 0")
                    return None
                return a_start, b_start, step_a, step_b, amount
            except ValueError:
                self.show_message("Ошибка ввода параметров спектра эллипсов")
                return None
            except Exception:
                self.show_message("Неизвестная ошибка")
                return None

        elif id == 2:
            try:
                a_start = float(self.a_start.text())
                b_start = float(self.b_start.text())
                amount = int(self.ab_amount.text())
                a_end = float(self.a_end.text())
                b_end = float(self.b_end.text())
                if amount <= 0:
                    self.show_message("Количество эллипсов должно быть больше 0")
                    return None
                if a_start <= 0 or b_start <= 0:
                    self.show_message("Начальные значения полуосей должны быть больше 0")
                    return None
                if a_end <= 0 or b_end <= 0:
                    self.show_message("Конечные значения полуосей должны быть больше 0")
                    return None
                if a_end <= a_start:
                    self.show_message("Конечное значение полуоси а должно быть больше начального")
                    return None
                if b_end <= b_start:
                    self.show_message("Конечное значение полуоси b должно быть больше начального")
                    return None
                step_a = (a_end - a_start) / (amount - 1)
                step_b = (b_end - b_start) / (amount - 1)
                return a_start, b_start, step_a, step_b, amount
            except ValueError:
                self.show_message("Ошибка ввода параметров спектра эллипсов")
                return None
            except Exception:
                self.show_message("Неизвестная ошибка")
                return None

        elif id == 3:
            try:
                a_start = float(self.a_start.text())
                b_start = float(self.b_start.text())
                step_a = float(self.step_a.text())
                step_b = float(self.step_b.text())
                a_end = float(self.a_end.text())
                b_end = float(self.b_end.text())
                if step_a <= 0:
                    self.show_message("Шаг увеличения полуоси a должен быть больше 0")
                    return None
                if step_b <= 0:
                    self.show_message("Шаг увеличения полуоси b должен быть больше 0")
                    return None
                if a_start <= 0 or b_start <= 0:
                    self.show_message("Начальные значения полуосей должны быть больше 0")
                    return None
                if a_end <= 0 or b_end <= 0:
                    self.show_message("Конечные значения полуосей должны быть больше 0")
                    return None
                if a_end <= a_start:
                    self.show_message("Конечное значение полуоси а должно быть больше начального")
                    return None
                if b_end <= b_start:
                    self.show_message("Конечное значение полуоси b должно быть больше начального")
                    return None
                amount = min(round((a_end - a_start) / step_a) + 1, round((b_end - b_start) / step_b) + 1)
                return a_start, b_start, step_a, step_b, amount
            except ValueError:
                self.show_message("Ошибка ввода параметров спектра эллипсов")
                return None
            except Exception:
                self.show_message("Неизвестная ошибка")
                return None

        elif id == 4:
            try:
                a_start = float(self.a_start.text())
                b_start = float(self.b_start.text())
                step_a = float(self.step_a.text())
                step_b = float(self.step_b.text())
                amount = int(self.ab_amount.text())
                if step_a <= 0:
                    self.show_message("Шаг увеличения полуоси a должен быть больше 0")
                    return None
                if step_b <= 0:
                    self.show_message("Шаг увеличения полуоси b должен быть больше 0")
                    return None
                if amount <= 0:
                    self.show_message("Количество эллипсов должно быть больше 0")
                    return None
                if a_start <= 0 or b_start <= 0:
                    self.show_message("Начальные значения полуосей должны быть больше 0")
                    return None
                return a_start, b_start, step_a, step_b, amount
            except ValueError:
                self.show_message("Ошибка ввода параметров спектра эллипсов")
                return None
            except Exception:
                self.show_message("Неизвестная ошибка")
                return None

    def draw_spectre(self):
        id = self.options.currentIndex()
        if id >= 0 and id <= 4:
            data = self.circle_get_spectre_data()
            if not data:
                return
            r_start = data[0]
            step = data[1]
            amount = data[2]
            if self.options.currentIndex() == 0:
                for i in range(amount):
                    ans = alg.canonical_circle([0, 0, r_start])
                    if ans:
                        self.draw_array(ans, self.get_color())
                    r_start += step
            elif self.options.currentIndex() == 1:
                for i in range(amount):
                    ans = alg.parametr_circle([0, 0, r_start])
                    if ans:
                        self.draw_array(ans, self.get_color())
                    r_start += step
            elif self.options.currentIndex() == 2:
                for i in range(amount):
                    ans = alg.bres_circle([0, 0, r_start])
                    if ans:
                        self.draw_array(ans, self.get_color())
                    r_start += step
            elif self.options.currentIndex() == 3:
                for i in range(amount):
                    ans = alg.central_point_circle([0, 0, r_start])
                    if ans:
                        self.draw_array(ans, self.get_color())
                    r_start += step
            elif self.options.currentIndex() == 4:
                for i in range(amount):
                    self.lib_draw_circle([0, 0, r_start], self.get_color())
                    r_start += step
        if id >= 5 and id <= 9:
            data = self.ellypse_get_spectre_data()
            if not data:
                return
            a_start = data[0]
            b_start = data[1]
            step_a = data[2]
            step_b = data[3]
            amount = data[4]
            if self.options.currentIndex() == 5:
                for i in range(amount):
                    ans = alg.canonical_ellypse([0, 0, a_start, b_start])
                    if ans:
                        self.draw_array(ans, self.get_color())
                    a_start += step_a
                    b_start += step_b
            elif self.options.currentIndex() == 6:
                for i in range(amount):
                    ans = alg.parametr_ellypse([0, 0, a_start, b_start])
                    if ans:
                        self.draw_array(ans, self.get_color())
                    a_start += step_a
                    b_start += step_b
            elif self.options.currentIndex() == 7:
                for i in range(amount):
                    ans = alg.bres_ellypse([0, 0, a_start, b_start])
                    if ans:
                        self.draw_array(ans, self.get_color())
                    a_start += step_a
                    b_start += step_b
            elif self.options.currentIndex() == 8:
                for i in range(amount):
                    ans = alg.central_point_ellypse([0, 0, a_start, b_start])
                    if ans:
                        self.draw_array(ans, self.get_color())
                    a_start += step_a
                    b_start += step_b
            elif self.options.currentIndex() == 9:
                for i in range(amount):
                    self.lib_draw_ellypse([0, 0, a_start, b_start], self.get_color())
                    a_start += step_a
                    b_start += step_b

    def circle_times(self):
        experiments_num = 100
        r_start = 10
        r_step = 50
        amount = 20
        canonical = []
        parametric = []
        bres = []
        mid_pnt = []
        x_axis = []
        for i in range(amount):
            times = 0.0
            for j in range(experiments_num):
                start = time.perf_counter_ns()
                alg.canonical_circle([0, 0, r_start])
                end = time.perf_counter_ns()
                times += (end - start)
            canonical.append([times / experiments_num])
            times = 0
            for j in range(experiments_num):
                start = time.perf_counter_ns()
                alg.parametr_circle([0, 0, r_start])
                end = time.perf_counter_ns()
                times += (end - start)
            parametric.append([times / experiments_num])
            times = 0
            for j in range(experiments_num):
                start = time.perf_counter_ns()
                alg.bres_circle([0, 0, r_start])
                end = time.perf_counter_ns()
                times += (end - start)
            bres.append([times / experiments_num])
            times = 0
            for j in range(experiments_num):
                start = time.perf_counter_ns()
                alg.central_point_circle([0, 0, r_start])
                end = time.perf_counter_ns()
                times += (end - start)
            mid_pnt.append([times / experiments_num])
            x_axis.append(r_start)
            r_start += r_step

        labels = ["Каноническое", "Параметрическое", "Брезенхем",
                  "Центральная точка"]
        plot.plots(labels, [canonical, parametric, bres, mid_pnt], x_axis, "Радиус, пиксели",
                   "Время построения, нс")
        
        
    def ellypse_times(self):
        experiments_num = 100
        a_start = 30
        b_start = 10
        r_step = 50
        amount = 20
        canonical = []
        parametric = []
        bres = []
        mid_pnt = []
        x_axis = []
        for i in range(amount):
            times = 0
            for j in range(experiments_num):
                start = time.perf_counter_ns()
                alg.canonical_ellypse([0, 0, a_start, b_start])
                end = time.perf_counter_ns()
                times += (end - start)
            canonical.append([times / experiments_num])
            times = 0
            for j in range(experiments_num):
                start = time.perf_counter_ns()
                alg.parametr_ellypse([0, 0, a_start, b_start])
                end = time.perf_counter_ns()
                times += (end - start)
            parametric.append([times / experiments_num])
            times = 0
            for j in range(experiments_num):
                start = time.perf_counter_ns()
                alg.bres_ellypse([0, 0, a_start, b_start])
                end = time.perf_counter_ns()
                times += (end - start)
            bres.append([times / experiments_num])
            times = 0
            for j in range(experiments_num):
                start = time.perf_counter_ns()
                alg.central_point_ellypse([0, 0, a_start, b_start])
                end = time.perf_counter_ns()
                times += (end - start)
            mid_pnt.append([times / experiments_num])
            x_axis.append(a_start)
            a_start += r_step
            b_start += r_step

        labels = ["Каноническое", "Параметрическое", "Брезенхем",
                  "Центральная точка"]
        plot.plots(labels, [canonical, parametric, bres, mid_pnt], x_axis, "Полуось a, пиксели",
                   "Время, нс")

    def clear_canvas(self):
        self.pixmap = QtGui.QPixmap(self.canvas.w, self.canvas.h)
        self.pixmap.fill(Qt.white)
        self.canvas.setPixmap(self.pixmap)
        self.canvas.setStyleSheet("border: 1px solid black;")


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()