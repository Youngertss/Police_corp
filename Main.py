from PIL import Image
from PIL import ImageFilter

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import(QApplication,QWidget,QPushButton,QLabel,QListWidget,
QFileDialog,QHBoxLayout,QVBoxLayout, QGroupBox, QInputDialog, QMessageBox)
from PyQt5.QtGui import QPixmap

import sqlite3 as sql
import os
from functions_.BD_work import add_person, search_with_name, check_all

flag_message_but=False
global_path_item=''                     #path  к выбраному фото

app = QApplication([])
#окно

win=QWidget()
win.setWindowTitle('Founder')
win.resize(600,500)

#виджеты для ГБ
inf=QLabel("Поиск по БД")
btn1=QPushButton('Добавить личность в базу')
btn2=QPushButton('Совершить поиск по базе')
lb_image=QLabel("Изображение")
btn_dir=QPushButton("Загрузить изображение")
lw_files=QListWidget()
#лайауты для ГРУПБОКСА
glayout=QHBoxLayout()

gvlayout1=QVBoxLayout()
gvlayout2=QVBoxLayout()

gvlayout1.addWidget(btn_dir, alignment=Qt.AlignLeft)
gvlayout1.addWidget(lw_files)
gvlayout2.addWidget(inf, alignment=Qt.AlignTop | Qt.AlignHCenter )
gvlayout2.addWidget(lb_image,95)
gvlayout1.addWidget(btn1)
gvlayout2.addWidget(btn2)
glayout.addLayout(gvlayout1,20)
glayout.addLayout(gvlayout2,80)

#Gruop Box (для красоты)
Groupb=QGroupBox("Police Corp.")
Groupb.setLayout(glayout)
#Расположение по лейаутам
main_layout=QVBoxLayout()
main_layout.addWidget(Groupb)

workdir = ""
def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def filter(files,extensions):
    result = []
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result

def showFileNamesList():
    try:
        extensions = [".jpg",".jpeg",".png",".gif",".bmp"]
        chooseWorkdir()
        filenames = filter(os.listdir(workdir),extensions)
        lw_files.clear()
        for filename in filenames:
            lw_files.addItem(filename)
    except FileNotFoundError:
        lb_image.setText("FileNotFound")

def show_message_box(title,text,btn1,btn2,booleann):
    global flag_message_but
    message_dialog=QMessageBox()
    message_dialog.setWindowTitle(title)
    message_dialog.setText(text)
    message_dialog.setStandardButtons(btn1 | btn2)
    message_dialog.setDefaultButton(btn2)
    message_dialog.buttonClicked.connect(check_button_flag)
    message_dialog.exec_()
    if booleann==True:
        return flag_message_but

def btn1_con():
    try:
        if show_message_box('Потверждение', "Добавить личность в БД по выбраннному вами фото?", QMessageBox.Yes, QMessageBox.Cancel,True):
            person_name=QInputDialog.getText(None,"Добавление в базу...","Введите имя, фамилию:")
            if add_person(person_name[0],global_path_item):
                show_message_box('Вышло', "Вы успено добавили личность.", QMessageBox.Ok, QMessageBox.Close,False)
            else:
                if show_message_box('Ошибка', "Нужно ввести имя и фамилию, и выбрать фото!", QMessageBox.Yes, QMessageBox.Close,True):
                    btn1_con()
    except:
        print("try btn1_con!\n---------------------------------------------------")
        
def btn_search_con():
    global flag_message_but
    global global_path_item
    try:
        if show_message_box('Действие', "Вы знаете имя подозреваемого?", QMessageBox.Yes, QMessageBox.No,True):
            suspect_name=QInputDialog.getText(None,"Поиск по базе...","Введите имя, фамилию(через пробел):")
            message_text="Такого человека не найдено"
            if suspect_name[0]!='':
                if search_with_name(suspect_name[0]):
                    message_text="Найден человек с таким именем в базе!"

            show_message_box('Действие', message_text, QMessageBox.Ok, QMessageBox.Close,False)
        
        else:
            if show_message_box('Подтверждение', "Совершить поиск преступника по выбраннному вами фото?", QMessageBox.Yes, QMessageBox.Cancel, True):
                if check_all(global_path_item):
                    show_message_box('Результат', "Такой человек есть в БД! За решотку его/её!", QMessageBox.Ok, QMessageBox.Close, False)
                else:
                    show_message_box('Результат', "Такого человека нету в базе данных.", QMessageBox.Ok, QMessageBox.Close, False)
    except: 
        print('try btn_search_con!\n---------------------------------------------------')

def check_button_flag(btn):
    global flag_message_but
    if btn.text()=="&Yes":
        flag_message_but=True
    else:
        flag_message_but=False
    
btn1.clicked.connect(btn1_con)
btn2.clicked.connect(btn_search_con)
btn_dir.clicked.connect(showFileNamesList)

class ImageProcessor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None

    def loadImage(self,dir,filename):
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir,filename)
        self.image = Image.open(image_path)

    def showImage(self,path):
        lb_image.hide()
        pixmapimage = QPixmap(path)
        w, h = lb_image.width(), lb_image.height()
        pixmapimage = pixmapimage.scaled(w,h,Qt.KeepAspectRatio)
        lb_image.setPixmap(pixmapimage)
        lb_image.show()
        
def showChoisenImage():
    try:
        global global_path_item
        if lw_files.currentRow() >= 0:
            filename = lw_files.currentItem().text()
            workimage.loadImage(workdir,filename)
            image_path = os.path.join(workimage.dir, workimage.filename)
            workimage.showImage(image_path)
            global_path_item=image_path     #path  к фото чтобы + в БД
    except:
        pass
workimage = ImageProcessor()
lw_files.currentRowChanged.connect(showChoisenImage)

win.setLayout(main_layout)

win.show()
app.exec_()