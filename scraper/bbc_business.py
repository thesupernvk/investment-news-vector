import feedparser
from scraper.safety import rate_limit, is_allowed


RSS_URL = "https://feeds.bbci.co.uk/news/business/rss.xml"


def fetch_bbc_business(max_articles=10):
    articles = []

    if not is_allowed(RSS_URL):
        return articles

    rate_limit("feeds.bbci.co.uk")

    feed = feedparser.parse(RSS_URL)

    for entry in feed.entries:
        title = entry.get("title")
        link = entry.get("link")

        if not title or not link:
            continue

        articles.append({
            "title": title,
            "link": link
        })

        if len(articles) >= max_articles:
            break

    return articles
