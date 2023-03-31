from datetime import datetime
f=open("log.txt","a")
def writeLog(message:str):
    logMsg=getLogMsg(message)
    print(logMsg,file=f)
    f.flush()
def getLogMsg(message:str)->str:
    cur_time=str(datetime.now())
    return f"{cur_time} {message}"

    