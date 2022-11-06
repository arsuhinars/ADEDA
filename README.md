# Задача 06. Сервис для расчета рыночной стоимости жилой недвижимости города Москвы
Данный сервис был разработан в рамках хакатона
[Лидеры цифровой трансформации 2022](https://leaders2022.innoagency.ru/) командой
ADEDA.

Состав команды:
- @arsuhinars - back-end
- @Aveocr - PM-manager
- @mister-mamaster - PM-manager
- @DashulkaUbivator - frontend
- @Ekaterina-Kas - frontend

# Используемый стек
* Backend:
Python, FastAPI, SQLAlchemy, Selenium, openpyxl и др.

# Краткое описание
1. Пользователь, заходя на сайт, авторизуется под своим логином и паролем
2. Импортирует таблицу с квартирами в соотвествии с Приложением 1
3. Выбирает нужную квартиру как эталонную
4. Сайт ищем аналоги и автоматически вычисляет корректировки
5. Пользователь при необходимости изменяет корректировки или выключает их
6. Экспортирует полученный результат как Excel таблицу

# Скриншоты
<img src="https://user-images.githubusercontent.com/36979003/200189092-bfde4de6-ab49-4aeb-82af-c28c624f6872.png" width="450"> <img src="https://user-images.githubusercontent.com/36979003/200188998-1c604d84-72a8-47f6-9a37-98b73d4a0b67.png" width="450">
<img src="https://user-images.githubusercontent.com/36979003/200189064-792e1f2f-867d-4a41-8533-46412b4fbc6f.png" width="450"> <img src="https://user-images.githubusercontent.com/36979003/200189139-6c19c80e-83ab-4ae6-87e1-9a29bc6200c0.png" width="450">
<img src="https://user-images.githubusercontent.com/36979003/200189125-1ef1794d-4e27-4d28-b94f-a70e3e4d5c76.png" width="450">


# Ручная установка
1. Скопируйте репозиторий. Для этого введите в терминале следующую команду:

    `git clone https://github.com/arsuhinars/ADEDA.git`

2. Убедитесь, что у вас установлен Python 3.10. Установите pipenv, если его нет:

    `pip install pipenv`

3. Перейдите в директорию `backend`. Установите все зависимости, для этого
    введите следующую команду в директории `backend`:

    `python -m pipenv install`

4. Создайте `.env` файл в директории `backend`. Ниже указан пример файла:

    ```ini
    DATABASE_URL=sqlite:///app.db
    SECRET_KEY=<случайный секретный ключ>

    ADMIN_LOGIN=<логин администратора>
    ADMIN_PASSWORD=<пароль администратора>
    ```

    Указывать логин и пароль администратора необходимо только при первом
    запуске, потом эти поля можно удалить, чтобы избежать их утечки при взломе.

5. Перейдите в директорию `backend`, введите следующую команду для запуска
    сервера:

    ```
    python -m pipenv shell
    uvicorn app.main:app
    ```

# Техническая часть
Про подробное описание API вы можете почитать [здесь](backend/README.md).
