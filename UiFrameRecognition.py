# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_FrameRecognition.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_frameRecognition(object):
    def setupUi(self, frameRecognition):
        frameRecognition.setObjectName("frameRecognition")
        frameRecognition.resize(1191, 531)
        self.label_7 = QtWidgets.QLabel(frameRecognition)
        self.label_7.setGeometry(QtCore.QRect(440, 10, 281, 31))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.lbImg = QtWidgets.QLabel(frameRecognition)
        self.lbImg.setGeometry(QtCore.QRect(270, 50, 640, 410))
        self.lbImg.setText("")
        self.lbImg.setPixmap(QtGui.QPixmap("../FaceID_Realtime_Detect/Logo/imgNone.png"))
        self.lbImg.setObjectName("lbImg")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(frameRecognition)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(340, 470, 111, 51))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.btStart = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.btStart.setFont(font)
        self.btStart.setObjectName("btStart")
        self.horizontalLayout_3.addWidget(self.btStart)
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(frameRecognition)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(730, 470, 111, 51))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.btEnd = QtWidgets.QPushButton(self.horizontalLayoutWidget_3)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.btEnd.setFont(font)
        self.btEnd.setObjectName("btEnd")
        self.horizontalLayout_4.addWidget(self.btEnd)

        self.retranslateUi(frameRecognition)
        QtCore.QMetaObject.connectSlotsByName(frameRecognition)

    def retranslateUi(self, frameRecognition):
        _translate = QtCore.QCoreApplication.translate
        frameRecognition.setWindowTitle(_translate("frameRecognition", "Frame"))
        self.label_7.setText(_translate("frameRecognition", "Nh???n Di???n Khu??n M???t"))
        self.btStart.setText(_translate("frameRecognition", "B???t ?????u"))
        self.btEnd.setText(_translate("frameRecognition", "K???t th??c"))

