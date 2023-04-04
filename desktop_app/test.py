import sys
import time
sys.path.append("../")
from parser.parser import Parsing
from database.scripts.fillBase import Database


if __name__ == "__main__":
    pars = Parsing()
    db = Database()
    photo_path = "../database/images/191_This-Man.jpg"
    #db.drop_table("Faces")
    #db.create_table("Faces")
    for i in range(0, 1000):
        db.insert_blob("Тест", "Тест", photo_path)
    #for i in range(0, 500):
        #for j in range(i * 1000, (i + 1) * 1000):
            #db.insert_blob("Гослинг", "Гослинг", photo_path)
        #start = time.time()
        #for j in range(2, 65, 2):
            #start = time.time()
            #pars.main_loop(photo_path, i)
            #stop = time.time() - start
            #with open("test.csv", "a") as f:
                #f.write(str((i + 1) * 1000) + ";" + str(j) + ";" + str(time.time() - start) + ";\n")
    



    
