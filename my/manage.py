#!/usr/bin/env python3
"""Django's command-line utility for administrative tasks."""
import os
import sys
from Adafruit_IO import MQTTClient
import base64
import cv2
import face_recognition
from demo.models import *
AIO_USERNAME = "vutranhoang1411"
AIO_KEY = "aio_fVka33U5AthCsw0KlHzeRqQO0uAE"
AIO_FEED_IDs = ["doan.locker1","doan.locker2","doan.locker3","doan.image-detect"]

client = MQTTClient(AIO_USERNAME,AIO_KEY)

def on_connect(client):
    print("Ket noi thanh cong!")
    for feed in AIO_FEED_IDs:
        client.subscribe(feed)
    
def subscribe(client , userdata , mid , granted_qos):
    print("Subscribe thanh cong ...")

def disconnected(client):
    print("Ngat ket noi ...")
    sys.exit (1)


def message(client , feed_id:str , payload:str):
    if feed_id=="doan.image-detect":
        #get img
        buffer=base64.b64decode(payload.encode())
        frame=cv2.imdecode(buffer)
        rgb_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

        #get first faceencode inside img
        target_encode=face_recognition.face_encodings(rgb_frame)[0]
        res=[]
        #get cabinet image
        cabinets = Cabinet.objects.filter(aval=False).select_related('customerid')
        for cabinet in cabinets:
            img_path=cabinet.customerid.image
            img=face_recognition.load_image_file("/home/hoangdeptrai/ki2nam3/do_an/backend/public/img/"+img_path)
            cur_encode=face_recognition.face_encodings(img)[0]
            if face_recognition.compare_faces([cur_encode],target_encode,0.5)[0]:
                res.append(cabinet.id)
        client.publish("doan.open-locker",','.join(str(x) for x in res))
            # cabinet_data={
            #     'id':cabinet.id,
            #     'path':cabinet.customerid.image,
            # }
            # data.append(cabinet_data)





        

client.on_connect = on_connect
client.on_message = message
client.on_subscribe = subscribe
client.on_disconnect=disconnected



def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    client.connect()
    client.loop_background()
    main()
