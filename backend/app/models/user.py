from sqlalchemy import Column, Integer, String, LargeBinary, Boolean

from . import Base

class User(Base):
    """ Модель пользователя """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    login = Column(String(32), unique=True, index=True)
    salt = Column(LargeBinary())
    password_key = Column(LargeBinary())
    is_admin = Column(Boolean(), default=False)
