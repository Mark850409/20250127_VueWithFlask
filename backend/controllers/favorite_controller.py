from flask_openapi3 import APIBlueprint, Tag
from services.favorite_service import FavoriteService
from schemas.favorite_schema import *
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging

logger = logging.getLogger(__name__)

favorite_bp = APIBlueprint('favorites', __name__, url_prefix='/api/favorites')
favorite_tag = Tag(name='favorites', description='最愛管理')

@favorite_bp.get('/', tags=[favorite_tag])
@jwt_required()
def get_favorites():
    """獲取當前用戶的所有最愛
    
    Returns:
        200: 
            favorites (List[FavoriteResponseSchema]): 最愛列表
        401: 未登入
        500: 服務器錯誤
    """
    try:
        user_id = get_jwt_identity()
        service = FavoriteService()
        favorites = service.get_user_favorites(user_id)
        return {'favorites': [favorite.to_dict() for favorite in favorites]}
    except Exception as e:
        logger.error(f"獲取最愛列表錯誤: {str(e)}", exc_info=True)
        return {'message': f'獲取最愛列表失敗: {str(e)}'}, 500

@favorite_bp.post('/', tags=[favorite_tag])
@jwt_required()
def create_favorite(body: FavoriteCreateSchema):
    """添加最愛
    
    Args:
        body (FavoriteCreateSchema): 最愛數據
    
    Returns:
        201: 創建成功
        400: 參數錯誤
        401: 未登入
        500: 服務器錯誤
    """
    try:
        user_id = get_jwt_identity()
        service = FavoriteService()
        favorite = service.create_favorite(user_id, body.store_id)
        return favorite.to_dict(), 201
    except ValueError as e:
        return {'message': str(e)}, 400
    except Exception as e:
        logger.error(f"創建最愛錯誤: {str(e)}", exc_info=True)
        return {'message': '創建最愛失敗'}, 500

@favorite_bp.delete('/<int:favorite_id>', tags=[favorite_tag])
@jwt_required()
def delete_favorite(path: FavoritePath):
    """刪除最愛
    
    Args:
        path (FavoritePath): 路徑參數
    
    Returns:
        204: 刪除成功
        401: 未登入
        404: 最愛不存在
        500: 刪除失敗
    """
    try:
        user_id = get_jwt_identity()
        service = FavoriteService()
        if service.delete_favorite(path.favorite_id, user_id):
            return '', 204
        return {'message': '最愛不存在'}, 404
    except ValueError as e:
        return {'message': str(e)}, 400
    except Exception as e:
        logger.error(f"刪除最愛錯誤: {str(e)}", exc_info=True)
        return {'message': '刪除最愛失敗'}, 500 