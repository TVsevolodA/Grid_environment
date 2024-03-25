from PyQt5.QtWidgets import QMainWindow, QStackedWidget

from main_window import MainWindow
from solution_window import SolutionWindow


class MainWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.num_win = False
        # self.main = MainWindow()
        # self.main.signal_close_notes_form.connect(self.change_screen)
        # self.central_widget.addWidget(self.main)

        # self.central_widget.setCurrentWidget(self.main)
        self.change_screen({})

    def change_screen(self, res_dict):
        self.num_win = not self.num_win
        if self.num_win:
            main = MainWindow()
            main.signal_close_notes_form.connect(self.change_screen)
            self.central_widget.addWidget(main)
            self.central_widget.setCurrentWidget(main)
        else:
            c = res_dict['N']
            s = res_dict['positions']
            count = len(s)
            print(f'Кол-во решений: {count}')
            # print(f'MAX кол-во ферзей: {res_dict['quantity']}')
            print(f'Решения: {s}')
            solution = SolutionWindow(c, s)
            solution.signal_close_notes_form.connect(self.change_screen)
            self.central_widget.addWidget(solution)
            self.central_widget.setCurrentWidget(solution)
