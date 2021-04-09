from dataclasses import dataclass
import datetime


@dataclass
class CacheItem:
    url: str
    request_time: datetime
    expiration: int
    headers: dict
    body: str
