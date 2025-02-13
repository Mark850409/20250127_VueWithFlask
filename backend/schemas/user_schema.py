from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
from dataclasses import dataclass
from flask_openapi3 import FileStorage
from pydantic import field_validator

class UserBaseSchema(BaseModel):
    """用戶基礎數據"""
    username: str = Field(..., description='用戶名稱', min_length=2, max_length=50)
    email: EmailStr = Field(..., description='電子郵件')

class UserRegisterSchema(UserBaseSchema):
    """用戶註冊請求參數"""
    username: str = Field(..., min_length=2, max_length=50, description='用戶名')
    email: EmailStr = Field(..., description='郵箱')
    password: str = Field(..., min_length=6, description='密碼')
    status: str = Field('Enabled', description='帳號狀態')

    class Config:
        schema_extra = {
            'example': {
                'username': 'test_user',
                'email': 'test@example.com',
                'password': 'password123',
                'confirmPassword': 'password123',
                'status': 'Enabled'
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
    status: Optional[str] = Field(None, description='帳號狀態')

    class Config:
        schema_extra = {
            'example': {
                'username': 'new_username',
                'email': 'new_email@example.com',
                'password': 'new_password123',
                'status': 'Disabled'
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
    status: str = Field('Enabled', description='帳號狀態')
    avatar: Optional[str] = Field(None, description='用戶頭像文件')

    class Config:
        schema_extra = {
            'example': {
                'username': 'test_user',
                'email': 'test@example.com',
                'password': 'Password123!',
                'status': 'Enabled',
                'avatar': 'file'  # 這裡會在 Swagger UI 中顯示文件上傳欄位
            }
        }

class UserAvatarParamsSchema(BaseModel):
    """頭像路徑參數"""
    filename: str = Field(..., description='頭像文件名')

class UserAvatarSchema(BaseModel):
    """用戶頭像上傳請求參數"""
    file: str = Field(..., description='頭像文件', format='binary')

    class Config:
        schema_extra = {
            'example': {
                'file': 'binary_file'
            }
        }

class FileUploadResponse(BaseModel):
    """圖片上傳響應"""
    url: str = Field(..., description='圖片URL')
    message: Optional[str] = Field(None, description='響應信息')

class UserRegisterResponse:
    """註冊響應"""
    description = '註冊成功'
    content = {
        'application/json': {
            'schema': UserResponseSchema
        }
    }

class UserRegisterMultipartSchema:
    """註冊請求體 (multipart/form-data)"""
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
                    'confirmPassword': {
                        'type': 'string',
                        'description': '確認密碼',
                        'minLength': 6,
                        'maxLength': 12
                    },
                    'status': {
                        'type': 'string',
                        'description': '帳號狀態',
                        'enum': ['Enabled', 'Disabled'],
                        'default': 'Enabled'
                    },
                    'avatar': {
                        'type': 'string',
                        'format': 'binary',
                        'description': '用戶頭像 (PNG, JPG, JPEG, GIF格式，最大2MB)'
                    }
                },
                'required': ['username', 'email', 'password', 'confirmPassword', 'status']
            }
        }
    }

class UploadFileForm(BaseModel):
    """文件上傳請求"""
    file: FileStorage = Field(
        ...,
        description='圖片文件 (支援 jpg、png、gif、webp 格式，最大 5MB)',
    )

class ForgotPasswordSchema(BaseModel):
    """忘記密碼請求參數"""
    email: EmailStr = Field(..., description='電子郵件')

    class Config:
        schema_extra = {
            'example': {
                'email': 'test@example.com'
            }
        }

class ResetPasswordSchema(BaseModel):
    """重設密碼請求參數"""
    token: str = Field(..., description='重設密碼 token')
    password: str = Field(
        ..., 
        description='新密碼 (需包含大小寫字母、數字和特殊符號)',
        min_length=6,
        max_length=12,
    )

    @field_validator('password')
    def validate_password(cls, v):
        """驗證密碼複雜度"""
        if not any(c.islower() for c in v):
            raise ValueError('密碼必須包含小寫字母')
        if not any(c.isupper() for c in v):
            raise ValueError('密碼必須包含大寫字母')
        if not any(c.isdigit() for c in v):
            raise ValueError('密碼必須包含數字')
        if not any(c in '!@#$%^&*' for c in v):
            raise ValueError('密碼必須包含特殊符號(!@#$%^&*)')
        return v

    class Config:
        schema_extra = {
            'example': {
                'token': 'reset_password_token',
                'password': 'Mark@8504091'
            }
        }

class VerifyResetTokenParams(BaseModel):
    """驗證重設密碼 token 路徑參數"""
    token: str = Field(..., description='重設密碼 token')

class VerifyResetTokenResponse(BaseModel):
    """驗證重設密碼 token 響應"""
    success: bool = Field(..., description='是否成功')
    message: Optional[str] = Field(None, description='錯誤訊息')

    class Config:
        schema_extra = {
            'example': {
                'success': True,
                'message': None
            }
        }


