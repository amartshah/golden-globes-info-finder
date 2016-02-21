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
        d[current_award][x.strip()] += 1
    return d

def capitalized(stri):
    return not not re.compile('\A[A-Z]').match(stri)

def is_mostly_capitalized(stri):
    R = re.compile(r'(\A|\s)[A-Z]\w')
    num_caps = len(re.findall(R, stri))
    r = re.compile(r'(\A|\s)[a-z]\w')
    num_lower = len(re.findall(r, stri))
    if num_caps > num_lower:
        return True
    else:
        return False

def trim_nom_dict(d):
    ignore_these = [',', '&amp;', 'and']
    for a, noms in d.iteritems():
        removed = 0
        for nom, count in noms.iteritems():
            if nom in ignore_these:
                noms[nom] = 0
                removed += 1
        # False negs or pos?
        if len(noms) - removed <= 4:
            continue
        for nom, count in noms.iteritems():
            if noms[nom] < 1:
                noms[nom] = 0
    return d

 # ideas
# nominees: won () over ____; wins () over ____; ___ should have won

# need to use regexes for actor/actress awards

def find_noms(year):
    current_award = None
    simple_official_awards = get_simple_official_awards()

    unverified_noms_for_current_award = []
    verified_noms = {}
    for k, v in simple_official_awards.iteritems():
        verified_noms[k] = defaultdict(lambda: 0)

    for tweet in tweets_i_care_about(year):
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
    final_dict = {}
    for k, v in verified_noms.iteritems():
        final_noms = []
        print k
        for nom, count in v.iteritems():
            if count > 0 and capitalized(nom) and is_mostly_capitalized(nom):
                print '-> -> ' + nom
                final_noms.append(nom)
        final_dict[k] = final_noms

    return final_dict


# find_noms(2015)
