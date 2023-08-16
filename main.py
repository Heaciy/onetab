import uvicorn
from fastapi import FastAPI

from routers.user import router as user_router
from routers.group import router as group_router
from routers.device import router as device_router


app = FastAPI()
app.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(group_router, prefix="/group", tags=["group"])
app.include_router(device_router, prefix="/device", tags=["device"])


if __name__ == "__main__":
    # uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
