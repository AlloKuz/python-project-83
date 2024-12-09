from page_analyzer.app import app as app_

import os
import pytest


@pytest.fixture
def app():
    new_app = app_
    new_app.config.update({
        "Testing": True,
        "SECRET_KEY": os.getenv("TEST_SECRET_KEY"),
    })
    return new_app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def test_index(client):
    response = client.get("/")
    assert "Бесплатно проверяйте сайты на SEO-пригодность" in response.text


def test_urls(client):
    response = client.get("/urls")
    assert "Последняя проверка" in response.text


def test_index_form(client):
    response = client.post("/urls", data={
        "url": "https://hexlet.io",
    }, follow_redirects=True)
    assert response.status_code == 200
    assert any(["Страница успешно добавлена" in response.text,
                "Страница уже существует" in response.text])
    assert "hexlet" in response.text
