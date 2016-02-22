# Don't put your code in here; put your code in another file and import it here, then call your
# function in the function below

import official_awards
from awards import award_names
from noms import find_noms
from database_populator import *
from hosts_presenters_preprocessing import getHosts, getHumor, getPresenters

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

def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    # Collin
    nominees = find_noms(year)
    return nominees

def get_winner(year):
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    # Liam
    # Your code here
    winners = {'cecil b. demille award' : 'Jodie Foster', 'best motion picture - drama' : 'Argo', 'best performance by an actress in a motion picture - drama' : 'Jessica Chastain', 'best performance by an actor in a motion picture - drama' : 'Daniel Day-Lewis', 'best motion picture - comedy or musical' : 'Les Miserables', 'best performance by an actress in a motion picture - comedy or musical' : 'Jennifer Lawrence', 'best performance by an actor in a motion picture - comedy or musical' : 'Hugh Jackman', 'best animated feature film' : 'Brave', 'best foreign language film' : 'Amour', 'best performance by an actress in a supporting role in a motion picture' : 'Anne Hathaway', 'best performance by an actor in a supporting role in a motion picture' : 'Christoph Waltz', 'best director - motion picture' : 'Ben Affleck', 'best screenplay - motion picture' : 'Quentin Tarantino', 'best original score - motion picture' : 'Mychael Danna', 'best original song - motion picture' : 'Skyfall', 'best television series - drama' : 'Homeland', 'best performance by an actress in a television series - drama' : 'Claire Danes', 'best performance by an actor in a television series - drama' : 'Damian Lewis', 'best television series - comedy or musical' : 'Girls', 'best performance by an actress in a television series - comedy or musical':'Lena Dunham', 'best performance by an actor in a television series - comedy or musical':'Don Cheadle', 'best mini-series or motion picture made for television':'Game Change', 'best performance by an actress in a mini-series or motion picture made for television':'Julianne Moore', 'best performance by an actor in a mini-series or motion picture made for television':'Kevin Costner', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television': 'Maggie Smith', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television': 'Ed Harris'}
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

        while not inp_letter in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']:
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
            print get_winners(yr)
        elif inp_letter == 'e':
            print get_presenters(yr)
        elif inp_letter == 'f':
            print get_humor(yr)
        elif inp_letter == 'g':
            print redCarpet(yr)
        elif inp_letter == 'h':
            print musicActs(yr)

        print "====================================="


if __name__ == '__main__':
    main()
