from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class RatingBaseSchema(BaseModel):
    """評分基礎數據"""
    comment: str = Field(..., description='評論內容')
    score: int = Field(..., description='評分', ge=1, le=5)
    store_id: int = Field(..., description='店家ID')

class RatingCreateSchema(RatingBaseSchema):
    """創建評分請求參數"""
    class Config:
        schema_extra = {
            'example': {
                'comment': '餐點美味，服務親切',
                'score': 5,
                'store_id': 1
            }
        }

class RatingUpdateSchema(BaseModel):
    """更新評分請求參數"""
    comment: Optional[str] = Field(None, description='評論內容')
    score: Optional[int] = Field(None, description='評分', ge=1, le=5)

    class Config:
        schema_extra = {
            'example': {
                'comment': '餐點美味，服務更加親切',
                'score': 5
            }
        }

class RatingResponseSchema(RatingBaseSchema):
    """評分響應數據"""
    id: int = Field(..., description='評分ID')
    user_id: int = Field(..., description='用戶ID')
    created_at: datetime = Field(..., description='創建時間')
    updated_at: datetime = Field(..., description='更新時間')

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'id': 1,
                'user_id': 1,
                'store_id': 1,
                'comment': '餐點美味，服務親切',
                'score': 5,
                'created_at': '2024-02-01 12:00:00',
                'updated_at': '2024-02-01 12:00:00'
            }
        } 