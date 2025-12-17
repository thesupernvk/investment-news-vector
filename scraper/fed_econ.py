import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from scraper.safety import is_allowed, rate_limit

BASE_URL = "https://www.federalreserve.gov"
ECON_URL = "https://www.federalreserve.gov/econres.htm"


def fetch_fed_econ(max_articles=5):
    articles = []

    if not is_allowed(ECON_URL):
        return articles

    rate_limit("www.federalreserve.gov")
    resp = requests.get(ECON_URL, timeout=20)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    for link in soup.select("a[href*='.htm']"):
        title = link.get_text(strip=True)
        href = link.get("href")

        if not title or not href:
            continue

        url = urljoin(BASE_URL, href)
        articles.append({"title": title, "link": url})

        if len(articles) >= max_articles:
            break

    return articles
