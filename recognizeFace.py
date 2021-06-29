import cv2
import numpy as np
import math
from training import preprocessing
from PIL import ImageFont, ImageDraw, Image
from SQLConnection import SQLConnection

face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')

def load_trained_model():
    eigen_vectors = np.loadtxt('model/eigen_vectors.csv', delimiter=',')
    eigen_faces = np.loadtxt('model/eigen_faces.csv', delimiter=',')
    mean_face = np.loadtxt('model/mean_face.csv', delimiter=',')
    with open('model/name_list.txt', 'r') as f:
        name_list = f.readlines()
    return mean_face, eigen_vectors, eigen_faces, name_list

def face_recognition(face, mean_face, eigen_vectors, eigen_faces):
    if face.shape != (100,100):
        face = cv2.resize(face, (100, 100))
    # face = preprocessing(face, 0.2)
    face = np.asarray(face).flatten().transpose()
    face = (face - mean_face).reshape((1,10000))
    weight = np.matmul(face, eigen_vectors).transpose()
    return nearest_neighbor_classifier(weight, eigen_faces)

def nearest_neighbor_classifier(unknown_face, eigen_faces):
    error = np.empty(eigen_faces.shape[1], float)
    for i in range(eigen_faces.shape[1]):
        face_i = eigen_faces[:, i].reshape((-1,1))
        # error[i] = np.linalg.norm(unknown_face - face_i)
        temp = 0
        for j in range(eigen_faces.shape[0]):
            temp += (unknown_face[j,0]-face_i[j,0])*(unknown_face[j,0]-face_i[j,0])
        error[i] = math.sqrt(temp)/eigen_faces.shape[0]
    idx = np.where(error==np.amin(error))
    return idx, error[idx]

def rotate_image(image, angle):
    if angle == 0: return image
    height, width = image.shape[:2]
    rot_mat = cv2.getRotationMatrix2D((width/2, height/2), angle, 0.9)
    result = cv2.warpAffine(image, rot_mat, (width, height), flags=cv2.INTER_LINEAR)
    return result

def rotate_point(pos, img, angle):
    if angle == 0: return pos
    x = pos[0] - img.shape[1]*0.4
    y = pos[1] - img.shape[0]*0.4
    newx = x*math.cos(math.radians(angle)) + y*math.sin(math.radians(angle)) + img.shape[1]*0.4
    newy = -x*math.sin(math.radians(angle)) + y*math.cos(math.radians(angle)) + img.shape[0]*0.4
    return int(newx), int(newy), pos[2], pos[3]

# if __name__ == '__main__':
#     SQL = SQLConnection()
#     font = ImageFont.truetype("arial.ttf", 32)


#     mean_face, eigen_vectors, eigen_faces, name_list = load_trained_model()
#     video_capture = cv2.VideoCapture(0)
#     while(video_capture.isOpened()):
#         ret, img = video_capture.read()
#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         gray = cv2.equalizeHist(gray)

#         for angle in [0, -20, 20, -40, 40]:
#             rimg = rotate_image(img, angle)
#             faces = face_cascade.detectMultiScale(rimg,  1.1, 2, 0|2, (100,100))
#             if len(faces):
#                 faces = [rotate_point(faces[0], img, -angle)]
#                 break
#         for x, y, w, h in faces:
#             cv2.rectangle(img, (x, y), (x+w, y+h), (0,255,0), 2)
#             test_face = gray[y:y+h, x:x+w]
#             id, score = face_recognition(test_face, mean_face, eigen_vectors, eigen_faces)
#             name_id = int(name_list[id[0][0]])
#             print(name_id)
#             data = SQL.queryDataOnly1("Select CID From ListID Where ID = '{}'".format(name_id))
#             print(data[0])
#             dataName = SQL.queryDataOnly1("Select HoTen From FaceID Where CMT = '{}'".format(data[0]))
#             print(str(dataName[0]))
            


#             #cv2.putText(img, str(name_id)+':'+id, (x+5,y-5), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255) , 2)
#             #cv2.putText(img, str(score[0]), (x + 5, y+h + 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1)
#             cv2.putText(img, str(data[0]), (x+5, y+h+25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255) , 2)
#             #cv2.putText(img, str(dataName[0]), (x+5, y+h+50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255) , 2)
#             img_pil = Image.fromarray(img)
#             draw = ImageDraw.Draw(img_pil)
#             draw.text((x+5, y+h+50), dataName[0], font=font)
#             img = np.array(img_pil)

#         cv2.imshow('img', img)
#         k = cv2.waitKey(30) & 0xff
#         if k==27:
#             break
#     video_capture.release()
