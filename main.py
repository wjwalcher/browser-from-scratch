from render.htmlrender import renderBody
from cache.cacheitem import CacheItem
from datetime import datetime
from url.urlfetcher import UrlFetch

url = input("Enter the URL to fetch: ")
fetcher = UrlFetch()
headers, body, scheme = fetcher.fetchUrl(str(url))
# Fetch twice to test caching
headers, body, scheme = fetcher.fetchUrl(str(url))
# print("Headers: {}\n Body: {}".format(headers, body))

renderBody(body, scheme)
