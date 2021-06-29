############################
# Author: Nguyễn Hồng Kỳ   #
# Mail: marinkqh@gmail.com #
# Phone Number: 0386685086 #
# Date: 10/5/2020          #
# Version: 1.0             #
############################
import pyodbc

class SQLConnection(object):
    def __init__(self):
        self.server = 'MARINKQH_LAN'
        self.database = 'FaceRecognition'
        self.username = 'sa'
        self.password = '123456'
        self.cnn = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER=' + self.server + ';DATABASE=' + self.database + ';UID=' + self.username + ';PWD=' + self.password)
        self.con = self.cnn.cursor()

    def setNameServer(self, server):
        self.server = server

    def setUser(self, username):
        self.username = username

    def setPassword(self, password):
        self.password = password

    def setDataBase(self, database):
        self.database = database

    def queryDataOnly1(self, query):
        self.con.execute(query)
        self.data = self.con.fetchone()
        return self.data

    def queryData(self, query):
        self.con.execute(query)
        self.data = self.con.fetchall()
        return self.data

    def queryNoReturn(self, query):
        with self.con:
            self.con.execute(query)
