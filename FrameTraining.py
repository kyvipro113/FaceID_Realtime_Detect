from UiFrameTraining import Ui_frameTrainning
from SQLConnection import SQLConnection
from training import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFrame
import sys    
import os
import numpy as np
class FrameTraining(QFrame, Ui_frameTrainning):
    def __init__(self, parent = None):
        QFrame.__init__(self, parent=parent)
        self.setupUi(self)

        self.txtNumFeature.setEnabled(False)
        self.txtNumLabel.setEnabled(False)

        self.loadData()

        # Event
        self.btTrainning.clicked.connect(self.trainingModel)

    def alter(self,title, message):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Information)
        msgBox.setWindowTitle(title)
        msgBox.setText(message)
        msgBox.exec_()

    def loadData(self):
        SQL = SQLConnection()
        dataResult = SQL.queryData("Select * From FaceID")
        self.dataTabFaceID.setRowCount(0)
        for row_number, row_data in enumerate(dataResult):
            self.dataTabFaceID.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.dataTabFaceID.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

        dataResult = SQL.queryData("Select CID, Count(ID) As NumImage From ListID Group by CID")
        self.dataTabImgID.setRowCount(0)
        for row_number, row_data in enumerate(dataResult):
            self.dataTabImgID.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.dataTabImgID.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

        self.dataTabImg.setRowCount(0)
        row_number = 0
        for file in os.listdir('dataset/'):
            if file[-3:] in ['jpg', 'png']:
                self.dataTabImg.insertRow(row_number)
                self.dataTabImg.setItem(row_number, 0, QtWidgets.QTableWidgetItem(str(file)))
                row_number += 1
            else:
                pass
        
        dataResult = SQL.queryData("Select Count(CID), COUNT(ID) From ListID")
        self.txtNumLabel.setText(str(dataResult[0][0]))
        self.txtNumFeature.setText(str(dataResult[0][1]))
    
    def trainingModel(self):
        try:
            dataset = load_dataset('dataset/')
            face_matrix, mean_face = create_matrix(dataset)
            if not os.path.exists('model'):
                os.mkdir('model')
            with open('model/name_list.txt', 'w') as name_list:
                for k in dataset.keys():
                    name_list.write(k+'\n')
            cov, eigen_vectors, eigen_faces = pca(face_matrix)
            np.savetxt('model/eigen_faces.csv', eigen_faces, delimiter=',')
            np.savetxt('model/eigen_vectors.csv', eigen_vectors, delimiter=',')
            np.savetxt('model/mean_face.csv', mean_face, delimiter=',')

            print('Saved mean_face', mean_face.shape, 'to model/mean_face.csv.')
            print('Saved eigen_vectors', eigen_vectors.shape, 'to model/mean_face.csv.')
            print('Saved eigen_faces', eigen_faces.shape, 'to model/mean_face.csv.')
            self.alter(title="Thông báo", message="Huấn luyện mô hình thành công!!")
        except:
            self.alter(title="Cảnh báo", message="Huấn luyện mô hình thất bại!!")