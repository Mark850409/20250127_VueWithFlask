from pydantic import BaseModel, Field
from typing import Optional, List

class GoogleMapsInfoCreate(BaseModel):
    place_id: str = Field(..., description='Google Place ID')
    place_names: str = Field(..., description='地點名稱')
    latitude: Optional[float] = Field(None, description='緯度')
    longitude: Optional[float] = Field(None, description='經度')
    address: Optional[str] = Field(None, description='地址')
    city: Optional[str] = Field(None, description='城市')
    city_CN: Optional[str] = Field(None, description='中文城市名')
    redirection_url: Optional[str] = Field(None, description='重定向URL')
    navigation_url: Optional[str] = Field(None, description='導航URL')

class GoogleMapsInfoResponse(GoogleMapsInfoCreate):
    id: int = Field(..., description='ID')
    created_at: str = Field(..., description='創建時間')
    updated_at: str = Field(..., description='更新時間')

class GoogleMapsInfoList(BaseModel):
    items: List[GoogleMapsInfoResponse]

# 新增處理結果的 response schema
class ProcessSuccessResponse(BaseModel):
    """成功處理的回應"""
    success: bool = Field(..., description='是否成功')
    message: str = Field(..., description='處理結果訊息')
    total_processed: int = Field(..., description='總處理筆數')
    new_records: int = Field(..., description='新增筆數')

    class Config:
        schema_extra = {
            "example": {
                "success": True,
                "message": "成功處理 100 筆資料，新增 50 筆記錄",
                "total_processed": 100,
                "new_records": 50
            }
        }

class ProcessErrorResponse(BaseModel):
    """處理失敗的回應"""
    success: bool = Field(..., description='是否成功')
    message: str = Field(..., description='錯誤訊息')
    error: str = Field(..., description='詳細錯誤資訊')

    class Config:
        schema_extra = {
            "example": {
                "success": False,
                "message": "處理資料失敗",
                "error": "Google Maps API 請求失敗"
            }
        } 