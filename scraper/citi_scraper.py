import requests
from bs4 import BeautifulSoup
from scraper.robots import is_allowed

BASE_URL = "https://www.citigroup.com"
INSIGHTS_URL = "https://www.citigroup.com/global/insights"


def fetch_citi_insights(max_articles=10):
    articles = []

    if not is_allowed(INSIGHTS_URL):
        return articles

    resp = requests.get(INSIGHTS_URL, timeout=20)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    for link in soup.select("a[href*='/global/insights/']"):
        title = link.get_text(strip=True)
        href = link.get("href")

        if not title or not href or len(title) < 15:
            continue

        url = href if href.startswith("http") else BASE_URL + href

        if not is_allowed(url):
            continue

        articles.append({"title": title, "link": url})

        if len(articles) >= max_articles:
            break

    print(f"Citi: fetched {len(articles)} articles")
    return articles
