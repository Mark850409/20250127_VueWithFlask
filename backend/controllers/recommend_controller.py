from flask_openapi3 import APIBlueprint, Tag
from services.recommend_service import RecommendService
from schemas.recommend_schema import (
    RecommendDataCreate,
    RecommendDataResponse,
    RecommendationQuery,
    RecommendationResponse,
    success_response,
    error_response
)

recommend_bp = APIBlueprint('recommend', __name__, url_prefix='/api')
recommend_tag = Tag(name='recommend', description='推薦系統 API')
recommend_service = RecommendService()

@recommend_bp.get(
    '/recommend_data',
    tags=[recommend_tag],
    responses={
        "200": {
            "description": "成功獲取推薦",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "status": {"type": "string"},
                            "message": {"type": "string"},
                            "data": {
                                "type": "array",
                                "items": {"$ref": "#/components/schemas/RecommendationResponse"}
                            }
                        }
                    }
                }
            }
        },
        "400": {
            "description": "請求參數錯誤"
        }
    }
)
def get_recommendations(query: RecommendationQuery):
    """
    獲取推薦數據API
    
    Args:
        query (RecommendationQuery): 查詢參數
            - user_id: 用戶ID
            - num_recommendations: 推薦數量
            
    Returns:
        200: 推薦列表
        400: 參數錯誤
    """
    try:
        recommendations = recommend_service.get_recommendations(
            query.user_id, 
            query.num_recommendations
        )
        
        validated_recommendations = [
            RecommendationResponse(**rec).dict() 
            for rec in recommendations
        ]
        
        return success_response(validated_recommendations)
    except Exception as e:
        return error_response(str(e))

@recommend_bp.post(
    '/recommend_data',
    tags=[recommend_tag],
    responses={
        "200": {
            "description": "成功創建推薦",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "status": {"type": "string"},
                            "message": {"type": "string"},
                            "data": {"$ref": "#/components/schemas/RecommendDataResponse"}
                        }
                    }
                }
            }
        },
        "400": {
            "description": "請求數據錯誤"
        }
    }
)
def create_recommend_data(body: RecommendDataCreate):
    """
    創建推薦數據API
    
    Args:
        body (RecommendDataCreate): 推薦數據
            - user_id: 用戶ID
            - restaurant_id: 餐廳ID
            - rating: 評分
            - distance: 距離
            - review_number: 評論數量
            - sentiment_score: 情感分數
            - weighted_score: 加權分數
            
    Returns:
        200: 創建成功的推薦數據
        400: 參數錯誤
    """
    try:
        if not body:
            return error_response('No data provided')
            
        result = recommend_service.create_recommend_data(body.dict())
        response = RecommendDataResponse(**result.to_dict())
        
        return success_response(response.dict())
    except Exception as e:
        return error_response(str(e)) 