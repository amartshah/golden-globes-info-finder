import re
from database_populator import tweets_i_care_about
from official_awards import OFFICIAL_AWARDS
from collections import defaultdict
import collections


def remove_punc(st):
    not_punct_re = re.compile('\w|\s')
    return ''.join([ch for ch in st if not_punct_re.match(ch)])

def get_simple_official_awards():
    return {a: remove_punc(a.lower()) for a in OFFICIAL_AWARDS}

def add_count_to_dict(arr, d, current_award):
    for x in arr:
        if d[current_award].get(x.strip()) is not None:
            d[current_award][x.strip()] += 1
        else:
            d[current_award][x.strip()] = 1
    return d

def capitalized(stri):
    return not not re.compile('\A[A-Z]').match(stri.strip())

def is_mostly_capitalized(stri):
    stri = stri.strip()
    R = re.compile(r'(\A|\s)[A-Z]\w')
    num_caps = len(re.findall(R, stri))
    r = re.compile(r'(\A|\s)[a-z]\w')
    num_lower = len(re.findall(r, stri))
    if num_caps > num_lower:
        return True
    else:
        return False

def trim_nom_dict(d):
    ignore_these = [',', '&amp;', 'and', '']
    new_dict = {}
    for award, noms in d.iteritems():
        # new_dict[award] = [x.strip().encode('ascii', 'ignore') for x, count in noms.iteritems()]
        new_dict[award] = [x.strip() for x, count in noms.iteritems() if x.strip() not in ignore_these and count > 0 and capitalized(x) and is_mostly_capitalized(x)]
    return new_dict

# ideas
# nominees: won () over ____; wins () over ____; ___ should have won
# need to use regexes for actor/actress awards

def find_noms(year):
    current_award = None
    simple_official_awards = get_simple_official_awards()

    unverified_noms_for_current_award = []
    verified_noms = {}
    for k, v in simple_official_awards.iteritems():
        verified_noms[k] = {}

    for tweet in tweets_i_care_about(year):
        # code to associate with a specific award ###################
        autoverified = False
        tweet_text = tweet['text'].encode('ascii', 'ignore')
        lc_tw = tweet_text.lower()
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
        ##############################################################

        if 'http' in lc_tw:
            continue


        # salty people ###############################################
        # re.compile('i wish\s (had)?won)
        # if 'was better than ' + winner ....

        # shoulda_regex = re.compile('should have won', re.IGNORECASE)
        # if re.search(shoulda_regex, lc_tw):
        #     subject_clause = shoulda_regex.split(tweet_text)[0]
        #     proper_noun_regex = re.compile('(([A-Z)]\w*\s?)+(\w*\s?)*)+\Z')
        #     print '.'
        #     mtch = re.search(proper_noun_regex, subject_clause)
        #     print '.'

        #     if not mtch:
        #         unverified_noms_for_current_award.append(mtch.group(1))
        #         print mtch.group(1)

        # nominees lists ##############################################
        # method using lists after 'nominees'

        presenter_regex = re.compile(r'(@\w*|[A-Z]\w*\s[A-Z]\w*)\s(present|introduce)s?')
        tw_without_presenters = re.sub(presenter_regex, '', tweet_text)
        noms_regex = re.compile(r'(nominees:\s)|(nominees are\s)', re.IGNORECASE)
        if re.search(noms_regex, tw_without_presenters):
            nominees_text = noms_regex.split(tw_without_presenters)[-1]
            nominees_text = re.sub(re.compile(r'#\w*'),'', nominees_text)
            nominees_text = nominees_text.split('.')[0]
            noms = list(set(re.compile('(\s&amp;\s|\sand\s|,\s|\n)').split(nominees_text)))
            unverified_noms_for_current_award += noms

        # add if autoverified #########################################

        if autoverified:
            verified_noms = add_count_to_dict(unverified_noms_for_current_award, verified_noms, current_award)
            unverified_noms_for_current_award = []

    # post processing #################################################
    verified_noms = trim_nom_dict(verified_noms)
    for award, noms in verified_noms.iteritems():
        print award
        for nom in noms:
            print '-> -> ' + nom

    return verified_noms
