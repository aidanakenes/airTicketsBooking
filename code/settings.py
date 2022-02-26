import os

DATABASE_URL = os.environ['POSTGRES_DSN'] or 'postgres://postgres:aknsm@localhost/postgres'
REDIS_URL = os.environ['REDIS_DSN'] or 'redis://localhost'
SEARCH_RESULTS_REDIS_TTL = int(os.environ['SEARCH_RESULTS_REDIS_TTL']) or 1800
CURRENCY_RESULTS_REDIS_TTL = int(os.environ['CURRENCY_RESULTS_REDIS_TTL']) or 86400
