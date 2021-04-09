# From following along with https://browser.engineering/http.html
import socket
import ssl
from .urlparser import parseUrl, parseRedirectPortPath
from cache.cache import Cache
from cache.cacheitem import CacheItem
from datetime import datetime


class UrlFetch:

    def __init__(self):
        self.cache = Cache()

    def fetchUrl(self, url):
        scheme, host, port, path = parseUrl(url)

        # First, check the cache
        headers, body = self.cache.lookupInCache(url)
        if (headers != None and body != None):
            return headers, body

        # TODO: Add support for data scheme to inline HTML
        assert scheme in ["http://",
                          "https://",
                          "view-source:"], "Invalid url scheme: {}".format(scheme)
        assert len(host) > 0, "No host provided"

        originalScheme = scheme
        
        if scheme == "view-source":
            scheme = "https://"

        headers, body, status = buildAndSendRequest(port, scheme, path, host)
        headers, body = handleRedirectIfNeeded(
            status, body, headers, port, scheme, path, host)

        self.cacheRequestIfNeeded(status, headers, url, body)

        return headers, body, originalScheme

    def cacheRequestIfNeeded(self, status, headers, url, body):
        if status != "200":
            return

        try:
            max_cache = headers['cache-control']
            if (max_cache == "no-store"):
                max_cache = 0
            elif (max_cache.startswith("max-age")):
                max_cache = int(max_cache[max_cache.index("=")+1:])
        except KeyError:
            max_cache = 0

        if (max_cache != 0):
            # Thu, 08 Apr 2021 19:27:31 GMT
            date = datetime.strptime(
                headers['date'], "%a, %m %b %Y %H:%M:%S %Z")
            self.cache.addItemToCache(
                CacheItem(url, date, max_cache, headers, body))


def handleRedirectIfNeeded(status, body, headers, port, scheme, path, host):
    MAX_REDIRECTS = 10
    if (status.startswith("3")):
        numRedirects = 1
        while(status.startswith("3") and numRedirects < MAX_REDIRECTS):
            redirectUrl = headers["location"]
            # Don't reuse existing host and scheme values
            if (not redirectUrl.startswith("/")):
                scheme, host, port, path = parseUrl(redirectUrl)
            else:
                # Handle the case where Location starts with "/"
                port, path = parseRedirectPortPath(redirectUrl)

            headers, body, status = buildAndSendRequest(
                port, scheme, path, host)

            numRedirects += 1

    return headers, body


def buildAndSendRequest(port, scheme, path, host):
    s = socket.socket(
        family=socket.AF_INET,
        type=socket.SOCK_STREAM,
        proto=socket.IPPROTO_TCP
    )

    s = useSslIfHttps(scheme, s, host)

    port = determinePort(port, scheme)
    path = determinePath(path)
    s.connect((host, port))
    requestString = buildRequestString(host, path, "close")
    bytesSent = s.send(requestString)
    # Now read back the response
    response = s.makefile("r", encoding="utf8", newline="\r\n")
    statusLine = response.readline()
    version, status, explanation = statusLine.split(" ", 2)
    # Read headers into a map
    headers = extractHeaders(response)
    body = response.read()
    s.close()
    return headers, body, status


def extractHeaders(response):
    headers = dict()
    while True:
        line = response.readline()
        if line == "\r\n":
            break
        header, value = line.split(":", 1)
        headers[header.lower()] = value.strip()
    return headers


def determinePort(providedPort, scheme):
    if providedPort == "" or providedPort == None:
        if scheme == "https://":
            return 443
        else:
            return 80
    else:
        return int(providedPort[1:])


def buildRequestString(host, path, connection):
    requestString = "GET {} HTTP/1.1\r\n".format(path).encode("utf8")
    requestString += "Host: {}\r\n".format(host).encode("utf8")
    requestString += "Connection: {}\r\n".format(connection).encode("utf8")
    # TODO: Add compression support
    # requestString += "Accept-Encoding: {}\r\n".format(compression).encode("utf8")
    requestString += b"User-Agent: Browser-Engineering/0.0\r\n\r\n"
    return requestString


def useSslIfHttps(scheme, s, host):
    if scheme == "https://":
        ctx = ssl.create_default_context()
        s = ctx.wrap_socket(s, server_hostname=host)
    return s


def determinePath(path):
    if path == "" or path == None:
        path = "/index.html"
    return path
