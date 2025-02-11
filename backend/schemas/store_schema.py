from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from flask_openapi3 import FileStorage
from enum import Enum

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
    city: str = Field(..., description='所在城市(英文)', max_length=50)
    city_CN: str = Field(..., description='所在城市(中文)', max_length=50)
    created_at: datetime = Field(..., description='創建時間')
    updated_at: datetime = Field(..., description='更新時間')
    tag: Optional[str] = Field(None, description='標籤', max_length=255)

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'id': 1,
                'name': '春水堂',
                'city': 'Taipei',
                'city_CN': '台北市',
                'created_at': '2024-01-31T10:00:00',
                'updated_at': '2024-01-31T10:00:00',
                'tag': 'drinks,tea'
            }
        }

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

class StorePath(BaseModel):
    """店家路徑參數"""
    store_id: int = Field(..., description='店家ID')

class CityPath(BaseModel):
    """城市路徑參數"""
    city: str = Field(..., description='城市名稱', example='台北')

class FileUploadResponse(BaseModel):
    """圖片上傳響應"""
    url: str = Field(..., description='圖片URL')
    message: Optional[str] = Field(None, description='響應信息')

class ErrorResponse(BaseModel):
    """錯誤響應"""
    message: str = Field(..., description='錯誤信息')

class UploadFileForm(BaseModel):
    """文件上傳請求"""
    file: FileStorage = Field(
        ...,
        description='圖片文件 (支援 jpg、png、gif、webp 格式，最大 5MB)',
    )

class SortField(str, Enum):
    """排序欄位選項"""
    RATING = "rating"
    REVIEW_NUMBER = "review_number"
    CREATED_AT = "created_at"
    DEFAULT = "default"
    DISTANCE = "distance"

class SortOrder(str, Enum):
    """排序方向"""
    ASC = "asc"
    DESC = "desc"

class StoreQuerySchema(BaseModel):
    """查詢參數"""
    limit: int = Field(..., description='返回筆數限制', ge=1, le=50)
    city: Optional[str] = Field(None, description='城市名稱(支持中英文)')
    sort_by: Optional[SortField] = Field(
        default=SortField.DEFAULT,
        description='排序欄位'
    )
    order: Optional[SortOrder] = Field(
        default=SortOrder.DESC,
        description='排序方向'
    )

    class Config:
        schema_extra = {
            'example': {
                'limit': 12,
                'city': '台北市',
                'sort_by': 'rating',
                'order': 'desc'
            }
        }
