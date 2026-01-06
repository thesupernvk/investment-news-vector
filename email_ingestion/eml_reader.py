from email import policy
from email.parser import BytesParser
from bs4 import BeautifulSoup
from datetime import datetime


def read_eml(path: str) -> dict:
    """
    Parse .eml file and extract clean text content + metadata
    """
    with open(path, "rb") as f:
        msg = BytesParser(policy=policy.default).parse(f)

    subject = msg.get("subject", "Newsletter")
    sender = msg.get("from", "")
    date_raw = msg.get("date", "")

    try:
        received_date = datetime.strptime(date_raw[:25], "%a, %d %b %Y %H:%M:%S")
    except Exception:
        received_date = None

    body = ""

    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()

            if content_type == "text/html":
                html = part.get_content()
                soup = BeautifulSoup(html, "html.parser")

                # Remove scripts/styles
                for tag in soup(["script", "style"]):
                    tag.decompose()

                body = soup.get_text(separator="\n", strip=True)
                break

            elif content_type == "text/plain" and not body:
                body = part.get_content()
    else:
        body = msg.get_content()

    return {
        "title": subject.strip(),
        "content": body.strip(),
        "metadata": {
            "source": "email",
            "sender": sender,
            "received_date": received_date.isoformat() if received_date else None
        }
    }
