import nltk
from nltk.tokenize import RegexpTokenizer
from database_populator import DB
import re
from official_awards import OFFICIAL_AWARDS
import string
import collections
from collections import defaultdict
import pymongo

AWARDS_THRESH = 3

# ideas
# nominees: won () over ____; wins () over ____; ___ should have won

def tweets_i_care_about():
    DB.tweets.ensure_index([('timestamp_ms', pymongo.ASCENDING)])
    return DB.tweets.find({ 'text': { '$not': re.compile('\ART @') } }).sort('timestamp_ms',pymongo.ASCENDING)

def remove_punc(st):
    not_punct_re = re.compile('\w|\s')
    return ''.join([ch for ch in st if not_punct_re.match(ch)])

def get_simple_official_awards():
    return {a: remove_punc(a.lower()) for a in OFFICIAL_AWARDS}

def add_count_to_dict(arr, d, current_award):
    for x in arr:
        d[current_award][x.strip()] += 1
    return d

def capitalized(str):
    return not not re.compile('\A[A-Z]').match(str)

def trim_nom_dict(d):
    ignore_these = [',', '&amp;', 'and']
    for a, noms in d.iteritems():
        removed = 0
        for nom, count in noms.iteritems():
            if nom in ignore_these:
                noms[nom] = 0
                removed += 1
        ## False negs or pos?
        # if len(noms) - removed <= 4:
        #     continue
        # for nom, count in noms.iteritems():
        #     if noms[nom] < 1:
        #         noms[nom] = 0
    return d

def find_noms():
    current_award = None
    simple_official_awards = get_simple_official_awards()

    unverified_noms_for_current_award = []
    verified_noms = defaultdict(lambda: defaultdict(lambda: 0))

    for tweet in tweets_i_care_about():
        autoverified = False
        lc_tw = tweet['text'].lower()
        puncless_tw = remove_punc(lc_tw)

        if current_award and simple_official_awards[current_award] in puncless_tw:
            verified_noms = add_count_to_dict(unverified_noms_for_current_award, verified_noms, current_award)
            unverified_noms_for_current_award = []
            autoverified = True
        else:
            for (real, simple) in simple_official_awards.iteritems():
                if simple in puncless_tw:
                    current_award = real
                    autoverified = True
                    unverified_noms_for_current_award = []
                    break

        if 'nominee' not in lc_tw or 'http' in lc_tw:
            continue

        presenter_regex = re.compile(r'(@\w*|[A-Z]\w*\s[A-Z]\w*)\s(present|introduce)')
        tw_without_presenters = re.sub(presenter_regex, ' ', tweet['text'])

        if 'nominees:' in lc_tw:
            nominees_text = re.compile(r'nominees:', re.IGNORECASE).split(tw_without_presenters)[-1]
            nominees_text = re.sub(re.compile(r'#\w*'),'', nominees_text)
            nominees_text = nominees_text.split('.')[0]
            noms = list(set(re.compile('(\s&amp;\s|\sand\s|,\s|\n)').split(nominees_text)))
            unverified_noms_for_current_award += noms
            if autoverified:
                verified_noms = add_count_to_dict(unverified_noms_for_current_award, verified_noms, current_award)
                unverified_noms_for_current_award = []

    verified_noms = trim_nom_dict(verified_noms)
    for k, v in verified_noms.iteritems():
        print k
        for nom, count in v.iteritems():
            if count > 0 and capitalized(nom):
                print '-> -> ' + nom


def award_names():
    # use timestamps
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
    fake_awards = ['best', 'best dressed', 'best speech', 'best act']
    awardCounter = collections.Counter(awards).iteritems()
    print [[k,v] for k, v in awardCounter if v >= thresh and k not in fake_awards]



# award_names()
find_noms()
