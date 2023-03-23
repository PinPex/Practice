import sys
from PySide6.QtWidgets import *
from PyQt5 import QtWidgets, uic

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = uic.loadUi("search.ui")
    window.show()
    window.label.setText("chlen")
    app.exec()
