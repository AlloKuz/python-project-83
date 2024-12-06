import validators
from urllib.parse import urlparse, urlunparse


def url_validator(data):
    if not validators.url(data["url"]):
        return {"url": "Wrong URL!"}
    return {}
