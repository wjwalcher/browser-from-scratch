from datetime import timedelta, datetime


class Cache:

    def __init__(self):
        self.cachelines = dict()

    def addItemToCache(self, cacheItem):
        self.cachelines[cacheItem.url] = cacheItem

    def lookupInCache(self, url):
        try:
            cacheItem = self.cachelines[url]
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
