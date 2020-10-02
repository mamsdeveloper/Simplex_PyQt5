import sys
import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon, QImage, QPainter, QPixmap
from PyQt5.QtWidgets import (QAbstractItemView, QAction, QApplication,
                             QCheckBox, QFileDialog, QFrame, QGridLayout,
                             QHeaderView, QLabel, QLineEdit, QMainWindow,
                             QMessageBox, QPushButton, QSlider, QTableWidget,
                             QTableWidgetItem, QTabWidget, QTextEdit, QWidget)
from xlrd import open_workbook
from xlwt import Font, Workbook, easyxf

import __main__
from functions import *

class my_tab_1_class(QWidget):
    def __init__(self):
        super().__init__()

        input_label = QLabel('Условие')
        ########
        output_label = QLabel('Решение')
        ########
        table_clear_button = QPushButton('Очистить', self)
        table_clear_button.setCursor(Qt.PointingHandCursor)
        table_clear_button.clicked.connect(self.TableClear)
        ########
        self.output_mod_button = QPushButton('Максимум', self)
        self.output_mod_button
        self.output_mod_button.clicked.connect(self.ModChange)
        self.mod = 0

        ########

        self.my_table_1 = QTableWidget(4, 4, self)
        self.my_table_1.setHorizontalHeaderLabels(['A1', 'A2', 'A3', 'B1'])
        self.my_table_1.setVerticalHeaderLabels(['A1', 'A2', 'A3', 'B2'])

        my_h_header = h_header_class(self.my_table_1)
        self.my_table_1.setHorizontalHeader(my_h_header)
        my_v_header = v_header_class(self.my_table_1)
        self.my_table_1.setVerticalHeader(my_v_header)

        for i in range(4):
            for j in range(4):
                item = QTableWidgetItem()
                self.my_table_1.setItem(i, j, item)

        self.my_table_1.cellChanged.connect(self.TableChange)
        self.input_mod = 0

        #########

        self.my_table_2 = QTableWidget(4, 4, self)
        self.my_table_2.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.my_table_2.setHorizontalHeaderLabels(['A1', 'A2', 'A3', 'B1'])
        self.my_table_2.setVerticalHeaderLabels(['A1', 'A2', 'A3', 'B2'])

        my_h_header = h_header_class(self.my_table_2)
        self.my_table_2.setHorizontalHeader(my_h_header)
        my_v_header = v_header_class(self.my_table_2)
        self.my_table_2.setVerticalHeader(my_v_header)

        for i in range(4):
            for j in range(4):
                item = QTableWidgetItem()
                self.my_table_2.setItem(i, j, item)

        ########

        box_layout_1 = QGridLayout()
        box_layout_1.setSpacing(20)

        box_layout_1.setRowStretch(0, 0)
        box_layout_1.setRowStretch(1, 1)
        box_layout_1.setRowStretch(2, 0)
        box_layout_1.setRowStretch(3, 1)

        box_layout_1.addWidget(input_label, 0, 0)
        box_layout_1.addWidget(table_clear_button, 0, 2)
        box_layout_1.addWidget(self.my_table_1, 1, 0, 1, 3)
        box_layout_1.addWidget(output_label, 2, 0)
        box_layout_1.addWidget(self.output_mod_button, 2, 2)
        box_layout_1.addWidget(self.my_table_2, 3, 0, 3, 3)

        self.setLayout(box_layout_1)

    #########

    def ModChange(self):
        mod_change(self)
        self.TableChange()

    def TableClear(self):
        table_clear(self)

    def TableChange(self):
        a, b, self.input_mod, able = input_data(self.my_table_1)

        if able and find_points(b):
            ans = answer(a, b, find_points(b))
            answer_view(self, b, ans[0], ans[1],
                        ans[2], ans[3], ans[4], ans[5])


