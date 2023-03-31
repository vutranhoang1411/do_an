  # TensorFlow is required for Keras to work
import cv2  # Install opencv-python
from time import sleep
#class locker help control the amount of http request
class Lock:
	def __init__(self) -> None:
		self.locked=False
	def free(self):
		self.locked=False
	def lock(self):
		self.locked=True
global_lock=Lock()

		
def helper(sec):
    sleep(sec)
    global_lock.free()  
# CAMERA can be 0 or 1 based on default camera of your computer
cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier('./data/haarcascade_frontalface_default.xml')


# while True:
#     ret, img = cap.read() 
#     # convert to gray scale of each frames
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
#     #regconize face
#     img_for_regconize=cv2.resize(img, (224, 224), interpolation=cv2.INTER_AREA)
#     img_for_regconize = np.asarray(img_for_regconize, dtype=np.float32).reshape(1, 224, 224, 3)
#     # Normalize the image array
#     img_for_regconize = (img_for_regconize / 127.5) - 1
#     # Predicts the model
#     prediction = model.predict(img_for_regconize)
#     #prediction=[[percentage of each class in the label file]]
#     percentage_list=prediction[0]
#     #index of the best perdicted item in label file
#     index=np.argmax(percentage_list)
#     class_name=class_names[index]
#     confidence_score=percentage_list[index]
#     # Print prediction and confidence score
#     has_face=int(class_name[0])

#     if has_face==0:
#         print("Detect face")
#         print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")
#         faces = face_cascade.detectMultiScale(gray, 1.3, 5)
#         for (x,y,w,h) in faces:
#         # To draw a rectangle in a face 
#             roi_color=img[y:y+h,x:x+w]
#             img_item="my-img.png"
#             cv2.imwrite(img_item,roi_color)
#             cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2) 
            
#     # Detects faces of different sizes in the input image

#     # Display an image in a window
#     cv2.imshow('detect_img',img)
  
#     # Wait for Esc key to stop
#     k = cv2.waitKey(30)
#     if k == 27:
#         break
#     # Grab the webcamera's image.
#     ret, image = camera.read()

#     # Resize the raw image into (224-height,224-width) pixels
#     image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

#     # Show the image in a window
#     cv2.imshow("Webcam Image", image)

#     # Make the image a numpy array and reshape it to the models input shape.
#     image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

#     # Normalize the image array
#     image = (image / 127.5) - 1

#     # Predicts the model
#     prediction = model.predict(image)
#     index = np.argmax(prediction)
#     class_name = class_names[index]
#     confidence_score = prediction[0][index]

#     # Print prediction and confidence score
#     print("Class:", class_name[2:], end="")
#     print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")

#     # Listen to the keyboard for presses.
#     keyboard_input = cv2.waitKey(1)

#     # 27 is the ASCII for the esc key on your keyboard.
#     if keyboard_input == 27:
#         break

# camera.release()
# cv2.destroyAllWindows()
