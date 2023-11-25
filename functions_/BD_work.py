import sqlite3 as sql
from functions_.face_dist import checkFace
from os import remove
#photos=cur.execute("SELECT photo_ FROM train_bd ")
def add_person(person_name,img_path):
    if person_name=='' or person_name==' ' or img_path=='' or img_path==' ':
        return False
    
    con=sql.connect("img_bd.db")
    cur=con.cursor()
    n=1
    for i in cur.execute("SELECT id FROM image_db"):
        n+=1
    with open (f"{img_path}","rb") as photo:
        h=photo.read()
        cur.execute("INSERT INTO image_db VALUES (?,?,?)", (n,person_name.lower(),h))
    con.commit()
    cur.close()
    con.close()
    
    return True


def search_with_name(suspect_name):
    con=sql.connect("img_bd.db")
    cur=con.cursor()
    
    cur.execute(f"SELECT name_second_name FROM image_db WHERE name_second_name = '{suspect_name.lower()}'")
    if cur.fetchone() is None:
        return False
    else:
        return True

    print("Получилось: search_with_name")
    con.commit()
    cur.close()
    con.close()


def check_all(img_path2):
    con=sql.connect("img_bd.db")
    cur=con.cursor()
    photos=cur.execute("SELECT photo FROM image_db")
    k=1
    for photo in photos:
        with open(f'{k}.jpg','wb') as file:
            file.write(photo[0])
            k+=1
    result=False
    for i in range(k-1):
        if checkFace(f'{i+1}.jpg',img_path2):
            result=True
            break
    
    for i in range(k-1):
        remove(f'{i+1}.jpg')

    con.commit()
    cur.close()
    con.close()
    
    return result

#check_all('img/1gp.jpg')
#k=4
#for i in range(k):
#        remove(f'{i+1}.jpg')
