import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from scraper.safety import is_allowed, rate_limit

BASE_URL = "https://www.bis.org"
BULLETINS_URL = "https://www.bis.org/publ/bisbull.htm"


def fetch_bis_bulletins(max_articles=5):
    articles = []

    if not is_allowed(BULLETINS_URL):
        return articles

    rate_limit("www.bis.org")
    resp = requests.get(BULLETINS_URL, timeout=20)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    for link in soup.select("a[href$='.pdf']"):
        title = link.get_text(strip=True)
        href = link.get("href")

        if not title or not href:
            continue

        url = urljoin(BASE_URL, href)
        articles.append({"title": f"BIS Bulletin: {title}", "link": url})

        if len(articles) >= max_articles:
            break

    return articles
