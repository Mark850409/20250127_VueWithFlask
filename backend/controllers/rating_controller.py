from flask_openapi3 import APIBlueprint, Tag
from services.rating_service import RatingService
from schemas.rating_schema import *
from pydantic import BaseModel, Field
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.google_maps_crawler_service import GoogleMapsCrawlerService
from typing import List, Optional, Dict
import logging

rating_bp = APIBlueprint('ratings', __name__, url_prefix='/api/ratings')
rating_tag = Tag(name='ratings', description='評分管理')

# 設置日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('crawler.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class RatingPath(BaseModel):
    """評分路徑參數"""
    rating_id: int = Field(..., description='評分ID')

class StorePath(BaseModel):
    """店家路徑參數"""
    place_id: str = Field(..., description='Google Place ID')

class CrawlerRequest(BaseModel):
    """爬蟲請求參數"""
    restaurant_name: str = Field(..., description='餐廳名稱', example='鼎泰豐')
    comment_count: int = Field(10, description='要爬取的評論數量', ge=1, le=100, example=10)

class ReviewData(BaseModel):
    """評論數據"""
    place_id: str = Field(..., description='Google Place ID')
    restaurant_name: str = Field(..., description='餐廳名稱')
    user: str = Field(..., description='使用者名稱')
    rating: float = Field(..., description='評分')
    text: Optional[str] = Field(None, description='評論內容')
    english_texts: Optional[str] = Field(None, description='英文評論內容')
    time: Optional[str] = Field(None, description='評論時間')
    positive_prob: Optional[float] = Field(None, description='正面情緒機率')
    negative_prob: Optional[float] = Field(None, description='負面情緒機率')
    composite_score: Optional[float] = Field(None, description='綜合分數')
    confidence: Optional[float] = Field(None, description='信心分數')
    keywords_scores: Optional[float] = Field(None, description='關鍵字分數')
    sentiment: Optional[str] = Field(None, description='情感分析結果')
    hash: str = Field(..., description='評論雜湊值')

class CrawlerResponse(BaseModel):
    """爬蟲響應"""
    success: bool = Field(..., description='是否成功')
    message: str = Field(..., description='結果訊息')
    data: List[ReviewData] = Field([], description='評論數據列表')
    error: Optional[str] = Field(None, description='錯誤訊息')

    class Config:
        schema_extra = {
            'example': {
                'success': True,
                'message': '成功爬取 10 筆評論',
                'data': [{
                    'place_id': 'ChIJxxx...',
                    'restaurant_name': '鼎泰豐',
                    'user': 'John Doe',
                    'rating': 5.0,
                    'text': '餐點美味，服務親切',
                    'english_texts': 'The food is delicious and the service is friendly',
                    'time': '1 週前',
                    'positive_prob': 0.85,
                    'negative_prob': 0.15,
                    'composite_score': 0.8,
                    'confidence': 0.9,
                    'keywords_scores': 0.75,
                    'sentiment': 'positive',
                    'hash': 'abc123...'
                }]
            }
        }

class ProcessAllRequest(BaseModel):
    """批次爬取請求參數"""
    comment_count: int = Field(10, description='每家餐廳要爬取的評論數量', ge=1, le=100, example=10)

class ProcessAllResponse(BaseModel):
    """批次處理響應"""
    success: bool = Field(..., description='是否成功')
    message: str = Field(..., description='結果訊息')
    total_restaurants: int = Field(..., description='處理的餐廳總數')
    total_reviews: int = Field(..., description='爬取的評論總數')
    failed_restaurants: List[Dict] = Field([], description='處理失敗的餐廳列表')

    class Config:
        schema_extra = {
            'example': {
                'success': True,
                'message': '批次處理完成，成功處理 95/100 家餐廳',
                'total_restaurants': 100,
                'total_reviews': 950,
                'failed_restaurants': [
                    {
                        'id': 1,
                        'name': '測試餐廳',
                        'error': '找不到餐廳'
                    }
                ]
            }
        }

@rating_bp.get('/place/<string:place_id>', tags=[rating_tag])
def get_store_ratings(path: StorePath):
    """獲取店家的所有評分
    
    Args:
        path (StorePath): 路徑參數
            place_id (str): Google Place ID
            
    Returns:
        200 (RatingResponseSchema): 評分列表
        500: 服務器錯誤
    """
    try:
        service = RatingService()
        ratings = service.get_store_ratings(path.place_id)
        return {'ratings': [rating.to_dict() for rating in ratings]}
    except Exception as e:
        return {'message': f'獲取評分列表失敗: {str(e)}'}, 500

