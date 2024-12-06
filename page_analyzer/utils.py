import validators


def is_url_valid(url):
    return validators.url(url)
