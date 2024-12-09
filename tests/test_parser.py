from page_analyzer import parser


def replaced_parser(path):
    with open(path) as f:
        data = f.read()
        return data


def test_parse_html():
    data = parser.parse_html("tests/fixtures/index.html",
                             parser=replaced_parser)
    assert data.get("title") == "Example site 1"
    assert data.get("h1") == "Some inner data"
    assert data.get("description") == "Lorem ipsum"