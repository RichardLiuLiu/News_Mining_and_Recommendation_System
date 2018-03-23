from pymongo import MongoClient

MONGO_HOST = 'localhost'
MONGO_PORT = '27017'
DB_NAME = 'tap_news'

client = MongoClient("%s:%s" % (MONGO_HOST, MONGO_PORT))

def get_db(db=DB_NAME):
    db = client[db]
    return db
