import os
import random
import requests

from lxml import html

CNN_NEWS_XPATH = "//p[contains(@class, 'zn-body__paragraph')]//text() | //div[contains(@class, 'zn-body__paragraph')]//text()"

USER_AGENTS_FILE = os.path.join(os.path.dirname(__file__), 'user_agents.txt')
USER_AGENTS = []

with open(USER_AGENTS_FILE, 'r') as uaf:
    for ua in uaf.readlines():
        if ua:
            USER_AGENTS.append(ua.strip()[1:-1])
random.shuffle(USER_AGENTS)

def get_headers():
    ua = random.choice(USER_AGENTS)
    headers = {
        "User-Agent" : ua
    }
    return headers

def extract_news(news_url):
    session_requests = requests.session()
    response = session_requests.get(news_url, headers=get_headers())
    news = {}

    try:
        tree = html.fromstring(response.content)
        news = tree.xpath(CNN_NEWS_XPATH)
        news = ''.join(news)
    except Exception:
        return {}

    return news
