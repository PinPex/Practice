import sys
import os
import time
#from PySide6.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QFileDialog, QLabel, QPushButton, QMessageBox

from parser.parser import Parsing

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

sys.path.append("../")

from database.scripts.fillBase import Database

class Desktop(QWidget):
    label: QLabel
    label_2: QLabel
    label_3: QLabel
    pushButton: QPushButton
    pushButton_2: QPushButton
    pushButton_3: QPushButton
    Window: QWidget
    num_of_threads: int = 64
    path_current_photo: str
    pars: Parsing
    def __init__(self, parent = None) -> None:
        super().__init__(parent)
        self.Window = uic.loadUi("./interfaces/search.ui")
        self.label = self.Window.label
        self.label_2 = self.Window.label_2
        self.label_3 = self.Window.label_3
        self.label.setScaledContents(True)
        self.label_2.setScaledContents(True)
        self.pushButton = self.Window.pushButton
        #self.pushButton_2 = self.Window.pushButton_2
        self.pushButton_3 = self.Window.pushButton_3
        self.set_clicker(self.pushButton_3, self.open_file)
        self.set_clicker(self.pushButton, self.find_human)

    def setLabelImage(self, label: QLabel, filepath):
        #label.setScaledContents(True)
        
        pixmap = QPixmap(filepath)
        
        label.setPixmap(pixmap.scaled(label.size(), Qt.KeepAspectRatio))
    
    def show(self) -> None:
        self.Window.show()
    def open_file(self):
        self.pars = Parsing()
        self.path_current_photo = QFileDialog.getOpenFileName(self)[0]
        self.setLabelImage(self.label, self.path_current_photo)
    def find_human(self):

        if self.pars.prepare_photo(self.path_current_photo) != 1:
            ## Testing with 10 runs
            #time_ = 0.0
            #for i in range(10):
                #start = time.time()
                #self.pars.main_loop(self.num_of_threads)
                #time_ += time.time() - start
            #print(time_ / 10)
            start = time.time()
            self.pars.main_loop(self.num_of_threads)
            print(time.time() - start)
            self.pars.write_to_file(self.pars.result[4], "temp.jpg")
            self.setLabelImage(self.label_2, "temp.jpg")
            self.label_3.setText(self.pars.result[2])
            os.remove("temp.jpg")
            
        else:
            mes = QMessageBox(self)
            mes.show()
            mes.setText(self.pars.error)
        
        

    
        
        
    def set_clicker(self, pushButton, command) -> None:
        pushButton.clicked.connect(command)