from page_analyzer.app import app as app_

import pytest
import uuid


@pytest.fixture
def app():
    new_app = app_
    new_app.config["TESTING"] = True,
    new_app.config["SECRET_KEY"] = str(uuid.uuid4())
    return new_app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def test_index(client):
    with client:
        response = client.get("/")
        assert "Бесплатно проверяйте сайты на SEO-пригодность" in response.text
