from PyQt5.QtWidgets import QApplication
from clsmainWindow import clsmainWindow
import sys

app = QApplication([])
f = clsmainWindow()
f.show()
sys.exit(app.exec_())