from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class PlaceQuery(BaseModel):
    """搜尋地點查詢參數"""
    input: str = Field(..., description='搜尋文字', example='台北101')

class PlaceDetailsQuery(BaseModel):
    """地點詳細資訊查詢參數"""
    place_id: str = Field(..., description='地點ID', example='ChIJmQrivHKsQjQR4MIK3c41aj8')
    language: str = Field('zh-TW', description='語言代碼')

class NearbySearchQuery(BaseModel):
    """附近搜尋查詢參數"""
    latitude: float = Field(..., description='緯度', example=25.033964)
    longitude: float = Field(..., description='經度', example=121.564468)
    radius: int = Field(..., description='搜尋半徑(公尺)', example=1000)
    place_type: str = Field(..., description='地點類型', example='restaurant')
    keyword: Optional[str] = Field(None, description='關鍵字')

class NavigationQuery(BaseModel):
    """導航查詢參數"""
    start_address: str = Field(..., description='起點地址', example='台北車站')
    end_address: str = Field(..., description='終點地址', example='台北101')
    mode: str = Field('driving', description='交通方式(driving/walking/bicycling/transit)')
    avoid: Optional[List[str]] = Field(None, description='避開項目(tolls/highways/ferries)')

class DistanceMatrixQuery(BaseModel):
    """距離矩陣查詢參數"""
    origins: List[str] = Field(..., description='起點地址列表')
    destinations: List[str] = Field(..., description='終點地址列表')
    mode: str = Field('driving', description='交通方式')

# Response Models
class PlaceResponse(BaseModel):
    """地點搜尋響應"""
    place_id: str

class ReviewModel(BaseModel):
    """評論模型"""
    author_name: str
    rating: float
    text: str
    time: str

class PlaceDetailsResponse(BaseModel):
    """地點詳細資訊響應"""
    restaurant_name: str
    reviews: List[ReviewModel]

class NearbyPlaceModel(BaseModel):
    """附近地點模型"""
    name: str
    place_id: str
    vicinity: str
    rating: float
    user_ratings_total: int
    location: dict
    types: List[str]
    business_status: str

class NearbySearchResponse(BaseModel):
    """附近搜尋響應"""
    results: List[NearbyPlaceModel]

class NavigationResponse(BaseModel):
    """導航響應"""
    navigation_url: str

class ErrorResponse(BaseModel):
    """錯誤響應"""
    error: str

class DistanceMatrixElement(BaseModel):
    """距離矩陣元素"""
    distance: Dict[str, str] = Field(..., description='距離信息')
    duration: Dict[str, str] = Field(..., description='時間信息')
    status: str = Field(..., description='狀態')

class DistanceMatrixRow(BaseModel):
    """距離矩陣行"""
    elements: List[DistanceMatrixElement]

class DistanceMatrixResponse(BaseModel):
    """距離矩陣響應"""
    destination_addresses: List[str] = Field(..., description='目的地地址列表')
    origin_addresses: List[str] = Field(..., description='起點地址列表')
    rows: List[DistanceMatrixRow] = Field(..., description='距離矩陣數據')
    status: str = Field(..., description='響應狀態') 