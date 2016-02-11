import pymongo
import json
from pymongo import MongoClient


CLIENT = MongoClient()
DB = CLIENT.test_database

def drop_collection():
    DB.drop_collection('tweets')

def pop_collection():
    drop_collection()
    json_data = open('./gg/gg2013.json').read()
    data = json.loads(json_data)
    DB.tweets.insert(data)

def hello_database():
    print DB.tweets.find_one()
