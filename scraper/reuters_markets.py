import feedparser
from urllib.parse import urlparse

from scraper.safety import is_allowed, rate_limit


RSS_URL = "https://www.reuters.com/rssFeed/marketsNews"


def fetch_reuters_markets(max_articles=10):
    articles = []

    if not is_allowed(RSS_URL):
        print("Reuters robots.txt disallows RSS")
        return articles

    rate_limit("www.reuters.com")

    feed = feedparser.parse(RSS_URL)

    for entry in feed.entries:
        title = entry.get("title")
        link = entry.get("link")

        if not title or not link:
            continue

        if not is_allowed(link):
            continue

        articles.append({
            "title": title,
            "link": link
        })

        if len(articles) >= max_articles:
            break

    return articles
