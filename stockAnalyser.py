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
from config import *


#setup
warnings.filterwarnings("ignore")


def main():
    
    print("Starting Stock Analyser")
    startTime = time.time()    
    os.makedirs('dataset', exist_ok = True)
    
    #get Reddit Titles
    dfTitles = pd.DataFrame()
    if not exists("dataset/redditTitles.csv"):
        redditApi = redditAPI()
        
        for subreddit in REDDIT_SUBREDDITS:
            dfTitles = dfTitles.append(redditApi.getTopSubredditTitles(subreddit, redditTimeFilter.WEEK.value))
        dfTitles.to_csv("dataset/redditTitles.csv", index = False)
    else:
        dfTitles = pd.read_csv("dataset/redditTitles.csv")
        print("Reddit Titles dataset already exists")
        
    if(dfTitles is None or len(dfTitles) == 0):
        print("*ERROR* Could not load reddit Titles - STOPPING PROGRAM")
        exit()
    
    print("Done getting reddit Titles: {} seconds".format(time.time()-startTime))  
        
        
    #get Comments    
    if not exists("dataset/redditComments.csv"):
        redditApi = redditAPI()
        dfComments = pd.DataFrame()
        
        for index, redditTitle in dfTitles.iterrows():
           dfComments = dfComments.append(redditApi.getPostComments(redditTitle['postId'], redditTitle['subredditName']))

        dfComments.to_csv("dataset/redditComments.csv", index = False)
    else:
        dfComments = pd.read_csv("dataset/redditComments.csv")
        print("Reddit Comments dataset already exists")
    
    if(dfComments is None or len(dfComments) == 0):
        print("*ERROR* Could not load reddit Comments - STOPPING PROGRAM")
        exit()
    
    print("Done getting reddit comments: {} seconds".format(time.time()-startTime))
    
    
    #extract stocks from comments
    stockExtract = stockExtractor()
    stocks, stockTexts = stockExtract.getStockCountFromDF(dfComments['commentText'])
    
    if(stocks is None or len(stocks) == 0):
        print("*ERROR* Could not parse stocks - STOPPING PROGRAM")
        exit()
    
    print("Done getting stocks from commennts: {} seconds".format(time.time()-startTime))
    
    #get Top Stocks
    topStocks, topStocksAndCount = getTopStocks(stocks)
    
    if(topStocks is None or len(topStocks) == 0):
        print("*ERROR* Could not get top stocks - STOPPING PROGRAM")
        exit()
    
    print("Done getting top stocks: {} seconds".format(time.time()-startTime))
    
    stockScores = stockTextSentimentAnalysis(topStocks, stockTexts)
    
    print("Done perfoming sentimal analysis on top stocks: {} seconds".format(time.time()-startTime))
    
    printSentimalAnalysis(topStocks, stockScores)
    
    


if __name__ == '__main__':
    main()
    