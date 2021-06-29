import cv2
import numpy as np
from PIL import Image
import pickle
import sqlite3

faceDetect=cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
cam=cv2.VideoCapture(0)
rec=cv2.face.LBPHFaceRecognizer_create()
rec.read("model/trainningData.csv")
id=0
#set text style
fontface = cv2.FONT_HERSHEY_SIMPLEX
fontscale = 1
fontcolor = (203,23,252)

#get data from sqlite by ID
def getProfile(id):
    ID = "0" + str(id)
    print(ID)
    profile = None
    from SQLConnection import SQLConnection
    SQL = SQLConnection()
    data = SQL.queryDataOnly1("Select * From FaceID Where CMT = '{}'".format(ID))
    for prof in data:
        profile = prof
    return profile

while(True):
    #camera read
    ret,img=cam.read()
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    faces = faceDetect.detectMultiScale(gray, 1.3,5)
    for(x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        id,conf=rec.predict(gray[y:y+h,x:x+w])
        print(id)
        #profile=getProfile(id)
        #set text to window
        #if(profile!=None):
        cv2.putText(img, str(id), (x+5, y+h+25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255) , 2)
            #cv2.putText(img, "ID: " + str(profile[1]), (x,y+h+30), fontface, fontscale, fontcolor ,2)
            #cv2.putText(img, "Name: " + str(profile[2]), (x,y+h+60), fontface, fontscale, fontcolor ,2)
            #cv2.putText(img, "Gender: " + str(profile[3]), (x,y+h+90), fontface, fontscale, fontcolor ,2)
        
        cv2.imshow('Face',img) 
    if cv2.waitKey(1)==ord('q'):
        break
cam.release()
cv2.destroyAllWindows()
