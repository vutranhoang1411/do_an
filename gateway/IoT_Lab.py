from time import sleep
from hardware_connector import *
from detect_image import *
from Adafruit_IO import MQTTClient
import sys
import threading


AIO_USERNAME = "vutranhoang1411"
AIO_KEY = "aio_YxmO16iRoAzE7EL325vzHzSl8JAG"
AIO_FEED_IDs = []

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
    pass

client.on_connect = on_connect
client.on_message = message
client.on_subscribe = subscribe
client.on_disconnect=disconnected
client.connect()
client.loop_background()
sleep(5)
#thread to read from serial
def receiveSerialMsg():
    while True:
        readSerial(client)

threading.Thread(target=receiveSerialMsg).start()

# main thread to detect img

cam=AICam()
cam.StartRecord()

    

    