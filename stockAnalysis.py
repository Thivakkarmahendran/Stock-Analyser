import pandas as pd

from config import *



def getTopStocks(stocks, printOutput: bool = False):
    
    symbols = dict(sorted(stocks.items(), key=lambda item: item[1], reverse = True))
    topStocks = list(symbols.keys())[0:TOP_NUMBER_OF_STOCKS]
        
    if printOutput:
        print(f"\n{TOP_NUMBER_OF_STOCKS} most mentioned Stocks: ")
    
    times = []
    top = []
    for stockName in topStocks:
        
        if printOutput:
            print(f"{stockName}: {symbols[stockName]}")
            
        top.append(f"{stockName}: {symbols[stockName]}")
        
    return topStocks, top


def printSentimalAnalysis(topStocks, scores):
    print(f"\nSentiment analysis of top {topStocks} picks:")
    scores = scores.T
    scores.index = ['Bearish', 'Neutral', 'Bullish', 'Total', 'Sentiment']
    print(scores)