from url.urlfetcher import fetchUrl
from render.htmlrender import renderBody

url = input("Enter the URL to fetch: ")
headers, body = fetchUrl(str(url))

# print("Headers: {}\n Body: {}".format(headers, body))

renderBody(body)
