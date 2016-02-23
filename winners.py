import re
from database_populator import tweets_i_care_about
from official_awards import OFFICIAL_AWARDS
from collections import defaultdict
import collections

sim_lists = [
    ['feature film', 'film', 'motion picture', 'movie'],
    ['television', 'tv'],
    ['comedy or musical', 'musical', 'comedy'],
    ['performance by an actress in a supporting role', 'supporting actress'],
    ['performance by an actor in a supporting role', 'supporting actor'],
    ['performance by an actress', 'actress'],
    ['performance by an actor', 'actor'],
    ['best performance by an actor in a miniseries or motion picture made for television', 'best actor in a mini series', 'best actor in a tv movie', 'best actor in a television movie', 'best actor in a tv mini series'],
    ['best performance by an actress in a miniseries or motion picture made for television', 'best actress in a mini series', 'best actress in a tv movie', 'best actress in a television movie', 'best actress in a tv mini series'],
    ['best performance by an actress in a television series  comedy or musical', 'best actress in a tv comedy', 'best actress in a tv musical', 'best actress in a comedy series', 'best actress in a musical series'],
    ['best original score  motion picture', 'best score', 'best original score', 'best score in a feature film']
]

def award_name_gen(name):
    names_genned = []
    names_genned.append(name)
    name = name.lower()
    for sims in sim_lists:
        for word in sims:
            if word in name:
                for sub in sims:
                    if sub == word:
                        continue
                    names_genned.append(name.replace(word, sub))
                break
    #print names_genned
    return names_genned

def remove_punc(st):
    not_punct_re = re.compile('\w|\s')
    return ''.join([ch for ch in st if not_punct_re.match(ch)])

def get_simple_official_awards():
    return {a: remove_punc(a.lower()) for a in OFFICIAL_AWARDS}

def add_count_to_dict(arr, d, current_award):
    for x in arr:
        d[current_award][x.strip()] += 1
    return d


def filter_false_positive(unfiltered_matches):
    filtered_matches = []
    black_list = ["an","on","in","the","a", "and"] #etc
    for match in unfiltered_matches:
        if match.lower() not in black_list:
            filtered_matches.append(match)
    return filtered_matches

def find_winners(year):
    current_award = None
    simple_official_awards = get_simple_official_awards()
    unverified_wins_current = []
    verified_wins = {}
    for k, v in simple_official_awards.iteritems():
        verified_wins[k] = defaultdict(lambda: 0)

    for tweet in tweets_i_care_about(year):
        autoverified = False
        lc_tw = tweet['text'].lower()
        puncless_tw = remove_punc(lc_tw)


        if current_award and simple_official_awards[current_award] in puncless_tw:
             verified_wins = add_count_to_dict(unverified_wins_current, verified_wins, current_award)
             unverified_wins_current = []
             autoverified = True
        else:
            for (real, simple) in simple_official_awards.iteritems():
                #print simple
                for x in award_name_gen(simple): 
                    if x in puncless_tw:
                        #print x
                        current_award = real
                        verified_wins = add_count_to_dict(unverified_wins_current, verified_wins, current_award)                       
                        #print current_award
                        autoverified = True
                        unverified_wins_current = []
        if 'wins' not in lc_tw and 'won' not in lc_tw and 'goes to' not in lc_tw or 'http' in lc_tw:
            #print "no"
            continue

        presenter_regex = re.compile(r'(@\w*|[A-Z]\w*\s[A-Z]\w*)\s(present|introduce)')
        tw_without_presenters = re.sub(presenter_regex, ' ', tweet['text'])

        if 'goes to' in lc_tw or 'wins' in lc_tw or 'won' in lc_tw:
            #print current_award
            if 'wins' in lc_tw:
                #print "yes"
                winner_text = re.compile(r'wins', re.IGNORECASE).split(tw_without_presenters)[0]
                winner_text = winner_text.encode('ascii', 'ignore')
                winner_text = re.sub(re.compile(r'#\w*'),'', winner_text)
           
            if 'won' in lc_tw:
                #print "yes"
                winner_text = re.compile(r'won', re.IGNORECASE).split(tw_without_presenters)[0]
                winner_text = winner_text.encode('ascii', 'ignore')
                winner_text = re.sub(re.compile(r'#\w*'),'', winner_text)
             #   print winner_text
            if 'goes to' in lc_tw:
                winner_text = re.compile(r'goes to', re.IGNORECASE).split(tw_without_presenters)[-1]
                winner_text = re.compile(r'for', re.IGNORECASE).split(winner_text)[0]
                winner_text = winner_text.encode('ascii', 'ignore')
                winner_text = re.sub(re.compile(r'#\w*'),'', winner_text)
             #   print winner_text
            # if 'winner' in lc_tw:
            #     #winner_text = re.compile(r'winner', re.IGNORECASE).split(tw_without_presenters)[-1]
            #     winner_text = tw_without_presenters.encode('ascii', 'ignore')
            #     winner_text = re.sub(re.compile(r'#\w*'),'', winner_text)
            prop = re.compile(r'([A-Z]{1}[a-z]{1,}(\s[A-Z]{1}[a-z]{1,})?)')
            matches = prop.findall(winner_text)
            #print matches, current_award
            matches = [i[0] for i in matches]
            matches = filter_false_positive(matches)
            #if autoverified:
            #if autoverified:
            #print current_award, matches
            wins = list(matches)
            #print "matches:", wins, current_award
            unverified_wins_current += wins
            #print wins
            #print wins
            if autoverified:   
                verified_wins = add_count_to_dict(unverified_wins_current, verified_wins, current_award)
                unverified_wins_current = []

    #verified_wins = trim_nom_dict(verified_wins)
    #print verified_wins
    final_dict = {}
    for k, v in verified_wins.iteritems():
        #print k
        highWin=''
        highCount= 0
        for win, count in v.iteritems():
            if count > highCount and win != '':
                highCount = count
            	highWin = win
        final_dict[k] = highWin
    return final_dict


# find_noms(2015)