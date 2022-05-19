#imports
from os.path import exists
import os
import pandas as pd
import time
import warnings

from stock_analyser.redditAPI import redditTimeFilter
from stock_analyser.redditAPI import redditAPI
from stock_analyser.twitterAPI import twitterAPI
from stock_analyser.stockExtractor import stockExtractor
from stock_analyser.stockAnalysis import getTopStocks, printSentimalAnalysis
from stock_analyser.sentimalAnalysis import stockTextSentimentAnalysis
from config import *


#setup
warnings.filterwarnings("ignore")

startTime = time.time()    
lastTaskTime = time.time()  



def getRedditTitles():
    
    os.makedirs('dataset', exist_ok = True)
    #get Reddit Titles
    dfTitles = pd.DataFrame()
    if not exists("dataset/redditTitles.csv") or (startTime - os.path.getmtime("dataset/redditTitles.csv") > DATA_REFRESH):
        
        if exists("dataset/redditTitles.csv"):
            os.remove("dataset/redditTitles.csv")
            os.remove("dataset/redditComments.csv")
        
        redditApi = redditAPI()
        
        for subreddit in REDDIT_SUBREDDITS:
            dfTitles = dfTitles.append(redditApi.getTopSubredditTitles(subreddit, redditTimeFilter.WEEK.value))
        dfTitles.to_csv("dataset/redditTitles.csv", index = False)
    else:
        print("Reddit Titles dataset already exists")
    
    print("Done getting reddit Titles: {} seconds".format(time.time()-startTime))
    lastTaskTime = time.time()
    
    return dfTitles

def getRedditComments():
    #get Comments    
    if not exists("dataset/redditComments.csv"):
        redditApi = redditAPI()
        dfTitles = pd.read_csv("dataset/redditTitles.csv")
        dfAllComments = pd.DataFrame()
        
        for index, redditTitle in dfTitles.iterrows():
           dfAllComments = dfAllComments.append(redditApi.getPostComments(redditTitle['postId'], redditTitle['subredditName']))

        dfAllComments.to_csv("dataset/redditComments.csv", index = False)
    else:
        dfAllComments = pd.read_csv("dataset/redditComments.csv")
        print("Reddit Comments dataset already exists")
    
    print("Done getting reddit comments: {} seconds".format(time.time()-startTime))
    
    return dfAllComments
    

def runRedditAnalysis():
      
    lastTaskTime = time.time()  

    #get Reddit Titles
    getRedditTitles()
    
    #get Reddit Comments
    dfAllComments = getRedditComments()
    
    #extract stocks from comments
    stockExtract = stockExtractor()
    stocks, stockTexts = stockExtract.getStockCountFromDF(dfAllComments['commentText'])
    
    print("Done getting stocks from comments: {} seconds".format(time.time()-lastTaskTime))
    lastTaskTime = time.time()
    
    #get Top Stocks
    topStocks, topStocksAndCount = getTopStocks(stocks)
    
    print(topStocksAndCount)
    
    print("Done getting top stocks: {} seconds".format(time.time()-lastTaskTime))
    lastTaskTime = time.time()
    
    stockScores = stockTextSentimentAnalysis(topStocks, stockTexts)
    
    print("Done perfoming sentiment analysis on top stocks: {} seconds".format(time.time()-lastTaskTime))
    
    
    printSentimalAnalysis(topStocks, stockScores)

    
