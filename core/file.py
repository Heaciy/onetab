import hashlib
from datetime import datetime, timedelta
from base64 import b64encode
from pathlib import Path
from datetime import datetime

import aiofiles
import aiofiles.os
from fastapi import UploadFile

from settings import settings
from models import User


def base64str(str_: str) -> str:
    return b64encode(str_.encode()).decode()


async def get_file_md5(file: UploadFile):
    md5_hash = hashlib.md5()
    while chunk := await file.read(settings.FILE.READ_BLOCK_SIZE):
        md5_hash.update(chunk)
    await file.seek(0)  # 复原文件指针
    return md5_hash.hexdigest()


def get_upload_directory(user: User):
    return Path(settings.FILE.UPLOAD_FILE_PATH) / base64str(user.username)


async def get_upload_file_path(user: User, file: UploadFile, date_time: datetime, md5: str = None) -> Path:
    file_md5 = await get_file_md5(file) if not md5 else md5
    # filepath_obj = Path(file.filename)
    # new_filename = filepath_obj.with_stem(base64str(filepath_obj.stem))
    # 格式: 秒级时间戳_文件MD5值_文件名BASE64值
    filename = f"{int(date_time.timestamp())}_{file_md5}_{base64str(file.filename)}"
    upload_path = get_upload_directory(user)
    return upload_path / filename


async def is_duplicate_file(user: User, file: UploadFile = None, md5: str = None):
    """检测是否存相同的文件"""
    if not md5:
        if not file:
            raise Exception("Param file and md5 can't both be None")
        md5 = await get_file_md5(file)
    upload_path = get_upload_directory(user)  # 默认此路径下只有文件
    if not upload_path.exists():
        return False
    filenames = [filename for filename in await aiofiles.os.listdir(upload_path)]
    for filename in filenames:
        segments = filename.split("_")
        if len(segments) > 2 and segments[1] == md5:
            # TODO: 加入文件名称判断 / 返回同名文件
            return True
    return False


async def can_upload_file_today(user: User):
    """判断用户今天还能不能上传文件"""
    upload_path = get_upload_directory(user)  # 默认此路径下只有文件
    if not upload_path.exists():
        return True
    filenames = [filename for filename in await aiofiles.os.listdir(upload_path)]
    # 获取今天的时间戳 开始到结束
    datetime_now = datetime.now()
    today_start = datetime_now.replace(
        hour=0, minute=0, second=0, microsecond=0)
    tomorrow_start = today_start + timedelta(days=1)
    # 优化点: 加排序
    timestamps = [int(filename.split("_")[0]) for filename in filenames]
    today_timestamps = [timestamp for timestamp in timestamps if
                        timestamp >= today_start.timestamp() and
                        timestamp < tomorrow_start.timestamp()]
    if len(today_timestamps) > settings.FILE.MAX_UPLOAD_NUM_PERR_DAY:
        return False
    return True


async def upload_group_file(user: User, file: UploadFile, date_time: datetime):
    # TODO: 限制上传文件的大小 限制每天上传的次数 限制用户文件个数 只保留最近一个月的?
    file_md5 = await get_file_md5(file)

    # 检查今天是否还能够上传文件
    if not await can_upload_file_today(user):
        raise Exception("Files uploaded today has reached the upper limit")
    # 检查文件类型
    if file.content_type not in settings.FILE.ALLOWED_GROUP_FILE_TYPE:
        raise Exception("File type not supported")
    # 检查文件大小
    if file.size > settings.FILE.MAX_FILE_SIZE:
        raise Exception("The maximum file size cannot exceed 8MB")
    # 检查是否是重复文件
    if await is_duplicate_file(user=user, md5=file_md5):
        raise Exception("Same file already exists")

    # 上传文件
    file_path = await get_upload_file_path(user, file, date_time, md5=file_md5)
    dir_path = file_path.parent
    await aiofiles.os.makedirs(dir_path, exist_ok=True)
    async with aiofiles.open(file_path, mode="wb+") as f:
        while chunk := await file.read(settings.FILE.READ_BLOCK_SIZE):
            await f.write(chunk)
    return file_path.name
