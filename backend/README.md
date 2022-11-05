# Описание API

## Доступные HTTP методы
1. `/auth/get_token`

    GET метод авторизации пользователя. После успешного выполнения JWT токен.
    Для доступа к некоторым методам требуется передать его в параметрах запроса
    как `token`.

    Параметры запроса:
    * `login` - логин пользователя
    * `password` - пароль для авторизации

    Формат ответа:
    ```json
    {
        "token": "string"
    }
    ```
2. `/auth/create_user`

    POST метод для создания нового пользователя. Для доступа требуется, чтобы
    пользователь был администратором.

    Параметры запроса:
    * `token` - JWT токен, полученный при авторизации

    Формат тела запроса:
    ```json
    {
        "login": "string",
        "password": "string",
        "is_admin": false
    }
    ```

    Формат ответа:
    ```json
    {}
    ```
3. `/table/parse`

    POST метод для парсинга Excel импортируемой таблицы с квартирами. В тело
    запроса необходимо передать сам файл.

    Параметры запроса:
    * `token` - JWT токен, полученный при авторизации

    Формат ответа:
    ```json
    [
        {
            "location": "string",
            "rooms_count": 0,
            "segment": "new",
            "floor": 0,
            "floors_count": 0,
            "flat_area": 0,
            "kitchen_area": 0,
            "has_balcony": true,
            "material": "brick",
            "state": "no",
            "metro_distance": 0
        }
    ]
    ```
4. `/table/create`

    POST метод экспорта полученных аналогов в таблицу Excel. В теле запроса
    необходимо передать эталонную квартиру `reference`, список с аналогами
    `house` и их корректировками `adjustments`.

    Параметры запроса:
    * `token` - JWT токен, полученный при авторизации

    Формат тела запроса:
    ```json
    {
        "reference": {
            "location": "string",
            "rooms_count": 0,
            "segment": "new",
            "floor": 0,
            "floors_count": 0,
            "flat_area": 0,
            "kitchen_area": 0,
            "has_balcony": false,
            "material": "panel",
            "state": "state",
            "metro_distance": 0
        },
        "analogs": [
            {
                "house": {
                    "id": 0,
                    "location": "string",
                    "rooms_count": 0,
                    "segment": "new",
                    "floor": 0,
                    "floors_count": 0,
                    "flat_area": 0.0,
                    "kitchen_area": 0,
                    "has_balcony": true,
                    "material": "panel",
                    "state": "modern",
                    "metro_station": "string",
                    "metro_distance": 0,
                    "price": 0,
                    "source_service": "avito",
                    "url": "string"
                },
                "adjustments": {
                    "trade": 0,
                    "area": 0,
                    "metro": 0,
                    "floor": 0,
                    "kitchen_area": 0,
                    "balcony": 0,
                    "repairs": 0
                }
            }
        ]
    }
    ```

    В ответе будет возвращена готовая таблица Excel

## Web-Socket endpoints
1. `/search_houses`

    Endpoint для поиска квартир.
    
    Последовательность общения сервера и клиента:
    1. При соединении, клиент должен передать в параметрах запроса `token`,
    полученный при авторизации.
    2. Отправляет сообщение с необходимым запросом, по которому будет идти поиск
    квартир. В запросе указываются следующие поля:
    - `house` - эталон для поиска
    - `adjustments` - словарь используемых корректировок при поиске
    - `max_house_count` - максимальное количество квартир в ответе
    3. После сервер по мере поиска возвращает результаты. В сообщении он
    отправляет список со всеми найденными объектами, отсортированными по их
    релевантности. У каждого объекта квартиры указывается поле `id`.
    Гарантируется, что значение поля для каждой квартиры будет сохраняться,
    даже если порядок в списке измениться.
    4. После достижения максимального количества квартир или если больше не
    удается найти квартиры, сервер закрывает соединение.
    
    Параметры запроса:
    * `token` - JWT токен, полученный при авторизации

    Формат запроса:
    ```json
    {
        "house": {
            "location": "string",
            "rooms_count": 0,
            "segment": "new",
            "floor": 0,
            "floors_count": 0,
            "flat_area": 0,
            "kitchen_area": 0,
            "has_balcony": true,
            "material": "brick",
            "state": "no",
            "metro_distance": 0
        },
        "adjustments": {
            "trade": false,
            "area": false,
            "metro": false,
            "floor": false,
            "kitchen_area": false,
            "balcony": false,
            "repairs": false
        },
        "max_house_count": 10
    }
    ```

    Формат сообщения списка квартир:
    ```json
    [
        {
            "id": 0,
            "location": "string",
            "rooms_count": 0,
            "segment": "new",
            "floor": 0,
            "floors_count": 0,
            "flat_area": 0,
            "kitchen_area": 0,
            "has_balcony": true,
            "material": "brick",
            "state": "no",
            "metro_station": "string",
            "metro_distance": 0,
            "price": 0,
            "source_service": "avito",
            "url": "string"
        }
    ]
    ```

## Типы перечислений
В схемах также используется такие типы, как перечисления. В основном они
представлены в виде JSON строки.

1. `HouseSegment`

    Описание сегмента дома. Допустимые значения:
    - `"new"` - новостройка
    - `"modern"` - современное жилье
    - `"old"` - старый жилой фонд
2. `HouseMaterial`

    Материал стен дома. Допустимые значения:
    - `"brick"` - кирпич
    - `"panel"` - панель
    - `"monolit"` - монолит
3. `HouseState`

    Описание состояния дома. Допустимые значения:
    - `"no"` - без отделки
    - `"state"` - муниципальный ремонт
    - `"modern"` - современная отделка
4. `SourceService`

    Тип источника. Допустимые значения: `"avito"`, `"cian"`

## Ошибки
При возникновении каких-либо ошибок сервер будет возвращать следующий JSON объект:
```json
{
    "error": "string",
    "error_verbose": "string"
}
```
Поле `error_verbose` является опциональным. Оно используется достаточно редко.
