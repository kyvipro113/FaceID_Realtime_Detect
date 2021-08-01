from UiLogin import Ui_Login
from MainWindow import MainWindow
from MainWindowLoginByFaceID import MainWindowLoginByFaceID
from SQLConnection import SQLConnection
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot
from PyQt5 import QtCore, QtGui, QtWidgets
import sys

class Login(QWidget, Ui_Login):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent=parent)
        self.setupUi(self)

        # Event
        self.btLogin.clicked.connect(self.loginSys)
        self.btExit.clicked.connect(self.exit)
        self.btLoginFaceID.clicked.connect(self.loginByFaceID)

    def alter(self, title, message):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Information)
        msgBox.setWindowTitle(title)
        msgBox.setText(message)
        msgBox.exec_()
    
    def loginSys(self):
        try:
            name =""
            SQL = SQLConnection()
            data = SQL.queryDataOnly1("Select CMT From Login Where Username = '{}' And Password = '{}'".format(self.txtUser.text(), self.txtPass.text()))
            if data is not None:
                for cID in data:
                    dataName = SQL.queryDataOnly1("Select HoTen From FaceID Where CMT = '{}'".format(cID))
                    for dtName in dataName:
                        name = dtName
                self.mainWindow = MainWindow(name)
                self.mainWindow.show()
                self.hide()
            else:
                self.alter(title="Cảnh báo", message="Đăng nhập thất bại!!")    
        except:
            self.alter(title="Cảnh báo", message="Kết nối cơ sở dữ liệu thất bại!!")

    def exit(self):
        QtWidgets.qApp.quit()

    def loginByFaceID(self):
        self.uiLoginFaceID = MainWindowLoginByFaceID()
        self.uiLoginFaceID.changeFlagForThread(flagThread=True)
        self.uiLoginFaceID.show()
        self.hide()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    login = Login()
    login.show()
    sys.exit(app.exec_())