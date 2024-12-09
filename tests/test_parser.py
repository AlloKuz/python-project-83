from page_analyzer import parser

import pytest

FIXTURES_PATH = "tests/fixtures"


@pytest.fixture
def html_content():
    # with open("tests/fixtures/index.html", "r") as f:
    #     return f.read()
    return """<!DOCTYPE html>
              <html lang="en">
              <head>
                  <meta charset="UTF-8">
                  <meta name="viewport"
                    content="width=device-width, initial-scale=1.0">
                  <meta name="description" content="Lorem ipsum">
                  <title>Example site 1</title>
              </head>
              <body>
                  <h1>Some inner data</h1>
                  <table>
                      <thead>
                          <tr>
                              <td></td>
                              <td></td>
                          </tr>
                          <tr>
                              <td></td>
                              <td></td>
                          </tr>
                          <tr>
                              <td></td>
                              <td></td>
                          </tr>
                          <tr>
                              <td></td>
                              <td></td>
                          </tr>
                          <tr>
                              <td></td>
                              <td></td>
                          </tr>
                      </thead>
                  </table>
              </body>
              </html>"""


def test_parse_html(html_content):
    data = parser.parse_html(html_content)
    assert data.get("title") == "Example site 1"
    assert data.get("h1") == "Some inner data"
    assert data.get("description") == "Lorem ipsum"
