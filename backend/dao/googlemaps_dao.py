from googlemaps import Client as GoogleMaps
from utils.time_utils import convert_to_taiwan_time
from typing import List, Dict, Optional, Tuple
import requests
from urllib.parse import urlencode

class GoogleMapsDAO:
    def __init__(self, api_key: str):
        """初始化 Google Maps 客戶端"""
        self.api_key = api_key
        self.gmaps = GoogleMaps(api_key)

    def find_place(self, input_text: str) -> str:
        """
        根據文字搜尋地點
        
        Args:
            input_text: 搜尋文字
            
        Returns:
            place_id: 地點ID
            
        Raises:
            ValueError: 找不到地點時拋出
        """
        try:
            result = self.gmaps.find_place(input_text, 'textquery')
            if not result['candidates']:
                raise ValueError('找不到符合的地點')
            return result['candidates'][0]['place_id']
        except Exception as e:
            raise ValueError(f'搜尋地點失敗: {str(e)}')

    def get_place_details(self, place_id: str, language: str = 'zh-TW') -> Tuple[str, List[Dict]]:
        """
        獲取地點詳細資訊
        
        Args:
            place_id: 地點ID
            language: 語言代碼
            
        Returns:
            Tuple[店名, 評論列表]
            
        Raises:
            ValueError: 獲取詳細資訊失敗時拋出
        """
        try:
            result = self.gmaps.place(place_id, language=language)
            if 'result' not in result:
                raise ValueError('無法獲取地點資訊')
                
            place_data = result['result']
            restaurant_name = place_data.get('name', 'Unknown')
            reviews = place_data.get('reviews', [])
            
            formatted_reviews = [{
                'author_name': review['author_name'],
                'rating': review['rating'],
                'text': review['text'],
                'time': convert_to_taiwan_time(review['time'])
            } for review in reviews]
            
            return restaurant_name, formatted_reviews
        except Exception as e:
            raise ValueError(f'獲取地點詳細資訊失敗: {str(e)}')

    def search_nearby(
        self, 
        location: Dict[str, float], 
        radius: int, 
        place_type: str,
        keyword: Optional[str] = None,
        language: str = 'zh-TW'
    ) -> List[Dict]:
        """
        搜尋附近地點
        
        Args:
            location: 包含經緯度的字典
            radius: 搜尋半徑(公尺)
            place_type: 地點類型
            keyword: 關鍵字
            language: 語言代碼
            
        Returns:
            地點列表
            
        Raises:
            ValueError: 搜尋失敗時拋出
        """
        try:
            params = {
                'location': location,
                'radius': radius,
                'type': place_type,
                'language': language
            }
            if keyword:
                params['keyword'] = keyword
                
            result = self.gmaps.places_nearby(**params)
            
            places = [{
                'name': place['name'],
                'place_id': place['place_id'],
                'vicinity': place.get('vicinity', 'N/A'),
                'rating': place.get('rating', 0),
                'user_ratings_total': place.get('user_ratings_total', 0),
                'location': place['geometry']['location'],
                'types': place.get('types', []),
                'business_status': place.get('business_status', 'UNKNOWN')
            } for place in result.get('results', [])]
            
            return places
        except Exception as e:
            raise ValueError(f'搜尋附近地點失敗: {str(e)}')

    def get_navigation_url(
        self, 
        start_address: str, 
        end_address: str,
        mode: str = 'driving',
        avoid: Optional[List[str]] = None
    ) -> str:
        """
        獲取導航 URL
        
        Args:
            start_address: 起點地址
            end_address: 終點地址
            mode: 交通方式 (driving/walking/bicycling/transit)
            avoid: 避開項目列表 (tolls/highways/ferries)
            
        Returns:
            導航 URL
            
        Raises:
            ValueError: 生成導航 URL 失敗時拋出
        """
        try:
            # 編碼地址
            start_encoded = urlencode({'': start_address})[1:]
            end_encoded = urlencode({'': end_address})[1:]
            
            # 構建基本 URL
            url = (
                'https://www.google.com/maps/dir/'
                f'?api=1'
                f'&origin={start_encoded}'
                f'&destination={end_encoded}'
                f'&travelmode={mode}'
            )
            
            # 添加避開選項
            if avoid:
                url += f'&avoid={"|".join(avoid)}'
            
            return url
        except Exception as e:
            raise ValueError(f'生成導航 URL 失敗: {str(e)}')

    def get_distance_matrix(
        self,
        origins: List[str],
        destinations: List[str],
        mode: str = 'driving',
        language: str = 'zh-TW'
    ) -> Dict:
        """
        獲取距離矩陣
        
        Args:
            origins: 起點地址列表
            destinations: 終點地址列表
            mode: 交通方式
            language: 語言代碼
            
        Returns:
            距離矩陣資訊
            
        Raises:
            ValueError: 獲取距離矩陣失敗時拋出
        """
        try:
            result = self.gmaps.distance_matrix(
                origins=origins,
                destinations=destinations,
                mode=mode,
                language=language
            )
            
            if result['status'] != 'OK':
                raise ValueError(f'距離矩陣請求失敗: {result["status"]}')
                
            return result
        except Exception as e:
            raise ValueError(f'獲取距離矩陣失敗: {str(e)}')

    def reverse_geocode(
        self,
        latitude: float,
        longitude: float,
        language: str = 'zh-TW'
    ) -> Dict:
        """
        將經緯度轉換為地址
        
        Args:
            latitude: 緯度
            longitude: 經度
            language: 語言代碼
            
        Returns:
            Dict: 包含地址信息的字典
            
        Raises:
            ValueError: 轉換失敗時拋出
        """
        try:
            result = self.gmaps.reverse_geocode(
                (latitude, longitude),
                language=language
            )
            
            if not result:
                raise ValueError('無法獲取地址信息')
                
            address_components = result[0]['address_components']
            formatted_address = result[0]['formatted_address']
            
            # 解析地址組件
            city = next(
                (comp['long_name'] for comp in address_components 
                 if 'administrative_area_level_1' in comp['types']),
                None
            )
            
            city_district = next(
                (comp['long_name'] for comp in address_components 
                 if 'administrative_area_level_2' in comp['types']),
                None
            )
            
            postal_code = next(
                (comp['long_name'] for comp in address_components 
                 if 'postal_code' in comp['types']),
                None
            )
            
            return {
                'formatted_address': formatted_address,
                'city': city,
                'city_district': city_district,
                'postal_code': postal_code
            }
            
        except Exception as e:
            raise ValueError(f'地理編碼失敗: {str(e)}') 