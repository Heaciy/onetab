from sqlalchemy.orm import Session

from db import User
from schemas.user import UserCreate
from core.auth import get_hashed_password


def get_user_by_username(db: Session, username: str) -> User | None:
    user = db.query(User).filter(User.username == username).first()
    return user


def get_user_by_email(db: Session, email: str) -> User | None:
    user = db.query(User).filter(User.email == email).first()
    return user


def create_user(db: Session, user: UserCreate) -> User:
    data = user.model_dump(exclude=["password_again"])
    data["password"] = get_hashed_password(data["password"])
    new_user = User(**data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
