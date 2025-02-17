from fastapi import FastAPI, APIRouter, Body, Query, Path
from pydantic import BaseModel
from api.api_functions.settings_functions import change_password_database, change_username_database

settings_router = APIRouter(prefix="/api/settings", tags=["Settings"])


class ChangePasswordRequest(BaseModel):
    OldPassword: str
    newPassword: str


@settings_router.put("/change-password")
async def change_password(data: ChangePasswordRequest):
    return change_password_database(data.OldPassword, data.newPassword)


class ChangeUsernameRequest(BaseModel):
    OldUsername: str
    newUsername: str


@settings_router.put("/change-username")
async def change_username(data: ChangeUsernameRequest):
    return change_username_database(data.OldUsername, data.newUsername)


class ResetProgressRequest(BaseModel):
    Password: str


# TODO: Implement the reset_progress endpoint
@settings_router.post("/reset-progress")
async def reset_progress(data: ResetProgressRequest):
    return {"acknowledgement": True}
