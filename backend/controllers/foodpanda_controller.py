from flask_openapi3 import APIBlueprint, Tag
from services.foodpanda_service import FoodpandaService
from schemas.foodpanda_schema import *
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging

logger = logging.getLogger(__name__)

# 創建多個藍圖，對應不同的路由前綴
foodpanda_core_bp = APIBlueprint('foodpanda_core', __name__, url_prefix='')
foodpanda_vendors_bp = APIBlueprint('foodpanda_vendors', __name__, url_prefix='/listing/api/v1/pandora')
foodpanda_menu_bp = APIBlueprint('foodpanda_menu', __name__, url_prefix='/api/v5')
foodpanda_feed_bp = APIBlueprint('foodpanda_feed', __name__, url_prefix='/vendors-gateway/api/v1/pandora')

foodpanda_tag = Tag(name='foodpanda', description='Foodpanda API')

# 推薦餐廳路由
@foodpanda_core_bp.get(
    "/api/v1/swimlanes", 
    tags=[foodpanda_tag],
    security=[{"ApiKeyAuth": []}]
)
def get_recommendations(query: swimlanesQuery):
    """獲取推薦餐廳
    
    Args:
        query: 查詢參數
            - longitude: 經度
            - latitude: 緯度
            - way: 取餐方式
            
    Returns:
        200: 推薦餐廳列表
        400: 參數錯誤
        500: 服務器錯誤
    """
    try:
        service = FoodpandaService()
        return service.get_recommendation_restaurants(
            longitude=query.longitude,
            latitude=query.latitude,
            way=query.way
        )
    except ValueError as e:
        return {'message': str(e)}, 400
    except Exception as e:
        logger.error(f"獲取推薦餐廳錯誤: {str(e)}", exc_info=True)
        return {'message': '獲取推薦餐廳失敗'}, 500

# 附近餐廳路由
@foodpanda_vendors_bp.get(
    "/vendors", 
    tags=[foodpanda_tag],
    security=[{"ApiKeyAuth": []}]
)
def get_nearby_restaurants(query: vendorsQuery):
    """獲取附近餐廳
    
    Args:
        query: 查詢參數
            - longitude: 經度
            - latitude: 緯度
            - way: 取餐方式
            - sort: 排序方式
            - cuisine: 料理類型
            - limit: 數量限制
            - offset: 偏移量
            
    Returns:
        200: 餐廳列表
        400: 參數錯誤
        500: 服務器錯誤
    """
    try:
        service = FoodpandaService()
        return service.get_nearby_restaurants(**query.dict())
    except ValueError as e:
        return {'message': str(e)}, 400
    except Exception as e:
        logger.error(f"獲取附近餐廳錯誤: {str(e)}", exc_info=True)
        return {'message': '獲取附近餐廳失敗'}, 500

# 餐廳菜單路由
@foodpanda_menu_bp.get(
    "/vendors/<restaurant_code>", 
    tags=[foodpanda_tag]
)
def get_restaurant_menu(path: getMenuRequest, query: MenuQuery):
    """獲取餐廳菜單
    
    Args:
        restaurant_code: 餐廳代碼
        query: 查詢參數
            - longitude: 經度
            - latitude: 緯度
            
    Returns:
        200: 餐廳菜單
        400: 參數錯誤
        404: 餐廳不存在
        500: 服務器錯誤
    """
    try:
        service = FoodpandaService()
        menu = service.get_restaurant_menu(
            restaurant_code=path.restaurant_code,
            longitude=query.longitude,
            latitude=query.latitude
        )
        if not menu:
            return {'message': '餐廳不存在'}, 404
        return menu
    except ValueError as e:
        return {'message': str(e)}, 400
    except Exception as e:
        logger.error(f"獲取餐廳菜單錯誤: {str(e)}", exc_info=True)
        return {'message': '獲取餐廳菜單失敗'}, 500

# 搜尋餐廳路由
@foodpanda_feed_bp.get(
    "/search",
    tags=[foodpanda_tag],
    security=[{"ApiKeyAuth": []}]
)
def search_restaurants(query: SearchRestaurantQuery):
    """搜尋餐廳
    
    Args:
        query: 查詢參數
            - query: 搜尋關鍵字
            - longitude: 經度
            - latitude: 緯度
            - limit: 限制筆數
            - offset: 偏移量
            - configuration: 配置類型
            - vertical: 垂直類型
            - search_vertical: 搜尋垂直類型
            - include_component_types: 包含組件類型
            - include_fields: 包含字段
            - language_id: 語言ID
            - opening_type: 開放類型
            
    Returns:
        200:
            - status_code: 狀態碼
            - message: 訊息
            - data: 
                - available_count: 可用餐廳數量
                - returned_count: 返回餐廳數量
                - items: 餐廳列表
                - aggregations: 分類統計
        400: 參數錯誤
        500: 服務器錯誤
    """
    try:
        service = FoodpandaService()
        result = service.search_restaurants(
            keyword=query.query,
            longitude=query.longitude,
            latitude=query.latitude,
            limit=query.limit,
            offset=query.offset
        )
        return result
    except ValueError as e:
        return {'message': str(e)}, 400
    except Exception as e:
        logger.error(f"搜尋餐廳錯誤: {str(e)}", exc_info=True)
        return {'message': '搜尋餐廳失敗'}, 500 