class my_tab_2_class(QWidget):
    def __init__(self):
        super().__init__()
        ########
        self.m_slider = QSlider(Qt.Vertical, self)
        self.m_slider.valueChanged[int].connect(self.SliderChange)
        self.m_slider.setRange(10, 100)
        self.m_slider.setSliderPosition(10)
        self.m_slider.setTickInterval(10)
        self.m_slider.setSingleStep(10)
        self.m = 10
        ########
        self.checkbox_polygon = QCheckBox('Область решений', self)
        self.checkbox_polygon.stateChanged.connect(self.update)
        self.checkbox_polygon.toggle()

        self.checkbox_vector = QCheckBox('Вектор', self)
        self.checkbox_vector.stateChanged.connect(self.update)
        self.checkbox_vector.toggle()

        self.checkbox_points = QCheckBox('Точки входа и выхода', self)
        self.checkbox_points.stateChanged.connect(self.update)
        self.checkbox_points.toggle()

        self.checkbox_marking = QCheckBox('Разметка', self)
        self.checkbox_marking.stateChanged.connect(self.update)
        self.checkbox_marking.toggle()
        ########
        self.paint_box = QFrame()
        self.paint_box.setFrameStyle(QFrame.Box)
        ########
        box_layout_2 = QGridLayout()
        box_layout_2.setHorizontalSpacing(60)
        box_layout_2.setVerticalSpacing(150)

        box_layout_2.addWidget(self.checkbox_polygon, 0, 0)
        box_layout_2.addWidget(self.checkbox_vector, 1, 0)
        box_layout_2.addWidget(self.checkbox_points, 2, 0)
        box_layout_2.addWidget(self.checkbox_marking, 3, 0)
        box_layout_2.addWidget(self.m_slider, 0, 1, 4, 1)
        box_layout_2.addWidget(self.paint_box, 0, 2, 4, 2)

        self.setLayout(box_layout_2)

    def SliderChange(self, m):
        self.m = m//5*5
        # АААААА мой первый костыль! яжпрограммист
        self.m_slider.setSliderPosition(self.m)
        self.update()

    def paintEvent(self, e):
        w = self.paint_box.width()
        h = self.paint_box.height()

        data = input_data(__main__.main_window.my_tab_1.my_table_1)
        if data[3]:
            points = find_points(data[1])
            p_min = [answer(data[0], data[1], points)[0][0],
                     answer(data[0], data[1], points)[0][1]]
            p_max = [answer(data[0], data[1], points)[3][0],
                     answer(data[0], data[1], points)[3][1]]
        ########

        self.graph = QImage(self.paint_box.size(), QImage.Format_ARGB32)
        self.graph.fill(Qt.white)

        if self.checkbox_marking.isChecked():
            self.graph = graph_marks(self.graph, self.m, w, h)

        if data[3] and self.checkbox_polygon.isChecked():
            self.graph = graph_polygon(self.graph, points, self.m, w, h)

        if data[3]:
            self.graph = graph_lines(self.graph, self.m, data[1], w, h)

        if data[3] and self.checkbox_vector.isChecked():
            self.graph = graph_vector(self.graph, self.m, data[0], w, h)

        if data[3] and self.checkbox_points.isChecked():
            self.graph = graph_points(
                self.graph, self.m, data[0], points, p_min, p_max, w, h)

        p = QPainter(self)
        p.drawImage(self.paint_box.pos(), self.graph)
        p.end()


class h_header_class(QHeaderView):
    def __init__(self, parent):
        QHeaderView.__init__(self, Qt.Horizontal, parent)

        self.setSectionResizeMode(1)


class v_header_class(QHeaderView):
    def __init__(self, parent):
        QHeaderView.__init__(self, Qt.Vertical, parent)

        self.setSectionResizeMode(1)


class TheoryWindow(QWidget):
    def __init__(self):
        super().__init__()

        t_edit = QTextEdit()
        t_edit.setFrameStyle(QFrame.Box)
        t_edit.setText('Линейное программирование — математическая дисциплина, посвящённая теории и методам решения экстремальных задач на множествах n-мерного векторного пространства, задаваемых системами линейных уравнений и неравенств.')
        t_edit.setReadOnly(True)
        t_layout = QGridLayout()
        t_layout.addWidget(t_edit, 0, 0)
        self.setLayout(t_layout)
        self.setFont(QFont('Arial', 12))
        self.setWindowIcon(QIcon(f'{os.getcwd()}\Assets\App.ico'))
        self.setWindowTitle('Теория')


