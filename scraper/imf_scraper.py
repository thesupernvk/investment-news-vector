import requests
from bs4 import BeautifulSoup
from scraper.robots import is_allowed

BASE_URL = "https://www.imf.org"
INSIGHTS_URL = "https://www.imf.org/en/Publications/WEO"


def fetch_imf_weo(max_articles=5):
    articles = []

    if not is_allowed(INSIGHTS_URL):
        return articles

    resp = requests.get(INSIGHTS_URL, timeout=20)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    for link in soup.select("a[href$='.pdf']"):
        href = link.get("href")
        title = link.get_text(strip=True)

        if not href or not title:
            continue

        url = href if href.startswith("http") else BASE_URL + href

        articles.append({"title": title, "link": url})

        if len(articles) >= max_articles:
            break

    print(f"IMF: fetched {len(articles)} PDFs")
    return articles
