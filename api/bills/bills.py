from api.mongo import db


def get_bills(username):
    collection = db["bills"]
    collection.find({"username": username})
    return collection