class InfWindow(QWidget):
    def __init__(self):
        super().__init__()

        title_lable = QLabel('Формат таблицы для открытия')

        picture_label_1 = QLabel()
        picture_1 = QPixmap(f'{os.getcwd()}\Assets\pic1.jpg')
        picture_label_1.setPixmap(picture_1)

        picture_label_2 = QLabel()
        picture_2 = QPixmap(f'{os.getcwd()}\Assets\pic2.jpg')
        picture_label_2.setPixmap(picture_2)

        layout = QGridLayout()

        layout.addWidget(title_lable, 0, 0)
        layout.addWidget(picture_label_1, 1, 0)
        layout.addWidget(picture_label_2, 1, 1)

        self.setLayout(layout)
        self.setFont(QFont('Arial', 12))
        self.setMaximumSize(640, 480)
        self.setWindowTitle('Формат таблицы для открытия')
        self.setWindowIcon(QIcon(f'{os.getcwd()}\Assets\App.ico'))


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        ########
        f = open(f'{os.getcwd()}\Assets\style.qss', 'r')
        self.setStyleSheet(f.read())
        f.close()

        my_menubar = self.menuBar()

        '''Fail'''
        M_Fail = my_menubar.addMenu('Файл')

        Open_Task = QAction('Открыть задачу', self)
        Open_Task.setShortcut('Ctrl+O')
        Open_Task.triggered.connect(self.OpenTask)

        Task_Save = QAction('Сохранить задачу', self)
        Task_Save.setShortcut('Ctrl+T')
        Task_Save.triggered.connect(self.TaskSave)

        Answer_Save = QAction('Сохранить решение', self)
        Answer_Save.setShortcut('Ctrl+A')
        Answer_Save.triggered.connect(self.AnswerSave)

        All_Save = QAction('Сохранить задачу и решение', self)
        All_Save.setShortcut('Ctrl+F')
        All_Save.triggered.connect(self.AllSave)

        Graph_Save = QAction('Сохранить график', self)
        Graph_Save.setShortcut('Ctrl+G')
        Graph_Save.triggered.connect(self.GraphSave)

        Programm_Exit = QAction('Выйти', self)
        Programm_Exit.setShortcut('Ctrl+C')
        Programm_Exit.triggered.connect(self.close)

        M_Fail.addAction(Open_Task)
        M_Fail.addAction(Task_Save)
        M_Fail.addAction(Answer_Save)
        M_Fail.addAction(All_Save)
        M_Fail.addAction(Graph_Save)
        M_Fail.addAction(Programm_Exit)

        '''Theory'''
        M_Inf = my_menubar.addMenu('Справка')

        Theory_Open = QAction('Открыть теорию', self)
        Theory_Open.setShortcut('Ctrl+T')
        Theory_Open.triggered.connect(self.TheoryOpen)

        Inf_Open = QAction('Справка', self)
        Inf_Open.setShortcut('Ctrl+I')
        Inf_Open.triggered.connect(self.InfOpen)

        M_Inf.addAction(Theory_Open)
        M_Inf.addAction(Inf_Open)
        '''Tasks'''
        M_Tasks = my_menubar.addMenu('Задачи')

        Task_1 = QAction('Задача №1', self)
        Task_1.triggered.connect(self.Task1)

        Task_2 = QAction('Задача №2', self)
        Task_2.triggered.connect(self.Task2)

        M_Tasks.addAction(Task_1)
        M_Tasks.addAction(Task_2)
        ########

        my_tab = QTabWidget(self)

        self.my_tab_1 = my_tab_1_class()

        self.my_tab_2 = my_tab_2_class()

        my_tab.addTab(self.my_tab_1, 'Решение')
        my_tab.addTab(self.my_tab_2, 'График')

        main_layout = QGridLayout()

        main_layout.addWidget(my_tab, 0, 0)

        central_widget = QWidget(self)
        central_widget.setLayout(main_layout)

        self.setCentralWidget(central_widget)
        self.setMinimumSize(500, 900)
        self.setWindowTitle('Simplex')
        self.setWindowIcon(QIcon(f'{os.getcwd()}\Assets\App.ico'))
        self.showMaximized()

    def OpenTask(self):
        filename = QFileDialog.getOpenFileName(
            self, "Выбирете файл", None, "*.xlsx, *.xls")
        if filename == ('', ''):
            return

        book = open_workbook(filename[0])
        sheet = book.sheets()[0]
        data = [[sheet.cell_value(r, c) for c in range(sheet.ncols)]
                for r in range(sheet.nrows)]

        for i in range(len(data)):
            for j in range(len(data[i])):
                try:
                    data[i][j] = int(data[i][j])
                except ValueError:
                    continue

        data = [list(map(str, i)) for i in data]

        k = self.my_tab_1.my_table_1

        k.setItem(0, 0, QTableWidgetItem(data[2][1]))
        k.setItem(0, 1, QTableWidgetItem(data[2][2]))
        k.setItem(0, 2, QTableWidgetItem(data[2][3]))
        k.setItem(1, 0, QTableWidgetItem(data[3][1]))
        k.setItem(1, 1, QTableWidgetItem(data[3][2]))
        k.setItem(1, 2, QTableWidgetItem(data[3][3]))
        k.setItem(2, 0, QTableWidgetItem(data[4][1]))
        k.setItem(2, 1, QTableWidgetItem(data[4][2]))
        k.setItem(2, 2, QTableWidgetItem(data[4][3]))

        k.setItem(0, 3, QTableWidgetItem(data[2][4]))
        k.setItem(1, 3, QTableWidgetItem(data[3][4]))
        k.setItem(2, 3, QTableWidgetItem(data[4][4]))
        k.setItem(3, 0, QTableWidgetItem(data[5][1]))
        k.setItem(3, 1, QTableWidgetItem(data[5][2]))
        k.setItem(3, 2, QTableWidgetItem(data[5][3]))

    def TaskSave(self):
        data = input_data(self.my_tab_1.my_table_1)

        filename = QFileDialog.getSaveFileName(
            None, 'Сохранение графика', 'Моя Задача.xls', '*.xls')
        if filename == ('', ''):
            return

        self.wb = Workbook()

        self.task_sheet(data)

        try:
            self.wb.save(filename[0])
        except PermissionError:
            mb = QMessageBox(QMessageBox.Critical,
                             "Ошибка", "Закройте файл",
                             buttons=QMessageBox.Ok,
                             parent=self)
            mb_view = mb.exec_()

    def AnswerSave(self):
        data = input_data(self.my_tab_1.my_table_1)

        try:
            ans = answer(data[0], data[1], find_points(data[1]))
            filename = QFileDialog.getSaveFileName(
                None, 'Сохранение графика', 'Мое Решение.xls', '*.xls')
            if filename == ('', ''):
                return

            self.wb = Workbook()

            self.answer_sheet(data, ans)

            try:
                self.wb.save(filename[0])
            except PermissionError:
                mb = QMessageBox(QMessageBox.Critical,
                                 "Ошибка", "Закройте файл",
                                 buttons=QMessageBox.Ok,
                                 parent=self)
                mb_view = mb.exec_()
        except TypeError:
            mb = QMessageBox(QMessageBox.Critical,
                             "Ошибка", "Недостаточно данных",
                             buttons=QMessageBox.Ok,
                             parent=self)
            mb_view = mb.exec_()

    def AllSave(self):
        data = input_data(self.my_tab_1.my_table_1)

        try:
            ans = answer(data[0], data[1], find_points(data[1]))

            filename = QFileDialog.getSaveFileName(
                None, 'Сохранение графика', 'Задача и Решение.xls', '*.xls')
            if filename == ('', ''):
                return

            self.wb = Workbook()

            self.task_sheet(data)
            self.answer_sheet(data, ans)

            try:
                self.wb.save(filename[0])
            except PermissionError:
                mb = QMessageBox(QMessageBox.Critical,
                                 "Ошибка", "Закройте файл",
                                 buttons=QMessageBox.Ok,
                                 parent=self)
                mb_view = mb.exec_()

        except TypeError:
            mb = QMessageBox(QMessageBox.Critical,
                             "Ошибка", "Недостаточно данных",
                             buttons=QMessageBox.Ok,
                             parent=self)
            mb_view = mb.exec_()

    def GraphSave(self):
        filename = QFileDialog.getSaveFileName(
            None, 'Сохранение графика', 'График.png', '*.png ')

        if filename == ('', ''):
            return

        try:
            self.my_tab_2.graph.save(filename[0], 'PNG')
        except AttributeError:
            mb = QMessageBox(QMessageBox.Critical,
                             "Ошибка", "Пустой график",
                             buttons=QMessageBox.Ok,
                             parent=self)
            mb_view = mb.exec_()

    def TheoryOpen(self):
        self.theory_window = TheoryWindow()
        self.theory_window.showMaximized()

    def InfOpen(self):
        self.inf_window = InfWindow()
        self.inf_window.show()

    def Task1(self):
        k = self.my_tab_1.my_table_1

        k.setItem(0, 0, QTableWidgetItem('5'))
        k.setItem(0, 1, QTableWidgetItem('6'))
        k.setItem(0, 2, QTableWidgetItem('8'))
        k.setItem(1, 0, QTableWidgetItem('7'))
        k.setItem(1, 1, QTableWidgetItem('3'))
        k.setItem(1, 2, QTableWidgetItem('11'))

        k.setItem(0, 3, QTableWidgetItem('40'))
        k.setItem(1, 3, QTableWidgetItem('30'))
        k.setItem(3, 0, QTableWidgetItem('20'))
        k.setItem(3, 1, QTableWidgetItem('35'))
        k.setItem(3, 2, QTableWidgetItem('15'))

    def Task2(self):
        k = self.my_tab_1.my_table_1

        k.setItem(0, 0, QTableWidgetItem('0.7'))
        k.setItem(0, 1, QTableWidgetItem('0.9'))
        k.setItem(0, 2, QTableWidgetItem('0.8'))
        k.setItem(1, 0, QTableWidgetItem('0.3'))
        k.setItem(1, 1, QTableWidgetItem('0.4'))
        k.setItem(1, 2, QTableWidgetItem('0.6'))

        k.setItem(0, 3, QTableWidgetItem('3'))
        k.setItem(1, 3, QTableWidgetItem('5'))
        k.setItem(3, 0, QTableWidgetItem('5'))
        k.setItem(3, 1, QTableWidgetItem('2'))
        k.setItem(3, 2, QTableWidgetItem('1'))

    def task_sheet(self, data):

        font0 = Font()
        font0.name = 'Arial'
        font0.colour_index = 0

        style0 = easyxf("font: color black; align: horiz center")

        ws = self.wb.add_sheet('Задача', cell_overwrite_ok=True)

        ws.write_merge(0, 0, 0, 4, 'Условие', style0)
        ws.write(1, 1, 'A')
        ws.write(1, 2, 'B')
        ws.write(1, 3, 'C')
        ws.write(1, 4, 'D')
        ws.write(2, 0, 'I')
        ws.write(3, 0, 'II')
        ws.write(4, 0, 'III')
        ws.write(5, 0, 'IV')

        if data[2] == 0:
            # 'a's
            ws.write(2, 1, data[0][0])
            ws.write(2, 2, data[0][1])
            ws.write(2, 3, data[0][2])
            ws.write(3, 1, data[0][3])
            ws.write(3, 2, data[0][4])
            ws.write(3, 3, data[0][5])
            # 'b's
            ws.write(2, 4, data[1][0])
            ws.write(3, 4, data[1][1])
            ws.write(5, 1, data[1][2])
            ws.write(5, 2, data[1][3])
            ws.write(5, 3, data[1][4])
        else:
            # 'a's
            ws.write(4, 1, data[0][0])
            ws.write(3, 1, data[0][1])
            ws.write(2, 1, data[0][2])
            ws.write(4, 2, data[0][3])
            ws.write(3, 2, data[0][4])
            ws.write(2, 2, data[0][5])
            # 'b's
            ws.write(5, 1, data[1][0])
            ws.write(5, 2, data[1][1])
            ws.write(4, 4, data[1][2])
            ws.write(3, 4, data[1][3])
            ws.write(2, 4, data[1][4])

    def answer_sheet(self, data, ans):

        font0 = Font()
        font0.name = 'Arial'
        font0.colour_index = 0

        style0 = easyxf("font: color black; align: horiz center")

        ws = self.wb.add_sheet('Решение', cell_overwrite_ok=True)

        # Минимум
        ws.write_merge(0, 0, 0, 4, 'Минимум', style0)
        ws.write(1, 1, 'A')
        ws.write(1, 2, 'B')
        ws.write(1, 3, 'C')
        ws.write(1, 4, 'D')
        ws.write(2, 0, 'I')
        ws.write(3, 0, 'II')
        ws.write(4, 0, 'III')
        ws.write(5, 0, 'IV')

        if data[2] == 0:
            # 'a's
            ws.write(2, 1, ans[0][0])
            ws.write(2, 2, ans[0][1])
            ws.write(2, 3, ans[0][2])
            ws.write(3, 1, ans[0][3])
            ws.write(3, 2, ans[0][4])
            ws.write(3, 3, ans[0][5])
            # 'b's
            ws.write(2, 4, data[1][0])
            ws.write(3, 4, data[1][1])
            ws.write(5, 1, data[1][2])
            ws.write(5, 2, data[1][3])
            ws.write(5, 3, data[1][4])
        else:
            # 'a's
            ws.write(4, 1, ans[0][0])
            ws.write(3, 1, ans[0][1])
            ws.write(2, 1, ans[0][2])
            ws.write(4, 2, ans[0][3])
            ws.write(3, 2, ans[0][4])
            ws.write(2, 2, ans[0][5])
            # 'b's
            ws.write(5, 1, data[1][0])
            ws.write(5, 2, data[1][1])
            ws.write(4, 4, data[1][2])
            ws.write(3, 4, data[1][3])
            ws.write(2, 4, data[1][4])

        ws.write(5, 4, 'F= '+str(ans[1]))

        if ans[2]:
            ws.write(4, 3, 'Бесконечное')
        else:
            ws.write(4, 3, 'Конечное')

        # Максимум
        ws.write_merge(7, 7, 0, 4, 'Максимум', style0)
        ws.write(8, 1, 'A')
        ws.write(8, 2, 'B')
        ws.write(8, 3, 'C')
        ws.write(8, 4, 'D')
        ws.write(9, 0, 'I')
        ws.write(10, 0, 'II')
        ws.write(11, 0, 'III')
        ws.write(12, 0, 'IV')

        if data[2] == 0:
            # 'a's
            ws.write(9, 1, ans[3][0])
            ws.write(9, 2, ans[3][1])
            ws.write(9, 3, ans[3][2])
            ws.write(10, 1, ans[3][3])
            ws.write(10, 2, ans[3][4])
            ws.write(10, 3, ans[3][5])
            # 'b's
            ws.write(9, 4, data[1][0])
            ws.write(10, 4, data[1][1])
            ws.write(12, 1, data[1][2])
            ws.write(12, 2, data[1][3])
            ws.write(12, 3, data[1][4])
        else:
            # 'a's
            ws.write(11, 1, ans[3][0])
            ws.write(10, 1, ans[3][1])
            ws.write(9, 1, ans[3][2])
            ws.write(11, 2, ans[3][3])
            ws.write(10, 2, ans[3][4])
            ws.write(9, 2, ans[3][5])
            # 'b's
            ws.write(12, 1, data[1][0])
            ws.write(12, 2, data[1][1])
            ws.write(10, 4, data[1][2])
            ws.write(9, 4, data[1][3])
            ws.write(8, 4, data[1][4])

        ws.write(12, 4, 'F= '+str(ans[4]))

        if ans[5]:
            ws.write(11, 3, 'Бесконечное')
        else:
            ws.write(11, 3, 'Конечное')


app = QApplication(sys.argv)
main_window = MainWindow()
app.exec_()
