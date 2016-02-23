# Don't put your code in here; put your code in another file and import it here, then call your
# function in the function below

import official_awards
from awards import award_names
from noms import find_noms
from winners import find_winners
from database_populator import *
from hosts_presenters_preprocessing import getHosts, getHumor, getPresenters
from funtasks import *

def get_hosts(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
    # Amar
    hosts = getHosts(year)
    return hosts

def get_awards(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    # Collin
    awards = award_names(year)
    return awards


def get_humor(year):
    return getHumor(year)

def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    # Collin
    nominees = find_noms(year)
    for award, winner in get_winner(year).iteritems():
        if winner not in nominees[award]:
            nominees[award].append(winner)
    return nominees

def get_winner(year):
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    # Liam
    # Your code here
    winners = find_winners(year)
    return winners

def get_presenters(year):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    # Amar
    presenters = getPresenters(year)
    return presenters

def get_humor(year):
    return getHumor(year)

def pre_ceremony():
    '''This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    Do NOT change the name of this function or what it returns.'''
    # Databse populator, etc.
    # Add in stuff that should be here as needed
    print "Populating database..."
    pop_if_not_populated()
    # pop_collection_2k13()
    # pop_collection_2k15()
    print "Pre-ceremony processing complete."
    return

def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    pre_ceremony() 

    while True:
        yr = None
        inp_letter = None

        while not (yr == '2015' or yr == '2013'):
            if yr != None:
                print "The year you entered was not understood - "
            print "From which year do you want info?"
            yr = raw_input('Year: ')

        while not inp_letter in ['a', 'b', 'c', 'd', 'e', 'f']:
            if inp_letter != None:
                print "The character you entered was not understood - "
            print "What information do you want? (enter letter)"
            print "a) hosts\nb) awards\nc) nominees\nd) winners\ne) presenters \nf) funny people\n"
            inp_letter = raw_input('Letter: ')

        print "\nWorking...\n"

        if inp_letter == 'a':
            print get_hosts(yr)
        elif inp_letter == 'b':
            print get_awards(yr)
        elif inp_letter == 'c':
            print get_nominees(yr)
        elif inp_letter == 'd':
            print get_winner(yr)
        elif inp_letter == 'e':
            print get_presenters(yr)
        elif inp_letter == 'f':
            print get_humor(yr)

        print "====================================="


if __name__ == '__main__':
    main()