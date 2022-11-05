import os
from os import environ, path

# Настройки БД
DATABASE_URL = environ.get('DATABASE_URL')
SECRET_KEY = environ.get('SECRET_KEY')


# Настройки авторизации
ACCESS_TOKEN_EXPIRE = 30 * 60
PASSWORD_SALT_LENGTH = 16

ADMIN_LOGIN = environ.get('ADMIN_LOGIN')
ADMIN_PASSWORD = environ.get('ADMIN_PASSWORD')


# Настройки парсера
PARSE_DELAY = 10
PARSER_BROWSER = 'firefox'
WEBDRIVER_OPTIONS = {
    'headless': False,
    'page_load_strategy': 'eager',
}


# Настройки поисковика
SEARCHER_QUERY_TIMEOUT = 5


# Настройки фронденда
FRONTEND_PATH = path.normpath(path.join(os.getcwd(), '../frontend'))
FRONTEND_ERROR_HANDLERS = {
    404: '',
    500: '',
    502: '',
    503: '',
    504: '',
}
FRONTEND_COMMON_ERROR_HANDLER = ''
