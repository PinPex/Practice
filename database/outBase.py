import sqlite3, os

def write_to_file(data, filename):
    # Преобразование двоичных данных в нужный формат
    with open(filename, 'wb') as file:
        file.write(data)
    print("Данный из blob сохранены в: ", filename, "\n")

def read_blob_data(emp_id):
    try:
        sqlite_connection = sqlite3.connect('sqlite_python.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sql_fetch_blob_query = """SELECT * from Faces where id = ?"""
        cursor.execute(sql_fetch_blob_query, (emp_id,))
        record = cursor.fetchall()
        for row in record:
            print("Id = ", row[0], "Name = ", row[1])
            name  = row[1]
            photo = row[2]

            print("Сохранение изображения сотрудника и резюме на диске \n")
            photo_path = os.path.join(name + ".jpg")
            write_to_file(photo, photo_path)
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")
            
read_blob_data(1)
