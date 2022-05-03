#imports
import praw
import pandas as pd
import warnings
import enum

from credentials import *
from config import *
from stock_analyser.sentimalAnalysis import cleanText

#setup
warnings.filterwarnings("ignore")

#ENUMS
class redditTimeFilter(enum.Enum):
    ALL = "all"
    DAY = "day"
    HOUR = "hour"
    MONTH = "month"
    WEEK = "week"
    YEAR = "year"



"""
EXAMPLE:
api = redditAPI()
df = api.getTopSubredditTitles("stocks", redditTimeFilter.WEEK.value)
"""

class redditAPI:
  
    redditApi = None
    
    def __init__(self):
        
        self.redditApi = praw.Reddit(
            client_id = REDDIT_CLIENT_ID,
            client_secret = REDDIT_SECRET_TOKEN,
            password = REDDIT_PASSWORD,
            username = REDDIT_USERNAME,
            user_agent="USERAGENT"  
        )
    
    #Extract Subreddit Titles - Top
    def getTopSubredditTitles(self, subredditName, timeFilter):

        dfPosts = pd.DataFrame()

        subreddit = self.redditApi.subreddit(subredditName)
        for post in subreddit.top(timeFilter):
            
            dfPosts = dfPosts.append({
                'subredditName' : subreddit.display_name, 
                'subredditId' : subreddit.id , 
                'subredditType' : "Top", 
                'subredditTimeFilter' : timeFilter, 
                'postTitle' : post.title, 
                'postId' : post.id, 
                'postScore' : post.score, 
                'postNumOfComments' : post.num_comments, 
                'postCreated' : pd.to_datetime(post.created, unit="s") 
            }, ignore_index = True)
            
        return dfPosts

    #Extract Subreddit Titles - Hot
    def getHotSubredditTitles(self, subredditName, timeFilter):

        df = pd.DataFrame()

        subreddit = self.redditApi.subreddit(subredditName)
        for post in subreddit.hot():
            df = df.append({
                'subredditName' : subreddit.display_name, 
                'subredditId' : subreddit.id , 
                'subredditType' : "Hot",  
                'postTitle' : post.title, 
                'postId' : post.id, 
                'postScore' : post.score, 
                'postNumOfComments' : post.num_comments, 
                'postCreated' : pd.to_datetime(post.created, unit="s") 
            }, ignore_index = True)

        return df

    #Extract Subreddit Titles - New
    def getNewSubredditTitles(self, subredditName, timeFilter):

        df = pd.DataFrame()

        subreddit = self.redditApi.subreddit(subredditName)
        for post in subreddit.new():
            df = df.append({
                'subredditName' : subreddit.display_name, 
                'subredditId' : subreddit.id , 
                'subredditType' : "New",  
                'postTitle' : post.title, 
                'postId' : post.id, 
                'postScore' : post.score, 
                'postNumOfComments' : post.num_comments, 
                'postCreated' : pd.to_datetime(post.created, unit="s") 
            }, ignore_index = True)

        return df
    
    #Extract comments from post
    def getPostComments(self, postId, subredditName):
        
        df = pd.DataFrame()
        post =  self.redditApi.submission(id = postId)
        
        try:
            for comment in post.comments:
                
                if(comment.score < MIN_REDDIT_COMMENT_SCORE): #discard comments with low score
                    continue
                
                commentText = cleanText(comment.body)
                
                df = df.append({
                'subredditName' : subredditName,  
                'postTitle' : post.title, 
                'postId' : post.id, 
                'commentText' : commentText, 
                'commentScore' : comment.score, 
                'commentCreated' : pd.to_datetime(comment.created, unit="s") 
                }, ignore_index = True)
                
                
        except Exception as e: print(e)
        
        return df
    
    
    
    
    
