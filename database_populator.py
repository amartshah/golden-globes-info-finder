import pymongo
import json
from pymongo import MongoClient
import re

CLIENT = MongoClient()
DB = CLIENT.test_database

def pop_collection_2k13():
    DB.drop_collection('tweets2k13')
    json_data = open('gg2013.json').read()
    data = json.loads(json_data)
    DB.tweets2k13.insert(data)

def pop_collection_2k15():
    DB.drop_collection('tweets2k15')
    json_data = open('gg2015.json').read()
    data = json.loads(json_data)
    DB.tweets2k15.insert(data)

def pop_if_not_populated():
    if DB.tweets2k15.count() < 100:
        pop_collection_2k15()
    if DB.tweets2k13.count() < 100:
        pop_collection_2k13()

def tweets_i_care_about(year):
    if str(year) == '2013':
        DB.tweets2k13.ensure_index([('timestamp_ms', pymongo.ASCENDING)])
        return DB.tweets2k13.find({ 'text': { '$not': re.compile('\ART @') } }).sort('timestamp_ms',pymongo.ASCENDING)
    else:
        DB.tweets2k15.ensure_index([('timestamp_ms', pymongo.ASCENDING)])
        return DB.tweets2k15.find({ 'text': { '$not': re.compile('\ART @') } }).sort('timestamp_ms',pymongo.ASCENDING)
