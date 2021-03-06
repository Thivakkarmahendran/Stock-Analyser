#imports
import pandas as pd

from config import *
from stock_analyser.logger import *

class stockExtractor:
  
    listOfStockSymbols = {}
    listOfStockNames = {}
    
    def __init__(self):
        try:
            dfStocks = pd.read_csv("dataset/nasdaqStocks.csv")
            self.listOfStockSymbols = dfStocks['Symbol']
            self.listOfStockNames = dfStocks['Name']
        except Exception as e: 
            logComment(e, loggerMessageType.ERROR.value, "stockExtractor.py") 
            global appRunSuccesful
            appRunSuccesful = False
        
    def getStockCountFromDF(self, textDF):
        
        tickers = {}
        tickerTexts = {}
        
        for comment in textDF:
           
           try: 
               wordSplit = comment.split(" ")
           except:
                wordSplit = []
           
           for word in wordSplit:

               word = word.replace("$", "")
               word = word.upper()
               
               if len(word) <= 5 and word in self.listOfStockSymbols.values and word not in STOCK_BLACKLIST:
                   if word in tickers:
                       tickers[word] += 1
                       tickerTexts[word].append(comment)
                   else: 
                       tickers[word] = 1
                       tickerTexts[word] = [comment]

        return tickers, tickerTexts
        
        

        
        