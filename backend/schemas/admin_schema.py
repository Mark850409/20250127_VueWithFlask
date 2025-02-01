from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class AdminPath(BaseModel):
    """管理員路徑參數"""
    admin_id: int = Field(..., description='管理員ID')

class AdminCreateSchema(BaseModel):
    """創建管理員請求參數"""
    username: str = Field(..., description='用戶名', min_length=2, max_length=50)
    email: EmailStr = Field(..., description='郵箱')
    password: str = Field(..., description='密碼', min_length=6)
    role: str = Field('admin', description='角色')
    status: str = Field('active', description='狀態')
    avatar: Optional[str] = Field(None, description='頭像')

class AdminUpdateSchema(BaseModel):
    """更新管理員請求參數"""
    username: Optional[str] = Field(None, description='用戶名', min_length=2, max_length=50)
    email: Optional[EmailStr] = Field(None, description='郵箱')
    password: Optional[str] = Field(None, description='密碼', min_length=6)
    role: Optional[str] = Field(None, description='角色')
    status: Optional[str] = Field(None, description='狀態')
    avatar: Optional[str] = Field(None, description='頭像')

class AdminResponseSchema(BaseModel):
    """管理員響應數據"""
    id: int = Field(..., description='管理員ID')
    username: str = Field(..., description='用戶名')
    email: str = Field(..., description='郵箱')
    role: str = Field(..., description='角色')
    status: str = Field(..., description='狀態')
    avatar: Optional[str] = Field(None, description='頭像')
    last_login: Optional[str] = Field(None, description='最後登入時間')
    created_at: str = Field(..., description='創建時間')
    updated_at: str = Field(..., description='更新時間') 