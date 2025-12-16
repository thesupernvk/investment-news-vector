import requests
from bs4 import BeautifulSoup
from readability import Document

HN_URL = "https://news.ycombinator.com/"

def fetch_hacker_news():
    response = requests.get(HN_URL, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    items = soup.select(".athing")

    articles = []
    for item in items:
        title_tag = item.select_one(".titleline a")
        if not title_tag:
            continue

        articles.append({
            "title": title_tag.get_text(strip=True),
            "link": title_tag.get("href")
        })

    return articles


def fetch_article_content(url: str) -> str:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        doc = Document(response.text)
        html = doc.summary()

        soup = BeautifulSoup(html, "html.parser")
        return soup.get_text(separator="\n", strip=True)
    except Exception as e:
        print(f"Failed to fetch article: {url} → {e}")
        return ""
