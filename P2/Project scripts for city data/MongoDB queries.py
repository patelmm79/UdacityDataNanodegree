import pymongo
import json
from pprint import pprint
from pymongo import Connection
from pymongo import MongoClient
# This file contains the queries to analyze Bogota data in MongoDB

def get_db(db_name):
    # For local use
    from pymongo import MongoClient
    client = MongoClient('localhost:27017')
    db = client[db_name]
    return db

db=get_db('Bogota')

client = MongoClient('localhost:27017')
db=client.Bogota

print "Number of documents:",db.streetdata.find().count()
print "Number of nodes:",db.streetdata.find({"type":"node"}).count()
print "Number of ways:",db.streetdata.find({"type":"way"}).count()

print "Number of users appearing once:",db.streetdata.aggregate([{"$group":{"_id":"$created.user", "count":{"$sum":1}}},
    {"$group":{"_id":"$count", "num_users":{"$sum":1}}}, {"$sort":{"_id":1}}, {"$limit":1}])
print "Top contributing user:",db.streetdata.aggregate([{"$group":{"_id":"$created.user", "count":{"$sum":1}}},{"$sort":{"count":-1}}, {"$limit":1}])

print "Top number amenities:",db.streetdata.aggregate([{"$match":{"amenity":{"$exists":1}}}, {"$group":{"_id":"$amenity",
"count":{"$sum":1}}}, {"$sort":{"count":-1}}, {"$limit":20}])


print "Amenities with cuisine:",  db.streetdata.aggregate([{"$match":{"cuisine":{"$exists":1}}},
{"$group":{"_id":"$amenity", "count":{"$sum":1}}}, {"$sort":{"count":-1}}, {"$limit":20}])

print "Restaurants by cuisine:",  db.streetdata.aggregate([{"$match":{"cuisine":{"$exists":1}, "amenity":"restaurant"}},
{"$group":{"_id":"$cuisine", "count":{"$sum":1}}},{"$sort":{"count":-1}}, {"$limit":20}])

print "Fast food cuisine:",       db.streetdata.aggregate([{"$match":{"cuisine":{"$exists":1},"amenity":"fast_food"}},
{"$group":{"_id":"$cuisine", "count":{"$sum":1}}},{"$sort":{"count":-1}}, {"$limit":20}])

print "Cafe by cuisine:",         db.streetdata.aggregate([{"$match":{"cuisine":{"$exists":1}, "amenity":"cafe"}},
{"$group":{"_id":"$cuisine", "count":{"$sum":1}}},{"$sort":{"count":-1}}, {"$limit":20}])

print "Restaurants without cuisine with pollo in name:",  db.streetdata.aggregate([{"$match":{"cuisine":{"$exists":0}, "amenity":"restaurant", "name":{"$regex": "[Pp]ollo"}}},
{"$group":{"_id":"$name", "count":{"$sum":1}}},{"$sort":{"count":-1}}, {"$limit":20}])

print "Fast food without cuisine with pollo in name:",  db.streetdata.aggregate([{"$match":{"cuisine":{"$exists":0}, "amenity":"fast_food", "name":{"$regex": "[Pp]ollo"}}},
{"$group":{"_id":"$name", "count":{"$sum":1}}},{"$sort":{"count":-1}}, {"$limit":20}])

print "Fast food without cuisine with hamburguesa:",  db.streetdata.aggregate([{"$match":{"cuisine":{"$exists":0}, "amenity":"fast_food", "name":{"$regex": "amburg"}}},
{"$group":{"_id":"$name", "count":{"$sum":1}}},{"$sort":{"count":-1}}, {"$limit":20}])

print "Restaurants without cuisine with pizza in name:",  db.streetdata.aggregate([{"$match":{"cuisine":{"$exists":0}, "amenity":"fast_food", "name":{"$regex": "[Pp]izza"}}},
{"$group":{"_id":"$name", "count":{"$sum":1}}},{"$sort":{"count":-1}}, {"$limit":20}])

print "Restaurants without cuisine with taco in name:",  db.streetdata.aggregate([{"$match":{"cuisine":{"$exists":0}, "amenity":"restaurant", "name":{"$regex": "[Tt]aco"}}},
{"$group":{"_id":"$name", "count":{"$sum":1}}},{"$sort":{"count":-1}}, {"$limit":20}])


print "Restaurants without cuisine:",  db.streetdata.aggregate([{"$match":{"cuisine":{"$exists":0}, "amenity":"restaurant"}},
{"$group":{"_id":"$name", "count":{"$sum":1}}},{"$sort":{"count":-1}}, {"$limit":40}])



