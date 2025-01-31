from flask_openapi3 import APIBlueprint, Tag
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from services.user_service import UserService
from datetime import datetime
import pytz
from schemas.user_schema import *

# 設定台灣時區
tw_tz = pytz.timezone('Asia/Taipei')

# API 藍圖和標籤
user_bp = APIBlueprint('users', __name__, url_prefix='/api/users')
user_tag = Tag(name='users', description='用戶管理')

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

    @classmethod
    def from_orm(cls, obj):
        # 將時間轉換為台灣時區
        if obj.register_time:
            obj.register_time = obj.register_time.replace(tzinfo=pytz.UTC).astimezone(tw_tz)
        if obj.update_time:
            obj.update_time = obj.update_time.replace(tzinfo=pytz.UTC).astimezone(tw_tz)
        return super().from_orm(obj)

    class Config:
        orm_mode = True
        json_encoders = {
            datetime: lambda dt: dt.strftime('%Y-%m-%d %H:%M:%S')
        }

class UserList(BaseModel):
    users: List[UserResponse]

class ErrorResponse(BaseModel):
    message: str

# 添加請求參數模型
class UserPath(BaseModel):
    user_id: int

class UserQuery(BaseModel):
    user_id: Optional[int] = None

@user_bp.get('/', tags=[user_tag])
def get_users():
    """獲取所有用戶
    
    Returns:
        200 (UserResponseSchema): 用戶列表
        500: 服務器錯誤
    """
    service = UserService()
    users = service.get_all_users()
    return {'users': [user.to_dict() for user in users]}

@user_bp.post('/', tags=[user_tag])
def create_user(body: UserCreateSchema):
    """創建用戶
    
    Args:
        body (UserCreateSchema): 用戶數據
        
    Returns:
        201 (UserResponseSchema): 創建成功
        400: 用戶名或郵箱已存在
        500: 服務器錯誤
    """
    service = UserService()
    
    # 檢查用戶名是否已存在
    if service.get_user_by_username(body.username):
        return {'message': '用戶名已存在'}, 400
    
    # 檢查郵箱是否已存在
    if service.get_user_by_email(body.email):
        return {'message': '郵箱已存在'}, 400
    
    user = service.create_user(body.dict())
    return user.to_dict(), 201

@user_bp.get('/<int:user_id>', tags=[user_tag])
def get_user(path: UserPath):
    """獲取指定用戶信息"""
    service = UserService()
    user = service.get_user(path.user_id)
    if not user:
        return ErrorResponse(message='用戶不存在').dict(), 404
    return UserResponse.from_orm(user).dict()

@user_bp.put('/<int:user_id>', tags=[user_tag])
def update_user(path: UserPath, body: UserUpdateSchema):
    """更新用戶
    
    Args:
        path (UserPath): 路徑參數
            user_id (int): 要更新的用戶ID
        body (UserUpdateSchema): 更新數據
            
    Example:
        PUT /api/users/1
        {
            "username": "mark_new",
            "email": "mark_new@example.com"
        }
        
    Returns:
        200 (UserResponseSchema): 更新成功
        400: 用戶名或郵箱已存在
        404: 用戶不存在
        500: 服務器錯誤
    """
    service = UserService()
    user_id = path.user_id
    
    # 檢查用戶是否存在
    existing_user = service.get_user(user_id)
    if not existing_user:
        return {'message': '用戶不存在'}, 404
    
    update_data = body.dict(exclude_unset=True)
    
    # 如果要更新用戶名，檢查是否已存在
    if 'username' in update_data:
        user = service.get_user_by_username(update_data['username'])
        if user and user.id != user_id:
            return {'message': '用戶名已存在'}, 400
    
    # 如果要更新郵箱，檢查是否已存在
    if 'email' in update_data:
        user = service.get_user_by_email(update_data['email'])
        if user and user.id != user_id:
            return {'message': '郵箱已存在'}, 400
    
    user = service.update_user(user_id, update_data)
    return user.to_dict()

@user_bp.delete('/<int:user_id>', tags=[user_tag])
def delete_user(path: UserPath):
    """刪除用戶
    
    Args:
        path (UserPath): 路徑參數
            user_id (int): 要刪除的用戶ID
            
    Example:
        DELETE /api/users/1
        
    Returns:
        204: 刪除成功
        404: 用戶不存在
        500: 刪除失敗
    """
    service = UserService()
    user_id = path.user_id
    
    # 檢查用戶是否存在
    existing_user = service.get_user(user_id)
    if not existing_user:
        return {'message': '用戶不存在'}, 404
    
    if service.delete_user(user_id):
        return '', 204
    return {'message': '刪除失敗'}, 500 