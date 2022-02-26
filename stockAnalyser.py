#imports
import imp
from os.path import exists
import os
import pandas as pd

from redditAPI import redditTimeFilter
from redditAPI import redditAPI
from stockExtractor import stockExtractor
from stockAnalysis import getTopStocks
from sentimalAnalysis import stockTextSentimentAnalysis




def main():
    
    print("Starting Stock Analyser")
    os.makedirs('dataset', exist_ok = True)
    
    #get Reddit Titles
    if not exists("dataset/redditTitles.csv"):
        redditApi = redditAPI()
        dfTitles = redditApi.getTopSubredditTitles("stocks", redditTimeFilter.WEEK.value)
        dfTitles.to_csv("dataset/redditTitles.csv", index = False)
    else:
        print("Reddit Titles dataset already exists")
        
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
    
    #extract stocks from Title
    dfAllComments = pd.read_csv("dataset/redditComments.csv")
    stockExtract = stockExtractor()
    stocks, stockTexts = stockExtract.getStockCountFromDF(dfAllComments['commentText'])
    
    #get Top Stocks
    topStocks, topStocksAndCount = getTopStocks(stocks)
    
    scores = stockTextSentimentAnalysis(topStocks, stockTexts)
    
    print(scores)

    
   
    
    
if __name__ == '__main__':
    main()
    