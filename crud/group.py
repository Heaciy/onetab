from datetime import datetime
from uuid import UUID
from typing import List

from sqlalchemy.orm import Session

import models
from schemas.group import GroupBase, GroupCreate, GroupUpdate
from db import Group


def get_group_by_uuid(db: Session, group_uuid: UUID) -> models.Group:
    group = db.query(Group).filter(Group.uuid == group_uuid).first()
    return group


def get_all_group(db: Session, user: models.User, device: models.Device) -> List[models.Group]:
    groups = db.query(Group).filter_by(
        user_id=user.id, device_id=device.id).all()
    return groups


def create_group(db: Session, group: GroupCreate, user: models.User, device: models.Device) -> models.Group:
    new_group = Group(**group.model_dump(mode="json", exclude=["device_uuid"]),
                      user_id=user.id,
                      device_id=device.id)
    db.add(new_group)
    db.commit()
    return new_group


def delete_group(db: Session, group_uuid: UUID) -> models.Group:
    group = db.query(Group).filter(Group.uuid == group_uuid).first()
    db.delete(group)
    db.commit()
    return group


def update_group(db: Session, old_group: models.Group, new_group: GroupUpdate) -> models.Group:
    for k, v in new_group.model_dump(mode="json").items():
        if hasattr(old_group, k):
            setattr(old_group, k, v)
    db.add(old_group)
    db.commit()
    return old_group
