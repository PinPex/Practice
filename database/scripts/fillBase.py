import sqlite3 as sq
import sys
from tkinter import filedialog as fd
import os
import face_recognition as face
from PIL import Image
import numpy as np
import io
print(str(os.getcwd()) )
class Database:
    con: sq.Connection
    def __init__(self) -> None:
        sq.register_adapter(np.ndarray, self.adapt_array)
        sq.register_converter("array", self.convert_array)
        self.con = sq.connect("../database/sqlite_python.db", detect_types=sq.PARSE_DECLTYPES)
    
    def adapt_array(self, arr):
        out = io.BytesIO()
        np.save(out, arr)
        out.seek(0)
        return sq.Binary(out.read())

    def convert_array(self, text):
        out = io.BytesIO(text)
        out.seek(0)
        return np.load(out)

    def convert_to_binary_data(self, filename):
        # Преобразование данных в двоичный формат
        with open(filename, 'rb') as file:
            blob_data = file.read()
        return blob_data


    def insert_blob(self, name: str, about: str, photo: str):
        cursor = self.con.cursor()
        image = face.load_image_file(photo)
        image_encoding = []
        if face.face_encodings(image):
            image_encoding = face.face_encodings(image)[0]
        else:
            print("Error: in known photo face not exists")
        photo_bin = self.convert_to_binary_data(photo)
        cursor.execute("""INSERT INTO Faces
                                    (name, about, code, photo) VALUES (?, ?, ?, ?)""", 
                                    (name, about, image_encoding, photo_bin))
        self.con.commit()
        cursor.close()

    def delete_sqlite_record(self, dev_id):
        cursor = self.con.cursor()
        print("Подключен к SQLite")

        sql_update_query = """DELETE from Faces where id = ?"""
        cursor.execute(sql_update_query, (dev_id, ))
        self.con.commit()
        print("Запись успешно удалена")
        self.con.commit()
        cursor.close()




    def create_table(self, name_table):
        sq.register_adapter(np.ndarray, self.adapt_array)

        # Converts TEXT to np.array when selecting
        sq.register_converter("array", self.convert_array)

        x = np.arange(12).reshape(2,6)
        cur = self.con.cursor()
        print("Подключен к SQLite")
        cur.execute("""
            CREATE TABLE """ + name_table + """ (
                id INTEGER,
                about TEXT,  
                name TEXT, 
                code array,
                photo BLOB,
                
                PRIMARY KEY("id" AUTOINCREMENT)
                );
        """)
        print("Таблица успешно создана")
        self.con.commit()
        cur.close()

    def drop_table(self, name_table):
        cursor = self.con.cursor()
        print("Подключен к SQLite")
        cursor.execute("DROP TABLE " + name_table)
        self.con.commit()
        print("Таблица успешно удалена")
        self.con.commit()
        cursor.close()

    def show_database(self):
            cursor = self.con.cursor()
            cursor.execute("SELECT * FROM Faces")
            records = cursor.fetchall()
            with open("../database/outinput/names.txt", "wb") as names:
                for row in records:
                    names.write(bytes(str(row[0])+ " " + row[2], "UTF-8"))
                    names.write(bytes("\n", "UTF-8"))

        



if __name__ == "__main__":
    db = Database()

    if sys.argv[1] == "-insert" or sys.argv[1] == "-ins":
        if len(sys.argv) != 5:
            print("Error: Expected 5 elements, finded " + str(len(sys.argv)) + "\n"
                  "You should get name, path to text(information), path to photo")
        else:
            with open(sys.argv[3], "r") as about:
                with open(sys.argv[2], "r") as name:
                    name_str: str = name.read()
                    about_str: str = about.read()
                    db.insert_blob(name_str, about_str, sys.argv[4])
    elif sys.argv[1] == "-show" or sys.argv[1] == "-shw":
        db.show_database()
    
    elif sys.argv[1] == "-terminal" or sys.argv[1] == "-term":
            while True:
                choice = input("\tMenu\n" + 
                               "1.Insert in database\n" + 
                               "2.Remove from database\n" +
                               "3.Drop table\n" +
                               "4.Create table\n" +
                               "5.Show\n" +
                               "6.Exit\n")
                if choice == "1":
                    photo_path = fd.askopenfilename()
                    name = input("What's name this human?\n")
                    about = fd.askopenfilename()
                    with open(about, "r") as file:
                        txt = file.read()
                        db.insert_blob(name, txt, photo_path)
                    
                if choice == "2":
                    num_remove = input("Set number of the note\n")
                    db.delete_sqlite_record(num_remove)
                if choice == "3":
                    db.drop_table("Faces")
                if choice == "4":
                    db.create_table("Faces")
                if choice == "5":
                    db.show_database()
                if choice == "6":
                    db.con.commit()
                    db.con.close()
                    break  
                db.con.commit()
    db.con.close()
    '''
    
    '''

    '''
    drop_table("Faces")
    create_table("Faces")
    #insert_blob(sys.argv[1], sys.argv[2])
    '''






