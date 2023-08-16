from typing import List
from uuid import UUID

from sqlalchemy.orm import Session
from schemas.device import DeviceCreate, DeviceUpdate

import models
from db import Device


def creata_device(db: Session, device: DeviceCreate, user: models.User) -> models.Device:
    device = Device(**device.model_dump(), user_id=user.id)
    db.add(device)
    db.commit()
    db.refresh(device)
    return device


def update_device(db: Session, old_device: models.Device, device: DeviceUpdate) -> models.Device:
    for k, v in device.model_dump().items():
        if hasattr(old_device, k):
            setattr(old_device, k, v)
    db.add(old_device)
    db.commit()
    return old_device


def get_all_device(db: Session, user: models.User) -> List[models.Device]:
    devices = db.query(Device).filter(Device.user_id == user.id)
    return devices


def get_device_by_uuid(db: Session, uuid: UUID) -> models.Device | None:
    device = db.query(Device).filter(Device.uuid == uuid).first()
    return device


def delete_device_by_uuid(db: Session, uuid: UUID) -> models.Device | None:
    device = db.query(Device).filter(Device.uuid == uuid).first()
    db.delete(device)
    db.commit()
    return device
