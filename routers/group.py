from datetime import datetime
from uuid import UUID
from typing import List

from fastapi import status
from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends
from fastapi import UploadFile, File, Form
from sqlalchemy.orm import Session


import models
from core.database import get_db
from deps.auth import get_current_active_user
from crud.device import get_device_by_uuid
from crud import group as crud_group
from schemas.group import GroupCreate, GroupUpdate, GroupDelete, DeviceUUID, GroupOut
from schemas.group import group_factory
from core.file import upload_group_file


router = APIRouter()


# @router.get("/all")
# async def get_all_group():
#     async with aiofiles.open("./tabs.json", "r", encoding="utf-8") as f:
#         return json.loads(await f.read())

@router.post("/all", summary="Get all groups", response_model=List[GroupOut])
def get_all_group(*,
                  db: Session = Depends(get_db),
                  device_uuid: DeviceUUID,
                  user: models.User = Depends(get_current_active_user)):
    device = get_device_by_uuid(db, device_uuid.device_uuid)
    if not device or device.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found"
        )
    groups = crud_group.get_all_group(db, user, device)
    return group_factory(device, groups)


@router.post("/create", summary="Create new group", response_model=GroupOut)
def create_group(*,
                 db: Session = Depends(get_db),
                 group: GroupCreate,
                 user: models.User = Depends(get_current_active_user)):
    device = get_device_by_uuid(db, group.device_uuid)
    if not device or device.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found"
        )
    uuid_exist = crud_group.get_group_by_uuid(db, group.uuid)
    if uuid_exist:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Group uuid already in use"
        )
    new_group = crud_group.create_group(db, group, user, device)
    return group_factory(device, new_group)


@router.put("/update", summary="Update group", response_model=GroupOut)
def update_group(*,
                 db: Session = Depends(get_db),
                 group: GroupUpdate,
                 user: models.User = Depends(get_current_active_user)):
    device = get_device_by_uuid(db, group.device_uuid)
    if not device or device.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found"
        )
    old_group = crud_group.get_group_by_uuid(db, group.uuid)
    if not old_group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not exist"
        )
    group = crud_group.update_group(db, old_group, group)
    return group_factory(device, group)


@router.delete("/delete", summary="Delete group")
def delete_group(*,
                 db: Session = Depends(get_db),
                 group_del: GroupDelete,
                 user: models.User = Depends(get_current_active_user)):
    group = crud_group.get_group_by_uuid(db, group_del.uuid)
    if not group or group.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Group not exist"
        )
    device = group.device
    group = crud_group.delete_group(db, group.uuid)
    return group_factory(device, group)

# TODO: 统一返回数据的格式
# TODO: 下面的两个接口都可以用上面的update方法替代


@router.post("/add_links", summary="Add links to group", response_model=GroupOut)
def add_links(*,
              db: Session = Depends(get_db),
              group_del: GroupDelete,
              user: models.User = Depends(get_current_active_user)):
    pass


@router.delete("/del_link", summary="Delete link from group")
def del_link():
    pass


@router.post("/import", summary="Import JSON file of tab groups")
async def import_group(*,
                       db: Session = Depends(get_db),
                       device_uuid: UUID = Form(),
                       file: UploadFile = File(),
                       user: models.User = Depends(get_current_active_user)):
    device = get_device_by_uuid(db, device_uuid)
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not exist"
        )
    try:
        # TODO: 限制文件名长度, 防止攻击
        file_name = await upload_group_file(user, file, datetime.now())
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    # TODO: 解析文件的流程放到异步任务中
    return {"device_uuid": device_uuid, "file": file_name}


@router.post("/export", summary="Export tab groups as JSON file")
def export_group():
    pass
