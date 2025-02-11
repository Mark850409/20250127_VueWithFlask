from dao.googlemaps_dao import GoogleMapsDAO
from typing import Dict, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class GoogleMapsService:
    def __init__(self, api_key: str):
        self.dao = GoogleMapsDAO(api_key)
    
    def find_place(self, input_text: str) -> Dict:
        """搜尋地點"""
        try:
            place_id = self.dao.find_place(input_text)
            return {'place_id': place_id}
        except Exception as e:
            logger.error(f"搜尋地點失敗: {str(e)}")
            raise ValueError(str(e))
    
    def get_place_details(self, place_id: str, language: str = 'zh-TW') -> Dict:
        """獲取地點詳細資訊"""
        try:
            name, reviews = self.dao.get_place_details(place_id, language)
            return {
                'restaurant_name': name,
                'reviews': reviews
            }
        except Exception as e:
            logger.error(f"獲取地點詳細資訊失敗: {str(e)}")
            raise ValueError(str(e))
    
    def search_nearby(
        self,
        latitude: float,
        longitude: float,
        radius: int,
        place_type: str,
        keyword: Optional[str] = None
    ) -> Dict:
        """搜尋附近地點"""
        try:
            location = {'lat': latitude, 'lng': longitude}
            places = self.dao.search_nearby(
                location=location,
                radius=radius,
                place_type=place_type,
                keyword=keyword
            )
            return {'results': places}
        except Exception as e:
            logger.error(f"搜尋附近地點失敗: {str(e)}")
            raise ValueError(str(e))
    
    def get_navigation_url(
        self,
        start_address: str,
        end_address: str,
        mode: str = 'driving',
        avoid: Optional[List[str]] = None
    ) -> Dict:
        """獲取導航 URL"""
        try:
            url = self.dao.get_navigation_url(
                start_address=start_address,
                end_address=end_address,
                mode=mode,
                avoid=avoid
            )
            return {'navigation_url': url}
        except Exception as e:
            logger.error(f"獲取導航 URL 失敗: {str(e)}")
            raise ValueError(str(e))
    
    def get_distance_matrix(
        self,
        origins: List[str],
        destinations: List[str],
        mode: str = 'driving'
    ) -> Dict:
        """獲取距離矩陣"""
        try:
            result = self.dao.get_distance_matrix(
                origins=origins,
                destinations=destinations,
                mode=mode
            )
            return result
        except Exception as e:
            logger.error(f"獲取距離矩陣失敗: {str(e)}")
            raise ValueError(str(e))
    
    def reverse_geocode(
        self,
        latitude: float,
        longitude: float,
        language: str = 'zh-TW'
    ) -> Dict:
        """將經緯度轉換為地址"""
        try:
            result = self.dao.reverse_geocode(latitude, longitude, language)
            return result
        except Exception as e:
            logger.error(f"地理編碼失敗: {str(e)}")
            raise ValueError(str(e)) 