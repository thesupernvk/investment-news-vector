import urllib.robotparser as robotparser
from urllib.parse import urlparse

_robot_parsers = {}


def is_allowed(url: str, user_agent: str = "*") -> bool:
    parsed = urlparse(url)
    base = f"{parsed.scheme}://{parsed.netloc}"

    if base not in _robot_parsers:
        rp = robotparser.RobotFileParser()
        rp.set_url(f"{base}/robots.txt")
        try:
            rp.read()
        except Exception:
            return False
        _robot_parsers[base] = rp

    return _robot_parsers[base].can_fetch(user_agent, url)
