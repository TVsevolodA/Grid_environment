from PyQt5.QtWidgets import QApplication

from main_widget import MainWidget

app = QApplication([])
window = MainWidget()
window.show()
app.exec()
