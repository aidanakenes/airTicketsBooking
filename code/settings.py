import os

POSTGRES_DSN = os.environ['POSTGRES_DSN'] if os.environ['POSTGRES_DSN'] else 'postgres://postgres:aknsm@localhost/postgres'
REDIS_DSN = os.environ['REDIS_DSN'] if os.environ['REDIS_DSN'] else 'redis://localhost'
SEARCH_RESULTS_REDIS_TTL = int(os.environ['SEARCH_RESULTS_REDIS_TTL']) if os.environ['SEARCH_RESULTS_REDIS_TTL'] else 1800
CURRENCY_RESULTS_REDIS_TTL = int(os.environ['CURRENCY_RESULTS_REDIS_TTL']) if os.environ['CURRENCY_RESULTS_REDIS_TTL'] else 86400
