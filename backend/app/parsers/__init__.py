from ..schemas import HouseBase

class Parser:
    """
    Базовый класс для парсеров. Поддерживает менеджер контекста
    """

    async def begin(self):
        """ Метод начала работы с парсером. Должен обязательно быть вызван """
        raise NotImplementedError()

    async def parse_next(self) -> HouseBase:
        """
        Метод парсинга следующего дома
        
        Гарантированно вызывает только исключение `ParseError` при возникновении
        ошибки парсинга
        """
        raise NotImplementedError()

    async def end(self):
        """ Метод окончания работы. Должен обязательно быть вызыван """
        raise NotImplementedError()
    
    async def __aenter__(self):
        await self.begin()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_trace):
        await self.end()
