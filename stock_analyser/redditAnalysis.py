#imports
from glob import glob
from os.path import exists
import os
import pandas as pd
import time
import warnings

from stock_analyser.redditAPI import redditTimeFilter
from stock_analyser.redditAPI import redditAPI
from stock_analyser.twitterAPI import twitterAPI
from stock_analyser.stockExtractor import stockExtractor
from stock_analyser.stockAnalysis import getTopStocks, printSentimalAnalysis, postTopStocks
from stock_analyser.sentimalAnalysis import stockTextSentimentAnalysis
from config import *
from stock_analyser.logger import *


#setup
warnings.filterwarnings("ignore")



def getRedditTitles():    
    #get Reddit Titles
    dfTitles = pd.DataFrame()
    
    try:
        if not exists("dataset/redditTitles.csv"):
            redditApi = redditAPI()
            
            for subreddit in REDDIT_SUBREDDITS:
                dfTitles = dfTitles.append(redditApi.getTopSubredditTitles(subreddit, redditTimeFilter.WEEK.value))
            if(len(dfTitles) > 0):
                dfTitles.to_csv("dataset/redditTitles.csv", index = False)
        else:
            logComment("Reddit Titles dataset already exists", loggerMessageType.ERROR.value, "RedditAnalysis.py")
    except Exception as e:
        logComment(e, loggerMessageType.ERROR.value, "RedditAnalysis.py")
        global appRunSuccesful
        appRunSuccesful = False
        
    return dfTitles

#get Comments 
def getRedditComments():
    dfAllComments = pd.DataFrame()
    
    try: 
        if not exists("dataset/redditComments.csv"):
            redditApi = redditAPI()
            
            dfTitles = pd.read_csv("dataset/redditTitles.csv")
            
            for index, redditTitle in dfTitles.iterrows():
                dfAllComments = dfAllComments.append(redditApi.getPostComments(redditTitle['postId'], redditTitle['subredditName']))

            dfAllComments.to_csv("dataset/redditComments.csv", index = False)
        else:
            dfAllComments = pd.read_csv("dataset/redditComments.csv")
            logComment("Reddit Comments dataset already exists", loggerMessageType.ERROR.value, "RedditAnalysis.py")
    except Exception as e:
        logComment(e, loggerMessageType.ERROR.value, "RedditAnalysis.py")
        global appRunSuccesful
        appRunSuccesful = False
    
    return dfAllComments
    

def runRedditAnalysis():
    global appRunSuccesful
    os.makedirs('dataset', exist_ok = True)
   
    if FRESH_RUN:
        logComment("FRESH RUN IS ENABLED", loggerMessageType.INFO.value, "RedditAnalysis.py")
         
    if FORCE_RUN:
        logComment("FORCE RUN IS ENABLED", loggerMessageType.INFO.value, "RedditAnalysis.py")
         
         
   
    if exists("dataset/redditTitles.csv") and FRESH_RUN:
        os.remove("dataset/redditTitles.csv")
        os.remove("dataset/redditComments.csv")
    
       
    if exists("dataset/redditTitles.csv") and (time.time() - os.path.getmtime("dataset/redditTitles.csv") < DATA_REFRESH) and not FORCE_RUN:
        logComment("Skipping stock analyser app since last run time is less than DATA_REFRESH", loggerMessageType.ERROR.value, "RedditAnalysis.py")
        return 
   
    lastTaskTime = time.time()  
    
    #get Reddit Titles
    getRedditTitles()
    logComment("Done getting reddit Titles: {} seconds".format(time.time()-lastTaskTime), loggerMessageType.INFO.value, "RedditAnalysis.py")
    lastTaskTime = time.time()  
    
    #get Reddit Comments
    dfAllComments = getRedditComments()
    logComment("Done getting reddit Comments: {} seconds".format(time.time()-lastTaskTime), loggerMessageType.INFO.value, "RedditAnalysis.py")
    
    #extract stocks from comments
    stockExtract = stockExtractor()
    
    try:
        stocks, stockTexts = stockExtract.getStockCountFromDF(dfAllComments['commentText'])
        logComment("Done getting stocks from comments: {} seconds".format(time.time()-lastTaskTime), loggerMessageType.INFO.value, "RedditAnalysis.py")
        lastTaskTime = time.time()
        
        #get Top Stocks
        topStocks, topStocksAndCount = getTopStocks(stocks)
        logComment("Done getting top stocks: {} seconds".format(time.time()-lastTaskTime), loggerMessageType.INFO.value, "RedditAnalysis.py")
        

        
        lastTaskTime = time.time()
        
        stockScores = stockTextSentimentAnalysis(topStocks, stockTexts)
        logComment("Done perfoming sentiment analysis on top stocks: {} seconds".format(time.time()-lastTaskTime), loggerMessageType.INFO.value, "RedditAnalysis.py")
        
        
        #publish results
        postTopStocks(topStocks, topStocksAndCount)
        #printSentimalAnalysis(topStocks, stockScores)
        
    except Exception as e: 
        logComment(e, loggerMessageType.ERROR.value, "RedditAnalysis.py")
        appRunSuccesful = False
    