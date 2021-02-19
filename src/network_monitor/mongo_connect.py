from pymongo import MongoClient

client = MongoClient("mongodb://hackerteam9:scanwire24x7@localhost:27017")
db = client['wirescope']


def save_interaction(interaction):
    db.interactions.insert_one(interaction)


def update_interaction(identifier, element):
    db.interactions.update_one({'_id': identifier}, {"$set": element})


def count_interactions_by_id(interaction_id):
    return db.interactions.count_documents({'interaction_id': interaction_id})


def get_interactions_by_id(interaction_id):
    return db.interactions.find({'interaction_id': interaction_id})
