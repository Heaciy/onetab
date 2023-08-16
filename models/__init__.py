from uuid import UUID
from typing import List

from pydantic import BaseModel as Base
from pydantic import EmailStr, AnyUrl, PastDatetime


class BaseModel(Base):
    create_time: PastDatetime
    update_time: PastDatetime


class User(BaseModel):
    id: int
    uuid: UUID
    username: str
    email: EmailStr


class Device(BaseModel):
    id: int
    uuid: UUID
    name: str
    user_id: int
    user: User


class Link(BaseModel):
    uuid: UUID
    title: str
    url: AnyUrl
    # domain: str


class Group(BaseModel):
    id: int
    uuid: UUID
    name: str
    links: List[Link]
    status: int
    user_id: int
    device_id: int
    user: User
    device: Device
