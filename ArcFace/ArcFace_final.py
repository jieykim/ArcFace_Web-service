import cv2
from deepface.commons import functions, distance as dst
import matplotlib.pyplot as plt
import ArcFace
import numpy as np
import os

model = ArcFace.loadModel()
model.load_weights("ArcFace\\arcface_weights.h5")

target_size = (112, 112)


from pathlib import Path

latest_image = max(Path("C:\\Users\\user\\final\\downloads").glob('*.[jJpP]*[gG]'), key=lambda x: x.stat().st_ctime, default=None)
# print(latest_image)

# Path 객체를 문자열로 변환하여 replace()를 사용합니다.
new_path = str(latest_image).replace("\\", "\\\\")
# print(new_path)

bx1_path = new_path     #    "bx2" + ".jpg"
img_path = "C:\\Users\\user\\final\\ArcFace\\local_img"
# print(img_path)
img_path_list = os.listdir(img_path)

detector_backend = 'opencv'
bx1 = functions.extract_faces(bx1_path, target_size = target_size, detector_backend = detector_backend)
img_list_extraction=[]
for i in img_path_list:
    img_list_extraction.append(functions.extract_faces(img_path +'\\{}'.format(i), target_size = target_size, detector_backend = detector_backend,enforce_detection=False))
    
metric = 'euclidean'



def findThreshold(metric):
    if metric == 'cosine':
        return 0.6871912959056619
    elif metric == 'euclidean':
        return 4.1591468986978075
    elif metric == 'euclidean_l2':
        return 1.1315718048269017
    
def verify(img1, img2):
    
    #representation
    
    img1_array = np.array([face_img for face_img, _, _ in img1])
    img2_array = np.array([face_img for face_img, _, _ in img2])
    
    img1_array = np.squeeze(img1_array, axis=1)
    img2_array = np.squeeze(img2_array, axis=1)

    # Representation
    img1_embedding = model.predict(img1_array)[0]
    img2_embedding = model.predict(img2_array)[0]

    if metric == 'cosine':
        distance = dst.findCosineDistance(img1_embedding, img2_embedding)
    elif metric == 'euclidean':
        distance = dst.findEuclideanDistance(img1_embedding, img2_embedding)
    elif metric == 'euclidean_l2':
        distance = dst.findEuclideanDistance(dst.l2_normalize(img1_embedding), dst.l2_normalize(img2_embedding))
    
    #------------------------------
    #verification
    
    threshold = findThreshold(metric)
    
    global cert
    
    if distance <= threshold:
        # print("they are same person")
        cert = True
        
    else:
        # print("they are different persons")
        
    # print("Distance is ",round(distance, 2)," whereas as expected max threshold is ",round(threshold, 2))
    
    #------------------------------
    # display
    
    # fig = plt.figure()
    
    # ax1 = fig.add_subplot(1,2,1)
    # plt.axis('off')
    # plt.imshow(img1_array[0][:,:,::-1])
    
    # ax2 = fig.add_subplot(1,2,2)
    # plt.axis('off')
    # plt.imshow(img2_array[0][:,:,::-1])
    
    # plt.show()
    
cert = False
# global cert = False
for i in img_list_extraction:
    verify(bx1,i)
    if cert == True:
        break
    
if cert:
    print("등록된 사람입니다")
else:
    print("미등록 인원입니다")
    
print(cert)