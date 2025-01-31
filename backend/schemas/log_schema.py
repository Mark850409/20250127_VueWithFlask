from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class LogBaseSchema(BaseModel):
    """日誌基礎數據"""
    user_id: Optional[int] = Field(None, description='用戶ID，不指定表示系統操作')
    action: str = Field(..., description='操作類型', min_length=1, max_length=50)
    description: str = Field(..., description='操作描述')
    ip_address: Optional[str] = Field(None, description='IP地址')
    status: Optional[str] = Field(None, description='狀態')

class LogCreateSchema(LogBaseSchema):
    """創建日誌請求參數"""
    class Config:
        schema_extra = {
            'example': {
                'user_id': 1,
                'action': 'login',
                'description': '用戶登入系統',
                'ip_address': '127.0.0.1',
                'status': 'success'
            }
        }

class LogResponseSchema(LogBaseSchema):
    """日誌響應數據"""
    id: int = Field(..., description='日誌ID')
    username: Optional[str] = Field(None, description='操作用戶名稱')
    created_at: datetime = Field(..., description='創建時間')

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'id': 1,
                'user_id': 1,
                'username': 'mark',
                'action': 'login',
                'description': '用戶登入系統',
                'ip_address': '127.0.0.1',
                'status': 'success',
                'created_at': '2024-01-31 13:18:29'
            }
        }

class LogPath(BaseModel):
    """日誌路徑參數"""
    log_id: int = Field(..., description='日誌ID')

class UserPath(BaseModel):
    """用戶路徑參數"""
    user_id: int = Field(..., description='用戶ID') 