import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

from scraper.safety import is_allowed, rate_limit

BASE_URL = "https://www.imf.org"
SEARCH_URL = "https://www.imf.org/en/search?q=capital%20markets&cf-type=NEWS"


def fetch_imf_capital_markets(max_articles=10):
    articles = []
    domain = urlparse(BASE_URL).netloc

    if not is_allowed(SEARCH_URL):
        return articles

    rate_limit(domain)
    resp = requests.get(SEARCH_URL, timeout=20)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    for link in soup.select("a[href^='/en/News/']"):
        title = link.get_text(strip=True)
        href = link.get("href")

        if not title or not href:
            continue

        url = urljoin(BASE_URL, href)

        if not is_allowed(url):
            continue

        articles.append({"title": title, "link": url})

        if len(articles) >= max_articles:
            break

    return articles
