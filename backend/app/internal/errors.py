from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException

from ..schemas import ErrorResponse


class AppError(Exception):
    """ Базовый внутренний класс для HTTP ошибок """
    def __init__(self, message: str, status_code: int):
        """
        Конструктор исключения

        * `message` - сообщение, содержащее информацию об ошибке
        * `status_code` - HTTP код ответа
        """
        self.message = message
        self.status_code = status_code

        super().__init__(message)


class UnauthorizedError(AppError):
    """ Класс для HTTP ошибки 401 не авторизован """
    def __init__(self):
        super().__init__('Authorization required', 401)


class ForbiddenError(AppError):
    """ Класс для HTTP ошибки 403 запрещено """
    def __init__(self):
        super().__init__('Forbidden', 403)


class ParseError(AppError):
    """ Класс ошибки парсинга """
    def __init__(self, message: str, source: str | None = None):
        """
        Конструктор исключения

        * `message` - сообщение, содержащее информацию об ошибке
        * `source` - источник ошибки
        """
        super().__init__(
            f'Parse error "{message}"' + 
            (f' ({source})' if source is not None else ''),
            400
        )


def app_exception_handler(request: Request, err: AppError):
    return JSONResponse(
        status_code=err.status_code,
        content=ErrorResponse(error=err.message).dict(exclude_none=True)
    )


def http_exception_handler(request: Request, err: HTTPException):
    return JSONResponse(
        status_code=err.status_code,
        content=ErrorResponse(error=str(err.detail)).dict(exclude_none=True)
    )


def validation_exception_handler(request: Request, err: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content=ErrorResponse(
            error='Validation error',
            error_verbose=str(err)
        ).dict(exclude_none=True)
    )
