import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from scraper.robots import is_allowed

BASE_URL = "https://www.ubs.com"
INSIGHTS_URL = "https://www.ubs.com/global/en/wealth-management/insights.html"


def fetch_ubs_insights(max_articles: int = 20):
    articles = []
    seen_urls = set()

    if not is_allowed(INSIGHTS_URL):
        print("UBS robots.txt disallows scraping insights page")
        return articles

    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; ResearchBot/1.0)"
    }

    response = requests.get(INSIGHTS_URL, headers=headers, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # UBS insights are linked via /insights/ paths
    for link in soup.select("a[href*='/insights/']"):
        if len(articles) >= max_articles:
            break

        href = link.get("href")
        title = link.get_text(strip=True)

        if not href or not title or len(title) < 20:
            continue

        url = urljoin(BASE_URL, href)

        if url in seen_urls:
            continue

        if not is_allowed(url):
            continue

        seen_urls.add(url)
        articles.append({
            "title": title,
            "link": url
        })

    print(f"UBS: fetched {len(articles)} articles")
    return articles
