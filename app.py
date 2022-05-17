#imports
import time

from stock_analyser.redditAnalysis import runRedditAnalysis

startTime = time.time()    

def main():
    
    print("***** Starting Stock Analyser ***** \n")
    
    #Analysis Reddit 
    runRedditAnalysis()
    
    print("***** Completed Stock Analyser in {} seconds ***** \n".format(time.time()-startTime))
    


if __name__ == '__main__':
    main()
    