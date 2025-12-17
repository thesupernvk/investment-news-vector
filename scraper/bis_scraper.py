import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from scraper.robots import is_allowed

BASE_URL = "https://www.bis.org"

ALLOWED_PUBLICATION_PAGES = [
    "https://www.bis.org/publ/qtrpdf/index.htm",   # Quarterly Review
    "https://www.bis.org/publ/arpdf/index.htm",    # Annual Economic Report
    "https://www.bis.org/publ/bisbull/index.htm",  # BIS Bulletins
]


def fetch_bis_reports(max_articles: int = 5):
    """
    Robots-compliant BIS scraper:
    - Scrapes only allowed publication indexes
    - Extracts PDF links
    """

    articles = []
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; ResearchBot/1.0)"
    }

    for index_url in ALLOWED_PUBLICATION_PAGES:
        if not is_allowed(index_url):
            print(f"BIS robots.txt disallows {index_url}")
            continue

        try:
            resp = requests.get(index_url, headers=headers, timeout=20)
            resp.raise_for_status()
        except requests.RequestException as e:
            print(f"BIS fetch failed for {index_url}: {e}")
            continue

        soup = BeautifulSoup(resp.text, "html.parser")

        for link in soup.select("a[href$='.pdf']"):
            href = link.get("href")
            title = link.get_text(strip=True)

            if not href or not title:
                continue

            pdf_url = urljoin(BASE_URL, href)

            if not is_allowed(pdf_url):
                continue

            articles.append({
                "title": f"BIS: {title}",
                "link": pdf_url
            })

            if len(articles) >= max_articles:
                break

        if len(articles) >= max_articles:
            break

    print(f"BIS (compliant): fetched {len(articles)} PDF reports")
    return articles
