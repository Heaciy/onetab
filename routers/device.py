from typing import List

from fastapi import APIRouter
from fastapi import status
from fastapi import HTTPException
from fastapi import Depends
from core.database import get_db
from sqlalchemy.orm import Session

import models
from deps.auth import get_current_active_user
from schemas.device import DeviceCreate, DeviceBase, DeviceDetele, DeviceUpdate
from crud import device as crud_device

router = APIRouter()


@router.post("/create", summary="Create new device", response_model=DeviceBase)
def create_device(*,
                  db: Session = Depends(get_db),
                  device: DeviceCreate,
                  user: models.User = Depends(get_current_active_user)):
    device = crud_device.creata_device(db, device, user)
    return device


@router.put("/update", summary="Update device", response_model=DeviceBase)
def update_device(*,
                  db: Session = Depends(get_db),
                  device: DeviceUpdate,
                  user: models.User = Depends(get_current_active_user)):
    old_device = crud_device.get_device_by_uuid(db, device.uuid)
    if not old_device or old_device.user_id != user.id:
        return HTTPException(
            status_code=status,
            detail="Device not exist"
        )
    device = crud_device.update_device(db, old_device, device)
    return device


@router.get("/all", summary="Get all device", response_model=List[DeviceBase])
def get_all_device(*,
                   db: Session = Depends(get_db),
                   user: models.User = Depends(get_current_active_user)):
    devices = crud_device.get_all_device(db, user)
    return devices


@router.delete("/delete", summary="Delete device", response_model=DeviceBase)
def delete_device(*,
                  db: Session = Depends(get_db),
                  device: DeviceDetele,
                  user: models.User = Depends(get_current_active_user)):
    device = crud_device.get_device_by_uuid(db, device.uuid)
    if not device or device.user_id != user.id:
        return HTTPException(
            status_code=status,
            detail="Device not exist"
        )
    device = crud_device.delete_device_by_uuid(db, device.uuid)
    return device
