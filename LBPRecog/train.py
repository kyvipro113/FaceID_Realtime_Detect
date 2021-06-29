import cv2
import os
import numpy as np
from PIL import Image

recognizer = cv2.face.LBPHFaceRecognizer_create()
path='dataset'

def getImagesAndLabels(path):
    #get the path of all the files in the folder
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
    faces=[]
    IDs=[]
    for imagePath in imagePaths:
        if imagePath[-3:] in ['jpg', 'png']:
            faceImg=Image.open(imagePath).convert('L')
            #faceImg.show()
            faceNp=np.array(faceImg,'uint8')
            #split to get ID of the image
            ID = int(os.path.split(imagePath)[-1].split('.')[0])
            faces.append(faceNp)
            print(ID)
            IDs.append(ID)
            #cv2.imshow("traning",faceNp)
            #cv2.waitKey()
        else:
            pass
    return IDs, faces

citizenIDs, faces = getImagesAndLabels(path)
#trainning
print(citizenIDs)
recognizer.train(faces, np.array(citizenIDs))
recognizer.save('model/trainningData.csv')

cv2.destroyAllWindows()

