from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import models
from schemas.user import UserCreate, UserBase, TokenSchema
from crud.user import get_user_by_username, get_user_by_email, create_user
from core.auth import create_access_token, create_refresh_token
from core.database import get_db
from deps.auth import authenticate_user, get_current_active_user


router = APIRouter()


@router.post("/signup", summary="Create new user", response_model=UserBase)
async def signup(data: UserCreate, db: Session = Depends(get_db)):
    exist_user = get_user_by_username(
        db, data.username) or get_user_by_email(db, data.email)
    if exist_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered")
    exist_user = get_user_by_email(db, data.email)
    if exist_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered")
    return create_user(db, data)


@router.post("/login", summary="Create access and refresh tokens for user", response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return {
        "access_token": create_access_token(user.username),
        "refresh_token": create_refresh_token(user.username),
    }


@router.get("/me", summary="Get details of currently logged in user", response_model=UserBase)
async def get_user_me(user: models.User = Depends(get_current_active_user)):
    return user
