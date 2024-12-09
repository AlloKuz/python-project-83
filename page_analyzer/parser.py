from bs4 import BeautifulSoup
import logging


logger = logging.getLogger(__name__)


def parse_html(html_text):
    soup = BeautifulSoup(html_text, "html.parser")
    h1_tag = soup.find("h1") or None
    description = soup.find("meta",
                            attrs={"name": "description"})
    if description:
        description = description.get("content")
    return {"title": soup.title.text,
            "h1": h1_tag.text if h1_tag else None,
            "description": description}
