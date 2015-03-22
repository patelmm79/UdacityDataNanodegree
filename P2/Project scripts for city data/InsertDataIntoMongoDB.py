import pymongo
import json
from pprint import pprint
from pymongo import Connection
# this file opens the JSON file and inserts the data into local MongoDB

json_file="bogota_colombia.osm.json"

def get_db(db_name):
    # For local use
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')  #local Mongo DB instance
    db = client[db_name]
    return db

db=get_db('Bogota') #set database name
with open (json_file,"rb") as jsonfile:
    
    data = json.load(jsonfile)
    
    streetdata=db.streetdata  
     
    for line in data:
         
         streetdata.insert(line)  #insert data into collection "streetdata"


