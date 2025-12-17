import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from scraper.safety import is_allowed, rate_limit

BASE_URL = "https://www.ecb.europa.eu"
ECB_URL = "https://www.ecb.europa.eu/press/blog/html/index.en.html"


def fetch_ecb_financial_stability(max_articles=5):
    articles = []

    if not is_allowed(ECB_URL):
        return articles

    rate_limit("www.ecb.europa.eu")
    resp = requests.get(ECB_URL, timeout=20)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    for link in soup.select("a[href*='/press/blog/']"):
        title = link.get_text(strip=True)
        href = link.get("href")

        if not title or not href:
            continue

        url = urljoin(BASE_URL, href)
        articles.append({"title": title, "link": url})

        if len(articles) >= max_articles:
            break

    return articles
