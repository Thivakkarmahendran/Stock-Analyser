import pandas as pd

from config import *
from stock_analyser.logger import *
from stock_analyser.twitterAPI import twitterAPI 



def getTopStocks(stocks):
    
    try:
        symbols = dict(sorted(stocks.items(), key=lambda item: item[1], reverse = True))
        topStocks = list(symbols.keys())[0 : TOP_NUMBER_OF_STOCKS]
                    
        topStocksCount = {}
        
        for stockName in topStocks:            
            topStocksCount[stockName] = symbols[stockName]
    except Exception as e: 
        logComment(e, loggerMessageType.ERROR.value, "stockAnalysis.py") 
        global appRunSuccesful
        appRunSuccesful = False
        
    return topStocks, topStocksCount


def postTopStocks(topStocks, topStocksCount):
    tweet = "The top mentoined stocks on Reddit for the past week are: \n"
    for stock in topStocks:  
        tweet = tweet + "- {}\n".format(stock)    
    
    twitterApi = twitterAPI()
    twitterApi.postTweet(tweet)      
        
    


def printSentimalAnalysis(topStocks, scores):
    print(f"\nSentiment analysis of top {topStocks} picks:")
    scores = scores.T
    scores.index = ['Bearish', 'Neutral', 'Bullish', 'Total', 'Sentiment']
    print(scores)