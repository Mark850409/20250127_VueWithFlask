from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class StoreBaseSchema(BaseModel):
    """店家基礎數據"""
    name: str = Field(..., description='店家名稱', min_length=1, max_length=100)
    address: str = Field(..., description='店家地址')
    city: str = Field(..., description='所在城市')
    phone: Optional[str] = Field(None, description='聯絡電話')
    business_hours: Optional[str] = Field(None, description='營業時間')
    description: Optional[str] = Field(None, description='店家描述')
    image_url: Optional[str] = Field(None, description='店家圖片URL')
    status: Optional[str] = Field('active', description='營業狀態：active-營業中，closed-已歇業')

class StoreCreateSchema(StoreBaseSchema):
    """創建店家請求參數"""
    class Config:
        schema_extra = {
            'example': {
                'name': '春水堂',
                'address': '台北市信義區信義路五段7號',
                'city': '台北市',
                'phone': '02-27201234',
                'business_hours': '10:00-22:00',
                'description': '台灣珍珠奶茶始祖',
                'image_url': 'https://example.com/store.jpg',
                'status': 'active'
            }
        }

class StoreUpdateSchema(BaseModel):
    """更新店家請求參數"""
    name: Optional[str] = Field(None, description='店家名稱', min_length=1, max_length=100)
    address: Optional[str] = Field(None, description='店家地址')
    city: Optional[str] = Field(None, description='所在城市')
    phone: Optional[str] = Field(None, description='聯絡電話')
    business_hours: Optional[str] = Field(None, description='營業時間')
    description: Optional[str] = Field(None, description='店家描述')
    image_url: Optional[str] = Field(None, description='店家圖片URL')
    status: Optional[str] = Field(None, description='狀態：active-營業中，closed-已歇業')

class StoreResponseSchema(StoreBaseSchema):
    """店家響應數據"""
    id: int = Field(..., description='店家ID')
    views: int = Field(..., description='瀏覽次數')
    avg_rating: float = Field(..., description='平均評分')
    rating_count: int = Field(..., description='評分數量')
    comment_count: int = Field(..., description='評論數量')
    created_at: datetime = Field(..., description='創建時間')
    updated_at: datetime = Field(..., description='更新時間')

    class Config:
        orm_mode = True 