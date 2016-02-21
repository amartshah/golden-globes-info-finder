import pymongo
import json
from pymongo import MongoClient
import re

CLIENT = MongoClient()
DB = CLIENT.test_database

def drop_collection():
    DB.drop_collection('tweets')

def pop_collection():
    drop_collection()
    json_data = open('./gg/gg2013.json').read()
    data = json.loads(json_data)
    DB.tweets.insert(data)

def pop_collection_2k15():
    drop_collection()
    json_data = open('./gg/gg2015.json').read()
    data = json.loads(json_data)
    DB.tweets.insert(data)

def pop_for_year(year):
    if str(year) == '2013':
        pop_collection()
    else:
        pop_collection_2k15()

def tweets_i_care_about():
    DB.tweets.ensure_index([('timestamp_ms', pymongo.ASCENDING)])
    return DB.tweets.find({ 'text': { '$not': re.compile('\ART @') } }).sort('timestamp_ms',pymongo.ASCENDING)

def hello_database():
    print DB.tweets.find_one()
