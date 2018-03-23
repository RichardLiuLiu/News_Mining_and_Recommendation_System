import os
import sys

from newspaper import Article

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
# sys.path.append(os.path.join(os.path.dirname(__file__), 'news_scraper'))

# import cnn_news_scraper # pylint: disable=E0401, C0413
from cloudAMQP_client import CloudAMQPClient   # pylint: disable=E0401, C0413

SCRAPE_NEWS_TASK_QUEUE_URL = "amqp://gxxrunfq:koLN7AWXswj_6FEGUSXxSLlXSrcm-uzp@skunk.rmq.cloudamqp.com/gxxrunfq"
SCRAPE_NEWS_TASK_QUEUE_NAME = "news_scraping_task_queue"

DEDUPE_NEWS_TASK_QUEUE_URL = 'amqp://wskfthsm:-tftvVWhTnghH3VPIYZRpqWo4aZ4hNBP@skunk.rmq.cloudamqp.com/wskfthsm'
DEDUPE_NEWS_TASK_QUEUE_NAME = 'news_deduping_task_queue'

SLEEP_TIME_IN_SECONDS = 5

dedupe_news_queue_client = CloudAMQPClient(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)
scrape_news_queue_client = CloudAMQPClient(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)


def handle_message(msg):
    if msg is None or not isinstance(msg, dict):
        print("message is broken")
        return
    
    task = msg

    article = Article(task['url'])
    article.download()
    article.parse()

    task['text'] = article.text

    dedupe_news_queue_client.send_message(task)

def run():
    while True:
        if scrape_news_queue_client is not None:
            msg = scrape_news_queue_client.get_message()
            if msg is not None:
                try:
                    handle_message(msg)
                except Exception as e:
                    print(e)
                    pass
            
            scrape_news_queue_client.sleep(SLEEP_TIME_IN_SECONDS)


if __name__ == "__main__":
    run()

