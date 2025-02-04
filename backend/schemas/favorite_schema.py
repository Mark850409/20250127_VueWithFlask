from pydantic import BaseModel, Field
from typing import Optional

class FavoritePath(BaseModel):
    """最愛路徑參數"""
    favorite_id: int = Field(..., description='最愛ID')

class FavoriteCreateSchema(BaseModel):
    """創建最愛請求參數"""
    store_id: int = Field(..., description='店家ID')
    store_name: str = Field(..., description='店家名稱')
    store_image: str = Field(..., description='店家圖片')
    username: str = Field(..., description='用戶名稱')

class FavoriteResponseSchema(BaseModel):
    """最愛響應數據"""
    id: int = Field(..., description='最愛ID')
    user_id: int = Field(..., description='用戶ID')
    store_id: int = Field(..., description='店家ID')
    store_name: str = Field(..., description='店家名稱')
    store_image: str = Field(..., description='店家圖片')
    username: str = Field(..., description='用戶名稱')
    created_at: str = Field(..., description='創建時間')
    updated_at: str = Field(..., description='更新時間') 