import sys
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt, QTimer
import time
from PyQt5.QtWidgets import QMessageBox
import math
import CG_3_alg as alg
import CG_3_plots as plot

eps = 0.0001

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Алгоритмы рисования отрезков")

        self.info = QtWidgets.QLabel()
        self.info.setText("Реализовать отрисовку отрезков попиксельно разными способами")
        self.info.adjustSize()

        self.msg = QtWidgets.QMessageBox()
        self.msg.setFont(QtGui.QFont("Times", 11))

        self.canvas = QtWidgets.QLabel()
        self.canvas.move(0, 0)
        self.canvas.w = 1100
        self.canvas.h = 1100
        self.canvas.adjustSize()
        self.pixmap = QtGui.QPixmap(self.canvas.w, self.canvas.h)
        self.pixmap.fill(Qt.white)
        self.canvas.setPixmap(self.pixmap)
        self.canvas.setStyleSheet("border: 1px solid black;")

        self.options = QtWidgets.QComboBox()
        self.options.addItem("Алгоритм ЦДА")
        self.options.addItem("Алгоритм Брезенхема(Действительный)")
        self.options.addItem("Алгоритм Брезенхема(Целый)")
        self.options.addItem("Алгоритм Брезенхема(С устранением ступенчатости)")
        self.options.addItem("Алгоритм Ву")
        self.options.addItem("Алгоритм Библиотечный")

        self.pixels = QtWidgets.QComboBox()
        self.pixels.addItem("Пиксели обычного размера")
        self.pixels.addItem("Крупные пиксели(кроме библиотечного алгоритма)")

        self.colors = QtWidgets.QComboBox()
        self.colors.addItem("Черный")
        self.colors.addItem("Красный")
        self.colors.addItem("Синий")
        self.colors.addItem("Цвет фона(Белый)")

        self.spectre_lable = QtWidgets.QLabel()
        self.spectre_lable.setText("Построение спектра:")
        self.spectre_lable.adjustSize()
        
        self.spectre_angle_lable = QtWidgets.QLabel()
        self.spectre_angle_lable.setText("Угол поворота:")
        self.spectre_angle = QtWidgets.QLineEdit()

        self.spectre_length_lable = QtWidgets.QLabel()
        self.spectre_length_lable.setText("Длина отрезка:")
        self.spectre_length = QtWidgets.QLineEdit()

        self.spectre_btn = QtWidgets.QPushButton()
        self.spectre_btn.setText("Построить спектр")
        self.spectre_btn.clicked.connect(self.draw_spectre)

        self.white_btn = QtWidgets.QPushButton()
        self.white_btn.setText("Цвет фона")
        self.white_btn.clicked.connect(lambda: self.set_color(3))

        self.black_btn = QtWidgets.QPushButton()
        self.black_btn.setText("Черный цвет")
        self.black_btn.clicked.connect(lambda: self.set_color(0))

        self.steps_analysis_btn = QtWidgets.QPushButton()
        self.steps_analysis_btn.setText("Построить графики ступенек от угла наклона")
        self.steps_analysis_btn.clicked.connect(self.steps_analysis)

        self.times_analysis_btn = QtWidgets.QPushButton()
        self.times_analysis_btn.setText("Построить графики времени от угла наклона")
        self.times_analysis_btn.clicked.connect(self.times_analysis)

        self.average_times_btn = QtWidgets.QPushButton()
        self.average_times_btn.setText("Построить графики среднего времени по спектру")
        self.average_times_btn.clicked.connect(self.average_times)

        self.clear_btn = QtWidgets.QPushButton()
        self.clear_btn.setText("Очистить холст")
        self.clear_btn.clicked.connect(self.clear_canvas)

        self.fir_dot = QtWidgets.QLabel()
        self.fir_dot.setText("Координаты первой точки:")
        self.fir_dot.adjustSize()

        self.sec_dot = QtWidgets.QLabel()
        self.sec_dot.setText("Координаты второй точки:")
        self.sec_dot.adjustSize()

        self.fir_x_lable = QtWidgets.QLabel()
        self.fir_x_lable.setText("x1:")
        self.fir_x_lable.adjustSize()
        self.fir_y_lable = QtWidgets.QLabel()
        self.fir_y_lable.setText("y1:")
        self.fir_y_lable.adjustSize()
        self.fir_x = QtWidgets.QLineEdit()
        self.fir_y = QtWidgets.QLineEdit()

        self.sec_x_lable = QtWidgets.QLabel()
        self.sec_x_lable.setText("x2:")
        self.sec_x_lable.adjustSize()
        self.sec_y_lable = QtWidgets.QLabel()
        self.sec_y_lable.setText("y2:")
        self.sec_y_lable.adjustSize()
        self.sec_x = QtWidgets.QLineEdit()
        self.sec_y = QtWidgets.QLineEdit()

        self.sec_dot = QtWidgets.QLabel()
        self.sec_dot.setText("Координаты второй точки:")
        self.sec_dot.adjustSize()

        self.btn = QtWidgets.QPushButton()
        self.btn.setText("Нарисовать")
        '''Поменять если что'''
        self.btn.clicked.connect(self.draw_lines)

        w = QtWidgets.QWidget()
        horiz = QtWidgets.QHBoxLayout()
        start = QtWidgets.QVBoxLayout()
        horiz.addLayout(start)
        points = QtWidgets.QGridLayout()
        coords = QtWidgets.QGridLayout()
        spectre_layout = QtWidgets.QGridLayout()

        spectre_layout.addWidget(self.spectre_angle_lable, 0, 0)
        spectre_layout.addWidget(self.spectre_angle, 0, 1)
        spectre_layout.addWidget(self.spectre_length_lable, 1, 0)
        spectre_layout.addWidget(self.spectre_length, 1, 1)
        points.addWidget(self.fir_dot, 0, 0)
        points.addWidget(self.sec_dot, 0, 1)
        coords.addWidget(self.fir_x_lable, 0, 0)
        coords.addWidget(self.fir_y_lable, 1, 0)
        coords.addWidget(self.fir_x, 0, 1)
        coords.addWidget(self.fir_y, 1, 1)
        coords.addWidget(self.sec_x_lable, 0, 2)
        coords.addWidget(self.sec_y_lable, 1, 2)
        coords.addWidget(self.sec_x, 0, 3)
        coords.addWidget(self.sec_y, 1, 3)
        
        w.setFont(QtGui.QFont("Times", 12))
        w.setLayout(horiz)
        self.setCentralWidget(w)
        start.addWidget(self.options)
        start.addWidget(self.colors)
        start.addWidget(self.pixels)
        start.addWidget(self.white_btn)
        start.addWidget(self.black_btn)
        start.addWidget(self.clear_btn)
        start.addWidget(self.spectre_lable)
        start.addLayout(spectre_layout)
        start.addWidget(self.spectre_btn)
        start.addWidget(self.steps_analysis_btn)
        start.addWidget(self.times_analysis_btn)
        start.addWidget(self.average_times_btn)
        start.addLayout(points)
        start.addLayout(coords)
        start.addWidget(self.btn)
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

    def check_data(self):
        try:
            x1 = float(self.fir_x.text())
            y1 = float(self.fir_y.text())
            x2 = float(self.sec_x.text())
            y2 = float(self.sec_y.text())
            return x1, y1, x2, y2
        except ValueError:
            self.show_message("Ошибка ввода координат точек отрезка")
            return None
        except Exception:
            self.show_message("Неизвестная ошибка")
            return None

    def check_spectre(self):
        try:
            angle = float(self.spectre_angle.text())
            length = float(self.spectre_length.text())
            if angle <= 0:
                self.show_message("Инкремент должен быть больше 0")
                return None
            if length <= 0:
                self.show_message("Длина отрезка должна быть больше 0")
                return None
            return angle, length
        except ValueError:
            self.show_message("Ошибка ввода угла поворота или длины отрезка")
            return None
        except Exception:
            self.show_message("Неизвестная ошибка")
            return None

    def show_message(self, error):
        self.msg.setIcon(QMessageBox.Warning)
        self.msg.setText(error)
        self.msg.setWindowTitle("Info")
        retval = self.msg.exec_()

    def draw_lines(self):
        if self.pixels.currentIndex() == 0:
            self.draw_line()
        else:
            self.draw_big_line()

    def draw_line(self):
        if self.options.currentIndex() == 0:
            ans = self.cda()
            self.draw_default(ans, self.get_color())
        elif self.options.currentIndex() == 1:
            ans = self.bresenham_ord()
            self.draw_default(ans, self.get_color())
        elif self.options.currentIndex() == 2:
            ans = self.bresenham_integers()
            self.draw_default(ans, self.get_color())
        elif self.options.currentIndex() == 3:
            ans = self.bresenham_del_steps()
            self.draw_with_intense(ans, self.get_color())
        elif self.options.currentIndex() == 4:
            ans = self.wu_alg()
            self.draw_with_intense(ans, self.get_color())
        elif self.options.currentIndex() == 5:
            data = self.check_data()
            self.lib_alg_draw(data, self.get_color())

    def draw_big_line(self):
        if self.options.currentIndex() == 0:
            ans = self.cda()
            self.draw_big_default(ans, self.get_color())
        elif self.options.currentIndex() == 1:
            ans = self.bresenham_ord()
            self.draw_big_default(ans, self.get_color())
        elif self.options.currentIndex() == 2:
            ans = self.bresenham_integers()
            self.draw_big_default(ans, self.get_color())
        elif self.options.currentIndex() == 3:
            ans = self.bresenham_del_steps()
            self.draw_big_with_intense(ans, self.get_color())
        elif self.options.currentIndex() == 4:
            ans = self.wu_alg()
            self.draw_big_with_intense(ans, self.get_color())
        elif self.options.currentIndex() == 5:
            data = self.check_data()
            self.show_message("К сожалению библиотечный алгоритм может нарисовать только обычные пиксели")
            #self.lib_alg_draw(data, self.get_color())

    def draw_default(self, array, color):
        painter = QtGui.QPainter(self.canvas.pixmap())
        pen = painter.pen()
        pen.setWidth(1)
        pen.setColor(QtGui.QColor(color))
        painter.setPen(pen)
        if not array:
            return -1
        for elem in array:
            painter.drawPoint(elem[0] + self.canvas.w // 2, int(self.canvas.h * 0.5) - elem[1])
        pixmap = self.canvas.pixmap()
        self.canvas.setPixmap(pixmap)
        return 0

    def draw_big_default(self, array, color):
        painter = QtGui.QPainter(self.canvas.pixmap())
        pen = painter.pen()
        pen.setWidth(3)
        pen.setColor(QtGui.QColor(color))
        painter.setPen(pen)
        if not array:
            return -1
        dx = 0
        dy = 0
        for i in range(len(array)):
            painter.drawPoint(array[i][0] + self.canvas.w // 2 + dx, int(self.canvas.h * 0.5) - array[i][1] - dy)
            if i < len(array) - 1:
                dx += (array[i + 1][0] - array[i][0]) * 2
                dy += (array[i + 1][1] - array[i][1]) * 2
        pixmap = self.canvas.pixmap()
        self.canvas.setPixmap(pixmap)
        return 0

    def draw_with_intense(self, array, color):
        painter = QtGui.QPainter(self.canvas.pixmap())
        pen = painter.pen()
        pen.setWidth(1)
        my_color = QtGui.QColor(color)
        pen.setColor(my_color)
        painter.setPen(pen)
        if not array:
            return -1
        for elem in array:
            my_color.setAlphaF(elem[2])
            pen.setColor(my_color)
            painter.setPen(pen)
            painter.drawPoint(elem[0] + self.canvas.w // 2, int(self.canvas.h * 0.5) - elem[1])
        pixmap = self.canvas.pixmap()
        self.canvas.setPixmap(pixmap)
        return 0

    def draw_big_with_intense(self, array, color):
        painter = QtGui.QPainter(self.canvas.pixmap())
        pen = painter.pen()
        pen.setWidth(3)
        my_color = QtGui.QColor(color)
        pen.setColor(my_color)
        painter.setPen(pen)
        if not array:
            return -1
        dx = 0
        dy = 0
        for i in range(len(array)):
            my_color.setAlphaF(array[i][2])
            pen.setColor(my_color)
            painter.setPen(pen)
            painter.drawPoint(array[i][0] + self.canvas.w // 2 + dx, int(self.canvas.h * 0.5) - array[i][1] - dy)
            if i < len(array) - 1:
                dx += (array[i + 1][0] - array[i][0]) * 2
                dy += (array[i + 1][1] - array[i][1]) * 2
        pixmap = self.canvas.pixmap()
        self.canvas.setPixmap(pixmap)
        return 0

    def cda(self):
        data = self.check_data()
        if not data:
            return None
        ans = alg.cda(data, 1)[0]
        return ans

    def bresenham_ord(self):
        data = self.check_data()
        if not data:
            return None
        ans = alg.bresenham_ord(data)[0]
        return ans

    def bresenham_integers(self):
        data = self.check_data()
        if not data:
            return None
        ans = alg.bresenham_integers(data)[0]
        return ans

    def bresenham_del_steps(self):
        data = self.check_data()
        if not data:
            return None
        ans = alg.bresenham_del_steps(data)[0]
        return ans

    def wu_alg(self):
        data = self.check_data()
        if not data:
            return None
        ans = alg.wu_alg(data)[0]
        return ans

    def lib_alg_draw(self, data, color):
        painter = QtGui.QPainter(self.canvas.pixmap())
        pen = painter.pen()
        pen.setWidth(1)
        pen.setColor(QtGui.QColor(color))
        painter.setPen(pen)
        x0 = int(data[0])
        y0 = int(data[1])
        x1 = int(data[2])
        y1 = int(data[3])
        painter.drawLine(x0 + self.canvas.w // 2, int(self.canvas.h * 0.5) - y0,
                         x1 + self.canvas.w // 2, int(self.canvas.h * 0.5) - y1,)
        pixmap = self.canvas.pixmap()
        self.canvas.setPixmap(pixmap)

    def draw_spectre(self):
        data = self.check_spectre()
        if not data:
            return -1
        angle = data[0] * math.pi / 180
        length = data[1]
        sum_angle = 0
        x0 = 0
        y0 = 0
        if self.pixels.currentIndex() == 0:
            while sum_angle < math.pi * 2:
                x1 = length * math.cos(sum_angle)
                y1 = length * math.sin(sum_angle)
                if self.options.currentIndex() == 0:
                    ans = alg.cda((x0, y0, x1, y1), 1)[0]
                    self.draw_default(ans, self.get_color())
                elif self.options.currentIndex() == 1:
                    ans = alg.bresenham_ord((x0, y0, x1, y1))[0]
                    self.draw_default(ans, self.get_color())
                elif self.options.currentIndex() == 2:
                    ans = alg.bresenham_integers((x0, y0, x1, y1))[0]
                    self.draw_default(ans, self.get_color())
                elif self.options.currentIndex() == 3:
                    ans = alg.bresenham_del_steps((x0, y0, x1, y1))[0]
                    self.draw_with_intense(ans, self.get_color())
                elif self.options.currentIndex() == 4:
                    ans = alg.wu_alg((x0, y0, x1, y1))[0]
                    self.draw_with_intense(ans, self.get_color())
                elif self.options.currentIndex() == 5:
                    self.lib_alg_draw([x0, y0, x1, y1], self.get_color())
                sum_angle += angle
        else:
            while sum_angle < math.pi * 2:
                x1 = length * math.cos(sum_angle)
                y1 = length * math.sin(sum_angle)
                if self.options.currentIndex() == 0:
                    ans = alg.cda((x0, y0, x1, y1), 1)[0]
                    self.draw_big_default(ans, self.get_color())
                elif self.options.currentIndex() == 1:
                    ans = alg.bresenham_ord((x0, y0, x1, y1))[0]
                    self.draw_big_default(ans, self.get_color())
                elif self.options.currentIndex() == 2:
                    ans = alg.bresenham_integers((x0, y0, x1, y1))[0]
                    self.draw_big_default(ans, self.get_color())
                elif self.options.currentIndex() == 3:
                    ans = alg.bresenham_del_steps((x0, y0, x1, y1))[0]
                    self.draw_big_with_intense(ans, self.get_color())
                elif self.options.currentIndex() == 4:
                    ans = alg.wu_alg((x0, y0, x1, y1))[0]
                    self.draw_big_with_intense(ans, self.get_color())
                elif self.options.currentIndex() == 5:
                    self.show_message("К сожалению библиотечный алгоритм может нарисовать только обычные пиксели")
                    #self.lib_alg_draw([x0, y0, x1, y1], self.get_color())
                    return
                sum_angle += angle
            
    def steps_analysis(self):
        data = self.check_spectre()
        if not data:
            return -1
        angle = data[0] * math.pi / 180
        step_angle = data[0]
        length = data[1]
        sum_angle = 0
        x0 = 0
        y0 = 0
        cda = []
        bres_ord = []
        bres_int = []
        bres_del = []
        wu = []
        print_angle = 0
        while sum_angle < math.pi * 2:
            x1 = length * math.cos(sum_angle)
            y1 = length * math.sin(sum_angle)

            steps = alg.cda((x0, y0, x1, y1), 1)[1]
            cda.append([steps, print_angle])
            
            steps = alg.bresenham_ord((x0, y0, x1, y1))[1]
            bres_ord.append([steps, print_angle])
            
            steps = alg.bresenham_integers((x0, y0, x1, y1))[1]
            bres_int.append([steps, print_angle])
            
            steps = alg.bresenham_del_steps((x0, y0, x1, y1))[1]
            bres_del.append([steps, print_angle])
            
            steps = alg.wu_alg((x0, y0, x1, y1))[1]
            wu.append([steps, print_angle])

            print_angle += step_angle
            sum_angle += angle
        labels = ["ЦДА", "Алгоритм Брезенхема(обычный)", "Алгоритм Брезенхема(целый)",
                  "Алгоритм Брезенхема(с устранением ступенчатости)", "Алгоритм Ву"]
        head = "Графики ступенчатости"
        plot.plots_by_angles(cda, bres_ord, bres_int, bres_del, wu, labels, head, "Количество ступенек", 1)

    def times_analysis(self):
        data = self.check_spectre()
        if not data:
            return -1
        angle = data[0] * math.pi / 180
        step_angle = data[0]
        length = data[1]
        sum_angle = 0 * math.pi / 180
        x0 = 0
        y0 = 0
        bres_ord = []
        bres_int = []
        bres_del = []
        wu = []
        cda = []
        print_angle = 0
        cnt = 200
        while sum_angle < math.pi * 2:
            x1 = length * math.cos(sum_angle)
            y1 = length * math.sin(sum_angle)

            res = 0
            for i in range(500):
                start = time.perf_counter_ns()
                alg.bresenham_ord((x0, y0, x1, y1))
                end = time.perf_counter_ns()
                res += end - start
            if sum_angle == 20:
                print(res)

            res = 0
            for i in range(cnt):
                start = time.perf_counter_ns()
                alg.cda((x0, y0, x1, y1), 0)
                end = time.perf_counter_ns()
                res += end - start
            cda.append([res / cnt, print_angle])

            res = 0
            for i in range(cnt):
                start = time.perf_counter_ns()
                alg.bresenham_ord((x0, y0, x1, y1))
                end = time.perf_counter_ns()
                res += end - start
            bres_ord.append([res / cnt, print_angle])
            #print(res / cnt)

            res = 0
            for i in range(cnt):
                start = time.perf_counter_ns()
                alg.bresenham_integers((x0, y0, x1, y1))
                end = time.perf_counter_ns()
                res += end - start
            bres_int.append([res / cnt, print_angle])

            res = 0
            for i in range(cnt):
                start = time.perf_counter_ns()
                alg.bresenham_del_steps((x0, y0, x1, y1))
                end = time.perf_counter_ns()
                res += end - start
            bres_del.append([res / cnt, print_angle])

            res = 0
            for i in range(cnt):
                start = time.perf_counter_ns()
                alg.wu_alg((x0, y0, x1, y1))
                end = time.perf_counter_ns()
                res += end - start
            wu.append([res / cnt, print_angle])

            print_angle += step_angle
            sum_angle += angle
        labels = ["ЦДА", "Алгоритм Брезенхема(обычный)", "Алгоритм Брезенхема(целый)",
                  "Алгоритм Брезенхема(с устранением ступенчатости)", "Алгоритм Ву"]
        head = "Графики времени"
        plot.plots_by_angles(cda, bres_ord, bres_int, bres_del, wu, labels, head, "Время, нс", 0)

    def average_times(self):
        data = self.check_spectre()
        if not data:
            return -1
        angle = data[0] * math.pi / 180
        step_angle = data[0]
        length = data[1]
        sum_angle = 0 * math.pi / 180
        x0 = 0
        y0 = 0
        cda = 0
        bres_ord = 0
        bres_int = 0
        bres_del = 0
        wu = 0
        cnt = 100
        angles_cnt = 0
        while sum_angle < math.pi * 2:
            angles_cnt += 1
            x1 = length * math.cos(sum_angle)
            y1 = length * math.sin(sum_angle)

            res = 0
            for i in range(500):
                start = time.perf_counter_ns()
                alg.bresenham_ord((x0, y0, x1, y1))
                end = time.perf_counter_ns()
                res += end - start
            if sum_angle == 20:
                print(res)

            res = 0
            for i in range(cnt):
                start = time.perf_counter_ns()
                alg.cda((x0, y0, x1, y1), 0)
                end = time.perf_counter_ns()
                res += end - start
            cda += res / cnt

            res = 0
            for i in range(cnt):
                start = time.perf_counter_ns()
                alg.bresenham_ord((x0, y0, x1, y1))
                end = time.perf_counter_ns()
                res += end - start
            bres_ord += res / cnt

            res = 0
            for i in range(cnt):
                start = time.perf_counter_ns()
                alg.bresenham_integers((x0, y0, x1, y1))
                end = time.perf_counter_ns()
                res += end - start
            bres_int += res / cnt

            res = 0
            for i in range(cnt):
                start = time.perf_counter_ns()
                alg.bresenham_del_steps((x0, y0, x1, y1))
                end = time.perf_counter_ns()
                res += end - start
            bres_del += res / cnt

            res = 0
            for i in range(cnt):
                start = time.perf_counter_ns()
                alg.wu_alg((x0, y0, x1, y1))
                end = time.perf_counter_ns()
                res += end - start
            wu += res / cnt
            sum_angle += angle
        
        bres_ord /= angles_cnt
        bres_int /= angles_cnt
        bres_del /= angles_cnt
        wu /= angles_cnt
        cda /= angles_cnt
        labels = ["ЦДА", "Брезенхем(обычный)", "Брезенхем(целый)",
                  "Брезенхем(с устранением)", "Алгоритм Ву"]
        plot.plots_average(labels, [cda, bres_ord, bres_int, bres_del, wu])

    def clear_canvas(self):
        self.pixmap = QtGui.QPixmap(self.canvas.w, self.canvas.h)
        self.pixmap.fill(Qt.white)
        self.canvas.setPixmap(self.pixmap)
        self.canvas.setStyleSheet("border: 1px solid black;")



app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()