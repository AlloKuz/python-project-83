from page_analyzer.utils import url_validate, url_normalize

import pytest


@pytest.mark.parametrize("url, answer", [
    (
        {"url": "https://hexlet.io"},
        {}
    ),
    (
        {"url": 50 * "https://hexlet.io"},
        {"url": "URL is too long"}
    ),
    (
        {"url": "nothexlet.io"},
        {"url": "Wrong URL!"}
    ),
])
def test_url_validate(url, answer):
    assert url_validate(url) == answer


@pytest.mark.parametrize("url, answer", [
    ("https://hexlet.io", "https://hexlet.io"),
    ("http://google.com/hexxlo?params=1", "http://google.com")
])
def test_normalize(url, answer):
    assert url_normalize(url) == answer
