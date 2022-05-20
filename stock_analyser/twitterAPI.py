import imp
import string
from xmlrpc.client import boolean
import tweepy 
from credentials import *
from config import *
from stock_analyser.logger import *

"""
    twitterApi = twitterAPI()
    twitterApi.postTweet("Hello World!!")
"""

class twitterAPI:
    
    twitterApi = None
    
    def __init__(self):
        
        auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_KEY_SECRET)
        auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
        
        self.twitterApi = tweepy.API(auth)
        self.isVerifyCredentials()
        
    
    def isVerifyCredentials(self):
        
        try:
            self.twitterApi.verify_credentials()
        except Exception as e:
            logComment("Error during authentication: {}".format(e), loggerMessageType.ERROR.value, "twitterAPI.py") 
            
            
    def postTweet(self, text: string):
        
        if not POST_TWEET:
            logComment("TWITTER POST disabled in the config", loggerMessageType.INFO.value, "twitterAPI.py")
            return
        
        try:
            self.twitterApi.update_status(status = text)
        except Exception as e: 
            logComment(e, loggerMessageType.ERROR.value, "twitterAPI.py")
            global appRunSuccesful
            appRunSuccesful = False
        
    def postTweetWithImage(self, text: string, imagePath: string):
        if not POST_TWEET:
            logComment("TWITTER POST disabled in the config", loggerMessageType.INFO.value, "twitterAPI.py")
            return
        
        try:
            self.twitterApi.update_with_media(imagePath, imagePath)
        except Exception as e: 
            logComment(e, loggerMessageType.ERROR.value, "twitterAPI.py")
            global appRunSuccesful
            appRunSuccesful = False
         