from bs4 import BeautifulSoup
import requests


def parse_html(url, parser=requests.get):
    text = parser(url)
    try:
        soup = BeautifulSoup(text, "html.parser")
        h1_tag = soup.find("h1") or None
        description = soup.find("meta",
                                attrs={"name": "description"}).get("content")
        return {"title": soup.title.text,
                "h1": h1_tag.text if h1_tag else None,
                "description": description}
    except Exception as e:
        print(f"Error: {e}! Can't parse a site '{url}'")
    return False
