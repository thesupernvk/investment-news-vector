from scraper.ubs_scraper import fetch_ubs_insights
from scraper.blackrock_scraper import fetch_blackrock_insights
from scraper.citi_scraper import fetch_citi_insights
from scraper.jpm_scraper import fetch_jpm_insights
from scraper.pimco_scraper import fetch_pimco_insights
from scraper.bis_scraper import fetch_bis_reports
from scraper.imf_scraper import fetch_imf_weo
from scraper.imf_capital_markets import fetch_imf_capital_markets
from scraper.imf_gfsr import fetch_imf_gfsr
from scraper.bis_bulletins import fetch_bis_bulletins
from scraper.fed_econ import fetch_fed_econ
from scraper.ecb_financial_stability import fetch_ecb_financial_stability
from scraper.reuters_markets import fetch_reuters_markets

SCRAPER_REGISTRY = {
    "fetch_ubs_insights": fetch_ubs_insights,
    "fetch_blackrock_insights": fetch_blackrock_insights,
    "fetch_citi_insights": fetch_citi_insights,
    "fetch_jpm_insights": fetch_jpm_insights,
    "fetch_pimco_insights": fetch_pimco_insights,
    "fetch_bis_reports": fetch_bis_reports,
    "fetch_imf_weo": fetch_imf_weo,
    "fetch_imf_capital_markets": fetch_imf_capital_markets,
    "fetch_imf_gfsr": fetch_imf_gfsr,
    "fetch_bis_bulletins": fetch_bis_bulletins,
    "fetch_fed_econ": fetch_fed_econ,
    "fetch_ecb_financial_stability": fetch_ecb_financial_stability,
    "fetch_reuters_markets": fetch_reuters_markets,
}
