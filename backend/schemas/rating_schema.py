from pydantic import BaseModel, Field
from typing import Optional

class RatingBaseSchema(BaseModel):
    """評分基礎數據"""
    place_id: str = Field(..., description='Google Place ID', max_length=500)
    restaurant_name: str = Field(..., description='餐廳名稱', max_length=200)
    user: str = Field(..., description='使用者名稱', max_length=100)
    rating: float = Field(..., description='評分')
    text: Optional[str] = Field(None, description='評論內容', max_length=2000)
    english_texts: Optional[str] = Field(None, description='英文評論內容', max_length=2000)
    time: Optional[str] = Field(None, description='評論時間', max_length=50)
    positive_prob: Optional[float] = Field(None, description='正面情緒機率')
    negative_prob: Optional[float] = Field(None, description='負面情緒機率')
    composite_score: Optional[float] = Field(None, description='綜合分數')
    confidence: Optional[float] = Field(None, description='信心分數')
    keywords_scores: Optional[float] = Field(None, description='關鍵字分數')
    sentiment: Optional[str] = Field(None, description='情感分析結果', max_length=500)
    hash: str = Field(..., description='評論雜湊值', max_length=500)

class RatingCreateSchema(RatingBaseSchema):
    """創建評分請求參數"""
    class Config:
        schema_extra = {
            'example': {
                'place_id': 'ChIJxxx...',
                'restaurant_name': '好吃餐廳',
                'user': 'John Doe',
                'rating': 5.0,
                'text': '餐點美味，服務親切',
                'english_texts': 'The food is delicious and the service is friendly',
                'time': '2024-02-01 12:00:00',
                'positive_prob': 0.85,
                'negative_prob': 0.15,
                'composite_score': 0.8,
                'confidence': 0.9,
                'keywords_scores': 0.75,
                'sentiment': 'positive',
                'hash': 'abc123...'
            }
        }

class RatingUpdateSchema(BaseModel):
    """更新評分請求參數"""
    place_id: Optional[str] = Field(None, description='Google Place ID', max_length=500)
    restaurant_name: Optional[str] = Field(None, description='餐廳名稱', max_length=200)
    user: Optional[str] = Field(None, description='使用者名稱', max_length=100)
    rating: Optional[float] = Field(None, description='評分')
    text: Optional[str] = Field(None, description='評論內容', max_length=2000)
    english_texts: Optional[str] = Field(None, description='英文評論內容', max_length=2000)
    time: Optional[str] = Field(None, description='評論時間', max_length=50)
    positive_prob: Optional[float] = Field(None, description='正面情緒機率')
    negative_prob: Optional[float] = Field(None, description='負面情緒機率')
    composite_score: Optional[float] = Field(None, description='綜合分數')
    confidence: Optional[float] = Field(None, description='信心分數')
    keywords_scores: Optional[float] = Field(None, description='關鍵字分數')
    sentiment: Optional[str] = Field(None, description='情感分析結果', max_length=500)
    hash: Optional[str] = Field(None, description='評論雜湊值', max_length=500)

    class Config:
        schema_extra = {
            'example': {
                'text': '餐點美味，服務更加親切',
                'rating': 5.0,
                'sentiment': 'positive'
            }
        }

class RatingResponseSchema(RatingBaseSchema):
    """評分響應數據"""
    id: int = Field(..., description='評分ID')

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'id': 1,
                'place_id': 'ChIJxxx...',
                'restaurant_name': '好吃餐廳',
                'user': 'John Doe',
                'rating': 5.0,
                'text': '餐點美味，服務親切',
                'english_texts': 'The food is delicious and the service is friendly',
                'time': '2024-02-01 12:00:00',
                'positive_prob': 0.85,
                'negative_prob': 0.15,
                'composite_score': 0.8,
                'confidence': 0.9,
                'keywords_scores': 0.75,
                'sentiment': 'positive',
                'hash': 'abc123...'
            }
        } 