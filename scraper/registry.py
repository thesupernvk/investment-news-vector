from scraper.hn_scraper import fetch_hacker_news
from scraper.ubs_scraper import fetch_ubs_insights
from scraper.blackrock_scraper import fetch_blackrock_insights

SCRAPER_REGISTRY = {
    "fetch_hacker_news": fetch_hacker_news,
    "fetch_ubs_insights": fetch_ubs_insights,
    "fetch_blackrock_insights": fetch_blackrock_insights,
}
