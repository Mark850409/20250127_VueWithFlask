from flask_openapi3 import APIBlueprint, Tag
from services.recommend_service import RecommendService
from schemas.recommend_schema import (
    RecommendDataCreate,
    RecommendDataResponse,
    RecommendationQuery,
    RecommendationResponse,
    success_response,
    error_response,
    RecommendResponse
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
    responses={"200": RecommendResponse, "400": RecommendResponse}
)
def create_recommend_data(body: RecommendDataCreate):
    """創建推薦數據
    
    Args:
        body: 包含用戶ID和推薦數量的請求體
    
    Returns:
        200: 創建成功
        400: 創建失敗
    """
    try:
        service = RecommendService()
        success = service.create_recommendations(
            user_id=body.user_id,
            num_recommendations=body.num_recommendations
        )
        
        if success:
            return {"message": "推薦數據創建成功"}, 200
        else:
            return {"message": "推薦數據創建失敗"}, 400
            
    except Exception as e:
        return {"message": f"創建推薦數據時發生錯誤: {str(e)}"}, 400 