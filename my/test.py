import face_recognition
from os import listdir
import numpy as np
img_files=listdir("./base_image")
knowface_encodes=[]
knowface_name=[]
for img_file in img_files:
    #get img name
    knowface_name.append(img_file.split(".")[0])

    #get encode
    img=face_recognition.load_image_file('./base_image/'+img_file)
    encode=face_recognition.face_encodings(img)[0]
    knowface_encodes.append(encode)

#get img from request

#process target img
target_img=face_recognition.load_image_file('./test.png')
target_encode=face_recognition.face_encodings(target_img)[0]

#get candidate matches list
matches=face_recognition.compare_faces(knowface_encodes,target_encode)
#get closet img to the target
face_distances = face_recognition.face_distance(knowface_encodes,target_encode)
best_match_index = np.argmin(face_distances)

if matches[best_match_index]:
    print(knowface_name[best_match_index])