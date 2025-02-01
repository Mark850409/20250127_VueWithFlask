from flask_openapi3 import APIBlueprint, Tag
from services.rating_service import RatingService
from schemas.rating_schema import *
from pydantic import BaseModel, Field
from flask_jwt_extended import jwt_required, get_jwt_identity

rating_bp = APIBlueprint('ratings', __name__, url_prefix='/api/ratings')
rating_tag = Tag(name='ratings', description='評分管理')

class RatingPath(BaseModel):
    """評分路徑參數"""
    rating_id: int = Field(..., description='評分ID')

class StorePath(BaseModel):
    """店家路徑參數"""
    store_id: int = Field(..., description='店家ID')

@rating_bp.get('/store/<int:store_id>', tags=[rating_tag])
def get_store_ratings(path: StorePath):
    """獲取店家的所有評分
    
    Args:
        path (StorePath): 路徑參數
            store_id (int): 店家ID
            
    Returns:
        200 (RatingResponseSchema): 評分列表
        500: 服務器錯誤
    """
    try:
        service = RatingService()
        ratings = service.get_store_ratings(path.store_id)
        return {'ratings': [rating.to_dict() for rating in ratings]}
    except Exception as e:
        return {'message': f'獲取評分列表失敗: {str(e)}'}, 500

@rating_bp.post('/', tags=[rating_tag])
@jwt_required()
def create_rating(body: RatingCreateSchema):
    """創建評分
    
    Args:
        body (RatingCreateSchema): 評分數據
            comment (str): 評論內容
            score (int): 評分 (1-5)
            store_id (int): 店家ID
            
    Returns:
        201 (RatingResponseSchema): 創建成功
            id (int): 評分ID
            user_id (int): 用戶ID
            store_id (int): 店家ID
            comment (str): 評論內容
            score (int): 評分
            created_at (datetime): 創建時間
            updated_at (datetime): 更新時間
        400: 
            - 參數錯誤
            - 店家不存在
            - 已經評分過此店家
        401: 未登入
        500: 服務器錯誤
        
    Security:
        Bearer: []
        
    Example:
        POST /api/ratings/
        {
            "comment": "餐點美味，服務親切",
            "score": 5,
            "store_id": 1
        }
    """
    try:
        service = RatingService()
        user_id = int(get_jwt_identity())
        
        rating_data = {
            'comment': body.comment,
            'score': body.score,
            'store_id': body.store_id
        }
        
        rating = service.create_rating(user_id, rating_data)
        return rating.to_dict(), 201
    except ValueError as e:
        return {'message': str(e)}, 400
    except Exception as e:
        # 記錄詳細錯誤信息
        print(f"創建評分錯誤: {str(e)}")
        return {'message': '創建評分失敗，請確認店家是否存在'}, 500

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
        # 獲取當前用戶ID
        current_user_id = int(get_jwt_identity())
        
        # 添加調試日誌
        print(f"當前用戶ID: {current_user_id}")
        print(f"要更新的評分ID: {path.rating_id}")
        
        # 先獲取評分信息
        rating = service.get_rating(path.rating_id)
        if rating:
            print(f"評分擁有者ID: {rating.user_id}")
        
        # 更新評分
        rating = service.update_rating(
            user_id=current_user_id,
            rating_id=path.rating_id,
            rating_data=body.dict(exclude_unset=True)
        )
        
        if not rating:
            return {'message': '評分不存在或無權限修改'}, 404
        return rating.to_dict()
    except ValueError as e:
        return {'message': str(e)}, 400
    except Exception as e:
        print(f"更新評分錯誤: {str(e)}")  # 添加錯誤日誌
        return {'message': f'更新評分失敗: {str(e)}'}, 500

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
        404: 評分不存在或無權限刪除
        500: 服務器錯誤
    """
    try:
        service = RatingService()
        # 獲取當前用戶ID
        current_user_id = int(get_jwt_identity())
        
        # 添加調試日誌
        print(f"當前用戶ID: {current_user_id}")
        print(f"要刪除的評分ID: {path.rating_id}")
        
        # 先獲取評分信息
        rating = service.get_rating(path.rating_id)
        if rating:
            print(f"評分擁有者ID: {rating.user_id}")
        
        # 刪除評分
        if service.delete_rating(current_user_id, path.rating_id):
            return '', 204
        return {'message': '評分不存在或無權限刪除'}, 404
    except ValueError as e:
        return {'message': str(e)}, 400
    except Exception as e:
        print(f"刪除評分錯誤: {str(e)}")  # 添加錯誤日誌
        return {'message': f'刪除評分失敗: {str(e)}'}, 500 