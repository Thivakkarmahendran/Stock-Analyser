#imports
import imp
from os.path import exists
import os
import pandas as pd
import time
import warnings

from redditAPI import redditTimeFilter
from redditAPI import redditAPI
from stockExtractor import stockExtractor
from stockAnalysis import getTopStocks, printSentimalAnalysis
from sentimalAnalysis import stockTextSentimentAnalysis


#setup
warnings.filterwarnings("ignore")


def main():
    
    redditSubreddits = ["stock", "wallstreetbets", "investing", "robinhood"]
    
    print("Starting Stock Analyser")
    startTime = time.time()    
    os.makedirs('dataset', exist_ok = True)
    
    #get Reddit Titles
    dfTitles = pd.DataFrame()
    if not exists("dataset/redditTitles.csv"):
        redditApi = redditAPI()
        
        for subreddit in redditSubreddits:
            dfTitles = dfTitles.append(redditApi.getTopSubredditTitles(subreddit, redditTimeFilter.WEEK.value))
        dfTitles.to_csv("dataset/redditTitles.csv", index = False)
    else:
        print("Reddit Titles dataset already exists")
    
    print("Done getting reddit Titles: {} seconds".format(time.time()-startTime))
        
        
        
        
    #get Comments    
    if not exists("dataset/redditComments.csv"):
        redditApi = redditAPI()
        dfTitles = pd.read_csv("dataset/redditTitles.csv")
        dfAllComments = pd.DataFrame()
        
        for index, redditTitle in dfTitles.iterrows():
           dfAllComments = dfAllComments.append(redditApi.getPostComments(redditTitle['postId'], redditTitle['subredditName']))

        dfAllComments.to_csv("dataset/redditComments.csv", index = False)
    else:
        print("Reddit Comments dataset already exists")
    
    print("Done getting reddit comments: {} seconds".format(time.time()-startTime))
    
    #extract stocks from comments
    dfAllComments = pd.read_csv("dataset/redditComments.csv")
    stockExtract = stockExtractor()
    stocks, stockTexts = stockExtract.getStockCountFromDF(dfAllComments['commentText'])
    
    print("Done getting stocks from commennts: {} seconds".format(time.time()-startTime))
    
    #get Top Stocks
    topStocks, topStocksAndCount = getTopStocks(stocks)
    
    print(topStocksAndCount)
    
    print("Done getting top stocks: {} seconds".format(time.time()-startTime))
    
    stockScores = stockTextSentimentAnalysis(topStocks, stockTexts)
    
    print("Done perfoming sentimal analysis on top stocks: {} seconds".format(time.time()-startTime))
    
    printSentimalAnalysis(topStocks, stockScores)
    
    


if __name__ == '__main__':
    main()
    