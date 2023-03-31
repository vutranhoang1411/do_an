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


ser = serial.Serial(port="/dev/pts/3", baudrate=115200)
mess = ""

def processData(data):
    #decode the data
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")
    #do something with the data
    #call http update

def readSerial():
    bytesToRead = ser.inWaiting()
    if (bytesToRead > 0):
        global mess
        mess = mess + ser.read(bytesToRead).decode("UTF-8")
        while ("#" in mess) and ("!" in mess):
            start = mess.find("!")
            end = mess.find("#")
            processData(mess[start:end + 1])
            if (end == len(mess)):
                mess = ""
            else:
                mess = mess[end+1:]
            #have to add error checking

def createSerialMessage(pac_id:int,dev_id:int,data:str)->str:
    return f"!{pac_id}:{dev_id}:{data}#"

def sendSerial(data):
    ser.write(str(data).encode("utf-8"))
