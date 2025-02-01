from flask_openapi3 import APIBlueprint, Tag
from services.store_service import StoreService
from schemas.store_schema import *
from pydantic import BaseModel, Field

store_bp = APIBlueprint('stores', __name__, url_prefix='/api/stores')
store_tag = Tag(name='stores', description='店家管理')

class StorePath(BaseModel):
    """店家路徑參數"""
    store_id: int = Field(..., description='店家ID')

class CityPath(BaseModel):
    """城市路徑參數"""
    city: str = Field(..., description='城市名稱', example='台北')

@store_bp.get('/', tags=[store_tag])
def get_stores():
    """獲取所有店家
    
    Returns:
        200 (StoreResponseSchema): 店家列表
        500: 服務器錯誤
    """
    try:
        service = StoreService()
        stores = service.get_all_stores()
        return {'stores': [store.to_dict() for store in stores]}
    except Exception as e:
        return {'message': f'獲取店家列表失敗: {str(e)}'}, 500

@store_bp.post('/', tags=[store_tag])
def create_store(body: StoreCreateSchema):
    """創建店家
    
    Args:
        body (StoreCreateSchema): 店家數據
        
    Returns:
        201 (StoreResponseSchema): 創建成功
        400: 參數錯誤
        500: 服務器錯誤
    """
    try:
        service = StoreService()
        store = service.create_store(body.dict())
        return store.to_dict(), 201
    except ValueError as e:
        return {'message': str(e)}, 400
    except Exception as e:
        return {'message': f'創建店家失敗: {str(e)}'}, 500

@store_bp.get('/<int:store_id>', tags=[store_tag])
def get_store(path: StorePath):
    """獲取指定店家
    
    Args:
        path (StorePath): 路徑參數
            store_id (int): 店家ID
            
    Returns:
        200 (StoreResponseSchema): 查詢成功
        404: 店家不存在
        500: 服務器錯誤
    """
    try:
        service = StoreService()
        store = service.get_store(path.store_id)
        if not store:
            return {'message': '店家不存在'}, 404
            
        # 增加瀏覽次數
        service.view_store(path.store_id)
        return store.to_dict()
    except Exception as e:
        return {'message': f'獲取店家失敗: {str(e)}'}, 500

@store_bp.put('/<int:store_id>', tags=[store_tag])
def update_store(path: StorePath, body: StoreUpdateSchema):
    """更新店家
    
    Args:
        path (StorePath): 路徑參數
            store_id (int): 店家ID
        body (StoreUpdateSchema): 更新數據
            
    Returns:
        200 (StoreResponseSchema): 更新成功
        404: 店家不存在
        500: 服務器錯誤
    """
    try:
        service = StoreService()
        store = service.get_store(path.store_id)
        if not store:
            return {'message': '店家不存在'}, 404
            
        store = service.update_store(path.store_id, body.dict(exclude_unset=True))
        return store.to_dict()
    except Exception as e:
        return {'message': f'更新店家失敗: {str(e)}'}, 500

@store_bp.delete('/<int:store_id>', tags=[store_tag])
def delete_store(path: StorePath):
    """刪除店家
    
    Args:
        path (StorePath): 路徑參數
            store_id (int): 店家ID
            
    Returns:
        204: 刪除成功
        404: 店家不存在
        500: 刪除失敗
        
    Example:
        DELETE /api/stores/1
    """
    try:
        service = StoreService()
        store = service.get_store(path.store_id)
        if not store:
            return {'message': '店家不存在'}, 404
            
        if service.delete_store(path.store_id):
            return '', 204
        return {'message': '刪除失敗'}, 500
    except Exception as e:
        return {'message': f'刪除店家失敗: {str(e)}'}, 500

@store_bp.get('/city/<string:city>', tags=[store_tag])
def get_stores_by_city(path: CityPath):
    """獲取指定城市的店家
    
    Args:
        path (CityPath): 路徑參數
            city (str): 城市名稱，例如：台北、台中、高雄
            
    Returns:
        200 (StoreResponseSchema): 店家列表
            stores (List[Store]): 店家列表
        500: 服務器錯誤
    
    Example:
        GET /api/stores/city/台北
        
    Response Example:
        {
            "stores": [
                {
                    "id": 1,
                    "name": "春水堂",
                    "address": "台北市信義區信義路五段7號",
                    "city": "台北市",
                    "phone": "02-27201234",
                    "business_hours": "10:00-22:00",
                    "description": "台灣珍珠奶茶始祖",
                    "image_url": "https://example.com/store.jpg",
                    "status": "active",
                    "views": 100,
                    "avg_rating": 4.5,
                    "rating_count": 10,
                    "comment_count": 5,
                    "created_at": "2024-01-31 10:00:00",
                    "updated_at": "2024-01-31 10:00:00"
                }
            ]
        }
    """
    try:
        service = StoreService()
        stores = service.get_stores_by_city(path.city)
        return {'stores': [store.to_dict() for store in stores]}
    except Exception as e:
        return {'message': f'獲取店家列表失敗: {str(e)}'}, 500 