from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field

# Request Schemas
class BannerPath(BaseModel):
    banner_id: int = Field(..., description="輪播圖ID")

class BannerQuery(BaseModel):
    is_active: Optional[bool] = Field(None, description="是否啟用")

class BannerCreateBody(BaseModel):
    banner_type: str = Field(..., description="輪播圖類型(home/feature/learning/pricing/food/footer/login/admin)")
    title: str = Field(..., max_length=100, description="標題")
    subtitle: str = Field(..., max_length=200, description="副標題")
    description: str = Field(..., description="描述")
    image_url: str = Field(..., max_length=500, description="圖片URL")
    alt: Optional[str] = Field(None, max_length=100, description="圖片替代文字")
    sort_order: Optional[int] = Field(0, description="排序順序")
    is_active: Optional[bool] = Field(True, description="是否啟用")

class BannerUpdateBody(BaseModel):
    banner_type: Optional[str] = Field(None, description="輪播圖類型(home/feature/learning/pricing/food/footer/login/admin)")
    title: Optional[str] = Field(None, max_length=100, description="標題")
    subtitle: Optional[str] = Field(None, max_length=200, description="副標題")
    description: Optional[str] = Field(None, description="描述")
    image_url: Optional[str] = Field(None, max_length=500, description="圖片URL")
    alt: Optional[str] = Field(None, max_length=100, description="圖片替代文字")
    sort_order: Optional[int] = Field(None, description="排序順序")
    is_active: Optional[bool] = Field(None, description="是否啟用")

# Response Schemas
class BannerSchema(BaseModel):
    id: int = Field(..., description="輪播圖ID")
    banner_type: str = Field(..., description="輪播圖類型")
    title: str = Field(..., description="標題")
    subtitle: str = Field(..., description="副標題")
    description: str = Field(..., description="描述")
    image_url: str = Field(..., description="圖片URL")
    alt: Optional[str] = Field(None, description="圖片替代文字")
    sort_order: int = Field(..., description="排序順序")
    is_active: bool = Field(..., description="是否啟用")
    created_at: datetime = Field(..., description="創建時間")
    updated_at: datetime = Field(..., description="更新時間")

class BannerResponse(BaseModel):
    data: BannerSchema

class BannerListResponse(BaseModel):
    data: List[BannerSchema]

class MessageResponse(BaseModel):
    message: str = Field(..., description="回應訊息") 

# 修改 banner_type 驗證模式
class BannerTypeParam(BaseModel):
    banner_type: str = Field(
        ..., 
        description="輪播圖類型", 
        pattern="^(home|feature|learning|pricing|food|footer|login|admin.*?)$"
    )