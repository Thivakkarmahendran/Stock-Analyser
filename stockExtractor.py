#imports
import pandas as pd

class stockExtractor:
  
    listOfStockSymbols = {}
    listOfStockNames = {}
    
    blacklist = {'I', 'ARE',  'ON', 'GO', 'NOW', 'CAN', 'UK', 'SO', 'OR', 'OUT', 'SEE', 'ONE', 'LOVE', 'U', 'STAY', 'HAS', 'BY', 'BIG', 'GOOD', 'RIDE', 'EOD', 'ELON', 'WSB', 'THE', 'A', 'ROPE', 'YOLO', 'TOS', 'CEO', 'DD', 'IT', 'OPEN', 'ATH', 'PM', 'IRS', 'FOR','DEC', 'BE', 'IMO', 'ALL', 'RH', 'EV', 'TOS', 'CFO', 'CTO', 'DD', 'BTFD', 'WSB', 'OK', 'PDT', 'RH', 'KYS', 'FD', 'TYS', 'US', 'USA', 'IT', 'ATH', 'RIP', 'BMW', 'GDP', 'OTM', 'ATM', 'ITM', 'IMO', 'LOL', 'AM', 'BE', 'PR', 'PRAY', 'PT', 'FBI', 'SEC', 'GOD', 'NOT', 'POS', 'FOMO', 'TL;DR', 'EDIT', 'STILL', 'WTF', 'RAW', 'PM', 'LMAO', 'LMFAO', 'ROFL', 'EZ', 'RED', 'BEZOS', 'TICK', 'IS', 'PM', 'LPT', 'GOAT', 'FL', 'CA', 'IL', 'MACD', 'HQ', 'OP', 'PS', 'AH', 'TL', 'JAN', 'FEB', 'JUL', 'AUG', 'SEP', 'SEPT', 'OCT', 'NOV', 'FDA', 'IV', 'ER', 'IPO', 'MILF', 'BUT', 'SSN', 'FIFA', 'USD', 'CPU', 'AT', 'GG', 'Mar', 'REAL', 'ME'}
    
    def __init__(self):
        dfStocks = pd.read_csv("dataset/nasdaqStocks.csv")
        self.listOfStockSymbols = dfStocks['Symbol']
        self.listOfStockNames = dfStocks['Name']
        
    def getStockCountFromDF(self, textDF):
        
        tickers = {}
        tickerTexts = {}
        
        for comment in textDF:
            
           wordSplit = comment.split(" ")
           for word in wordSplit:

               word = word.replace("$", "")
               word.upper()
               
               if len(word) <= 5 and word in self.listOfStockSymbols.values and word not in self.blacklist:
                   if word in tickers:
                       tickers[word] += 1
                       tickerTexts[word].append(comment)
                   else: 
                       tickers[word] = 1
                       tickerTexts[word] = [comment]

        return tickers, tickerTexts
        
        

        
        