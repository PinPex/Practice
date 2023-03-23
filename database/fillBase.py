import sqlite3 as sq
import sys
from tkinter import filedialog as fd
import os
import face_recognition as face
from PIL import Image
import numpy as np
import io

def convert_to_binary_data(filename):
    # Преобразование данных в двоичный формат
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return blob_data


def insert_blob(name, about, photo, con):
    cursor = con.cursor()
    print("Подключен к SQLite")
    image = face.load_image_file(photo)
    image_encoding = []
    if face.face_encodings(image):
        image_encoding = face.face_encodings(image)[0]
    else:
        print("Error: in known photo face not exists")
    photo_bin = convert_to_binary_data(photo)
    cursor.execute("""INSERT INTO Faces
                                (name, about, code, photo) VALUES (?, ?, ?, ?)""", 
                                (name, about, image_encoding, photo_bin))
    cursor.close()

def delete_sqlite_record(dev_id, con):
    cursor = con.cursor()
    print("Подключен к SQLite")

    sql_update_query = """DELETE from Faces where id = ?"""
    cursor.execute(sql_update_query, (dev_id, ))
    con.commit()
    print("Запись успешно удалена")
    cursor.close()

def adapt_array(arr):
    out = io.BytesIO()
    np.save(out, arr)
    out.seek(0)
    return sq.Binary(out.read())

def convert_array(text):
    out = io.BytesIO(text)
    out.seek(0)
    return np.load(out)


def create_table(name_table, con):
    sq.register_adapter(np.ndarray, adapt_array)

    # Converts TEXT to np.array when selecting
    sq.register_converter("array", convert_array)

    x = np.arange(12).reshape(2,6)
    cur = con.cursor()
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
    cur.close()

def drop_table(name_table, con):
    cursor = con.cursor()
    print("Подключен к SQLite")
    cursor.execute("DROP TABLE " + name_table)
    con.commit()
    print("Таблица успешно удалена")
    cursor.close()

def show_database(con):
        cursor = con.cursor()
        cursor.execute("SELECT * FROM Faces")
        records = cursor.fetchall()
        print(len(records))
        for row in records:
            print(row[2])

#drop_table("Faces")
#create_table("Faces")
sq.register_adapter(np.ndarray, adapt_array)
# Converts TEXT to np.array when selecting
sq.register_converter("array", convert_array)
con = sq.connect("sqlite_python.db", detect_types=sq.PARSE_DECLTYPES)

while True:
    
    choice = input("""\tMenu
1.Insert in database
2.Remove from database
3.Drop table
4.Create table
5.Show
6.Exit\n""")
    #os.system('clear')
    if choice == "1":
        photo_path = fd.askopenfilename()
        name = input("What's name this human?\n")
        about = fd.askopenfilename()
        with open(about, "r") as file:
            txt = file.read()
            insert_blob(name, txt, photo_path, con)
        
    if choice == "2":
        num_remove = input("Set number of the note\n")
        delete_sqlite_record(num_remove, con)
    if choice == "3":
        drop_table("Faces", con)
    if choice == "4":
        create_table("Faces", con)
    if choice == "5":
        show_database(con)
    if choice == "6":
        con.commit()
        con.close()
        break  
    con.commit()


'''
drop_table("Faces")
create_table("Faces")
#insert_blob(sys.argv[1], sys.argv[2])
'''






