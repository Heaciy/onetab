from sqlalchemy import Column, ForeignKey
from sqlalchemy import Text, JSON, BigInteger, SmallInteger, Uuid, Boolean
from sqlalchemy.sql import text
from sqlalchemy.orm import relationship

from core.database import BaseModel


class User(BaseModel):
    __tablename__ = 'user'
    id = Column(BigInteger, primary_key=True)
    uuid = Column(Uuid, unique=True, nullable=False,
                  server_default=(text("gen_random_uuid()")))
    username = Column(Text, nullable=False)
    email = Column(Text, unique=True, nullable=False)
    password = Column(Text)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    devices = relationship("Device", back_populates="user")
    groups = relationship("Group", back_populates="user")


class Device(BaseModel):
    __tablename__ = 'device'
    id = Column(BigInteger, primary_key=True)
    uuid = Column(Uuid, unique=True, nullable=False,
                  server_default=(text("gen_random_uuid()")))
    name = Column(Text, nullable=False)
    user_id = Column(BigInteger, ForeignKey("public.user.id"))
    user = relationship("User", back_populates="devices")
    groups = relationship("Group", back_populates="device")


class Group(BaseModel):
    __tablename__ = 'group'
    id = Column(BigInteger, primary_key=True)
    uuid = Column(Uuid, unique=True, nullable=False,
                  server_default=(text("gen_random_uuid()")))
    name = Column(Text)
    links = Column(JSON, nullable=False)
    status = Column(SmallInteger)
    user_id = Column(BigInteger, ForeignKey("public.user.id"))
    device_id = Column(BigInteger, ForeignKey("public.device.id"))
    user = relationship("User", back_populates="groups")
    device = relationship("Device", back_populates="groups")
