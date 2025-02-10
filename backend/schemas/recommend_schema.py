from pydantic import BaseModel, Field
from typing import Optional, List, Any

class RecommendDataCreate(BaseModel):
    """推薦數據創建請求"""
    user_id: int = Field(..., description='用戶ID', gt=0)
    num_recommendations: int = Field(..., description='推薦數量', ge=1, le=20)

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": 1,
                "num_recommendations": 8
            }
        }

class RecommendDataResponse(BaseModel):
    """推薦數據回應模型"""
    id: int = Field(..., description='推薦ID')
    user_id: int = Field(..., description='用戶ID')
    restaurant_id: str = Field(..., description='餐廳ID')
    rating: Optional[float] = Field(None, description='評分')
    distance: Optional[float] = Field(None, description='距離')
    review_number: Optional[int] = Field(None, description='評論數量')
    sentiment_score: Optional[float] = Field(None, description='情感分數')
    weighted_score: Optional[float] = Field(None, description='加權分數')

class RecommendationQuery(BaseModel):
    """推薦查詢參數模型"""
    user_id: int = Field(..., description='用戶ID')
    num_recommendations: int = Field(5, description='推薦數量')

class RecommendationResponse(BaseModel):
    """推薦回應模型"""
    name: str = Field(..., description='餐廳名稱')
    latitude: float = Field(..., description='緯度')
    longitude: float = Field(..., description='經度')
    redirection_url: str = Field(..., description='重定向URL')
    navigation_url: str = Field(..., description='導航URL')
    city: str = Field(..., description='城市')
    distance: float = Field(..., description='距離')
    rating: float = Field(..., description='評分')
    review_number: int = Field(..., description='評論數量')

class RecommendResponse(BaseModel):
    """推薦響應"""
    message: str = Field(..., description='響應信息')

def success_response(data=None, message="Success"):
    """成功回應格式"""
    response = {
        "status": "success",
        "message": message
    }
    if data is not None:
        response["data"] = data
    return response

def error_response(message="Error", code=400):
    """錯誤回應格式"""
    return {
        "status": "error",
        "message": message
    }, code 