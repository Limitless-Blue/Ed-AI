from fastapi import FastAPI, APIRouter, Body, Query, Path
from pydantic import BaseModel

settings_router = APIRouter(prefix="/api/settings", tags=["Settings"])


class ChangePasswordRequest(BaseModel):
    OldPassword: str
    newPassword: str


@settings_router.put("/change-password")
async def change_password(data: ChangePasswordRequest):
    return {"acknowledgement": True}


class ChangeUsernameRequest(BaseModel):
    OldUsername: str
    newUsername: str


@settings_router.put("/change-username")
async def change_username(data: ChangeUsernameRequest):
    return {"acknowledgement": True}


class ResetProgressRequest(BaseModel):
    Password: str


@settings_router.post("/reset-progress")
async def reset_progress(data: ResetProgressRequest):
    return {"acknowledgement": True}
