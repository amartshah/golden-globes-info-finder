import json
import nltk
import operator
import sys
import re

filename = sys.argv[-1]
dress_keywords = ["wearing", "gorgeous", "lovely", "stunning", "beautiful"]
music_keywords = ["rocking", "performing", "playing", "jamming"]
punctuation_stopwords = [".", '"', ",", "?", "!", "/", "'", "-", "_", ";", ":", "&", ',"', '",', ")", "(", "Golden", "Globes", "@", "GoldenGlobes", "I", "we", "http", "://", "/", "co", "The", "She"]
stopwords = nltk.corpus.stopwords.words('english') + punctuation_stopwords

def loadParsedTweets(filename):
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



# mycomp version
def lookthroughTweets(keywords, year):
    if str(year) == '2015':
        filename = 'gg2015.json'
    else:
        filename = 'gg2013.json'
    parsedTweets = loadParsedTweets(filename)
    fTweets = [tweet for tweet in parsedTweets if any(x in tweet for x in keywords)]
    #print fTweets
    return fTweets



### github version
##def lookthroughTweets(keywords, year):
##    if str(year) == '2015':
##        filename = 'gg/gg2015.json'
##    else:
##        filename = 'gg/gg2013.json'
##    parsedTweets = loadParsedTweets(filename)
##    fTweets = [tweet for tweet in parsedTweets if any(x in tweet for x in keywords)]
##    #print fTweets
##    return fTweets



def makeWords(tweets,stopwords):
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

def makeNames(tweets,stopwords):
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


def getNames(worddict,namedict,num):
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
    #print finalnames
    return finalnames.keys()


def redCarpet(year):
    hostTweets = lookthroughTweets(dress_keywords, year)
    wordDict = makeWords(hostTweets, stopwords)
    nameList = makeNames(hostTweets, stopwords)
    RC = getNames(wordDict, nameList, 1)

    output = []
    for rc in RC:
        h_final = rc.encode("utf-8")
        output.append(h_final)
    RC = output
    print RC
    return RC

def musicActs(year):
    musicTweets = lookthroughTweets(music_keywords, year)
    wordDict = makeWords(musicTweets, stopwords)
    nameList = makeNames(musicTweets, stopwords)
    music = getNames(wordDict, nameList, 1)

    output = []
    for m in music:
        h_final = m.encode("utf-8")
        output.append(h_final)
    music = output
    print music
    return music


redCarpet("2013")
musicActs("2013")

