from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# 基本統計數據
class StatItem(BaseModel):
    title: str
    value: str
    trend: float
    unit: str
    icon: str
    iconColor: str
    path: str

class BasicStatsResponse(BaseModel):
    stats: List[StatItem]

# 熱門店家
class ShopItem(BaseModel):
    id: int
    name: str
    address: str
    city: str
    city_CN: str
    rating: float
    review_number: int
    increase: float

class TopShopsResponse(BaseModel):
    topShops: List[ShopItem]

# 最新評論
class ReviewItem(BaseModel):
    id: int
    user: str
    place_id: str
    restaurant_name: str
    rating: float
    text: str
    english_texts: Optional[str]
    createdAt: datetime

class LatestReviewsResponse(BaseModel):
    latestReviews: List[ReviewItem]

# 系統日誌
class LogItem(BaseModel):
    id: int
    type: str
    message: str
    timestamp: str

class SystemLogsResponse(BaseModel):
    systemLogs: List[LogItem]

# 活動數據
class HourlyActivityData(BaseModel):
    dates: List[str]
    values: List[int]

class ActivityData(BaseModel):
    dates: List[str]
    values: List[int]
    hourly: HourlyActivityData

class ActivityDataResponse(BaseModel):
    activityData: ActivityData

# 完整儀表板響應（用於向後兼容）
class DashboardStatsResponse(BaseModel):
    stats: List[StatItem]
    topShops: List[ShopItem]
    latestReviews: List[ReviewItem]
    systemLogs: List[LogItem]
    activityData: ActivityData 