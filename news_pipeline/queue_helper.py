import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
from cloudAMQP_client import CloudAMQPClient # pylint: disable=E0401, C0413

SCRAPE_NEWS_TASK_QUEUE_URL = "amqp://gxxrunfq:koLN7AWXswj_6FEGUSXxSLlXSrcm-uzp@skunk.rmq.cloudamqp.com/gxxrunfq"
SCRAPE_NEWS_TASK_QUEUE_NAME = "news_scraping_task_queue"

DEDUPE_NEWS_TASK_QUEUE_URL = 'amqp://wskfthsm:-tftvVWhTnghH3VPIYZRpqWo4aZ4hNBP@skunk.rmq.cloudamqp.com/wskfthsm'
DEDUPE_NEWS_TASK_QUEUE_NAME = 'news_deduping_task_queue'

def clear_queue(queue_url, queue_name):
    scrape_news_queue_client = CloudAMQPClient(queue_url, queue_name)
    num_of_messages = 0

    while True:
        if scrape_news_queue_client is not None:
            msg = scrape_news_queue_client.get_message()
            
            if msg is None:
                print("Cleared %d messages." % num_of_messages)
                return
            
            num_of_messages += 1


if __name__ == "__main__":
    clear_queue(SCRAPE_NEWS_TASK_QUEUE_URL, SCRAPE_NEWS_TASK_QUEUE_NAME)
    clear_queue(DEDUPE_NEWS_TASK_QUEUE_URL, DEDUPE_NEWS_TASK_QUEUE_NAME)
