import json
import nltk
import operator
import sys
import re

filename = sys.argv[-1]
OFFICIAL_AWARDS = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
host_keywords = ["host", "hosting", "hosts", "hosted"]
presenters_keywords = ["presenting", "giving", "presenters", "Presenters", "Presenting"]
potential_hosts = []
#accounts for other words as well
punctuation_stopword = [".", '"', ",", "?", "!", "/", "'", "-", "_", ";", ":", "&", ',"', '",', ")", "(", "Golden", "Globes", "@", "GoldenGlobes", "I", "we", "http", "://", "/", "co"]
stopwords = nltk.corpus.stopwords.words('english') + punctuation_stopword


def loadParsedTweets(filename):
    stupidwords = [];
    """
    Takes a json file name and extracts a list of tweets. The tweets are then
    tokenized and a list of parsed tweets is returned.
    """
    try:
        with open(filename) as fl:
            jsonObj = json.load(fl)
            tweets = [tweet["text"] for tweet in jsonObj]
    except (MemoryError, ValueError):
        with open(filename) as fl:
            tweets = [json.loads(line)["text"] for line in fl]
    parsedTweets = [nltk.wordpunct_tokenize(tweet) for tweet in tweets]    
    for tweet in parsedTweets:
        for token in tweet:
            if token in stopwords:
                tweet.remove(token)
    return parsedTweets


def lookthroughTweets(host_keywords,stopwords):
    parsedTweets = loadParsedTweets(filename)
    fTweets = [tweet for tweet in parsedTweets if any(x in tweet for x in host_keywords)]
    #print fTweets
    return fTweets


# def buildnamelist():
#     tweets = lookthroughTweets(host_keywords,stopwords)
#     namelist = []
#     for tweet in tweets:
#         tweetnames = re.findall('([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)'," ".join(tweet))
#         for name in tweetnames:
#             if name not in namelist:
#                 namelist.append(name)
#     return namelist

def CreateWords(tweets,stopwords):
    dictofwords = dict()
    for tweet in tweets:
        for word in tweet:
            if word[0].isupper():
                if word not in stopwords:
                    if word not in dictofwords:
                        dictofwords[word] = 0
                    dictofwords[word] += 1
    #print dictofwords
    return dictofwords

def CreateNames(tweets,stopwords):
    RegexNames = dict()
    for tweet in tweets:
        tweetnames = re.findall('([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)'," ".join(tweet))
        for name in tweetnames:
            if name not in stopwords:
                if name not in RegexNames:
                    RegexNames[name] = 0
                RegexNames[name] += 1
    #print RegexNames
    return RegexNames

def ObtainNames(worddict,namedict,num):
    finalnames = dict()
    twords = worddict.copy()
    tnames = namedict.copy()
    for i in range(num):
        dispName = ""
        counter = -1
        for word in sorted(twords, key=twords.get, reverse=True):
            for name in sorted(tnames, key=tnames.get, reverse=True):
                if word in name:
                    if tnames[name] + twords[word] > counter:
                        counter = tnames[name] + twords[word]
                        dispName = name
        finalnames[dispName] = counter
    return finalnames.keys()

def getHosts():
    hostTweets = lookthroughTweets(host_keywords,stopwords)
    wordDict = CreateWords(hostTweets, stopwords)
    nameList = CreateNames(hostTweets, stopwords)
    hosts = ObtainNames(wordDict, nameList, 1)
    return hosts

def getPresenters(tweets, noms, category):
    badwordsperaward = stopwords + noms + category    
    presentersTweets = lookthroughTweets1(presenters_keywords,stopwords)
    wordDict = CreateWords(presentersTweets, stopwords)
    nameList = CreateNames(presentersTweets, stopwordsperaward)
    presenters = ObtainNames(wordDict, nameList, 2)
    return presenters

def lookthroughTweets1(presenters_keywords,stopwords):
    parsedTweets = loadParsedTweets(filename)
    fTweets = [tweet for tweet in parsedTweets if any(x in tweet for x in presenters_keywords)]
    #print fTweets
    return fTweets


def get_hosts(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here


    return hosts

def get_awards(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    # Your code here
    return awards

def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    # Your code here
    return nominees

def get_winner(year):
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    return winners

def get_presenters(year):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    # Your code here
    return presenters

def pre_ceremony():
    '''This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    print "Pre-ceremony processing complete."
    return

def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    # Your code here
    return

if __name__ == '__main__':
    main()