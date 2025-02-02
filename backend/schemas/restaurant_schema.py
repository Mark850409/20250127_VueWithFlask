from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class ErrorResponse(BaseModel):
    """錯誤響應模型"""
    error: str = Field(..., description='錯誤訊息')
    details: Optional[Dict[str, Any]] = Field(None, description='詳細錯誤信息')

class SuccessResponse(BaseModel):
    """成功響應模型"""
    message: str = Field(..., description='成功訊息')
    data: Optional[Dict[str, Any]] = Field(None, description='返回的數據')

class RestaurantData(BaseModel):
    """餐廳數據模型"""
    name: str = Field(..., description='餐廳名稱')
    normalized_name: str = Field(..., description='正規化名稱')
    address: str = Field(..., description='地址')
    budget: Optional[float] = Field(None, description='預算')
    city: str = Field(..., description='城市')
    city_CN: str = Field(..., description='中文城市名')
    customer_phone: Optional[str] = Field(None, description='客服電話')
    description: Optional[str] = Field(None, description='描述')
    hero_image: Optional[str] = Field(None, description='主圖片')
    hero_listing_image: Optional[str] = Field(None, description='列表圖片')
    distance: Optional[float] = Field(None, description='距離')
    is_new_until: Optional[str] = Field(None, description='新店期限')
    latitude: Optional[float] = Field(None, description='緯度')
    longitude: Optional[float] = Field(None, description='經度')
    minimum_delivery_fee: Optional[float] = Field(None, description='最低外送費')
    minimum_delivery_time: Optional[int] = Field(None, description='最短外送時間')
    minimum_order_amount: Optional[float] = Field(None, description='最低訂單金額')
    minimum_pickup_time: Optional[int] = Field(None, description='最短自取時間')
    primary_cuisine_id: Optional[str] = Field(None, description='主要料理類型ID')
    rating: Optional[float] = Field(None, description='評分')
    redirection_url: Optional[str] = Field(None, description='重定向URL')
    review_number: Optional[int] = Field(None, description='評論數量')
    tag: Optional[str] = Field(None, description='標籤') 