@rating_bp.post('/', tags=[rating_tag])
@jwt_required()
def create_rating(body: RatingCreateSchema):
    """創建評分
    
    Args:
        body (RatingCreateSchema): 評分數據
            place_id (str): Google Place ID
            restaurant_name (str): 餐廳名稱
            user (str): 使用者名稱
            rating (float): 評分
            text (str, optional): 評論內容
            english_texts (str, optional): 英文評論內容
            time (str, optional): 評論時間
            positive_prob (float, optional): 正面情緒機率
            negative_prob (float, optional): 負面情緒機率
            composite_score (float, optional): 綜合分數
            confidence (float, optional): 信心分數
            keywords_scores (float, optional): 關鍵字分數
            sentiment (str, optional): 情感分析結果
            hash (str): 評論雜湊值
            
    Returns:
        201 (RatingResponseSchema): 創建成功
        400: 參數錯誤
        401: 未登入
        500: 服務器錯誤
    """
    try:
        service = RatingService()
        rating_data = body.dict(exclude_unset=True)
        print("Rating data:", rating_data)  # 調試信息
        rating = service.create_rating(rating_data)
        return rating.to_dict(), 201
    except Exception as e:
        print(f"Error creating rating: {str(e)}")  # 調試信息
        return {'message': '創建評分失敗'}, 500

@rating_bp.put('/<int:rating_id>', tags=[rating_tag])
@jwt_required()
def update_rating(path: RatingPath, body: RatingUpdateSchema):
    """更新評分
    
    Args:
        path (RatingPath): 路徑參數
            rating_id (int): 評分ID
        body (RatingUpdateSchema): 更新數據
            
    Returns:
        200 (RatingResponseSchema): 更新成功
        400: 參數錯誤
        401: 未登入
        404: 評分不存在
        500: 服務器錯誤
    """
    try:
        service = RatingService()
        rating_data = body.dict(exclude_unset=True)
        rating = service.update_rating(path.rating_id, rating_data)
        if not rating:
            return {'message': '評分不存在'}, 404
        return rating.to_dict()
    except ValueError as e:
        return {'message': str(e)}, 400
    except Exception as e:
        print(f"更新評分錯誤: {str(e)}")
        return {'message': '更新評分失敗'}, 500

@rating_bp.delete('/<int:rating_id>', tags=[rating_tag])
@jwt_required()
def delete_rating(path: RatingPath):
    """刪除評分
    
    Args:
        path (RatingPath): 路徑參數
            rating_id (int): 評分ID
            
    Returns:
        204: 刪除成功
        400: 參數錯誤
        401: 未登入
        404: 評分不存在
        500: 服務器錯誤
    """
    try:
        service = RatingService()
        if service.delete_rating(path.rating_id):
            return '', 204
        return {'message': '評分不存在'}, 404
    except ValueError as e:
        return {'message': str(e)}, 400
    except Exception as e:
        print(f"刪除評分錯誤: {str(e)}")
        return {'message': '刪除評分失敗'}, 500

@rating_bp.post(
    '/crawler',
    tags=[rating_tag],
    responses={
        200: CrawlerResponse,
        400: {"description": "請求參數錯誤"},
        401: {"description": "未登入"},
        500: {"description": "服務器錯誤"}
    }
)
@jwt_required()
def crawl_restaurant_reviews(body: CrawlerRequest):
    """爬取餐廳評論
    
    此 API 用於爬取指定餐廳的 Google Maps 評論，並進行情感分析和關鍵字分析。
    
    Args:
        body (CrawlerRequest): 請求參數
            restaurant_name (str): 餐廳名稱
            comment_count (int): 要爬取的評論數量，默認10筆，最多100筆
            
    Returns:
        200: 爬取成功
            success (bool): 是否成功
            message (str): 結果訊息
            data (List[ReviewData]): 評論數據列表
            error (Optional[str]): 錯誤訊息
        400: 參數錯誤
        401: 未登入
        500: 服務器錯誤
    """
    try:
        service = GoogleMapsCrawlerService()
        result = service.crawl_restaurant_reviews(
            body.restaurant_name,
            body.comment_count
        )
        
        if result['success']:
            return result, 200
        else:
            return result, 400
            
    except Exception as e:
        return {
            'success': False,
            'message': '爬取評論失敗',
            'error': str(e),
            'data': []
        }, 500

@rating_bp.post(
    '/crawler/all',
    tags=[rating_tag],
    responses={
        200: ProcessAllResponse,
        400: {"description": "請求參數錯誤"},
        401: {"description": "未登入"},
        500: {"description": "服務器錯誤"}
    }
)
@jwt_required()
def process_all_restaurants(body: ProcessAllRequest):
    """批次爬取所有餐廳的評論
    
    此 API 會爬取資料庫中所有餐廳的 Google Maps 評論，並進行情感分析和關鍵字分析。
    處理結果會保存到資料庫和 CSV 文件中。
    
    Args:
        body (ProcessAllRequest): 請求參數
            comment_count (int): 每家餐廳要爬取的評論數量，默認10筆，最多100筆
    
    Returns:
        200: 處理成功
            success (bool): 是否成功
            message (str): 結果訊息
            total_restaurants (int): 處理的餐廳總數
            total_reviews (int): 爬取的評論總數
            failed_restaurants (List[Dict]): 處理失敗的餐廳列表
        400: 參數錯誤
        401: 未登入
        500: 服務器錯誤
    """
    try:
        service = GoogleMapsCrawlerService()
        result = service.process_all_restaurants(comment_count=body.comment_count)
        return result, 200 if result['success'] else 500
    except Exception as e:
        logger.error(f"批次處理時發生錯誤: {str(e)}")
        return {
            'success': False,
            'message': '批次處理失敗',
            'error': str(e),
            'total_restaurants': 0,
            'total_reviews': 0,
            'failed_restaurants': []
        }, 500 