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
        return {
            'favorites': [
                {
                    'id': favorite.id,
                    'user_id': favorite.user_id,
                    'store_id': favorite.store_id,
                    'store_name': favorite.store_name,
                    'store_image': favorite.store_image,
                    'address': favorite.address,
                    'city': favorite.city,
                    'city_CN': favorite.city_CN,
                    'customer_phone': favorite.customer_phone,
                    'description': favorite.description,
                    'is_new_until': favorite.is_new_until,
                    'redirection_url': favorite.redirection_url,
                    'navigation_url': favorite.navigation_url,
                    'rating': favorite.rating,
                    'review_number': favorite.review_number,
                    'username': favorite.username,
                    'created_at': favorite.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'updated_at': favorite.updated_at.strftime('%Y-%m-%d %H:%M:%S')
                } for favorite in favorites
            ]
        }
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
        favorite = service.create_favorite(
            user_id=user_id,
            store_id=body.store_id
        )
        return favorite.to_dict(), 201
    except ValueError as e:
        return {'message': str(e)}, 400
    except Exception as e:
        print(str(e))
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

@favorite_bp.get('/check/<int:store_id>', tags=[favorite_tag])
@jwt_required()
def check_favorite_status(path: FavoriteCheckPath):
    """檢查指定店家是否已收藏
    
    Args:
        path (FavoriteCheckPath): 路徑參數，包含店家ID
    
    Returns:
        200: 
            is_favorite (bool): 是否已收藏
            favorite_id (int): 最愛ID(如果已收藏)
        401: 未登入
        500: 服務器錯誤
    """
    try:
        user_id = get_jwt_identity()
        if not user_id:
            logger.error("未獲取到用戶ID")
            return {'message': '請先登入'}, 401
            
        logger.info(f"開始檢查最愛狀態 - 用戶ID: {user_id}, 店家ID: {path.store_id}")
        
        if not path.store_id or path.store_id <= 0:
            logger.error(f"無效的店家ID: {path.store_id}")
            return {'message': '無效的店家ID'}, 400
        
        service = FavoriteService()
        result = service.check_favorite_status(user_id, path.store_id)
        logger.info(f"檢查最愛狀態結果: {result}")
        
        if not isinstance(result, dict) or 'is_favorite' not in result:
            logger.error(f"服務返回無效的結果格式: {result}")
            return {'message': '服務器內部錯誤'}, 500
        
        response_data = {
            'favorites': [{
                'id': result['favorite_id'],
                'user_id': user_id,
                'store_id': path.store_id,
                'is_favorite': result['is_favorite']
            }] if result['is_favorite'] else []
        }
        logger.info(f"返回的資料: {response_data}")
        
        return response_data, 200
        
    except ValueError as e:
        error_msg = f"參數錯誤: {str(e)}"
        logger.error(error_msg)
        return {'message': error_msg}, 400
        
    except Exception as e:
        error_msg = f"檢查最愛狀態錯誤: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return {
            'message': '檢查最愛狀態失敗',
            'error': str(e),
            'status': 'error'
        }, 500 