import re


def parseUrl(url):
    if(url.startswith("view-source:")):
        expr = "(view-source:)([a-z]*\.*[\w\d][\w\d]*\.[a-z]*)(:\d*)?(\/.*)?"
    elif (url.startswith("http://") or url.startswith("https://")):
        expr = "(https?:\/\/)([a-z]*\.*[\w\d][\w\d]*\.[a-z]*)(:\d*)?(\/.*)?"
    else:
        raise Exception("Unsopported scheme")

    match = re.match(expr, url)
    scheme, host, port, path = match.groups()

    return (scheme, host, port, path)


def parseRedirectPortPath(url):
    expr = "\/(:\d+)?(.*)?"
    match = re.match(expr, url)
    port, path = match.groups()

    return port, path
