import re


def parseUrl(url):
    # Only support http in this toy browser
    assert url.startswith("http://") or url.startswith("https://")
    # Could do it this way, but I'd like to be more robust, so will use Regex
    # scheme = url[len("http://")]
    # This is nicer since we can easily modify the expression later
    # to capture new patterns
    expr = "(https?:\/\/)([a-z]*\.*[\w\d][\w\d]*\.[a-z]*)(:\d*)?(\/.*)?"
    match = re.match(expr, url)
    scheme, host, port, path = match.groups()

    return (scheme, host, port, path)
