from os import environ

DATABASE_URL = environ.get('DATABASE_URL')
SECRET_KEY = environ.get('SECRET_KEY')

ADMIN_LOGIN = environ.get('ADMIN_LOGIN')
ADMIN_PASSWORD = environ.get('ADMIN_PASSWORD')

ACCESS_TOKEN_EXPIRE = 30 * 60

CACHE_SETTINGS = {
    'DEFAULT_TIMEOUT': 300
}

PASSWORD_SALT_LENGTH = 16

PARSE_DELAY = 10
PARSER_BROWSER = 'firefox'
WEBDRIVER_OPTIONS = {
    'headless': False,
    'page_load_strategy': 'eager',
}
