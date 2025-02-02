from pydantic import BaseModel, Field
from typing import Optional, List, Dict

class Point(BaseModel):
    longitude: float = Field(..., description='經度', example=121.51005746084171)
    latitude: float = Field(..., description='緯度', example=25.039975278728466)

class Location(BaseModel):
    point: Point

class SearchRestaurantQuery(BaseModel):
    """搜尋餐廳查詢參數"""
    query: str = Field(..., description='搜尋關鍵字', example='星巴克')
    longitude: float = Field(..., description='經度', example=120.3025185)
    latitude: float = Field(..., description='緯度', example=22.639473)
    limit: int = Field(48, description='限制筆數', ge=1, le=100)
    offset: int = Field(0, description='偏移量', ge=0)
    configuration: str = Field('undefined', description='配置類型')
    vertical: str = Field('restaurants', description='垂直類型')
    search_vertical: str = Field('restaurants', description='搜尋垂直類型')
    include_component_types: str = Field('vendors', description='包含組件類型')
    include_fields: str = Field('feed', description='包含字段')
    language_id: str = Field('6', description='語言ID')
    opening_type: str = Field('delivery', description='開放類型')
    platform: str = Field('web', description='平台')
    language_code: str = Field('zh', description='語言代碼')
    customer_type: str = Field('regular', description='顧客類型')
    dynamic_pricing: int = Field(0, description='動態定價')
    brand: str = Field('foodpanda', description='品牌')
    country_code: str = Field('tw', description='國家代碼')
    use_free_delivery_label: str = Field('false', description='使用免費配送標籤')

class vendorsQuery(BaseModel):
    """獲取附近餐廳查詢參數"""
    longitude: str = Field(..., description='經度', example='121.51005746084171')
    latitude: str = Field(..., description='緯度', example='25.039975278728466')
    way: Optional[str] = Field(None, description='取餐方式(外送、外帶自取)')
    country: str = Field('tw', description='國家')
    dynamic_pricing: Optional[str] = Field('0', description='動態定價')
    configuration: Optional[str] = Field('Variant1', description='配置')
    budgets: Optional[str] = Field(None, description='預算範圍')
    cuisine: Optional[str] = Field(None, description='料理類型')
    sort: Optional[str] = Field(None, description='排序方式(rating_desc、delivery_time_asc、distance_asc)')
    food_characteristic: Optional[str] = Field(None, description='食物特色')
    use_free_delivery_label: Optional[bool] = Field(False, description='使用免費配送標籤')
    vertical: Optional[str] = Field('restaurants', description='垂直類型')
    limit: str = Field('48', description='限制筆數')
    offset: Optional[str] = Field('0', description='偏移量')
    customer_type: Optional[str] = Field('regular', description='顧客類型')
    has_discount: Optional[bool] = Field(False, description='是否有折扣')

class swimlanesQuery(BaseModel):
    """獲取推薦餐廳查詢參數"""
    longitude: str = Field(..., description='經度', example='121.51005746084171')
    latitude: str = Field(..., description='緯度', example='25.039975278728466')
    brand: str = Field('foodpanda', description='品牌')
    language_code: str = Field('zh', description='語言代碼')
    language_id: str = Field('6', description='語言ID')
    country_code: str = Field('tw', description='國家代碼')
    dynamic_pricing: str = Field('0', description='動態定價')
    use_free_delivery_label: bool = Field(False, description='使用免費配送標籤')
    way: str = Field('外送', description='取餐方式')
    config: str = Field('Original', description='配置類型')
    vertical_type: str = Field('restaurants', description='垂直類型')
    opening_type: str = Field('delivery', description='開放類型')
    cuisine: Optional[str] = Field(None, description='料理類型')

class getMenuRequest(BaseModel):
    """獲取菜單路徑參數"""
    restaurant_code: str = Field(..., description='餐廳代碼', example='g1mk')

class MenuQuery(BaseModel):
    """獲取菜單查詢參數"""
    include: str = Field('menus', description='包含內容')
    language_id: str = Field('6', description='語言ID')
    dynamic_pricing: str = Field('0', description='動態定價')
    opening_type: str = Field('delivery', description='開放類型')
    longitude: str = Field(..., description='經度', example='121.51005746084171')
    latitude: str = Field(..., description='緯度', example='25.039975278728466') 