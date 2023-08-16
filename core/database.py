from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from sqlalchemy.ext.declarative import declarative_base


from settings import settings

Base = declarative_base()
engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


class BaseModel(Base):
    __abstract__ = True
    __table_args__ = {'schema': 'public'}
    create_time = Column(DateTime, default=datetime.now,
                         server_default=text("(now())"))
    update_time = Column(DateTime, default=datetime.now,
                         onupdate=datetime.now, server_default=text("(now())"))


SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
