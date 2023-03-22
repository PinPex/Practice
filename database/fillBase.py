import sqlite3 as sq
import sys
from tkinter import filedialog as fd
import os

def convert_to_binary_data(filename):
    # Преобразование данных в двоичный формат
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return blob_data

def insert_blob(name, photo):
    try:
        sqlite_connection = sq.connect('sqlite_python.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sqlite_insert_blob_query = """INSERT INTO Faces
                                  (name, photo) VALUES (?, ?)"""

        emp_photo = convert_to_binary_data(photo)
        # Преобразование данных в формат кортежа
        data_tuple = (name, emp_photo)
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        sqlite_connection.commit()
        print("Изображение и файл успешно вставлены как BLOB в таблицу")
        cursor.close()

    except sq.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")

def delete_sqlite_record(dev_id):
    try:
        sqlite_connection = sq.connect('sqlite_python.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sql_update_query = """DELETE from Faces where id = ?"""
        cursor.execute(sql_update_query, (dev_id, ))
        sqlite_connection.commit()
        print("Запись успешно удалена")
        cursor.close()

    except sq.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")

def create_table(name_table):
    try:
        sqlite_connection = sq.connect('sqlite_python.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")
        cursor.execute("""
            CREATE TABLE """ + name_table + """ (
                id INTEGER, 
                name TEXT, 
                photo BLOB,
                PRIMARY KEY("id" AUTOINCREMENT)
                );
        """)
        sqlite_connection.commit()
        print("Таблица успешно создана")
        cursor.close()

    except sq.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")

def drop_table(name_table):
    try:
        sqlite_connection = sq.connect('sqlite_python.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")
        cursor.execute("DROP TABLE " + name_table)
        sqlite_connection.commit()
        print("Таблица успешно удалена")
        cursor.close()

    except sq.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")

def show_database():
    try:
        sqlite_connection = sq.connect('sqlite_python.db')
        cursor = sqlite_connection.cursor()
        cursor.execute("SELECT * FROM Faces")
        records = cursor.fetchall()
        for row in records:
            print(row[1])

    except sq.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            #print("Соединение с SQLite закрыто")

while True:
    
    choice = input("""\tMenu
1.Insert in database
2.Remove from database
3.Drop table
4.Create table
5.Show
6.Exit\n""")
    os.system('clear')
    if choice == "1":
        photo_path = fd.askopenfilename()
        name = input("What's name this human?\n")
        insert_blob(name, photo_path)
    if choice == "2":
        num_remove = input("Set number of the note\n")
        delete_sqlite_record(num_remove)
    if choice == "3":
        drop_table("Faces")
    if choice == "4":
        create_table("Faces")
    if choice == "5":
        show_database()
    if choice == "6":
        break

#insert_blob(sys.argv[1], sys.argv[2])







