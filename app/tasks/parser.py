from . import repeat_every

@repeat_every(seconds=10)
async def parser_task():
    """ Задача для парсинга данных с сайтов каждые 15 минут """
    print('Started parsing')
