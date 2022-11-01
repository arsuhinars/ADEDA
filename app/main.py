import asyncio

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
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

app = FastAPI()

# Добавляем пути
from .routes.auth import router as auth_router

app.include_router(auth_router)

# Добавляем обработчики ошибок
from .internal.errors import AppException
from .schemas import ErrorResponse

@app.exception_handler(AppException)
def app_exception_handler(request: Request, err: AppException):
    return JSONResponse(
        status_code=err.status_code,
        content=ErrorResponse(error=err.message).dict(exclude_none=True)
    )


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, err: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content=ErrorResponse(
            error='Validation error',
            error_verbose=str(err)
        ).dict(exclude_none=True)
    )


# Импортируем модуль для регулярных задач
from app.tasks import repated_tasks

@app.on_event('startup')
async def on_server_starts():
    """ Запускаем повторяемые задачи при запуске сервера """
    for task in repated_tasks:
        await task()


import uvicorn

if __name__ == '__main__':
    uvicorn.run(app)
