# Third party imports
from pymongo import MongoClient
# Local imports
import config as con

client = MongoClient(con.mongoConnectionString)

print(client.list_database_names())

db = client.test

print(db.list_collection_names())