from urllib.parse import urlparse

import validators


def url_validate(data):
    if len(data["url"]) > 255:
        return {"url": "URL is too long"}

    if not validators.url(data["url"]):
        return {"url": "Wrong URL!"}
    return {}


def url_normalize(url):
    parts = urlparse(url)
    return f"{parts.scheme}://{parts.netloc}".lower()
