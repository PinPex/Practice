import sqlite3 as sq
import face_recognition as face
import sys
import os
import threading
import time
import numpy as np
import io

Time = 0

def write_to_file(data, filename):
    with open(filename, 'wb') as file:
        file.write(data)

def parsing(row, unknown_encoding):
    results = face.compare_faces([row[3]], unknown_encoding)
    if results[0] == True:
        write_to_file(row[4], "photo.jpg")
        with open('name.txt', 'w') as f:
            f.write(row[2] + "\n")
        with open('information.txt', 'w') as f:
            f.write(row[1] + "\n")

        print(time.time() - Time)
        sys.exit(0)

def thread_job(records, unknown_encoding, i, num_of_threads):
    num = int(len(records) / num_of_threads)
    L = (i) * num
    R = (i + 1) * num
    if R < len(records) and i == num_of_threads - 1:
        R = len(records)
    for j in range(L, R):
        parsing(records[j], unknown_encoding)
    
def adapt_array(arr):
    out = io.BytesIO()
    np.save(out, arr)
    out.seek(0)
    return sq.Binary(out.read())

def convert_array(text):
    out = io.BytesIO(text)
    out.seek(0)
    return np.load(out)

if __name__ == "__main__":
    path = str(os.getcwd()) 
    sq.register_adapter(np.ndarray, adapt_array)
    sq.register_converter("array", convert_array)
    
    con = sq.connect(path[:path.rindex('/')] + '/database/sqlite_python.db', detect_types=sq.PARSE_DECLTYPES)

    cursor = con.cursor()
    cursor.execute("SELECT * FROM Faces")
    records = cursor.fetchall()

    unknown_image = face.load_image_file(str(sys.argv[1]))
    unknown_encoding = []
    if face.face_encodings(unknown_image):
        unknown_encoding = face.face_encodings(unknown_image)[0]
    else:
        print("Error: in unknown photo face not exists")
        exit()
    
    num_of_threads = int(sys.argv[2])
    Time = time.time()
    threads = [
            threading.Thread(target=thread_job, args=(records, unknown_encoding, i, num_of_threads))
            for i in range(0, num_of_threads)
        ]
    for thread in threads:
        thread.start()
    