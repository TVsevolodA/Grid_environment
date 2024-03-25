import requests
import functools
from PyQt5.QtCore import pyqtSignal, QSize, Qt, QThread
from PyQt5.QtGui import QIntValidator, QMovie
from PyQt5.QtWidgets import QMainWindow, QLineEdit, QLabel, QPushButton, QVBoxLayout, QWidget, QGridLayout, QScrollArea


class MyThread(QThread):
    end_work_signal = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.maximum_number_queens = 0
        self.decisions = []
        self.N = 8
        self.posns = '[]'

    def set_parameters(self, N, posns):
        self.N = N
        self.posns = posns

    def check_combinations(self, NEW_NUMBER_QUEENS, COMBINATIONS):
        if NEW_NUMBER_QUEENS > self.maximum_number_queens:
            self.maximum_number_queens = NEW_NUMBER_QUEENS
            self.decisions.clear()
            self.decisions.extend(COMBINATIONS)
        elif NEW_NUMBER_QUEENS == self.maximum_number_queens:
            self.decisions.extend(COMBINATIONS)

    def run(self):
        URL = 'http://localhost:5000/assign_task'

        arguments = {'data': f'{self.N}|{self.posns}', 'name_files': ['kernel.py']}

        response = requests.get(URL, json=arguments)

        data = response.json()
        for solution_option in data:
            queens = int(solution_option[0])
            arrangements = solution_option[1:]
            self.check_combinations(queens, arrangements)
        # data['N'] = self.N
        self.decisions = list(set(self.decisions))
        end_result = {'N': self.maximum_number_queens, 'positions': self.decisions}
        self.end_work_signal.emit(end_result)


class MainWindow(QMainWindow):
    signal_close_notes_form = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.window = None
        self.myThread = None
        self.grid = None
        self.input = None
        self.positions = set()
        self.MIN_N = 4
        self.MAX_N = 100
        self.create_ui()

    def generate(self):
        positions_list = []

        for pos in self.positions:
            args_pos = pos.split(';')
            positions_list.append([int(args_pos[0]), int(args_pos[1])])
        self.positions.clear()

        input_field = self.input.text()
        N = int(input_field) if len(input_field) != 0 else 8
        positions_str = str(positions_list)
        self.myThread.set_parameters(N, positions_str)
        self.myThread.start()

    def create_ui(self):
        self.setWindowTitle('Расстановка ферзей')
        label = QLabel('Введите размер сетки:')

        self.input = QLineEdit()
        self.input.textChanged.connect(self.rebuild_board)
        self.input.setValidator(QIntValidator(self.MIN_N, self.MAX_N))

        self.grid = QGridLayout()
        self.grid.setSpacing(0)

        button = QPushButton('Сгенерировать')
        button.clicked.connect(self.generate)

        self.myThread = MyThread()
        self.myThread.started.connect(self.on_started)
        self.myThread.finished.connect(self.on_finished)
        self.myThread.end_work_signal.connect(self.changing_window, Qt.QueuedConnection)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setLayout(self.grid)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.input)
        layout.addWidget(button)
        layout.addWidget(scroll)

        self.draw_board()

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def rebuild_board(self):
        N = self.input.text()
        for i in reversed(range(self.grid.count())):
            self.grid.itemAt(i).widget().deleteLater()
        if len(N) != 0:
            self.draw_board(int(N))
        else:
            self.draw_board()

    def draw_board(self, N=8):
        WHITE = '#ffffff'
        BLACK = '#000000'
        for x in range(N):
            for y in range(N):
                cell = QLabel()
                cell.setAlignment(Qt.AlignCenter)
                cell.mousePressEvent = functools.partial(self.change_queen, label=cell)
                cell.resize(QSize(10, 10))
                if x % 2 == 0:
                    color = WHITE if y % 2 == 0 else BLACK
                else:
                    color = BLACK if y % 2 == 0 else WHITE
                cell.setObjectName(f'{x};{y};{color}')
                cell.setStyleSheet(
                    'QLabel{' +
                    f'background-color: {color};' + '}QLabel:hover {border: 2.5px solid rgb(0, 255, '
                                                    '0); background-color: #66ff66}')
                self.grid.addWidget(cell, x, y)

    def change_queen(self, event, label=None):
        args_label = label.objectName().split(';')
        if len(label.text()) != 0:
            label.setText('')
            label.setStyleSheet(f'background-color: {args_label[2]}')
            self.positions.remove(label.objectName())
        else:
            label.setText('Ф')
            label.setStyleSheet('background-color: #008000')
            self.positions.add(label.objectName())
        print(label.objectName())

    def on_started(self):
        label = QLabel('Выполняется подсчет.\nПожалуйста подождите!')
        label_anim = QLabel()
        movie = QMovie('/home/vsevolod/Projects/Python/Grid_environment/app/loading.gif')
        label_anim.setMovie(movie)
        movie.start()
        label_anim.show()

        layuot = QVBoxLayout()
        layuot.addWidget(label)
        layuot.addWidget(label_anim)

        self.window = QWidget()
        self.window.setLayout(layuot)
        self.window.show()

    def on_finished(self):
        self.window.destroy()

    def changing_window(self, res_dict):
        self.signal_close_notes_form.emit(res_dict)
