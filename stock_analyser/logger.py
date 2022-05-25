import datetime
import enum
import imp
import os
import pandas as pd

from config import LOGGER_DEBUG
from setup import APP_VERSION, APP_NAME

appRunSuccesful = True
loggerOutput = pd.DataFrame()

#ENUMS
class loggerMessageType(enum.Enum):
    ERROR = "ERROR"
    INFO = "INFO"
    APP_STATUS = "APP STATUS"



def logComment(message:str, type: str, fileName: str):
    global loggerOutput
    
    if LOGGER_DEBUG:
        print("{}: {}".format(type, message))
    
    loggerOutput = loggerOutput.append({'Timestamp': datetime.datetime.now(), 'Type': type, 'Message': message, 'File Name': fileName, 'Version': APP_VERSION}, ignore_index = True)
    

def exportLog():
    global loggerOutput
    global appRunSuccesful
        
    os.makedirs('Logs', exist_ok = True)
    loggerOutput = loggerOutput.append({'Timestamp': datetime.datetime.now(), 'Type': loggerMessageType.APP_STATUS.value, 'Message': "App run succesful: {}".format(appRunSuccesful), 'File Name': "logger.py", 'Version': APP_VERSION}, ignore_index = True)
    loggerOutput.to_csv('Logs/{}-{}-LOG_{}.csv'.format(APP_NAME, APP_VERSION, datetime.datetime.now()))