from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime

class UserBaseSchema(BaseModel):
    """用戶基礎數據"""
    username: str = Field(..., description='用戶名稱', min_length=2, max_length=50)
    email: EmailStr = Field(..., description='電子郵件')

class UserRegisterSchema(UserBaseSchema):
    """用戶註冊請求參數"""
    password: str = Field(..., description='密碼', min_length=6)

    class Config:
        schema_extra = {
            'example': {
                'username': 'test_user',
                'email': 'test@example.com',
                'password': 'password123'
            }
        }

class UserLoginSchema(BaseModel):
    """用戶登入請求參數"""
    email: EmailStr = Field(..., description='電子郵件')
    password: str = Field(..., description='密碼')

    class Config:
        schema_extra = {
            'example': {
                'email': 'test@example.com',
                'password': 'password123'
            }
        }

class UserUpdateSchema(BaseModel):
    """更新用戶請求參數"""
    username: Optional[str] = Field(None, description='用戶名稱', min_length=2, max_length=50)
    email: Optional[EmailStr] = Field(None, description='電子郵件')
    password: Optional[str] = Field(None, description='密碼', min_length=6)

    class Config:
        schema_extra = {
            'example': {
                'username': 'new_username',
                'email': 'new_email@example.com',
                'password': 'new_password123'
            }
        }

class UserResponseSchema(UserBaseSchema):
    """用戶響應數據"""
    id: int = Field(..., description='用戶ID')
    created_at: datetime = Field(..., description='創建時間')
    updated_at: datetime = Field(..., description='更新時間')

    class Config:
        orm_mode = True

class UserPath(BaseModel):
    """用戶路徑參數"""
    user_id: int = Field(..., description='用戶ID') 