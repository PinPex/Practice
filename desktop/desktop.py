import sys
import os
#from PySide6.QtWidgets import *
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QLabel, QPushButton, QSizePolicy
from PyQt5 import QtGui

class MainWindow(QWidget):
    label: QLabel
    label_2: QLabel
    label_3: QLabel
    pushButton: QPushButton
    pushButton_2: QPushButton
    pushButton_3: QPushButton
    app: QApplication
    Window: QWidget
    num_of_threads: int = 4
    path_current_photo: str
    def __init__(self, Window, app) -> None:
        super().__init__()
        self.app = app
        self.Window = Window
        self.Window.setWindowTitle("Определить человека по фото")
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
        path = str(os.getcwd()) 
        os.system("python3 " + path[:path.rindex('/')] + "/parser/parser.py " + self.path_current_photo + 
                  " " + str(self.num_of_threads))
        self.setLabelImage(self.label_2, "photo.jpg")
        with open("name.txt", "r") as f:
            self.label_3.setText(f.read())
        os.remove("name.txt")
        os.remove("information.txt")
        os.remove("photo.jpg")

        
        
    def set_clicker(self, pushButton, command) -> None:
        pushButton.clicked.connect(command)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(uic.loadUi("search.ui"), app)
    
    window.show()
    
    app.exec()
