import cnn_news_scraper as scraper

EXPECTED_NEWS = "If I don't win the election, (news) ratings are going to go so far down, they'll be out of business, every one of them"
CNN_NEWS_URL = "https://www.cnn.com/2018/03/10/politics/warren-not-running-for-president/index.html"

def test_basic():
    news = scraper.extract_news(CNN_NEWS_URL)

    print (news)
    assert EXPECTED_NEWS in news
    print ("test_basic passed!")

if __name__ == "__main__":
    test_basic()
