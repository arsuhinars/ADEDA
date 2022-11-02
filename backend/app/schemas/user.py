from pydantic import BaseModel

class UserCreate(BaseModel):
    """ Схема, используемая для создания пользователя """
    login: str
    password: str
    is_admin = False
