import json
import pickle
import os
import redis
import sys

from datetime import datetime
from bson.json_util import dumps

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
import mongodb_client   # pylint: disable=E0401, C0413
import recommendation_service_client   # pylint: disable=E0401, C0413
from cloudAMQP_client import CloudAMQPClient    # pylint: disable=E0401, C0413


NEWS_TABLE_NAME = "news"

REDIS_HOST = "localhost"
REDIS_PROT = 6379
redis_client = redis.StrictRedis(REDIS_HOST, REDIS_PROT, db=0)

LOG_CLICKS_TASK_QUEUE_URL = "amqp://riwzpord:0w0xHbeo00dpid1Bhx4hF6ZQ1QuegGlB@skunk.rmq.cloudamqp.com/riwzpord"
LOG_CLICKS_TASK_QUEUE_NAME = "click_logging_task_queue"
cloudAMQP_client = CloudAMQPClient(LOG_CLICKS_TASK_QUEUE_URL, LOG_CLICKS_TASK_QUEUE_NAME)

NEWS_LIST_BATCH_SIZE = 10
NEWS_LIST_LIMIT = 200
USER_NEWS_TIMEOUT_IN_SECONDS = 60

def getOneNews():
    db = mongodb_client.get_db()
    news = db[NEWS_TABLE_NAME].find_one()
    return news


def getNewsSummariesForUser(user_id, page_num):
    page_num = int(page_num)
    begin_index = (page_num - 1) * NEWS_LIST_BATCH_SIZE
    end_index = page_num * NEWS_LIST_BATCH_SIZE

    sliced_news = []
    db = mongodb_client.get_db()

    if redis_client.get(user_id) is not None:
        news_digest = pickle.loads(redis_client.get(user_id))
        sliced_news_digest = news_digest[begin_index : end_index]
        sliced_news = list(db[NEWS_TABLE_NAME].find({'digest':{'$in':sliced_news_digest}}))
    else:       
        total_news = list(db[NEWS_TABLE_NAME].find().sort([('publishedAt', -1)]).limit(NEWS_LIST_LIMIT))
        total_news_digest = [x['digest'] for x in total_news]

        redis_client.set(user_id, pickle.dumps(total_news_digest))
        redis_client.expire(user_id, USER_NEWS_TIMEOUT_IN_SECONDS)

        sliced_news = total_news[begin_index : end_index]
    
    for news in sliced_news:
        del news['text']
        if news['publishedAt'].date() == datetime.today().date():
            news['time'] = 'today'
    
    return json.loads(dumps(sliced_news))


def logNewsClickForUser(user_id, news_id):
    message = {'userId': user_id, 'newsId': news_id, 'timestamp': str(datetime.utcnow())}
    cloudAMQP_client.send_message(message)