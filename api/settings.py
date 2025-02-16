from fastapi import APIRouter
from pydantic import BaseModel

settings_router = APIRouter(prefix="/api/settings", tags=["Settings"])


class ChangePasswordRequest(BaseModel):
    OldPassword: str
    newPassword: str


@settings_router.put("/change-password")
async def change_password(data: ChangePasswordRequest):
    return {"acknowledgement": True}
