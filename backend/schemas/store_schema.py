from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class StoreBaseSchema(BaseModel):
    """店家基礎數據"""
    name: str = Field(..., description='店家名稱', max_length=255)
    normalized_name: str = Field(..., description='正規化店家名稱', max_length=255)
    address: str = Field(..., description='店家地址', max_length=255)
    city: str = Field(..., description='所在城市', max_length=50)
    city_CN: str = Field(..., description='所在城市(中文)', max_length=50)
    customer_phone: Optional[str] = Field(None, description='客服電話', max_length=20)
    description: Optional[str] = Field(None, description='店家描述')
    budget: Optional[float] = Field(None, description='預算')
    distance: Optional[float] = Field(None, description='距離')
    hero_image: Optional[str] = Field(None, description='主要圖片', max_length=255)
    hero_listing_image: Optional[str] = Field(None, description='列表圖片', max_length=255)
    is_new_until: Optional[datetime] = Field(None, description='新店期限')
    latitude: Optional[float] = Field(None, description='緯度')
    longitude: Optional[float] = Field(None, description='經度')
    minimum_delivery_fee: Optional[float] = Field(None, description='最低外送費')
    minimum_delivery_time: Optional[int] = Field(None, description='最短外送時間')
    minimum_order_amount: Optional[float] = Field(None, description='最低訂單金額')
    minimum_pickup_time: Optional[int] = Field(None, description='最短自取時間')
    primary_cuisine_id: Optional[str] = Field(None, description='主要料理類型ID', max_length=50)
    rating: Optional[float] = Field(None, description='評分')
    redirection_url: Optional[str] = Field(None, description='重定向URL', max_length=255)
    review_number: Optional[int] = Field(None, description='評論數量')
    tag: Optional[str] = Field(None, description='標籤', max_length=255)

class StoreCreateSchema(StoreBaseSchema):
    """創建店家請求參數"""
    class Config:
        schema_extra = {
            'example': {
                'name': '春水堂',
                'normalized_name': 'chun-shui-tang',
                'address': '台北市信義區信義路五段7號',
                'city': 'Taipei',
                'city_CN': '台北市',
                'customer_phone': '02-27201234',
                'description': '台灣珍珠奶茶始祖',
                'budget': 300.0,
                'hero_image': 'https://example.com/hero.jpg',
                'hero_listing_image': 'https://example.com/listing.jpg',
                'latitude': 25.0339,
                'longitude': 121.5644,
                'minimum_delivery_fee': 60.0,
                'minimum_order_amount': 200.0,
                'primary_cuisine_id': 'bubble-tea',
                'tag': 'drinks,tea'
            }
        }

class StoreUpdateSchema(BaseModel):
    """更新店家請求參數"""
    name: Optional[str] = Field(None, description='店家名稱', max_length=255)
    normalized_name: Optional[str] = Field(None, description='正規化店家名稱', max_length=255)
    address: Optional[str] = Field(None, description='店家地址', max_length=255)
    city: Optional[str] = Field(None, description='所在城市', max_length=50)
    city_CN: Optional[str] = Field(None, description='所在城市(中文)', max_length=50)
    customer_phone: Optional[str] = Field(None, description='客服電話', max_length=20)
    description: Optional[str] = Field(None, description='店家描述')
    budget: Optional[float] = Field(None, description='預算')
    distance: Optional[float] = Field(None, description='距離')
    hero_image: Optional[str] = Field(None, description='主要圖片', max_length=255)
    hero_listing_image: Optional[str] = Field(None, description='列表圖片', max_length=255)
    is_new_until: Optional[datetime] = Field(None, description='新店期限')
    latitude: Optional[float] = Field(None, description='緯度')
    longitude: Optional[float] = Field(None, description='經度')
    minimum_delivery_fee: Optional[float] = Field(None, description='最低外送費')
    minimum_delivery_time: Optional[int] = Field(None, description='最短外送時間')
    minimum_order_amount: Optional[float] = Field(None, description='最低訂單金額')
    minimum_pickup_time: Optional[int] = Field(None, description='最短自取時間')
    primary_cuisine_id: Optional[str] = Field(None, description='主要料理類型ID', max_length=50)
    rating: Optional[float] = Field(None, description='評分')
    redirection_url: Optional[str] = Field(None, description='重定向URL', max_length=255)
    review_number: Optional[int] = Field(None, description='評論數量')
    tag: Optional[str] = Field(None, description='標籤', max_length=255)

class StoreResponseSchema(StoreBaseSchema):
    """店家響應數據"""
    id: int = Field(..., description='店家ID')
    created_at: datetime = Field(..., description='創建時間')
    updated_at: datetime = Field(..., description='更新時間')

    class Config:
        orm_mode = True

class StoreCrawlerResponse(BaseModel):
    """爬蟲響應數據"""
    message: str = Field(..., description='成功信息')
    data: dict = Field(..., description='爬取統計數據', example={
        'total_fetched': 100,
        'fetched_by_city': {
            '台北市': 30,
            '新北市': 25,
            '桃園市': 45
        },
        'total_duration_seconds': 300
    })

    class Config:
        schema_extra = {
            'example': {
                'message': '資料抓取完成',
                'data': {
                    'total_fetched': 100,
                    'fetched_by_city': {
                        '台北市': 30,
                        '新北市': 25,
                        '桃園市': 45
                    },
                    'total_duration_seconds': 300
                }
            }
        }

class ErrorResponse(BaseModel):
    """錯誤響應數據"""
    message: str = Field(..., description='錯誤信息')

    class Config:
        schema_extra = {
            'example': {
                'message': '爬取資料失敗: 連接超時'
            }
        } 