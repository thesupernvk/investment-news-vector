import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from scraper.safety import is_allowed, rate_limit

BASE_URL = "https://www.imf.org"
GFSR_URL = "https://www.imf.org/en/Publications/GFSR"


def fetch_imf_gfsr(max_articles=5):
    articles = []

    if not is_allowed(GFSR_URL):
        return articles

    rate_limit("www.imf.org")
    resp = requests.get(GFSR_URL, timeout=20)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    for link in soup.select("a[href$='.pdf']"):
        title = link.get_text(strip=True)
        href = link.get("href")

        if not title or not href:
            continue

        url = urljoin(BASE_URL, href)
        articles.append({"title": title, "link": url})

        if len(articles) >= max_articles:
            break

    return articles
