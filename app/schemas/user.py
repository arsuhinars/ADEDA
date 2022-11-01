from pydantic import BaseModel

class UserCreate(BaseModel):
    login: str
    password: str
    is_admin = False


class UserBase(BaseModel):
    id: int
    login: str
