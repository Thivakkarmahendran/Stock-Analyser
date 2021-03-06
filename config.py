
#config
REDDIT_SUBREDDITS = ["stocks", "StockMarket", "wallstreetbets", "investing", "robinhood"]
DATA_REFRESH = 432000 #in seconds (5 days)


MIN_REDDIT_COMMENT_SCORE = 10
TOP_NUMBER_OF_STOCKS = 5
LOGGER_DEBUG = False
FORCE_RUN = False
FRESH_RUN = False
POST_TWEET = True



STOCK_BLACKLIST = {'I', 'ARE',  'ON', 'GO', 'NOW', 'CAN', 'UK', 'SO', 'OR', 'OUT', 'SEE', 'ONE', 'LOVE', 'U', 'STAY', 'HAS', 'BY', 'BIG', 'GOOD', 'RIDE', 'EOD', 'ELON', 'WSB', 'THE', 'A', 'ROPE', 'YOLO', 'TOS', 'CEO', 'DD', 'IT', 'OPEN', 'ATH', 'PM', 'IRS', 'FOR','DEC', 'BE', 'IMO', 'ALL', 'RH', 'EV', 'TOS', 'CFO', 'CTO', 'DD', 'BTFD', 'WSB', 'OK', 'PDT', 'RH', 'KYS', 'FD', 'TYS', 'US', 'USA', 'IT', 'ATH', 'RIP', 'BMW', 'GDP', 'OTM', 'ATM', 'ITM', 'IMO', 'LOL', 'AM', 'BE', 'PR', 'PRAY', 'PT', 'FBI', 'SEC', 'GOD', 'NOT', 'POS', 'FOMO', 'TL;DR', 'EDIT', 'STILL', 'WTF', 'RAW', 'PM', 'LMAO', 'LMFAO', 'ROFL', 'EZ', 'RED', 'BEZOS', 'TICK', 'IS', 'PM', 'LPT', 'GOAT', 'FL', 'CA', 'IL', 'MACD', 'HQ', 'OP', 'PS', 'AH', 'TL', 'JAN', 'FEB', 'JUL', 'AUG', 'SEP', 'SEPT', 'OCT', 'NOV', 'FDA', 'IV', 'ER', 'IPO', 'MILF', 'BUT', 'SSN', 'FIFA', 'USD', 'CPU', 'AT', 'GG', 'Mar', 'REAL', 'ME', 'GET', 'VERY', 'ANY', 'TECH', 'NEXT', 'FUND', 'BEAT', 'EVER', 'CASH', 'GROW', 'FREE', 'HUGE', 'MOVE', 'PLAY', 'LIFE', 'ELSE', 'GAME', 'TALK', 'HOPE', 'NICE', 'CARE', 'RUN', 'WW', 'COST', 'LIVE', 'MIND', 'TURN', 'TRUE', 'CAR', 'COOL'}

# adding wsb/reddit flavour to vader to improve sentiment analysis, score: 4.0 to -4.0
CUSTOM_SENTIMENT_ANALYSIS = {
    'citron': -4.0,  
    'hidenburg': -4.0,        
    'moon': 4.0,
    'highs': 2.0,
    'mooning': 4.0,
    'long': 2.0,
    'short': -2.0,
    'call': 4.0,
    'calls': 4.0,    
    'put': -4.0,
    'puts': -4.0,    
    'break': 2.0,
    'tendie': 2.0,
    'tendies': 2.0,
    'town': 2.0,     
    'overvalued': -3.0,
    'undervalued': 3.0,
    'buy': 4.0,
    'sell': -4.0,
    'gone': -1.0,
    'gtfo': -1.7,
    'paper': -1.7,
    'bullish': 3.7,
    'bearish': -3.7,
    'bagholder': -1.7,
    'stonk': 1.9,
    'green': 1.9,
    'money': 1.2,
    'print': 2.2,
    'rocket': 2.2,
    'bull': 4.0,
    'bear': -4.0,
    'pumping': -1.0,
    'sus': -3.0,
    'offering': -2.3,
    'rip': -4.0,
    'downgrade': -3.0,
    'upgrade': 3.0,     
    'maintain': 1.0,          
    'pump': 1.9,
    'hot': 1.5,
    'drop': -2.5,
    'rebound': 1.5,  
    'crack': 2.5,
    'gang': 2.0,
    'scam': -2.0,
    'chamath': -2.0,
    'snake': -2.0,
    'squezze': 3.0,
    'bag': -4.0,
    'fly': 2.0,     
    'way': 2.0,     
    'high': 2.0,
    'volume': 2.5,
    'low': -2.0,
    'trending': 3.0,
    'upwards': 3.0,
    'prediction': 1.0,     
    'cult': -1.0,     
    'big': 2.0
    }