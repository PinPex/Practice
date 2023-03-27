import sys
import os
#from PySide6.QtWidgets import *
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QLabel, QPushButton, QSizePolicy, QTextEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
sys.path.append("../")
from database.scripts.fillBase import Database

class Add(QWidget):
    label: QLabel
    pushButton_2: QPushButton
    pushButton_3: QPushButton
    lineEdit: QLineEdit
    lineEdit_2: QLineEdit
    textEdit: QTextEdit
    Window: QWidget
    num_of_threads: int = 4

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.Window : QWidget = uic.loadUi("../database/interfaces/Add.ui")
        self.label : QLabel = self.Window.label
        self.label.setScaledContents(True)
        self.pushButton_2 : QPushButton = self.Window.pushButton_2
        self.pushButton_3 : QPushButton = self.Window.pushButton_3
        self.lineEdit : QLineEdit = self.Window.lineEdit
        self.lineEdit_2 : QLineEdit = self.Window.lineEdit_2
        self.textEdit : QTextEdit = self.Window.textEdit
        self.set_clicker(self.pushButton_2, self.open_photo)
        self.set_clicker(self.pushButton_3, self.add_database)

    def write_in_file(self, name_file, text, code):
        with open(name_file, "wb") as name_file:
            name_file.write(bytes(text, code))

    def add_database(self):
        db = Database()
        db.insert_blob(str(self.lineEdit.text()), str(self.textEdit.toHtml()), str(self.lineEdit_2.text()))
            
        

    def open_photo(self):
        path = QFileDialog.getOpenFileName(self)[0]
        self.lineEdit_2.setText(path)
        self.setLabelImage(self.label, path)


    def setLabelImage(self, label: QLabel, filepath):
        image = QImage(filepath)
        pp = QPixmap(image)
        pp = pp.scaled(200, 200, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatioByExpanding)
        label.setPixmap(pp)
        label.setMaximumSize(pp.width(), pp.height())
        
    def show(self) -> None:
        self.Window.show()

        
        
    def set_clicker(self, pushButton: QPushButton, command) -> None:
        pushButton.clicked.connect(command)