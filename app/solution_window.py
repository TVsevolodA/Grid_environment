import ast
from PyQt5.QtCore import pyqtSignal, Qt, QSize
from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QGridLayout, QScrollArea, QFrame, \
    QSizePolicy


def draw_board(N, solution):
    grid = QGridLayout()
    grid.setSpacing(0)
    WHITE = '#ffffff'
    BLACK = '#000000'
    for x in range(N):
        for y in range(N):
            cell = QLabel()
            cell.setAlignment(Qt.AlignCenter)
            cell.resize(QSize(10, 10))
            if x % 2 == 0:
                color = WHITE if y % 2 == 0 else BLACK
            else:
                color = BLACK if y % 2 == 0 else WHITE

            if [x, y] in solution:
                cell.setText('Ф')
                cell.setStyleSheet('background-color: #008000;')
            else:
                cell.setStyleSheet(f'background-color: {color};')
            grid.addWidget(cell, x, y)
    return grid


class SolutionWindow(QMainWindow):
    signal_close_notes_form = pyqtSignal(dict)

    def __init__(self, N, pos):
        super().__init__()
        self.layout = None
        self.quantity = N
        self.solutions = pos
        self.create_ui()

    def create_ui(self):
        self.setWindowTitle('Расстановка ферзей. Комбинации')
        label = QLabel('Решения:')

        button = QPushButton('На главную')
        button.clicked.connect(self.generate)

        self.layout = QVBoxLayout()
        self.layout.addWidget(label)
        self.layout.addWidget(button)

        self.draw_solutions()

        container = QWidget()
        container.setLayout(self.layout)

        scroll = QScrollArea()
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)
        scroll.setWidget(container)

        self.setCentralWidget(scroll)

    def generate(self):
        self.signal_close_notes_form.emit({})

    def draw_solutions(self):
        for solution in self.solutions:
            solution = ast.literal_eval(solution)
            board = draw_board(self.quantity, solution)

            separador = QFrame()
            separador.setFrameShape(QFrame.HLine)
            # separador.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
            separador.setLineWidth(3)

            self.layout.addWidget(separador)
            self.layout.addLayout(board)
