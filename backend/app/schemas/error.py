from pydantic import BaseModel

class ErrorResponse(BaseModel):
    """ Класс представления ответа с ошибкой """
    error: str
    error_verbose: str | None = None
