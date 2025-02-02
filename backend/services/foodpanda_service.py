from typing import List, Optional
from dao.foodpanda_dao import FoodpandaDAO
import logging

logger = logging.getLogger(__name__)

class FoodpandaService:
    def __init__(self):
        self.dao = FoodpandaDAO()
    
    def search_restaurants(self, keyword: str, longitude: float, latitude: float, limit: int = 48, offset: int = 0) -> dict:
        """搜尋餐廳"""
        try:
            return self.dao.search_restaurants(keyword, longitude, latitude, limit, offset)
        except Exception as e:
            logger.error(f"搜尋餐廳服務錯誤: {str(e)}", exc_info=True)
            raise ValueError(str(e))

    def get_nearby_restaurants(self, longitude: str, latitude: str, **kwargs) -> dict:
        """獲取附近餐廳"""
        try:
            return self.dao.get_nearby_restaurants(longitude, latitude, **kwargs)
        except Exception as e:
            logger.error(f"獲取附近餐廳服務錯誤: {str(e)}", exc_info=True)
            raise ValueError(str(e))

    def get_recommendation_restaurants(self, longitude: str, latitude: str, way: str = '外送') -> List[dict]:
        """獲取推薦餐廳"""
        try:
            return self.dao.get_recommendation_restaurants(longitude, latitude, way)
        except Exception as e:
            logger.error(f"獲取推薦餐廳服務錯誤: {str(e)}", exc_info=True)
            raise ValueError(str(e))

    def get_restaurant_menu(self, restaurant_code: str, longitude: str, latitude: str) -> dict:
        """獲取餐廳菜單"""
        try:
            return self.dao.get_restaurant_menu(restaurant_code, longitude, latitude)
        except Exception as e:
            logger.error(f"獲取餐廳菜單服務錯誤: {str(e)}", exc_info=True)
            raise ValueError(str(e)) 