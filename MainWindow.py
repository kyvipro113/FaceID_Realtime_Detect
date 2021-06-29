from UiMainWindow import Ui_MainWindow
from FrameGetImage import FrameGetImage
from FrameRecognition import FrameRecognition
from FrameTraining import FrameTraining
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
import cv2
import sys    

class MainWindow(QMainWindow, Ui_MainWindow):
    
    def __init__(self, fullName, parent = None):
        QMainWindow.__init__(self, parent=parent)
        self.setupUi(self)

        self.fullName = fullName

        # User Control
        self.UIRecognition = None
        self.UIGetImg = None
        self.UITraining = None

        self.load()

        # Event
        self.tabTrain.tabBarClicked.connect(self.tabClicked)

    def load(self):
        self.lbName.setText(self.fullName)

    def cleanUI(self):
        if(self.UIRecognition):
            self.UIRecognition.hide()
            del self.UIRecognition
            self.UIRecognition = None
        if(self.UIGetImg):
            self.UIGetImg.hide()
            del self.UIGetImg
            self.UIGetImg = None
        if(self.UITraining):
            self.UITraining.hide()
            del self.UITraining
            self.UITraining = None
    
    def tabClicked(self, index):
        self.cleanUI()
        if(index == 0):
            self.UIRecognition = FrameRecognition(self.mainFrame)
            self.UIRecognition.show()
        if(index == 1):
            self.UIGetImg = FrameGetImage(self.mainFrame)
            self.UIGetImg.show()
        if(index == 2):
            self.UITraining = FrameTraining(self.mainFrame)
            self.UITraining.show()
    
# if __name__ == "__main__":
#     app = QtWidgets.QApplication(sys.argv)
#     mainWindow = MainWindow()
#     mainWindow.show()
#     sys.exit(app.exec_())