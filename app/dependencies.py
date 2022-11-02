from fastapi import Header, Depends
from sqlalchemy.orm import Session

from .internal import auth
from .internal.errors import UnauthorizedError
from .db import SessionLocal
from .models import User

def get_db_session():
    """
    Зависимость для получения сессии базы данных. Закрытие сессии происходит
    автоматически.
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_current_user(
    x_token: str = Header(''),
    session: Session = Depends(get_db_session)
    ):
    """
    Зависимость для получения текущего авторизованного пользователя.
    Если пользователь не авторизован, то возвращает `None`
    """
    return auth.get_user_by_token(x_token, session)


def check_and_get_user(user: User = Depends(get_current_user)):
    """
    Зависимость для проверки авторизации пользователя,
    которая затем возвращает его.
    """
    if not user:
        raise UnauthorizedError()
    return user


def check_authorization(x_token: str = Header('')):
    """ Зависимость для проверки авторизации пользователя """
    if not auth.verify_user_token(x_token):
        raise UnauthorizedError()
