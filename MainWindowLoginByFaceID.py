from UiMainWindowLoginByFaceID import Ui_MainWindowLoginByFaceID
from MainWindow import MainWindow
from SQLConnection import SQLConnection
from recognizeFace import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QAction
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QImage, QPixmap
from PIL import ImageFont, ImageDraw, Image
import sys 
import os
import time

flag = False
name = ""

class Thread(QThread):
    changePixmap = pyqtSignal(QImage)

    def run(self):
        global flag
        global flagMainWindow
        global name
        SQL = SQLConnection()
        font = ImageFont.truetype("arial.ttf", 32)
        mean_face, eigen_vectors, eigen_faces, name_list = load_trained_model()
        video_capture = cv2.VideoCapture(0)
        face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
        while(flag):
            ret, img = video_capture.read()
            if ret:
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                gray = cv2.equalizeHist(gray)
                for angle in [0, -20, 20, -40, 40]:
                    rimg = rotate_image(img, angle)
                    faces = face_cascade.detectMultiScale(rimg,  1.1, 2, 0|2, (100,100))
                    if len(faces):
                        faces = [rotate_point(faces[0], img, -angle)]
                        break
                for x, y, w, h in faces:
                    cv2.rectangle(img, (x, y), (x+w, y+h), (0,255,0), 2)
                    test_face = gray[y:y+h, x:x+w]
                    id, score = face_recognition(test_face, mean_face, eigen_vectors, eigen_faces)
                    name_id = int(name_list[id[0][0]])   
                    #print(name_id)
                    data = SQL.queryDataOnly1("Select CID From ListID Where ID = '{}'".format(name_id))
                    print(data[0])
                    cv2.putText(img, str(data[0]), (x+5, y+h+25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0) , 2)
                    # dataName = SQL.queryDataOnly1("Select HoTen, MaSV, Lop, GioiTinh From FaceID Where CMT = '{}'".format(data[0]))
                    # print(str(dataName[0]))     

                    dataVerify = SQL.queryDataOnly1("Select Login.Username, Login.Password, FaceID.HoTen From Login, FaceID Where Login.CMT ='{}' And FaceID.CMT = '{}'".format(data[0], data[0]))
                    if dataVerify is not None:
                        print(dataVerify[2])
                        name = dataVerify[2]
                        img_pil = Image.fromarray(img)
                        draw = ImageDraw.Draw(img_pil)
                        draw.text((x+5, y+h+30), dataVerify[2], font=font, fill=(255, 0, 0, 255))
                        img = np.array(img_pil)
                        flagMainWindow = True
                    else:
                        img_pil = Image.fromarray(img)
                        draw = ImageDraw.Draw(img_pil)
                        draw.text((x+5, y+h+30), "Người dùng không có trong CSDL", font=font, fill=(255, 0, 0, 255))
                        img = np.array(img_pil)
                rgbImage = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)
        video_capture.release()

class MainWindowLoginByFaceID(QMainWindow, Ui_MainWindowLoginByFaceID):
    def __init__(self, parent = None):
        QMainWindow.__init__(self, parent=parent)
        self.setupUi(self)

        endRecognition = QAction("Quit", self)
        endRecognition.triggered.connect(self.closeEvent)

        menubar = self.menuBar()
        headerMenu = menubar.addMenu("")
        headerMenu.addAction(endRecognition)

        # Thread Video Recognition
        self.threadRecognition = Thread(self)
        self.threadRecognition.changePixmap.connect(self.setImage)
        self.threadRecognition.start()

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.lbImg.setPixmap(QPixmap.fromImage(image))
        global name
        global flag
        self.mainWindow = MainWindow(name)
        if(name != ""):
            self.mainWindow.show()
            flag = False
            self.threadRecognition.exit()


    def closeEvent(self, event):
        global flag
        if (flag):
            flag = False
            self.threadRecognition.exit()
            event.accept()
            from Login import Login
            self.uiLogin = Login()
            self.uiLogin.show()

    def changeFlagForThread(self, flagThread):
        global flag
        if not (flag):
            flag = flagThread

        

