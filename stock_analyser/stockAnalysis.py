import pandas as pd

from config import *
from stock_analyser.logger import *



def getTopStocks(stocks):
    
    try:
        symbols = dict(sorted(stocks.items(), key=lambda item: item[1], reverse = True))
        topStocks = list(symbols.keys())[0 : TOP_NUMBER_OF_STOCKS]
                    
        times = []
        top = []
        for stockName in topStocks:            
            #times.append(symbols[stockName])
            top.append(f"{stockName}: {symbols[stockName]}")
    except Exception as e: 
        logComment(e, loggerMessageType.ERROR.value, "stockAnalysis.py") 
        global appRunSuccesful
        appRunSuccesful = False
        
    return topStocks, top





def printSentimalAnalysis(topStocks, scores):
    print(f"\nSentiment analysis of top {topStocks} picks:")
    scores = scores.T
    scores.index = ['Bearish', 'Neutral', 'Bullish', 'Total', 'Sentiment']
    print(scores)