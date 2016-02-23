from database_populator import tweets_i_care_about
import re
import string
import collections

AWARDS_THRESH = 3


def delete_duplicate_names(awards):
    awards = sorted(awards, key=lambda tup: tup[1])
    final_awards = []
    # there can't be more than one award that contains the words from all the same sets
    similars_lists = [
        ['tv', 'series'],
        ['musical or comedy', 'musical', 'comedy']
    ]
    # unless there are differences in presence or absence of these words
    differentiators = [
        'actress',
        'supporting',
        'drama',
        'director',
        'score',
        'song'
    ]

    for award, count in awards:
        descriptors_vec = []
        for slist in similars_lists:
            has = False
            for s in slist:
                if s in award:
                    descriptors_vec.append(1)
                    has = True
                    break
            if not has:
                descriptors_vec.append(0)

        for d in differentiators:
            if d in award:
                descriptors_vec.append(1)
            else:
                descriptors_vec.append(0)

        similar_already_in = False
        for added_award, added_award_descriptor in final_awards:
            if descriptors_vec == added_award_descriptor:
                similar_already_in = True
                break
        if not similar_already_in:
            final_awards.append((award, descriptors_vec))

    return [a for a, d in final_awards]

def award_names(year):
    best_re = re.compile('best ', re.IGNORECASE)
    trans_words = re.compile('\s(at|for|dressed|award|and|i\s|golden|http)', re.IGNORECASE)

    awards = []
    for tweet in tweets_i_care_about(year):
        tweet_text = tweet['text'].encode('ascii', 'ignore')
        tweet_pieces = re.compile('[^\s\w-]').split(tweet_text.replace('#',''))
        award_tweets = [x.lower() for x in tweet_pieces if 'wins best' in x or 'won best' in x]
        for award_piece in award_tweets:
            award_name = 'best ' + best_re.split(award_piece)[-1].rstrip()
            awards.append(trans_words.split(award_name)[0].encode('ascii', 'ignore'))

    thresh = max(AWARDS_THRESH, len(awards)/400)

    fake_awards = ['best', 'best dressed', 'best speech', 'best act', 'best actor', 'best actress']
    awardCounter = collections.Counter(awards).iteritems()
    ret = [[k,v] for k, v in awardCounter if v > thresh and k not in fake_awards]
    # ret = delete_duplicate_names(ret)
    ret = [k for k, v in ret.iteritems()]
    return ret
