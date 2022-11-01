from pydantic import BaseModel
from datetime import datetime, timedelta

from .config import CACHE_SETTINGS

class __CacheRecord(BaseModel):
    value: any
    expires: datetime

__memcache: dict[__CacheRecord] = {}

def get(key: str, default: any = None):
    """ 
    Получить значение кэша по его ключу
    
    * `key` - ключ кэша
    * `default` - значение, возвращаемое, если значения с заданным ключом не
    существует
    """
    if key in __memcache and __memcache[key].timeout < datetime.now():
        return __memcache.get(key).value
    return default


def set(
    key: str,
    value: any,
    timeout: int = CACHE_SETTINGS['DEFAULT_TIMEOUT']
    ):
    """
    Изменить значения кэша по его ключу

    * `key` - ключ кэша
    * `value` - значение, которое будет записано в кэш
    * `timeout` - время, через которое запись станет неактивной,
    по стандарту - время, указанное в `config.py`. Если указан `None`, то запись
    будет существовать вечно
    """
    __memcache[key] = __CacheRecord(
        value,
        datetime().now + timedelta(seconds=timeout)
    )


def get_or_set(
    key: str,
    default: any = None,
    timeout: int = CACHE_SETTINGS['DEFAULT_TIMEOUT']):
    """
    Получить значения кэша. Если его не существует, то создать и записать
    заданное значение.

    * `key` - ключ кэша
    * `default` - значение, которое будет записано, если кэша не существует
    * `timeout` - время, через которое запись станет неактивной.
    Подробнее в `set`
    """
    if key in __memcache and __memcache[key].timeout < datetime.now():
        return __memcache[key].value

    set(key, default, timeout)
    return default
