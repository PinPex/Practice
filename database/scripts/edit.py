import sys
import os
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QLabel, QPushButton, QSizePolicy, QTextEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
sys.path.append("../")
from database.scripts import add, show
from database.scripts.fillBase import Database



class Delete(QWidget):
    pushButton: QPushButton
    lineEdit: QLineEdit
    textEdit: QTextEdit
    Window: QWidget
    db: Database
    def __init__(self, parent = None) -> None:
        super().__init__(parent)
        self.Window : QWidget = uic.loadUi("../database/interfaces/Delete.ui")
        self.pushButton = self.Window.pushButton
        self.lineEdit = self.Window.lineEdit
        self.textEdit = self.Window.textEdit
        self.set_clicker(self.pushButton, self.delete)
        self.db = Database()
        
    def delete(self):
        self.db.delete_sqlite_record(int(self.lineEdit.text()))

    def show(self) -> None:
        self.Window.show()

    
        
    def set_clicker(self, pushButton: QPushButton, command) -> None:
        pushButton.clicked.connect(command)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Delete("../database/interfaces/Database.ui")
    
    window.show()
    app.exec()