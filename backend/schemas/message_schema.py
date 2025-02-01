from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class MessageCreateSchema(BaseModel):
    """創建留言請求參數"""
    content: str = Field(..., description='留言內容', min_length=1)
    
    class Config:
        schema_extra = {
            'example': {
                'content': '這是一條測試留言'
            }
        }

class MessageUpdateSchema(BaseModel):
    """更新留言請求參數"""
    content: str = Field(..., description='留言內容', min_length=1)
    
    class Config:
        schema_extra = {
            'example': {
                'content': '這是更新後的留言內容'
            }
        }

class MessageResponseSchema(BaseModel):
    """留言響應數據"""
    id: int = Field(..., description='留言ID')
    user_id: int = Field(..., description='用戶ID')
    user: str = Field(..., description='用戶名')
    content: str = Field(..., description='留言內容')
    created_at: str = Field(..., description='創建時間')
    updated_at: str = Field(..., description='更新時間')
    
    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'id': 1,
                'user_id': 1,
                'user': 'test_user',
                'content': '這是一條測試留言',
                'created_at': '2024-02-01 12:00:00',
                'updated_at': '2024-02-01 12:00:00'
            }
        } 