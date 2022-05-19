#imports
import time
import datetime
import pandas as pd

from stock_analyser.redditAnalysis import runRedditAnalysis
from stock_analyser.logger import *
    
appRunSuccesful = True
loggerOutput = pd.DataFrame()

def main():    
    appStartTime = time.time() 
    logComment("***** Starting Stock Analyser *****", loggerMessageType.INFO.value, "app.py")
    
    #Analysis Reddit 
    #runRedditAnalysis()
    
    logComment("***** Completed Stock Analyser in {} (hrs:mins:seconds) *****".format(str(datetime.timedelta(seconds = time.time()-appStartTime))), loggerMessageType.INFO.value, "app.py")
    exportLog()
    


if __name__ == '__main__':
    main()
    