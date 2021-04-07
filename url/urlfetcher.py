# From following along with https://browser.engineering/http.html
import socket
import ssl
from .urlparser import parseUrl


def fetchUrl(url):
    scheme, host, port, path = parseUrl(url)

    assert scheme in ["http://",
                      "https://"], "Invalid url scheme: {}".format(scheme)
    assert len(host) > 0, "No host provided"

    s = socket.socket(
        family=socket.AF_INET,
        type=socket.SOCK_STREAM,
        proto=socket.IPPROTO_TCP
    )

    port = determinePort(port, scheme)
    path = determinePath(path)

    s = useSslIfHttps(scheme, s, host)

    s.connect((host, port))

    requestString = buildRequestString(host, path)
    bytesSent = s.send(requestString)

    # Now read back the response
    response = s.makefile("r", encoding="utf8", newline="\r\n")
    statusLine = response.readline()
    version, status, explanation = statusLine.split(" ", 2)
    assert status == "200", "{}: {}".format(status, explanation)

    # Read headers into a map
    headers = extractHeaders(response)

    # Grab the body
    body = response.read()
    s.close()

    return headers, body


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


def buildRequestString(host, path):
    return "GET {} HTTP/1.0\r\n".format(path).encode("utf8") + "Host: {}\r\n\r\n".format(host).encode("utf8")


def useSslIfHttps(scheme, s, host):
    if scheme == "https://":
        ctx = ssl.create_default_context()
        s = ctx.wrap_socket(s, server_hostname=host)
    return s


def determinePath(path):
    if path == "" or path == None:
        path = "/index.html"
    return path
