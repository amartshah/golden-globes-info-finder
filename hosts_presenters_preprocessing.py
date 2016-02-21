import json
import nltk
import operator
import sys
import re

#amar shah
host_keywords = ["host", "hosting", "hosts", "hosted"]
presenters_keywords = ["presenting", "presenters", "Presenters", "Presenting"]
#accounts for other words as well
punctuation_stopword = [".", '"', ",", "?", "!", "/", "'", "-", "_", ";", ":", "&", ',"', '",', ")", "(", "Golden", "Globes", "@", "GoldenGlobes", "I", "we", "http", "://", "/", "co", "Hollywood", "Hooray"]
stopwords = nltk.corpus.stopwords.words('english') + punctuation_stopword
humor_keywords = ["hilarious", "funny", "comedian", "best joke", "hysterical"]

winners = {'cecil b. demille award' : 'Jodie Foster', 'best motion picture - drama' : 'Argo', 'best performance by an actress in a motion picture - drama' : 'Jessica Chastain', 'best performance by an actor in a motion picture - drama' : 'Daniel Day-Lewis', 'best motion picture - comedy or musical' : 'Les Miserables', 'best performance by an actress in a motion picture - comedy or musical' : 'Jennifer Lawrence', 'best performance by an actor in a motion picture - comedy or musical' : 'Hugh Jackman', 'best animated feature film' : 'Brave', 'best foreign language film' : 'Amour', 'best performance by an actress in a supporting role in a motion picture' : 'Anne Hathaway', 'best performance by an actor in a supporting role in a motion picture' : 'Christoph Waltz', 'best director - motion picture' : 'Ben Affleck', 'best screenplay - motion picture' : 'Quentin Tarantino', 'best original score - motion picture' : 'Mychael Danna', 'best original song - motion picture' : 'Skyfall', 'best television series - drama' : 'Homeland', 'best performance by an actress in a television series - drama' : 'Claire Danes', 'best performance by an actor in a television series - drama' : 'Damian Lewis', 'best television series - comedy or musical' : 'Girls', 'best performance by an actress in a television series - comedy or musical':'Lena Dunham', 'best performance by an actor in a television series - comedy or musical':'Don Cheadle', 'best mini-series or motion picture made for television':'Game Change', 'best performance by an actress in a mini-series or motion picture made for television':'Julianne Moore', 'best performance by an actor in a mini-series or motion picture made for television':'Kevin Costner', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television': 'Maggie Smith', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television': 'Ed Harris'}

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


def lookthroughTweets(keywords, year):
    if str(year) == '2015':
        filename = 'gg2015.json'
    else:
        filename = 'gg2013.json'
    parsedTweets = loadParsedTweets(filename)
    fTweets = [tweet for tweet in parsedTweets if any(x in tweet for x in keywords)]
    #print fTweets
    return fTweets

def lookthroughTweets2(presentersTweets,test1):
    fTweets = [tweet for tweet in presentersTweets if any(x in tweet for x in test1)]
    #print fTweets
    return fTweets

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
    #print finalnames
    return finalnames.keys()

def getHosts(year):
    hostTweets = lookthroughTweets(host_keywords, year)
    wordDict = CreateWords(hostTweets, stopwords)
    nameList = CreateNames(hostTweets, stopwords)
    hosts = ObtainNames(wordDict, nameList, 1)

    output = []
    for host in hosts:
        h_final = host.encode("utf-8") 
        output.append(h_final)
    hosts = output
    print hosts
    return hosts

def getHumor(year):
    humorTweets = lookthroughTweets(humor_keywords, year)
    wordDict = CreateWords(humorTweets, stopwords)
    nameList = CreateNames(humorTweets, stopwords)
    comedians = ObtainNames(wordDict, nameList, 1)
    output = []
    for comedian in comedians:
        c_final = comedian.encode("utf-8") 
        output.append(c_final)
    comedians = output
    #comedians.replace("Show ", "")
    print comedians[0]
    return comedians

def getPresenters(year):
    presenters = dict()
    presentersTweets = lookthroughTweets(presenters_keywords, year)
    for w in winners:
        test = []
        #presenters_keywords.append(winners[w])
        #presentersTweets = lookthroughTweets(presenters_keywords)
        test = winners[w].split()
        #print test 
        specificTweets = lookthroughTweets2(presentersTweets, test)
        #print specificTweets
        for t in test:
            stopwords.append(t)
        #print stopwords
        wordDict = CreateWords(specificTweets, stopwords)
        nameList = CreateNames(specificTweets, stopwords)
        presentersper = ObtainNames(wordDict, nameList, 4)
        output = []
        for presenter in presentersper:
            presenters_final = presenter.encode("utf-8") 
            output.append(presenters_final)
            presentersper = output
        presentersper = output
        presenters[w] = presentersper
        #print presentersper
        #presenters.key() = winners.key()
        pop_amount = len(test)
        for x in range(0, pop_amount):
            stopwords.pop()
    print presenters
    return presenters






#getHosts("2013")
#getPresenters("2013")
#getHumor("2013")


if __name__ == '__main__':
    main()