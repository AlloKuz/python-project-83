from page_analyzer.app import app as app_

import os
import pytest


class DbMock:

    def __enter__(self):
        pass

    def __exit__(self):
        pass

    def cursor(self):
        # return cursor-like object
        pass


@pytest.fixture
def app():
    new_app = app_
    new_app.config.update({
        "TESTING": True,
        "SECRET_KEY": os.getenv("TEST_SECRET_KEY"),
        "DATABASE_URL": "",
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
