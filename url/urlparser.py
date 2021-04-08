import re


def parseUrl(url):
    assert url.startswith("http://") or url.startswith("https://")

    expr = "(https?:\/\/)([a-z]*\.*[\w\d][\w\d]*\.[a-z]*)(:\d*)?(\/.*)?"
    match = re.match(expr, url)
    scheme, host, port, path = match.groups()

    return (scheme, host, port, path)


def parseRedirectPortPath(url):
    expr = "\/(:\d+)?(.*)?"
    match = re.match(expr, url)
    port, path = match.groups()

    return port, path
