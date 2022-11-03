from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from .db import SessionLocal, engine
from .models import Base, User
from .schemas import UserCreate
from .internal.auth import create_user
from app import config


# Генерируем таблицы для моделей
Base.metadata.create_all(bind=engine)

# Автоматически создаем аккаунт администратора
if config.ADMIN_LOGIN and config.ADMIN_PASSWORD:
    with SessionLocal() as session:
        if session.query(User).filter(User.is_admin == True).count() == 0:
            create_user(UserCreate(
                login = config.ADMIN_LOGIN,
                password = config.ADMIN_PASSWORD,
                is_admin = True
            ), session)
        session.commit()


# Создаем объект приложения
app = FastAPI()


# Добавляем обработчики путей
from .routes.auth import router as auth_router
from .routes.table import router as table_router

app.include_router(auth_router)
app.include_router(table_router)


# Добавляем обработчик веб-сокетов
from .ws import searcher_endpoint

app.add_api_websocket_route('/search_houses', searcher_endpoint)


# Добавляем обработчики ошибок
from .internal.errors import *

app.add_exception_handler(AppError, app_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(500, internal_error_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)


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
