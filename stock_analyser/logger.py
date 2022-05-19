import datetime
import enum
import os
import pandas as pd

from config import LOGGER_DEBUG



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
    
    loggerOutput = loggerOutput.append({'Timestamp': datetime.datetime.now(), 'Type': type, 'Message': message, 'File Name': fileName}, ignore_index = True)
    

def exportLog():
    global loggerOutput
    global appRunSuccesful
        
    os.makedirs('Logs', exist_ok = True)
    loggerOutput = loggerOutput.append({'Timestamp': datetime.datetime.now(), 'Type': loggerMessageType.APP_STATUS.value, 'Message': "App run succesful: {}".format(appRunSuccesful), 'File Name': "logger.py"}, ignore_index = True)
    loggerOutput.to_csv('Logs/LOG_{}.csv'.format(datetime.datetime.now()))