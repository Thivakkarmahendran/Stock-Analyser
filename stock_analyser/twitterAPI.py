import string
from xmlrpc.client import boolean
import tweepy 
from credentials import *
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
        self.twitterApi.update_status(status = text)
        
    def postTweetWithImage(self, text: string, imagePath: string):
        self.twitterApi.update_with_media(imagePath, imagePath)
         