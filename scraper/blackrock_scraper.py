import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from scraper.robots import is_allowed

BASE_URL = "https://www.blackrock.com"
INSIGHTS_URL = "https://www.blackrock.com/us/individual/insights"


def fetch_blackrock_insights(max_articles: int = 20):
    articles = []
    seen_urls = set()

    if not is_allowed(INSIGHTS_URL):
        print("BlackRock robots.txt disallows scraping insights page")
        return articles

    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; ResearchBot/1.0)"
    }

    response = requests.get(INSIGHTS_URL, headers=headers, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # BlackRock insights link pattern is stable
    for link in soup.select("a[href*='/insights/']"):
        if len(articles) >= max_articles:
            break

        href = link.get("href")

        title_el = link.find(["h2", "h3", "span"])
        title = title_el.get_text(strip=True) if title_el else link.get_text(strip=True)

        if not href or not title or len(title) < 15:
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

    print(f"BlackRock: fetched {len(articles)} articles")
    return articles
