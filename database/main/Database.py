import sys
import os
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QLabel, QPushButton, QSizePolicy, QTextEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
print(str(os.getcwd()) )
sys.path.append("../")
from database.scripts import add, show, delete
from database.scripts.fillBase import Database



class DatabaseMenu(QWidget):
    pushButton: QPushButton
    pushButton_2: QPushButton
    pushButton_3: QPushButton
    pushButton_4: QPushButton
    pushButton_5: QPushButton
    Window: QWidget
    db: Database
    def __init__(self, parent = None) -> None:
        super().__init__(parent)
        self.Window : QWidget = uic.loadUi("../database/interfaces/Database.ui")
        self.pushButton = self.Window.pushButton
        self.pushButton_2 = self.Window.pushButton_2
        self.pushButton_3 = self.Window.pushButton_3
        self.pushButton_4 = self.Window.pushButton_4
        self.pushButton_5 = self.Window.pushButton_5
        self.set_clicker(self.pushButton, self.run_add)
        self.set_clicker(self.pushButton_2, self.run_show)
        self.set_clicker(self.pushButton_3, self.run_drop)
        self.set_clicker(self.pushButton_4, self.run_create)
        self.set_clicker(self.pushButton_5, self.run_delete)
        self.db = Database()
        
    def run_add(self):
        add_window = add.Add(self)
        add_window.show()

    def run_show(self):
        self.db.show_database()
        show_window = show.Show(self)
        show_window.show()

    def run_drop(self):
        self.db.drop_table("Faces")

    def run_create(self):
        self.db.create_table("Faces")
    
    def run_delete(self):
        delete_window = delete.Delete(self)
        delete_window.show()
    def show(self) -> None:
        self.Window.show()

    
        
    def set_clicker(self, pushButton: QPushButton, command) -> None:
        pushButton.clicked.connect(command)