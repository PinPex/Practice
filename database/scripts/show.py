import sys
import os
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QLabel, QPushButton, QSizePolicy, QTextEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
sys.path.append("../")
from database.scripts.fillBase import Database

class Show(QWidget):
    Window: QWidget
    textEdit: QTextEdit
    pushButton: QPushButton
    db: Database
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.db = Database()
        self.Window : QWidget = uic.loadUi("../database/interfaces/Show.ui")
        self.textEdit = self.Window.textEdit
        self.pushButton = self.Window.pushButton
        self.set_clicker(self.pushButton, self.update_list)
        self.update_list()
    def show(self) -> None:
        self.Window.show()
    
    def update_list(self):
        self.db.show_database()
        with open("../database/outinput/names.txt") as names:
            self.textEdit.setText(names.read())

    def set_clicker(self, pushButton: QPushButton, command) -> None:
        pushButton.clicked.connect(command)
