import os

DATABASE_URL = os.environ['booking']
REDIS_URL = os.environ['search']
REDIS_TTL = os.environ['cache_ttl']
