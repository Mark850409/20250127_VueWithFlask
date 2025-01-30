from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBaseSchema(BaseModel):
    username: str
    email: EmailStr
    avatar: Optional[str]
    status: str = 'Enabled'

class UserCreateSchema(UserBaseSchema):
    password: str

class UserUpdateSchema(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    avatar: Optional[str]
    status: Optional[str]

class UserSchema(UserBaseSchema):
    id: int
    register_time: datetime
    update_time: datetime

    class Config:
        orm_mode = True 