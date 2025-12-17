import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

from scraper.safety import rate_limit

BASE_URL = "https://design.citi.net"
START_URL = "https://design.citi.net/ds/icgds/angular/docs/components/alerts/overview"


# ---------------------------------------------------------
# Helper: code-aware content extraction
# ---------------------------------------------------------
def extract_component_content(soup: BeautifulSoup) -> str:
    """
    Extract component documentation with code-aware formatting.
    """

    parts = []

    main = soup.find("main") or soup

    for el in main.find_all(["h2", "h3", "p", "ul", "ol", "pre"]):
        # Headers
        if el.name in ["h2", "h3"]:
            parts.append(f"\n## {el.get_text(strip=True)}\n")

        # Paragraphs
        elif el.name == "p":
            text = el.get_text(strip=True)
            if text:
                parts.append(text)

        # Lists
        elif el.name in ["ul", "ol"]:
            for li in el.find_all("li"):
                parts.append(f"- {li.get_text(strip=True)}")

        # Code blocks
        elif el.name == "pre":
            code = el.get_text()
            if code.strip():
                parts.append("\n```")
                parts.append(code)
                parts.append("```")

    return "\n".join(parts)


# ---------------------------------------------------------
# Main crawler
# ---------------------------------------------------------
def fetch_all_citi_components(max_articles=50):
    """
    Crawl all Citi Design System Angular components automatically.
    """

    articles = []
    rate_limit(urlparse(START_URL).netloc)

    resp = requests.get(START_URL, timeout=20)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    component_urls = set()

    # ---- Sidebar navigation ----
    for link in soup.select("a[href*='/components/']"):
        href = link.get("href")
        if not href:
            continue

        if not href.endswith("/overview"):
            continue

        full_url = urljoin(BASE_URL, href)
        component_urls.add(full_url)

    # ---- Visit each component page ----
    for url in sorted(component_urls):
        rate_limit(urlparse(url).netloc)

        page = requests.get(url, timeout=20)
        page.raise_for_status()

        page_soup = BeautifulSoup(page.text, "html.parser")

        title_el = page_soup.find("h1")
        title = title_el.get_text(strip=True) if title_el else "Citi Design Component"

        # ✅ NOW THIS IS RESOLVED
        content = extract_component_content(page_soup)

        articles.append({
            "title": title,
            "link": url,
            "content": content
        })

        if len(articles) >= max_articles:
            break

    return articles
