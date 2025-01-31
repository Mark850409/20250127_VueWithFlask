from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class UserBaseSchema(BaseModel):
    """用戶基礎數據"""
    username: str = Field(..., description='用戶名', min_length=2, max_length=50)
    email: EmailStr = Field(..., description='電子郵件')
    status: Optional[str] = Field('Enabled', description='狀態：Enabled-啟用，Disabled-禁用')
    avatar: Optional[str] = Field(None, description='頭像URL')

class UserCreateSchema(UserBaseSchema):
    """創建用戶請求參數"""
    password: str = Field(..., description='密碼', min_length=6, max_length=20)

    class Config:
        schema_extra = {
            'example': {
                'username': 'mark',
                'email': 'mark@example.com',
                'password': 'password123',
                'status': 'Enabled',
                'avatar': 'https://example.com/avatar.jpg'
            }
        }

class UserUpdateSchema(BaseModel):
    """更新用戶請求參數"""
    username: Optional[str] = Field(None, description='用戶名', min_length=2, max_length=50)
    email: Optional[EmailStr] = Field(None, description='電子郵件')
    password: Optional[str] = Field(None, description='密碼', min_length=6, max_length=20)
    status: Optional[str] = Field(None, description='狀態：Enabled-啟用，Disabled-禁用')
    avatar: Optional[str] = Field(None, description='頭像URL')

    class Config:
        schema_extra = {
            'example': {
                'username': 'mark_new',
                'email': 'mark_new@example.com',
                'password': 'newpassword123',
                'status': 'Enabled',
                'avatar': 'https://example.com/new_avatar.jpg'
            }
        }

class UserResponseSchema(UserBaseSchema):
    """用戶響應數據"""
    id: int = Field(..., description='用戶ID')
    register_time: datetime = Field(..., description='註冊時間')
    update_time: datetime = Field(..., description='更新時間')

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'id': 1,
                'username': 'mark',
                'email': 'mark@example.com',
                'status': 'Enabled',
                'avatar': 'https://example.com/avatar.jpg',
                'register_time': '2024-01-31 13:18:29',
                'update_time': '2024-01-31 13:18:29'
            }
        }

class UserPath(BaseModel):
    """用戶路徑參數"""
    user_id: int = Field(..., description='用戶ID') 