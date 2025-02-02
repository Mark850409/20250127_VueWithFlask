from flask_openapi3 import APIBlueprint, Tag
from flask import jsonify
from services.restaurant_service import RestaurantService
from schemas.restaurant_schema import ErrorResponse, SuccessResponse
import logging

logger = logging.getLogger(__name__)
restaurant_tag = Tag(name='restaurant', description='餐廳資料管理')

restaurant_bp = APIBlueprint('restaurant', __name__, url_prefix='/api/v1/restaurants')
service = RestaurantService()

@restaurant_bp.get(
    '/crawl',
    tags=[restaurant_tag],
    responses={"200": SuccessResponse, "400": ErrorResponse, "500": ErrorResponse}
)
def crawl_restaurants():
    """
    爬取 Foodpanda 餐廳資料
    
    此端點會爬取 Foodpanda 上的餐廳資料並存入資料庫
    """
    try:
        result = service.crawl_restaurants()
        return jsonify(result)
    except Exception as e:
        logger.error(f"爬取餐廳資料失敗: {str(e)}")
        return jsonify({'error': '爬取資料失敗'}), 500 