import requests
from bs4 import BeautifulSoup
from scraper.robots import is_allowed

BASE_URL = "https://www.jpmorgan.com"
INSIGHTS_URL = "https://www.jpmorgan.com/insights"


def fetch_jpm_insights(max_articles: int = 10):
    articles = []

    if not is_allowed(INSIGHTS_URL):
        print("JPMorgan robots.txt disallows scraping")
        return articles

    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; ResearchBot/1.0)"
    }

    try:
        resp = requests.get(INSIGHTS_URL, headers=headers, timeout=20)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"JPMorgan fetch failed: {e}")
        return articles  # <-- DO NOT CRASH PIPELINE

    soup = BeautifulSoup(resp.text, "html.parser")

    for link in soup.select("a[href]"):
        href = link.get("href")
        title = link.get_text(strip=True)

        if not href or not title or len(title) < 20:
            continue

        # JPM links are often relative
        if href.startswith("/"):
            url = BASE_URL + href
        elif href.startswith("http"):
            url = href
        else:
            continue

        if "/insights/" not in url:
            continue

        if not is_allowed(url):
            continue

        articles.append({
            "title": title,
            "link": url
        })

        if len(articles) >= max_articles:
            break

    print(f"JPMorgan: fetched {len(articles)} articles")
    return articles
