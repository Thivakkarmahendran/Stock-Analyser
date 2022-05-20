#imports
from lib2to3.pgen2.tokenize import tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer
import emoji 
import re
import string
import en_core_web_sm
import pandas as pd
import numpy as np
from stock_analyser.logger import *

from config import *

def removeEmoji(text: str) -> str:
    return emoji.get_emoji_regexp().sub(r'', text)

def removePunctuation(text: str) -> str:
    text  = "".join([char for char in text if char not in string.punctuation])
    return re.sub('[0-9]+', '', text) 


def removeStopWord(text: str) -> str:
    nlp = en_core_web_sm.load()
    stopwords = nlp.Defaults.stop_words
    
    for word in text:
        if(word in stopwords):
            text.replace(word, "")
            
    return text
    

def cleanText(text: str) -> str:
    
    text = removeEmoji(text)
    text = text.lower()
    text = text.strip()
    text = removePunctuation(text)
    text = removeStopWord(text)
        
    return text



def stockTextSentimentAnalysis(topStocks, stockTexts):
    
    scores = {}
    
    vader = SentimentIntensityAnalyzer()
    
    # adding custom words from data.py 
    vader.lexicon.update(CUSTOM_SENTIMENT_ANALYSIS)
    
    
    for stock in topStocks:
        stockComments = stockTexts[stock]
        for comment in stockComments:
            
            sentimentComment = vader.polarity_scores(comment)
            
            if stock in scores:
                for key, _ in sentimentComment.items():
                    scores[stock][key] += sentimentComment[key]
            else:
                scores[stock] = sentimentComment
        
        for key in ['neg', 'neu', 'pos', 'compound']:
            scores[stock][key] = scores[stock][key] / len(stockComments)
    
    
    df = pd.DataFrame.from_dict(scores)
    df = df.T
    
    try:
        def conditions(s):
            if (s['compound'] >= 0.05):
                return "Positive"
            elif (s['compound'] <= -0.05):
                return "Negative"
            else:
                return "Neutral"
        
        df['Sentiment'] = df.apply(conditions, axis=1)        
    except Exception as e: 
        logComment(e, loggerMessageType.ERROR.value, "sentimalAnalysis.py") 
        global appRunSuccesful
        appRunSuccesful = False
      
    return df