from datetime import datetime

from jose import jwt
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi import status
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError

from core.database import get_db
from crud.user import get_user_by_username
from db import User
from schemas.user import TokenPayload
from core.auth import AUTH, verify_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/login", scheme_name="JWT")


def authenticate_user(db: Session, username: str, password: str) -> User:
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    try:
        payload = jwt.decode(
            token, AUTH.JWT_SECRET_KEY, algorithms=[AUTH.ALGORITHM]
        )
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"}
            )
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

    user = get_user_by_username(db, token_data.sub)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
