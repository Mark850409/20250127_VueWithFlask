from flask_openapi3 import APIBlueprint, Tag
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from services.user_service import UserService
from datetime import datetime

# API 藍圖和標籤
user_bp = APIBlueprint('users', __name__, url_prefix='/api/users')
user_tag = Tag(name='users', description='用戶管理操作')

# 請求和響應模型
class UserBase(BaseModel):
    username: str
    email: EmailStr
    avatar: Optional[str]
    status: str = 'Enabled'

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    avatar: Optional[str]
    status: Optional[str]

class UserResponse(UserBase):
    id: int
    register_time: datetime
    update_time: datetime

    class Config:
        orm_mode = True

class UserList(BaseModel):
    users: List[UserResponse]

class ErrorResponse(BaseModel):
    message: str

@user_bp.get('/', tags=[user_tag])
def get_users():
    """獲取所有用戶列表"""
    service = UserService()
    users = service.get_all_users()
    return UserList(users=users).dict()

@user_bp.post('/', tags=[user_tag])
def create_user(body: UserCreate):
    """創建新用戶"""
    service = UserService()
    user = service.create_user(body.dict())
    return UserResponse.from_orm(user).dict(), 201

@user_bp.get('/<int:user_id>', tags=[user_tag])
def get_user(user_id: int):
    """獲取指定用戶信息"""
    service = UserService()
    user = service.get_user(user_id)
    if not user:
        return ErrorResponse(message='用戶不存在').dict(), 404
    return UserResponse.from_orm(user).dict()

@user_bp.put('/<int:user_id>', tags=[user_tag])
def update_user(user_id: int, body: UserUpdate):
    """更新用戶信息"""
    service = UserService()
    user = service.update_user(user_id, body.dict(exclude_unset=True))
    if not user:
        return ErrorResponse(message='用戶不存在').dict(), 404
    return UserResponse.from_orm(user).dict()

@user_bp.delete('/<int:user_id>', tags=[user_tag])
def delete_user(user_id: int):
    """刪除用戶"""
    service = UserService()
    if service.delete_user(user_id):
        return '', 204
    return ErrorResponse(message='用戶不存在').dict(), 404 