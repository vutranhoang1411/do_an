import face_recognition
import cv2
import numpy as np
import simple_lock
import threading
from time import sleep
import base64

def UnlockLock(lock):
    sleep(30)
    lock.Unlock()
class AICam:
    def __init__(self,client):
        self.video_capture=cv2.VideoCapture(0)
        self.client=client

    def StartRecord(self):
        lock=simple_lock.Lock()
        process_this_frame=True
        while True:
            ret, frame = self.video_capture.read()
            if process_this_frame:
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
                rgb_small_frame = cv2.cvtColor(small_frame,cv2.COLOR_BGR2RGB)
                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(rgb_small_frame)
                if len(face_locations)>0:
                  if lock.Locked==False:
                        lock.Lock()
                        threading.Thread(target=UnlockLock,args=(lock,)).start()
                        img_bytes=cv2.imencode('.jpg',rgb_small_frame)[1].tobytes()
                        data=base64.b64encode(img_bytes)
                        self.client.publish("doan.image-detect",data)   
            

            process_this_frame = not process_this_frame
            for (top, right, bottom, left) in face_locations:
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)

            # Display the resulting image
            cv2.imshow('Video', frame)

            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.video_capture.release()
        cv2.destroyAllWindows()
