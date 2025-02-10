from flask_openapi3 import APIBlueprint, Tag
from services.recommend_service import RecommendService
from schemas.recommend_schema import (
    RecommendationQuery,
    success_response,
    error_response,
    API_RESPONSES
)

recommend_bp = APIBlueprint('recommend', __name__, url_prefix='/api')
recommend_tag = Tag(name='recommend', description='推薦系統 API')
recommend_service = RecommendService()

@recommend_bp.get(
    '/hybrid_recommend_data',
    tags=[recommend_tag],
    responses=API_RESPONSES["HybridRecommendation"]
)
def get_recommendations(query: RecommendationQuery):
    """
    獲取混合推薦數據API
    
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
        return success_response(recommendations)
    except Exception as e:
        return error_response(str(e))

@recommend_bp.get(
    '/collaborative_recommendations',
    tags=[recommend_tag],
    responses=API_RESPONSES["CollaborativeRecommendation"]
)
def get_collaborative_recommendations(query: RecommendationQuery):
    """
    獲取協同過濾推薦數據API
    
    Args:
        query (RecommendationQuery): 查詢參數
            - user_id: 用戶ID
            - num_recommendations: 推薦數量
            
    Returns:
        200: 推薦列表
        400: 參數錯誤
    """
    try:
        recommendations = recommend_service.get_collaborative_recommendations(
            query.user_id, 
            query.num_recommendations
        )
        return success_response(recommendations)
    except Exception as e:
        return error_response(str(e))

@recommend_bp.get(
    '/content_recommendations',
    tags=[recommend_tag],
    responses=API_RESPONSES["ContentRecommendation"]
)
def get_content_recommendations(query: RecommendationQuery):
    """
    獲取內容推薦數據API
    
    Args:
        query (RecommendationQuery): 查詢參數
            - user_id: 用戶ID
            - num_recommendations: 推薦數量
            
    Returns:
        200: 推薦列表
        400: 參數錯誤
    """
    try:
        recommendations = recommend_service.get_content_recommendations(
            query.user_id, 
            query.num_recommendations
        )
        return success_response(recommendations)
    except Exception as e:
        return error_response(str(e))