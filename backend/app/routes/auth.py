from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from ..dependencies import get_db_session, check_and_get_user
from ..internal.auth import authenticate_user, create_jwt_token
from ..internal.auth import create_user as auth_create_user
from ..internal.errors import AppError, ForbiddenError
from ..models import User
from ..schemas import UserCreate

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

@router.get(
    '/get_token',
    summary='Авторизоваться и получить токен'
    )
def get_token(
    login: str,
    password: str,
    session: Session = Depends(get_db_session)
    ):
    """
    Метод авторизации пользователя. После успешного выполнения возвращает JSON
    объект с полем `token`, в котором записан JWT токен. Для доступа к некоторым
    методам требуется передать его в параметрах запроса как `token`.

    Параметры запроса:
    * `login` - логин пользователя
    * `password` - пароль для авторизации
    """
    user = authenticate_user(login, password, session)
    if not user:
        raise AppError('User does not exist', 400)
    return JSONResponse({'token': create_jwt_token(user)})


@router.post(
    '/create_user',
    summary='Зарегистрировать нового пользователя')
def create_user(
    user: UserCreate,
    curr_user: User = Depends(check_and_get_user),
    session: Session = Depends(get_db_session)):
    """
    Метод регистрации нового пользователя. Для доступа требуется, чтобы 
    пользователь был администратором.

    В теле запроса необходимо передать поля в формате JSON:
    `login`, `password`, `is_admin`(опционально) 
    """
    if not curr_user.is_admin:
        raise ForbiddenError()
    auth_create_user(user, session)
    return JSONResponse({})
