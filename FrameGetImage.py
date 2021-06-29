from UiFrameGetImage import Ui_frameGetImage
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from SQLConnection import SQLConnection
import cv2
import sys   
import os

flag = False
imgCapture = None
countImg = 0
citizenID = None

class Thread(QThread):
    changePixmap = pyqtSignal(QImage)

    def run(self):
        global imgCapture
        cap = cv2.VideoCapture(0)
        face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
        while (flag):
            ret, frame = cap.read()
            if ret:
                grayImg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                grayImg = cv2.equalizeHist(grayImg)
                faces = face_cascade.detectMultiScale(grayImg, 1.1, 2, 0|2, (100,100))
                for (x, y ,w, h) in faces:
                    cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
                ## Change
                    imgCapture = grayImg[y:y+h, x:x+w]
                    imgCapture = cv2.resize(imgCapture, (100,100))
                ##
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)
        cap.release()



class FrameGetImage(QFrame, Ui_frameGetImage):
    def __init__(self, parent = None):
        QFrame.__init__(self, parent=parent)
        self.setupUi(self)

        self.comboGender.addItem("Nam")
        self.comboGender.addItem("Nữ")
        self.btStart.setEnabled(False)
        self.btCapture.setEnabled(False)
        self.btEnd.setEnabled(False)

        self.loadData()

        # Thread Video Stream
        self.theadVStream = Thread(self)
        self.theadVStream.changePixmap.connect(self.setImage)

        # Event
        self.btStart.clicked.connect(self.startVideoStream)
        self.btCapture.clicked.connect(self.captureImg)
        self.btEnd.clicked.connect(self.endVideoStream)

        self.dataTab.cellClicked.connect(self.cellClick)
        self.btAdd.clicked.connect(self.insertData)
        self.btFix.clicked.connect(self.updateData)
        self.btDel.clicked.connect(self.deleteData)
        self.btClear.clicked.connect(self.refresh)

    
    @pyqtSlot(QImage)
    def setImage(self, image):
        self.lbImg.setPixmap(QPixmap.fromImage(image))

    def startVideoStream(self):
        global flag
        if not (flag):
            
            self.btCapture.setEnabled(True)
            self.btEnd.setEnabled(True)
            self.btAdd.setEnabled(False)
            self.btFix.setEnabled(False)
            self.btDel.setEnabled(False)
            self.btClear.setEnabled(False)

            flag = True
            self.theadVStream.start()

    def endVideoStream(self):
        self.btAdd.setEnabled(True)
        self.btFix.setEnabled(True)
        self.btDel.setEnabled(True)
        self.btClear.setEnabled(True)
        self.btStart.setEnabled(False)
        self.btCapture.setEnabled(False)
        self.btEnd.setEnabled(False)
        
        global flag
        if(flag):
            flag = False
        self.theadVStream.exit()
    

    def captureImg(self):
        global flag
        if (flag):
            flag = False
            global countImg
            countImg += 1
            path = 'dataset'
            if not os.path.exists(path):
                os.mkdir(path)
            global imgCapture
            cv2.imwrite(os.path.join(path, citizenID + '.' +str(countImg)+'.jpg'), imgCapture)
            #print(citizenID)
            SQL = SQLConnection()
            SQL.queryNoReturn("Insert Into ListID Values('{}', '{}')".format(countImg, citizenID))

    def alter(self,title, message):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Information)
        msgBox.setWindowTitle(title)
        msgBox.setText(message)
        msgBox.exec_()

    def loadData(self):
        global countImg
        SQL = SQLConnection()
        dataResult = SQL.queryData("Select * From FaceID")
        self.dataTab.setRowCount(0)
        for row_number, row_data in enumerate(dataResult):
            self.dataTab.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.dataTab.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))
        dataResult = SQL.queryDataOnly1("Select TOP(1) ID From ListID Order by ID DESC")
        countImg = int(dataResult[0])

    def cellClick(self):
        global citizenID
        row = self.dataTab.currentRow()
        citizenID = self.dataTab.item(row, 0).text()
        self.txtID.setText(self.dataTab.item(row, 0).text())
        self.txtFullName.setText(self.dataTab.item(row, 1).text())
        self.txtStudentID.setText(self.dataTab.item(row, 2).text())
        self.txtClassR.setText(self.dataTab.item(row, 3).text())
        self.comboGender.setCurrentText(self.dataTab.item(row, 4).text())
        
        self.btStart.setEnabled(True)

    def insertData(self):
        global citizenID
        try:
            citizenID = self.txtID.text()
            SQL = SQLConnection()
            SQL.queryNoReturn("Insert Into FaceID Values('{}', N'{}', '{}', '{}', N'{}')".format(self.txtID.text(), self.txtFullName.text(), self.txtStudentID.text(), self.txtClassR.text(), self.comboGender.currentText()))
            self.alter(title="Thông báo", message="Thao tác thực hiện thành công") 
            self.btStart.setEnabled(True)
        except:
            self.alter(title="Cảnh báo", message="Thao tác thực hiện thất bại!!")
        finally:
            self.loadData()
    
    def updateData(self):
        try:
            SQL = SQLConnection()
            SQL.queryNoReturn("Update FaceID Set HoTen =  N'{}', MaSV = '{}', Lop = '{}', GioiTinh = N'{}' Where CMT = '{}'".format(self.txtFullName.text(), self.txtStudentID.text(), self.txtClassR.text(), self.comboGender.currentText(), self.txtID.text()))
            self.alter(title="Thông báo", message="Thao tác thực hiện thành công") 
        except:
            self.alter(title="Cảnh báo", message="Thao tác thực hiện thất bại!!")
        finally:
            self.loadData()

    def deleteData(self):
        try:
            global citizenID
            citizenID = None
            SQL = SQLConnection()
            SQL.queryNoReturn("Delete FaceID Where CMT = '{}'".format(self.txtID.text()))
            SQL.queryNoReturn("Delete ListID Where CID = '{}'".format(self.txtID.text()))
            self.alter(title="Thông báo", message="Thao tác thực hiện thành công") 
        except:
            self.alter(title="Cảnh báo", message="Thao tác thực hiện thất bại!!")
        finally:
            self.loadData()

    def refresh(self):
        global citizenID
        citizenID = None
        self.txtID.setText("")
        self.txtFullName.setText("")
        self.txtStudentID.setText("")
        self.txtClassR.setText("")
        self.comboGender.setCurrentText("Nam")
        self.lbImg.setPixmap(QtGui.QPixmap("../Face Recognition ver 1.0/Logo/imgNone.png"))
       




    