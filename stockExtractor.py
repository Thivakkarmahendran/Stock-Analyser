#imports
import pandas as pd

from config import *

class stockExtractor:
  
    listOfStockSymbols = {}
    listOfStockNames = {}
    dfStocks = pd.DataFrame()
    
    def __init__(self):
        self.dfStocks = pd.read_csv("dataset/nasdaqStocks.csv")
        self.listOfStockSymbols = self.dfStocks['Symbol']
        self.listOfStockNames = self.dfStocks['Name']
        
    def getStockCountFromDF(self, textDF):
  
        tickers = {}
        tickerTexts = {}
        
        for comment in textDF:
           
           try: 
               wordSplit = comment.split(" ")
           except:
                wordSplit = []
           
           for word in wordSplit:
               
               #convert stock names to symbol
               try:
                tempDF = self.dfStocks[self.dfStocks["Name"].str.contains(word)]
                if(len(tempDF) == 1):
                    word = tempDF["Symbol"].values[0]
               except Exception as e:
                   print(e)
                

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
        
        

        
        