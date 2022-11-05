from os import urandom
from hashlib import pbkdf2_hmac
from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from jose import jwt, JWTError

from ..schemas import UserCreate
from ..models import User
from ..db import SessionLocal
from app import config

def hash_password(password: str, salt: bytes):
    """ Метод генерации ключа для пароля с помощью соли """
    key = pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        iterations=100_000
    )
    return key


def create_user(user: UserCreate, session: Session):
    """
    Метод добавления нового пользователя в базу данных

    * `user` - объект пользователя, содержащий данные для его создания
    * `session` - текущая сессия для взаимодействия с базой данных
    """
    salt = urandom(config.PASSWORD_SALT_LENGTH)

    db_user = User(
        login = user.login,
        salt = salt,
        password_key = hash_password(user.password, salt),
        is_admin = user.is_admin
    )

    session.add(db_user)


def authenticate_user(login: str, password: str, session: Session):
    """
    Метод авторизации пользователя

    * `login` - логин пользователя
    * `password` - введеный пароль
    * `session` - текущая сессия для взаимодействия с БД

    Возвращает `None`, если пользователь не найден или введеный пароль неверный.
    Если данные введены верно, то возвращает объект пользователя
    """
    user = get_user_by_login(login, session)
    if not user:
        return None
    if not verify_user_password(user, password):
        return None
    return user


def get_user_by_login(login: str, session: Session) -> User:
    """ Найти пользователя из базы данных по его логину """
    return session.query(User).filter(User.login == login).first()


def get_user_by_token(token: str, session: Session) -> (User | None):
    """
    Найти пользователя из базы данных по его JWT токену.

    Возвращает `None`, если передан невалидный токен
    """
    try:
        token_data = jwt.decode(token, config.SECRET_KEY)
        user_id = int(token_data['sub'])
        return session.query(User).filter(User.id == user_id).first()
    except JWTError:
        return None


def verify_user_password(user: User, password: str):
    """ Метод проверки правильности пароля для пользователя """
    return hash_password(password, user.salt) == user.password_key


def verify_user_token(token: str):
    """ Метод проверки JWT токена на валидность """
    try:
        jwt.decode(token, config.SECRET_KEY)
        return True
    except JWTError:
        return False


def create_jwt_token(user: User):
    """
    Создать JWT токен для пользователя, по которому он сможет использовать сайт
    """
    token = jwt.encode({
        'sub': str(user.id),
        'exp': datetime.now() + timedelta(seconds=config.ACCESS_TOKEN_EXPIRE)
    }, config.SECRET_KEY)
    return token


def check_and_create_admin():
    """
    Метод для проверки и создания аккаунта администратора.
    Логин и пароль указываются в .env файле
    """
    # Автоматически создаем аккаунт администратора
    if config.ADMIN_LOGIN is not str or config.ADMIN_PASSWORD is not str:
        return

    with SessionLocal() as session:
        if session.query(User).filter(User.is_admin == True).count() == 0:
            create_user(UserCreate(
                login = config.ADMIN_LOGIN,
                password = config.ADMIN_PASSWORD,
                is_admin = True
            ), session)
        session.commit()
