from datetime import datetime
from uuid import UUID, uuid4
from typing import List

from pydantic import BaseModel
from pydantic import Field, AnyUrl, PastDatetime

import models


class DeviceUUID(BaseModel):
    device_uuid: UUID


class Link(BaseModel):
    uuid: UUID = Field(default_factory=uuid4)
    title: str
    url: AnyUrl


class GroupBase(BaseModel):
    uuid: UUID = Field(default_factory=uuid4)
    name: str
    links: List[Link]
    status: int
    device_uuid: UUID


class GroupCreate(GroupBase):
    pass


class GroupUpdate(GroupBase):
    update_time: PastDatetime = Field(default_factory=datetime.now)


class GroupDelete(BaseModel):
    uuid: UUID


class GroupAddLinks(BaseModel):
    uuid: UUID
    links: List[Link]


class GroupDelLink(BaseModel):
    uuid: UUID
    link_uuid: UUID


class GroupOut(GroupBase):
    create_time: PastDatetime
    update_time: PastDatetime


def group_factory(device: models.Device | UUID, data: models.Group | List[models.Group]) -> GroupOut | List[GroupOut]:
    def handle(data: models.Group):
        return GroupOut(uuid=data.uuid,
                        name=data.name,
                        links=data.links,
                        status=data.status,
                        device_uuid=device if isinstance(
                            device, UUID) else device.uuid,
                        create_time=data.create_time,
                        update_time=data.update_time)
    # TODO: 自动化转换
    if isinstance(data, list):
        return [handle(item) for item in data]
    return handle(data)
