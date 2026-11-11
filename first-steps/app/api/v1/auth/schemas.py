from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field

Role = Literal["user", "editor", "admin"]


class UserBase(BaseModel):
    email: EmailStr
    full_name: str | None = None
    model_config = ConfigDict(from_attributes=True)


class UserPublic(UserBase):
    id: int
    role: Role
    is_active: bool


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(
        min_length=8,
        max_length=72
    )
    full_name: str = Field(
        min_length=3,
        max_length=70
    )


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(
        max_length=72
    )


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserPublic


class RoleUpdate(BaseModel):
    role: Role


class TokenData(BaseModel):
    sub: str
    username: str
