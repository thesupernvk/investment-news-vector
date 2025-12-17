from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://design.citi.net"
START_URL = "https://design.citi.net/ds/icgds/angular/docs/components/alerts/overview"

# 👉 Adjust if needed
SYSTEM_CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def extract_rendered_content(soup: BeautifulSoup) -> str:
    """
    Extract rendered Angular documentation from <app-doc-section>
    """
    parts = []

    for section in soup.select("app-doc-section"):
        title = section.get("sectiontitle")
        if title:
            parts.append(f"\n## {title}\n")

        # Text
        for p in section.find_all("p"):
            text = p.get_text(strip=True)
            if text:
                parts.append(text)

        # Lists
        for li in section.find_all("li"):
            parts.append(f"- {li.get_text(strip=True)}")

        # Code blocks
        for pre in section.find_all("pre"):
            code = pre.get_text()
            if code.strip():
                parts.append("\n```")
                parts.append(code)
                parts.append("```")

    return "\n".join(parts)


def fetch_all_citi_components(max_articles=50):
    """
    Crawl ALL Angular components using rendered DOM.
    """
    articles = []

    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path=SYSTEM_CHROME_PATH,
            headless=True
        )

        page = browser.new_page()

        # Load initial page
        page.goto(START_URL, timeout=60000)

        # Wait for sidebar items to render
        page.wait_for_selector("div[data-path]", timeout=30000)

        # Extract sidebar component paths
        components = page.evaluate("""
            () => Array.from(
                document.querySelectorAll("div[data-path]")
            ).map(el => ({
                label: el.getAttribute("data-label"),
                path: el.getAttribute("data-path")
            }))
        """)

        seen = set()

        for comp in components:
            label = comp["label"]
            path = comp["path"]

            if not path or path in seen:
                continue

            seen.add(path)

            component_url = urljoin(BASE_URL, path + "/overview")

            page.goto(component_url, timeout=60000)

            # Wait for Angular doc content
            page.wait_for_selector("app-doc-section", timeout=30000)

            html = page.content()
            soup = BeautifulSoup(html, "html.parser")

            content = extract_rendered_content(soup)

            if not content.strip():
                continue

            articles.append({
                "title": label,
                "link": component_url,
                "content": content
            })

            if len(articles) >= max_articles:
                break

        browser.close()

    return articles
