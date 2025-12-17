import time
import urllib.robotparser as robotparser
from urllib.parse import urlparse

_robot_cache = {}
LAST_REQUEST_TS = {}
MIN_DELAY_SECONDS = 2.0   # global polite rate limit


def is_allowed(url: str, user_agent: str = "*") -> bool:
    parsed = urlparse(url)
    base = f"{parsed.scheme}://{parsed.netloc}"

    if base not in _robot_cache:
        rp = robotparser.RobotFileParser()
        rp.set_url(f"{base}/robots.txt")
        rp.read()
        _robot_cache[base] = rp

    return _robot_cache[base].can_fetch(user_agent, url)


def rate_limit(domain: str):
    now = time.time()
    last = LAST_REQUEST_TS.get(domain, 0)
    elapsed = now - last

    if elapsed < MIN_DELAY_SECONDS:
        time.sleep(MIN_DELAY_SECONDS - elapsed)

    LAST_REQUEST_TS[domain] = time.time()
