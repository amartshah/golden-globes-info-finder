import nltk
from nltk.tokenize import RegexpTokenizer
from database_populator import DB
import re
from official_awards import OFFICIAL_AWARDS
import string
import collections

AWARDS_THRESH = 3

# ideas
# nominees: won () over ____; wins () over ____; ___ should have won


def tweets_i_care_about():
    return DB.tweets.find({ 'text': { '$not': re.compile('\ART @') } })

def remove_punc(st):
    not_punct_re = re.compile('\w|\s')
    return ''.join([ch for ch in st if not_punct_re.match(ch)])

def find_noms():
    for tweet in tweets_i_care_about():
        lc_tw = tweet['text'].lower()
        if 'nominees' not in lc_tw or 'congrat' in lc_tw:
            continue

        for award in OFFICIAL_AWARDS:
            award_parts = award.split('-')
            all_parts_match = True
            for award_part in award_parts:
                if remove_punc(award_part.strip()).lower() not in remove_punc(lc_tw):
                    all_parts_match = False
                    break

            if not all_parts_match:
                continue

            print tweet['text']
            # if remove_punc(award).lower() in remove_punc(tweet['text'].lower():

find_noms()


def award_names():
    best_re = re.compile('best ', re.IGNORECASE)
    trans_words = re.compile('\s(at|for|dressed|award|and|i\s|golden|http)', re.IGNORECASE)

    awards = []
    for tweet in tweets_i_care_about():
        tweet_pieces = re.compile('[^\s\w-]').split(tweet['text'].replace('#',''))
        award_tweets = [x.lower() for x in tweet_pieces if 'wins best' in x or 'won best' in x]
        for award_piece in award_tweets:
            award_name = 'best ' + best_re.split(award_piece)[-1].rstrip()
            awards.append(trans_words.split(award_name)[0])

    thresh = max(AWARDS_THRESH, len(awards)/400)
    print [[k,v] for k, v in collections.Counter(awards).iteritems() if v >= thresh and k != 'best']

# award_names()
