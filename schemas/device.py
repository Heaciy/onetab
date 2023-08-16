from datetime import datetime

from uuid import UUID, uuid4
from pydantic import BaseModel, Field, PastDatetime


class DeviceBase(BaseModel):
    name: str = Field(max_length=16)
    uuid: UUID = Field(default_factory=uuid4)


class DeviceCreate(DeviceBase):
    pass


class DeviceUpdate(DeviceBase):
    update_time: PastDatetime = Field(default_factory=datetime.now)


class DeviceDetele(BaseModel):
    uuid: UUID
