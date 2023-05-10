import serial.tools.list_ports

# def getPort():
#     ports = serial.tools.list_ports.comports()
#     N = len(ports)
#     commPort = "None"
#     for i in range(0, N):
#         port = ports[i]
#         strPort = str(port)
#         if "USB Serial Device" in strPort:
#             splitPort = strPort.split(" ")
#             commPort = (splitPort[0])
#     return commPort

# def printPort():
#     ports = serial.tools.list_ports.comports()
#     N = len(ports)
#     commPort = "None"
#     for i in range(0, N):
#         port = ports[i]
#         strPort = str(port)
#         print(strPort)


ser = serial.Serial(port="/dev/ttyUSB0", baudrate=115200)
mess = ""

def preProcessData(data:str)->str:
    start=-1
    for c in range(len(data)):
        if data[c]=='!':
            start=c
    data=data[start:]
    data = data.replace("!", "")
    data = data.replace("#", "")
    return data

def processData(client,data):
    #decode the data
    data=preProcessData(data)

    #data format:   <dev id>:<0/1>
    splitData = data.split(":")
    dev_id=splitData[0]
    payload=splitData[1]

    
    if dev_id=="1":
        client.publish("doan.locker1",payload)
    elif dev_id=="2":
        client.publish("doan.locker2",payload)
    elif dev_id=="3":
        client.publish("doan.locker3",payload)

def readSerial(client):
    bytesToRead = ser.inWaiting()
    if (bytesToRead > 0):
        global mess
        mess = mess + ser.read(bytesToRead).decode("UTF-8")
        while ("#" in mess) and ("!" in mess):
            start = mess.find("!")
            end = mess.find("#")
            processData(client,mess[start:end + 1])
            if (end == len(mess)):
                mess = ""
            else:
                mess = mess[end+1:]
            #have to add error checking


def sendSerial(data):
    ser.write(str(data).encode("utf-8"))
