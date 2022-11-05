from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from .db import engine
from .models import Base
from .internal.auth import check_and_create_admin
from .api import app as api_app
from app import config


# Генерируем таблицы для моделей
Base.metadata.create_all(bind=engine)
# Создаем аккаунт администратора
check_and_create_admin()


# Создаем объект приложения
app = FastAPI()


# Добавляем редирект на главную страницу
@app.get('/')
def index_page():
    return RedirectResponse('/main')


# Монтируем приложение для API
app.mount('/api', api_app)
# Монтируем файлы фронтенда
app.mount('/', StaticFiles(directory=config.FRONTEND_PATH, html=True))


# Добавляем обработчики ошибок
@app.exception_handler(404)
def not_found_error_handler(request, err):
    return RedirectResponse('/errors/error404.html')

@app.exception_handler(500)
def internal_error_handler(request, err):
    return RedirectResponse('/errors/error500.html')

@app.exception_handler(502)
def bad_gateway_handler(request, err):
    return RedirectResponse('/errors/error502.html')

@app.exception_handler(503)
def service_unavailable_handler(request, err):
    return RedirectResponse('/errors/error503.html')

@app.exception_handler(504)
def gateway_timeout_handler(request, err):
    return RedirectResponse('/errors/error504.html')


# Добавляем обработчики событий запуска и выключения сервера
from app.internal import webdriver_helper

@app.on_event('startup')
def on_start():
    webdriver_helper.on_start()


@app.on_event('shutdown')
def on_shutdown():
    webdriver_helper.on_end()


import uvicorn

if __name__ == '__main__':
    uvicorn.run(app)
