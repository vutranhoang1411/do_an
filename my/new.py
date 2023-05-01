
import sys
from Adafruit_IO import MQTTClient
import base64
import cv2
import face_recognition
import numpy
import psycopg2

conn = psycopg2.connect(
    dbname="do_an",
    user="root",
    password="Hoang2002",
    host="localhost",
    port="5432"
)

AIO_USERNAME = "vutranhoang1411"
AIO_KEY = "aio_nHIY69pgQGiya2p1XZm4Q5JjgYnO"
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
    cur = conn.cursor()
    if feed_id=="doan.image-detect":
        cur.execute("""
            select cabinet.id, customer.photo 
            from cabinet left join customer on cabinet.userid=customer.id 
            where cabinet.avail=false;;
        """)
        cabinets = cur.fetchall()
        #get img
        buffer=base64.b64decode(payload)
        frame = cv2.imdecode(numpy.frombuffer(buffer,dtype=numpy.uint8),cv2.IMREAD_COLOR)
        rgb_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        #get first faceencode inside img
        encodes=face_recognition.face_encodings(rgb_frame)
        if len(encodes)==0:
            return
        target_encode=encodes[0]
        res=[]
        #get cabinet image
        for cabinet in cabinets:
            img_path=cabinet[1]
            img=face_recognition.load_image_file("/home/hoangdeptrai/ki2nam3/do_an/backend/public/img/"+img_path)
            cur_encode=face_recognition.face_encodings(img)
            if face_recognition.compare_faces(cur_encode,target_encode)[0]:
                res.append(cabinet[0])
        if len(res)>0:
            client.publish("doan.open-locker",','.join(str(x) for x in res))


client.on_connect = on_connect
client.on_message = message
client.on_subscribe = subscribe
client.on_disconnect=disconnected
client.connect()
client.loop_blocking()




