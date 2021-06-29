import os
import cv2
import numpy as np
import math

def adjust_gamma(image, gamma=0.2):
	invGamma = 1.0 / gamma
	table = np.array([((i / 255.0) ** invGamma) * 255
		for i in np.arange(0, 256)]).astype("uint8")
	return cv2.LUT(image, table)

def preprocessing(img, gamma=0.2, sigma0=1.0, sigma1=2.0, norm=10):
    img = adjust_gamma(img, gamma)

    if sigma0>0 and sigma1>0:
        ksize1 = np.arange(math.ceil(-3.0*sigma0-0.5), math.floor(3.0*sigma0+0.5), 1).size
        ksize2 = np.arange(math.ceil(-3.0*sigma1-0.5), math.floor(3.0*sigma1+0.5), 1).size
        if ksize1%2==0: ksize1+=1
        if ksize2%2==0: ksize2+=1
        gaussian1 = cv2.GaussianBlur(img, (ksize1,ksize1), sigma0, borderType=cv2.BORDER_REPLICATE)
        gaussian2 = cv2.GaussianBlur(img, (ksize2,ksize2), sigma1, borderType=cv2.BORDER_REPLICATE)
        img = gaussian1 - gaussian2

    if norm:
        a = 0.1
        trim = abs(norm)
        img_a = np.power(np.absolute(img), a)
        img = img/(np.power(np.mean(img_a), 1/a))

        img_b = np.power(np.minimum(np.full(img.shape,trim),np.absolute(img)), a)
        img = img/(np.power(np.mean(img_b), 1/a))

        img = trim*np.tanh(img/trim)
    return img

def load_dataset(path):
    dataset = {}
    for file in os.listdir(path):
        if file[-3:] in ['jpg', 'png']:
            name = os.path.split(file)[-1].split('.')[1]
            print('Loaded',file, 'with name_id', name)
            img = cv2.imread(os.path.join(path,file), cv2.IMREAD_GRAYSCALE)
            if img.shape != (100,100):
                img = img.resize(img, (100,100))
            img = cv2.equalizeHist(img)
            # img = preprocessing(img, 0.2)
            img = np.asarray(img)
            dataset.update({name: img})
        else:
            pass
    return dataset

def create_matrix(face_dataset):
    face_num = len(face_dataset)
    face_matrix = np.zeros((10000, face_num))
    i = 0
    for k in face_dataset.keys():
        face_matrix[:, i] = face_dataset[k].flatten()
        i += 1
    mean_face = np.empty((1,10000), float)
    mean_face = face_matrix.sum(axis=1)/face_num
    for i in range(face_num):
        face_matrix[:, i] = face_matrix[:, i] - mean_face
    return face_matrix, mean_face

def pca(face_matrix):
    face_num = face_matrix.shape[1]
    eigen_num = face_num
    cov_matrix = np.matmul(face_matrix.transpose(), face_matrix)/face_num
    eigen_values, eigen_vectors = np.linalg.eig(cov_matrix)
    eigen_vectors = eigen_vectors[:, eigen_values.argsort()[::-1]][:, 0:eigen_num]
    eigen_vectors = np.matmul(face_matrix, eigen_vectors)
    eigen_faces = np.empty((eigen_num, face_num))
    for i in range(face_num):
        eigen_faces[:, i] = np.matmul(face_matrix[:, i].transpose(), eigen_vectors).transpose()
    return cov_matrix, eigen_vectors, eigen_faces

if __name__ == '__main__':
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
