from datetime import timedelta, datetime


class Cache:

    def __init__(self):
        self.cacheLines = dict()

    def addItemToCache(self, cacheItem):
        self.cacheLines[cacheItem.url] = cacheItem

    def lookupInCache(self, url):
        try:
            cacheItem = self.cacheLines[url]
        except KeyError:
            return None, None

        if validateLookup(cacheItem):
            return cacheItem.headers, cacheItem.body

        return None, None


# Determine using current time,
# initial lookup time, and max
# cache time whether this item is
# still valid
def validateLookup(cacheItem):
    if ((cacheItem.request_time + timedelta(seconds=cacheItem.expiration)) > datetime.now()):
        return True

    return False
