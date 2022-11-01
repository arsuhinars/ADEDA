from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from .db import SessionLocal, engine
from .models import Base, User

# Генерируем таблицы для моделей
Base.metadata.create_all(bind=engine)

app = FastAPI()


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

