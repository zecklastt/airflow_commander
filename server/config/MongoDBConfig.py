import pymongo


def get_connection():
    try:
        mongo = MongoConnection('commanders')
        collection = mongo.get_collection('commander_day')
        return collection
    except Exception:
        raise Exception


class MongoConnection:
    def __init__(self, db_name):
        self.client = pymongo.MongoClient('mongodb://localhost:27017')
        self.db = self.client[db_name]

    def get_collection(self, collection_name):
        try:
            return self.db[collection_name]
        except Exception:
            raise Exception
