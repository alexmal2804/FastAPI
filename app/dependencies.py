from fastapi import Depends, HTTPException, status

from .db import get_user
from .models import UserWithData
from .security import get_user_from_token


def get_current_user(current_username: str = Depends(get_user_from_token)) -> UserWithData:
    """Получаем текущего пользователя по имени из токена"""
    user = get_user(current_username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
