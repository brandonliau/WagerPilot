# Third party imports
from pymongo import MongoClient
# Local imports
import wagerpilot.config as con

def getCollection(database: str, collection: str):
    client = MongoClient(con.mongoConnectionString)
    col = client[database][collection]
    return col

def insertDoc(database: str, collection: str, item: dict):
    client = MongoClient(con.mongoConnectionString)
    client[database][collection].insert_one(item)

def insertMany(database: str, collection: str, items: list):
    client = MongoClient(con.mongoConnectionString)
    client[database][collection].insert_many(items)

def deleteDoc(database: str, collection: str, item: dict):
    client = MongoClient(con.mongoConnectionString)
    client[database][collection].delete_one(item)

def deleteMany(database: str, collection: str, item: dict):
    client = MongoClient(con.mongoConnectionString)
    client[database][collection].delete_many(item)  
