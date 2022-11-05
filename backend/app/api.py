from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError


# Создаем объект приложения для API
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
