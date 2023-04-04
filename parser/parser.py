import sqlite3 as sq
import face_recognition as face
import sys
import os
import threading
import time
import numpy as np
import io
from queue import Queue



class Parsing:
    def __init__(self) -> None:
        pass

    result: list = list()

    def write_to_file(self, data, filename):
        with open(filename, 'wb') as file:
            file.write(data)

    def parsing(self, row, unknown_encoding):
        results = face.compare_faces([row[3]], unknown_encoding)
        if results[0] == True:
            self.result = row

    def thread_job(self, records, unknown_encoding, i, num_of_threads):
        
        num = int(len(records) / num_of_threads)
        L = (i) * num
        R = (i + 1) * num
        if R < len(records) and i == num_of_threads - 1:
            R = len(records)
        for j in range(L, R):
            self.parsing(records[j], unknown_encoding)
        
    def adapt_array(self, arr):
        out = io.BytesIO()
        np.save(out, arr)
        out.seek(0)
        return sq.Binary(out.read())

    def convert_array(self, text):
        out = io.BytesIO(text)
        out.seek(0)
        return np.load(out)

    arr = []

    error: str

    def prepare_photo(self, photo_path):
        unknown_image = face.load_image_file(photo_path)
        if face.face_encodings(unknown_image):
            self.arr = face.face_encodings(unknown_image)[0]
        else:
            self.error = "Error: in unknown photo face not exists"
            return 1

    def main_loop(self, num_of_threads = 4):
        path = str(os.getcwd()) 
        sq.register_adapter(np.ndarray, self.adapt_array)
        sq.register_converter("array", self.convert_array)
        
        con = sq.connect(path[:path.rindex('/')] + '/database/sqlite_python.db', detect_types=sq.PARSE_DECLTYPES)

        cursor = con.cursor()
        cursor.execute("SELECT * FROM Faces")
        records = cursor.fetchall()

        
        
        threads = [
                threading.Thread(target=self.thread_job, args=(records, self.arr, i, num_of_threads))
                for i in range(0, num_of_threads)
            ]
        for thread in threads:
            
            thread.start()
        for thread in threads:
            thread.join()
        return self.result
    