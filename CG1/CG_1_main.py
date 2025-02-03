import sys
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

import CG1_calc as calc, CG_1_canvas as cnv


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Решение геометрической задачи")

        self.setStyleSheet("QLabel {font-size: 10pt}")
        self.setStyleSheet("QPushButton {font-size: 10pt}")
        self.setStyleSheet("QTableWidget {font-size: 10pt}")

        self.window2 = cnv.CanvasWindow()

        self.first_table = QtWidgets.QTableWidget(self)
        self.first_table.setFont(QtGui.QFont("Times", 9))
        self.first_table.setColumnCount(2)
        self.first_table.setHorizontalHeaderLabels(
            ["x1", "y1"])
        #self.points_table.resizeColumnsToContents()
        for i in range(5):
            self.first_table.insertRow(i)
        self.first_table.setItem(0, 0, QtWidgets.QTableWidgetItem("0"))
        self.first_table.setItem(0, 1, QtWidgets.QTableWidgetItem("1"))
        self.first_table.setItem(1, 0, QtWidgets.QTableWidgetItem("1"))
        self.first_table.setItem(1, 1, QtWidgets.QTableWidgetItem("0"))
        self.first_table.setItem(2, 0, QtWidgets.QTableWidgetItem("-1"))
        self.first_table.setItem(2, 1, QtWidgets.QTableWidgetItem("0"))

        self.second_table = QtWidgets.QTableWidget(self)
        self.second_table.setFont(QtGui.QFont("Times", 9))
        self.second_table.setColumnCount(2)
        self.second_table.setHorizontalHeaderLabels(
            ["x2", "y2"])
        # self.points_table.resizeColumnsToContents()
        for i in range(5):
            self.second_table.insertRow(i)
        self.second_table.setItem(0, 0, QtWidgets.QTableWidgetItem("5"))
        self.second_table.setItem(0, 1, QtWidgets.QTableWidgetItem("1"))
        self.second_table.setItem(1, 0, QtWidgets.QTableWidgetItem("8"))
        self.second_table.setItem(1, 1, QtWidgets.QTableWidgetItem("-2"))
        self.second_table.setItem(2, 0, QtWidgets.QTableWidgetItem("5"))
        self.second_table.setItem(2, 1, QtWidgets.QTableWidgetItem("-5"))

        self.info = QtWidgets.QLabel()
        self.info.setText("Даны два множества точек на плоскости. Найти пару окружностей,\n"
                          "каждая из которых проходит хотя бы через три различные точки своего множества,\n"
                          "таких, что хотя бы одна из их общих внешних касательных параллельна оси абсцисс\n")
        self.info.adjustSize()

        self.add_empty_fir = QtWidgets.QPushButton()
        self.add_empty_fir.setFixedWidth(400)
        self.add_empty_fir.setText("Добавить пустую строку (табл 1)")
        self.add_empty_fir.clicked.connect(self.add_fir)
        self.add_empty_fir.setFont(QtGui.QFont("Times", 9))

        self.add_empty_sec = QtWidgets.QPushButton()
        self.add_empty_sec.setFixedWidth(400)
        self.add_empty_sec.setText("Добавить пустую строку (табл 2)")
        self.add_empty_sec.clicked.connect(self.add_sec)
        self.add_empty_sec.setFont(QtGui.QFont("Times", 9))

        self.clear_fir = QtWidgets.QPushButton()
        self.clear_fir.setFixedWidth(400)
        self.clear_fir.setText("Очистить первую таблицу")
        self.clear_fir.clicked.connect(lambda: self.clear_all(1))
        self.clear_fir.setFont(QtGui.QFont("Times", 9))

        self.clear_sec = QtWidgets.QPushButton()
        self.clear_sec.setFixedWidth(400)
        self.clear_sec.setText("Очистить вторую таблицу")
        self.clear_sec.clicked.connect(lambda: self.clear_all(2))
        self.clear_sec.setFont(QtGui.QFont("Times", 9))

        self.main_process_btn = QtWidgets.QPushButton()
        self.main_process_btn.setFixedWidth(400)
        self.main_process_btn.setText("Решить задачу")
        self.main_process_btn.clicked.connect(self.main_process)
        self.main_process_btn.setFont(QtGui.QFont("Times", 9))

        self.delete_fir_btn = QtWidgets.QPushButton()
        self.delete_fir_btn.setFixedWidth(400)
        self.delete_fir_btn.setText("Удалить выбранную строку (табл 1)")
        self.delete_fir_btn.clicked.connect(self.delete_first)
        self.delete_fir_btn.setFont(QtGui.QFont("Times", 9))

        self.delete_sec_btn = QtWidgets.QPushButton()
        self.delete_sec_btn.setFixedWidth(400)
        self.delete_sec_btn.setText("Удалить выбранную строку (табл 2)")
        self.delete_sec_btn.clicked.connect(self.delete_second)
        self.delete_sec_btn.setFont(QtGui.QFont("Times", 9))

        self.msg = QtWidgets.QMessageBox()
        self.msg.setFont(QtGui.QFont("Times", 9))

        w = QtWidgets.QWidget()
        start = QtWidgets.QVBoxLayout()
        start.addWidget(self.info)
        l = QtWidgets.QGridLayout()
        w.setLayout(start)
        l.addWidget(self.add_empty_fir, 1, 0)
        l.addWidget(self.add_empty_sec, 1, 1)
        l.addWidget(self.delete_fir_btn, 2, 0)
        l.addWidget(self.delete_sec_btn, 2, 1)
        l.addWidget(self.clear_fir, 3, 0)
        l.addWidget(self.clear_sec, 3, 1)
        l.addWidget(self.first_table, 4, 0)
        l.addWidget(self.second_table, 4, 1)
        l.addWidget(self.main_process_btn, 6, 0)
        start.addLayout(l)
        self.setCentralWidget(w)

    # Функция проверки корректности введенных координат точки
    def check_point(self, i, tablenum):
        try:
            if tablenum == 1:
                x = self.first_table.item(i, 0)
                y = self.first_table.item(i, 1)
                if x and y:
                    x = float(self.first_table.item(i, 0).text())
                    y = float(self.first_table.item(i, 1).text())
                elif x or y:
                    return 1     #если заполнены не все ячейки
                else:
                    return 2     #если обе ячейки строки пусты, не считаем это ошибкой, но не вносим в список
            elif tablenum == 2:
                x = self.second_table.item(i, 0)
                y = self.second_table.item(i, 1)
                if x and y:
                    x = float(self.second_table.item(i, 0).text())
                    y = float(self.second_table.item(i, 1).text())
                elif x or y:
                    return 1  # если заполнены не все ячейки
                else:
                    return 2  # если обе ячейки строки пусты, не считаем это ошибкой, но не вносим в список

            return 0
        except ValueError:
            return -1
        except Exception:
            return -2

    # Функция добавляет пустую строку в таблицу
    def add_fir(self):
        row_pos = self.first_table.rowCount()
        self.first_table.insertRow(row_pos)

    def add_sec(self):
        row_pos = self.second_table.rowCount()
        self.second_table.insertRow(row_pos)

    # Функция вывода сообщения об ошибке
    def show_message(self, error):
        self.msg.setIcon(QMessageBox.Warning)
        self.msg.setText(error)
        self.msg.setWindowTitle("Info")
        retval = self.msg.exec_()

    # Функция очистки таблицы
    def clear_all(self, tabnum):
        if tabnum == 1:
            self.first_table.clearContents()
        elif tabnum == 2:
            self.second_table.clearContents()

    # Функция подготовки данных для рассчета задачи
    def main_process(self):
        i = 0
        fir_dots = []
        sec_dots = []
        while i < self.first_table.rowCount():
            rc = self.check_point(i, 1)
            if rc == 0:
                x = float(self.first_table.item(i, 0).text())
                y = float(self.first_table.item(i, 1).text())
                num = i + 1
                fir_dots.append([num, [x, y]])
            elif rc == 1:
                self.show_message(f"В строке {i + 1} первой таблицы заполнены не все ячейки")
                return 1
            elif rc == -1:
                self.show_message(f"Некорректные данные в строке {i + 1} первой таблицы")
                return 1
            elif rc == -2:
                self.show_message("Неизвестная ошибка")
                return 1

            i += 1

        i = 0
        while i < self.second_table.rowCount():
            rc = self.check_point(i, 2)
            if rc == 0:
                x = float(self.second_table.item(i, 0).text())
                y = float(self.second_table.item(i, 1).text())
                num = i + 1
                sec_dots.append([num, [x, y]])
            elif rc == 1:
                self.show_message(f"В строке {i + 1} второй таблицы заполнены не все ячейки")
                return 1
            elif rc == -1:
                self.show_message(f"Некорректные данные в строке {i + 1} второй таблицы")
                return 1
            elif rc == -2:
                self.show_message("Неизвестная ошибка")
                return 1

            i += 1

        if len(fir_dots) < 3:
            self.show_message("Нужно хотя бы три точки первого типа для рассчета")
            return 2
        if len(sec_dots) < 3:
            self.show_message("Нужно хотя бы три точки второго типа для рассчета")
            return 2

        points, touch_points, cir = calc.find_circles(fir_dots, sec_dots)
        if points == None:
            self.show_message("Не найдено ни одной подходящей пары окружностей")
            return
        self.window2.show()
        up, down, right, left = calc.pixmap_params(cir[0], cir[1])
        self.window2.draw_coord_lines(left, right, up, down)

        for elem in points[0]:
            self.window2.draw_point(left, right, up, down, elem[1][0], elem[1][1], elem[0], 'red')
        for elem in points[1]:
            self.window2.draw_point(left, right, up, down, elem[1][0], elem[1][1], elem[0], 'blue')

        self.window2.draw_circle(left, right, up, down, cir[0][0], cir[0][1], cir[0][2], 'red')
        self.window2.draw_circle(left, right, up, down, cir[1][0], cir[1][1], cir[1][2], 'blue')

        self.window2.draw_line(left, right, up, down, touch_points[0][0], touch_points[1][0], 'black')
        self.window2.draw_line(left, right, up, down, touch_points[0][1], touch_points[1][1], 'black')

        self.window2.answer.setText("Обнаружены окружности с указанным свойством:\n"
                                    "Окружность первого множества задается точками:\n"
                                    f"{points[0][0][0]}: [{points[0][0][1][0]:5.2f}, {points[0][0][1][1]:5.2f}]\n"
                                    f"{points[0][1][0]}: [{points[0][1][1][0]:5.2f}, {points[0][1][1][1]:5.2f}]\n"
                                    f"{points[0][2][0]}: [{points[0][2][1][0]:5.2f}, {points[0][2][1][1]:5.2f}]\n"
                                    "Окружность второго множества задается точками:\n"
                                    f"{points[1][0][0]}: [{points[1][0][1][0]:5.2f}, {points[1][0][1][1]:5.2f}]\n"
                                    f"{points[1][1][0]}: [{points[1][1][1][0]:5.2f}, {points[1][1][1][1]:5.2f}]\n"
                                    f"{points[1][2][0]}: [{points[1][2][1][0]:5.2f}, {points[1][2][1][1]:5.2f}]\n")
        self.window2.answer.adjustSize()


    # Функция удаления выбранной строки в первой таблице
    def delete_first(self):
        if self.first_table.activated and self.first_table.currentRow() != -1:
            self.first_table.removeRow(self.first_table.currentRow())
            self.first_table.selectionModel().clearCurrentIndex()
        else:
            self.show_message("Не выбрана строка")

    # Функция удаления выбранной строки в второй таблице
    def delete_second(self):
        if self.second_table.activated and self.second_table.currentRow() != -1:
            self.second_table.removeRow(self.second_table.currentRow())
            self.second_table.selectionModel().clearCurrentIndex()
        else:
            self.show_message("Не выбрана строка")


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()