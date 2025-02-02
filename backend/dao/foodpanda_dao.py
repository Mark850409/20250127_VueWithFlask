from typing import List, Optional
from models.foodpanda import FoodpandaSearch, db
from utils.foodpandaAPI import FoodPandaSpider
import logging

logger = logging.getLogger(__name__)

class FoodpandaDAO:
    @staticmethod
    def search_restaurants(user_id: int, keyword: str, longitude: str, latitude: str) -> dict:
        """搜尋餐廳"""
        try:
            # 記錄搜尋
            search = FoodpandaSearch(
                user_id=user_id,
                keyword=keyword,
                longitude=longitude,
                latitude=latitude
            )
            db.session.add(search)
            db.session.commit()
            
            # 調用 Foodpanda API
            spider = FoodPandaSpider(longitude=longitude, latitude=latitude)
            results = spider.search_restaurants(keyword=keyword)
            
            return {
                'search_id': search.id,
                'results': results
            }
        except Exception as e:
            logger.error(f"搜尋餐廳錯誤: {str(e)}", exc_info=True)
            raise

    @staticmethod
    def get_nearby_restaurants(longitude: str, latitude: str, **kwargs) -> dict:
        """獲取附近餐廳"""
        try:
            spider = FoodPandaSpider(longitude=longitude, latitude=latitude)
            return spider.get_nearby_restaurants(**kwargs)
        except Exception as e:
            logger.error(f"獲取附近餐廳錯誤: {str(e)}", exc_info=True)
            raise

    @staticmethod
    def get_recommendation_restaurants(longitude: str, latitude: str, way: str = '外送') -> List[dict]:
        """獲取推薦餐廳"""
        try:
            spider = FoodPandaSpider(longitude=longitude, latitude=latitude)
            return spider.get_recommendation_restaurants(way=way)
        except Exception as e:
            logger.error(f"獲取推薦餐廳錯誤: {str(e)}", exc_info=True)
            raise

    @staticmethod
    def get_restaurant_menu(restaurant_code: str, longitude: str, latitude: str) -> dict:
        """獲取餐廳菜單"""
        try:
            spider = FoodPandaSpider(longitude=longitude, latitude=latitude)
            return spider.get_info_menu(restaurant_code=restaurant_code)
        except Exception as e:
            logger.error(f"獲取餐廳菜單錯誤: {str(e)}", exc_info=True)
            raise 