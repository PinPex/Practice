import sqlite3 as sq
import face_recognition as face
from PIL import Image
import sys
import os
import threading
import time

Time = 0

def write_to_file(data, filename):
    # Преобразование двоичных данных в нужный формат
    with open(filename, 'wb') as file:
        file.write(data)
    #print("Данный из blob сохранены в: ", filename, "\n")

def parsing(row, unknown_encoding, i):

    temp_file_name = "temp" + str(i) + ".jpg"
    write_to_file(row[2], temp_file_name)
    known_image = face.load_image_file(temp_file_name)
    os.remove(temp_file_name)
    known_encoding = []
    if face.face_encodings(known_image):
        known_encoding = face.face_encodings(known_image)[0]
    else:
        print("Error: in known photo face not exists")
    
    results = face.compare_faces([known_encoding], unknown_encoding)
    
    if results[0] == True:
        print (row[1])
        print("Time without threads:")
        print(time.time() - Time)
        sys.exit(0)

def parsing_threads(row, unknown_encoding, i):

    temp_file_name = "temp" + str(i) + ".jpg"
    write_to_file(row[2], temp_file_name)
    known_image = face.load_image_file(temp_file_name)
    os.remove(temp_file_name)
    known_encoding = []
    if face.face_encodings(known_image):
        known_encoding = face.face_encodings(known_image)[0]
    else:
        print("Error: in known photo face not exists")
    
    results = face.compare_faces([known_encoding], unknown_encoding)
    
    if results[0] == True:
        print (row[1])
        sys.exit(0)

def thread_job(records, unknown_encoding, i, num_of_threads):
    num = int(len(records) / num_of_threads)
    L = (i - 1) * num
    R = (i) * num
    if R < len(records) and i == num_of_threads - 1:
        R = len(records)
    for j in range(L, R):
        parsing_threads(records[j], unknown_encoding, j)
    
if __name__ == "__main__":
    try:
        unknown_image = face.load_image_file(str(sys.argv[1]))
        unknown_encoding = []
        if face.face_encodings(unknown_image):
            unknown_encoding = face.face_encodings(unknown_image)[0]
        else:
            print("Error: in unknown photo face not exists")
            exit()
        
        path = str(os.getcwd()) 
        sqlite_connection = sq.connect(path[0:len(path) - 6] + 'database/sqlite_python.db')
        cursor = sqlite_connection.cursor()
        cursor.execute("SELECT * FROM Faces")
        records = cursor.fetchall()
        
        num_of_threads = 8
        Time = time.time()
        threads = [
                threading.Thread(target=thread_job, args=(records, unknown_encoding, i, num_of_threads))
                for i in range(1, num_of_threads + 1)
            ]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        
            
        print("Time with threads:")
        print(time.time() - Time)
        
        Time = time.time()
        for i in range(0, len(records)):
            parsing(records[i], unknown_encoding, i)
        
    
    except sq.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            #print("Соединение с SQLite закрыто")