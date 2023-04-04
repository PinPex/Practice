import sys
import os
#from PySide6.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QLabel, QPushButton, QSizePolicy, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
from parser.parser import Parsing
from parser.parser import face

from queue import Queue
from PyQt5.QtCore import Qt
from PIL import Image
sys.path.append("../")
import time
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
        self.pushButton_2 = self.Window.pushButton_2
        self.pushButton_3 = self.Window.pushButton_3
        self.set_clicker(self.pushButton_3, self.open_file)
        self.set_clicker(self.pushButton, self.find_human)

    def setLabelImage(self, label: QLabel, filepath):
        image = QImage(filepath)
        pp = QPixmap.fromImage(image.scaled(label.width(), label.height()))
        label.setPixmap(pp)
    
    def show(self) -> None:
        self.Window.show()
    def open_file(self):
        self.pars = Parsing()
        self.path_current_photo = QFileDialog.getOpenFileName(self)[0]
        self.setLabelImage(self.label, self.path_current_photo)
    def find_human(self):
        start = time.time()

        image = QImage(self.path_current_photo)
        pp = QPixmap(image)
        pp = pp.scaled(210, 210, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatioByExpanding) # with some images breaks
        pp.save("temp3.jpg")
        
        bin_face = face.load_image_file("temp3.jpg")
        print(face.face_locations(bin_face)) #crop in this positions
        
        image = Image.open("temp3.jpg")
        #os.remove("temp3.jpg")
        tup = face.face_locations(bin_face)[0]
        print(tup)
        image = image.crop((tup[3], tup[0], tup[1], tup[2]))
        image = image.convert('RGB')
        image.save("temp2.jpg")

        image = QImage("temp2.jpg")
        #os.remove("temp2.jpg")
        pp = QPixmap(image)
        pp = pp.scaled(60, 60, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatioByExpanding) # with some images breaks
        
        pp.save("temp1.jpg")



        if self.pars.prepare_photo("temp1.jpg") != 1:
            self.pars.main_loop(self.num_of_threads)
            self.pars.write_to_file(self.pars.result[4], "temp.jpg")
            self.setLabelImage(self.label_2, "temp.jpg")
            self.label_3.setText(self.pars.result[2])
            os.remove("temp.jpg")
            print(time.time() - start)
        else:
            mes = QMessageBox(self)
            mes.show()
            mes.setText(self.pars.error)
        #os.remove("temp1.jpg")
        
        

    
        
        
    def set_clicker(self, pushButton, command) -> None:
        pushButton.clicked.connect(command)