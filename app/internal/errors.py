
class ParseError(Exception):
    """ Класс ошибки парсинга """
    def __init__(self, message: str, source: str):
        """
        Конструктор исключения

        * `message` - сообщение, содержащее информацию об ошибке
        * `source` - источник ошибки
        """
        super().__init__(f'Parse error "{message}" on {source}')


class AppException(Exception):
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


class UnauthorizedException(AppException):
    """ Класс для HTTP ошибки 401 не авторизован """
    def __init__(self):
        super().__init__('Authorization required', 401)


class ForbiddenException(AppException):
    """ Класс для HTTP ошибки 403 запрещено """
    def __init__(self):
        super().__init__('Forbidden', 403)
