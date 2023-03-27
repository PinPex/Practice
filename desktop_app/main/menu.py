import sys
import os
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QLabel, QPushButton, QSizePolicy, QTextEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage

sys.path.append("../")
from database.scripts import add, show
from database.scripts.fillBase import Database
from database.main.Database import DatabaseMenu
from desktop_app.scripts.desktop import Desktop



class Menu(QWidget):
    pushButton: QPushButton
    pushButton_2: QPushButton
    Window: QWidget
    db: Database
    def __init__(self) -> None:
        super().__init__()
        self.Window : QWidget = uic.loadUi("./interfaces/Menu.ui")
        self.pushButton = self.Window.pushButton
        self.pushButton_2 = self.Window.pushButton_2
        self.set_clicker(self.pushButton, self.openSearch)
        self.set_clicker(self.pushButton_2, self.openBase)
        self.db = Database()

    def show(self) -> None:
        self.Window.show()
    def openSearch(self):
        window_search = Desktop(self)
        window_search.show()
    def openBase(self):
        window_search = DatabaseMenu(self)
        window_search.show()
    
        
    def set_clicker(self, pushButton: QPushButton, command) -> None:
        pushButton.clicked.connect(command)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    
    window = Menu()
    
    
    window.show()
    app.exec()