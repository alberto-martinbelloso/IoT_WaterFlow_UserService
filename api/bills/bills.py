from api.mongo import db

def get_bills(username):
    collection = db["bills"]
    return collection.find({"username": username})


def get_all_bills():
    collection = db["bills"]
    return collection.find({})

