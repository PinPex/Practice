import sys
import os
#from PySide6.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QLabel, QPushButton, QSizePolicy
from PyQt5 import QtGui
from parser.parser import Parsing
from queue import Queue

class Desktop(QWidget):
    label: QLabel
    label_2: QLabel
    label_3: QLabel
    pushButton: QPushButton
    pushButton_2: QPushButton
    pushButton_3: QPushButton
    Window: QWidget
    num_of_threads: int = 4
    path_current_photo: str
    def __init__(self, parent = None) -> None:
        super().__init__(parent)
        self.Window = uic.loadUi("./interfaces/search.ui")
        self.label = self.Window.label
        self.label_2 = self.Window.label_2
        self.label_3 = self.Window.label_3
        self.label.setScaledContents(True)
        self.label_2.setScaledContents(True)
        self.pushButton = self.Window.pushButton
        self.pushButton_2 = self.Window.pushButton_2
        self.pushButton_3 = self.Window.pushButton_3
        self.set_clicker(self.pushButton_3, self.open_file)
        self.set_clicker(self.pushButton, self.find_human)

    def setLabelImage(self, label: QLabel, filepath):
        image = QtGui.QImage(filepath)
        pp = QtGui.QPixmap.fromImage(image.scaled(label.width(), label.height()))
        label.setPixmap(pp)
        
    def show(self) -> None:
        self.Window.show()
    def open_file(self):
        self.path_current_photo = QFileDialog.getOpenFileName(self)[0]
        self.setLabelImage(self.label, self.path_current_photo)
    def find_human(self):
        pars = Parsing()
        pars.main_loop(self.path_current_photo, self.num_of_threads)
        pars.write_to_file(pars.result[4], "temp.jpg")
        self.setLabelImage(self.label_2, "temp.jpg")
        self.label_3.setText(pars.result[2])
        os.remove("temp.jpg")

        
        
    def set_clicker(self, pushButton, command) -> None:
        pushButton.clicked.connect(command)