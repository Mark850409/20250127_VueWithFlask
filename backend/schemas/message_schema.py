from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class MessageCreateSchema(BaseModel):
    """創建留言請求參數"""
    content: str = Field(..., description='評論內容', min_length=1)
    store_id: int = Field(..., description='店家ID')
    rating: float = Field(..., description='評分', ge=0, le=5)
    
    class Config:
        schema_extra = {
            'example': {
                'content': '這家店的珍珠奶茶真的很好喝！',
                'store_id': 1,
                'rating': 4.5
            }
        }

class MessageUpdateSchema(BaseModel):
    """更新留言請求參數"""
    content: Optional[str] = Field(None, description='評論內容', min_length=1)
    rating: Optional[float] = Field(None, description='評分', ge=0, le=5)
    status: Optional[str] = Field(None, description='留言狀態', pattern='^(pending|approved|rejected)$')
    
    class Config:
        schema_extra = {
            'example': {
                'content': '這是更新後的評論內容',
                'rating': 4.0,
                'status': 'approved'
            }
        }

class MessageResponseSchema(BaseModel):
    """留言響應數據"""
    id: int = Field(..., description='評論ID')
    user_id: int = Field(..., description='用戶ID')
    store_id: int = Field(..., description='店家ID')
    user: str = Field(..., description='用戶名')
    store_name: str = Field(..., description='店家名稱')
    store_image: str = Field(..., description='店家圖片')
    rating: float = Field(..., description='評分')
    content: str = Field(..., description='評論內容')
    created_at: str = Field(..., description='創建時間')
    updated_at: str = Field(..., description='更新時間')
    status: str = Field(..., description='狀態')
    replies: list = Field(default=[], description='回覆列表')
    
    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'id': 1,
                'user_id': 1,
                'store_id': 1,
                'user': 'test_user',
                'store_name': '清心福全',
                'store_image': 'https://example.com/shop1.jpg',
                'rating': 4.5,
                'content': '這家店的珍珠奶茶真的很好喝！',
                'created_at': '2024-02-01 12:00:00',
                'updated_at': '2024-02-01 12:00:00',
                'status': 'approved',
                'replies': [
                    {
                        'id': 1,
                        'user_name': '店家',
                        'content': '謝謝您的支持！',
                        'create_time': '2024-02-01 12:30:00'
                    }
                ]
            }
        } 