from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class StatItem(BaseModel):
    title: str
    value: str
    trend: float
    unit: str
    icon: str
    iconColor: str

class ShopItem(BaseModel):
    id: int
    name: str
    rating: float
    orderCount: int
    increase: float

class ReviewItem(BaseModel):
    id: int
    userName: str
    userAvatar: str
    storeName: str
    rating: float
    content: str
    createdAt: str

class LogItem(BaseModel):
    id: int
    type: str
    message: str
    timestamp: str

class ActivityData(BaseModel):
    dates: List[str]
    values: List[int]

class DashboardStatsResponse(BaseModel):
    stats: List[StatItem]
    topShops: List[ShopItem]
    latestReviews: List[ReviewItem]
    systemLogs: List[LogItem]
    activityData: ActivityData 