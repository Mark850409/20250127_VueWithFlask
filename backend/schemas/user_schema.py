from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
from dataclasses import dataclass

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

@dataclass
class UserRegisterFileSchema:
    """用戶註冊文件上傳"""
    avatar: Optional[str] = Field(None, description='用戶頭像文件')

class UserRegisterFormSchema(BaseModel):
    """用戶註冊表單"""
    username: str = Field(..., description='用戶名稱', min_length=2, max_length=50)
    email: EmailStr = Field(..., description='電子郵件')
    password: str = Field(..., description='密碼', min_length=6, max_length=12)
    avatar: Optional[str] = Field(None, description='用戶頭像文件')

    class Config:
        schema_extra = {
            'example': {
                'username': 'test_user',
                'email': 'test@example.com',
                'password': 'Password123!',
                'avatar': 'file'  # 這裡會在 Swagger UI 中顯示文件上傳欄位
            }
        }

class UserAvatarParamsSchema(BaseModel):
    """頭像路徑參數"""
    filename: str = Field(..., description='頭像文件名')

class UserAvatarResponse:
    """頭像響應"""
    description = '頭像文件'
    content = {
        'image/*': {
            'schema': {
                'type': 'string',
                'format': 'binary'
            }
        }
    }

class UserRegisterResponse:
    """註冊響應"""
    description = '註冊成功'
    content = {
        'application/json': {
            'schema': UserResponseSchema
        }
    }

class UserRegisterRequestBody:
    """註冊請求體"""
    description = '用戶註冊表單'
    content = {
        'multipart/form-data': {
            'schema': {
                'type': 'object',
                'properties': {
                    'username': {
                        'type': 'string',
                        'description': '用戶名稱',
                        'minLength': 2,
                        'maxLength': 50
                    },
                    'email': {
                        'type': 'string',
                        'format': 'email',
                        'description': '電子郵件'
                    },
                    'password': {
                        'type': 'string',
                        'description': '密碼',
                        'minLength': 6,
                        'maxLength': 12
                    },
                    'avatar': {
                        'type': 'string',
                        'format': 'binary',
                        'description': '用戶頭像 (PNG, JPG, JPEG, GIF格式，最大2MB)'
                    }
                },
                'required': ['username', 'email', 'password']
            }
        }
    } 