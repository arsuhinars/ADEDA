from os import environ

DATABASE_URL = environ.get('DATABASE_URL')

CACHE_SETTINGS = {
    'DEFAULT_TIMEOUT': 300
}
