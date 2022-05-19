import datetime
import enum
import os

from app import loggerOutput
from app import appRunSuccesful


#ENUMS
class loggerMessageType(enum.Enum):
    ERROR = "ERROR"
    INFO = "INFO"
    APP_STATUS = "APP STATUS"



def logComment(message:str, type: str, fileName: str):
    global loggerOutput
    loggerOutput = loggerOutput.append({'Timestamp': datetime.datetime.now(), 'Type': type, 'Message': message, 'File Name': fileName}, ignore_index = True)
    

def exportLog():
    global loggerOutput
    global appRunSuccesful
    
    os.makedirs('Logs', exist_ok = True)
    loggerOutput = loggerOutput.append({'Timestamp': datetime.datetime.now(), 'Type': loggerMessageType.APP_STATUS.value, 'Message': "App run succesful: {}".format(appRunSuccesful), 'File Name': "logger.py"}, ignore_index = True)
    loggerOutput.to_csv('Logs/LOG_{}.csv'.format(datetime.datetime.now()))