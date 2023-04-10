import thread6
from time import sleep
# from hardware_connector import *
from log import *
# from random import randint
from detect_image import *


#thread to read from serial
# def receiceSerialMsg():
#     while True:
#         readSerial()

# thread6.run_threaded(receiceSerialMsg)

# main thread to detect img
while True:
    ret,frame=cap.read()
    faces=face_cascade.detectMultiScale(cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY))

    for (x,y,w,h) in faces:
        roi_color=frame[y:y+h,x:x+w]
        img_item="my-img.png"

        if global_lock.locked==False:
            #lock to prevent to many http request to sv
            global_lock.lock()
            thread6.run_threaded(helper,2)
			#demo send htpp
            cv2.imwrite(img_item,roi_color)
            

        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,0),2) 
        
    
    cv2.imshow("frame",frame)
    key=cv2.waitKey(20)
    if key==27:
        break


    

    