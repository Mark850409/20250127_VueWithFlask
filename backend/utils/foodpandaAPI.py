import time
import json
import requests
import logging

logger = logging.getLogger(__name__)

class FoodPandaSpider():
    """foodpanda 爬蟲"""

    def __init__(self, longitude, latitude) -> None:
        """初始化

        :param longitude: 自身所在經度
        :param latitude: 自身所在緯度
        """
        self.longitude = longitude
        self.latitude = latitude
        # 簡化 headers
        self.base_headers = {
            'accept': '*/*'
        }
        self.headers = {
            'x-disco-client-id': 'web',  # 添加必要的 header
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.recommendation_url = 'https://disco.deliveryhero.io/listing/api/v1/pandora/vendors'
        self.service_url = 'https://tw.fd-api.com/api/v5'

    def request_get(self, url, params=None, headers=None):
        """送出 GET 請求，取得回傳 JSON 資料"""
        # 合併 headers
        request_headers = {**self.base_headers, **(headers or {})}
        
        r = requests.get(url, params=params, headers=request_headers)
        if r.status_code != requests.codes.ok:
            print(f'網頁載入發生問題：{url}')
            print(f'Status code: {r.status_code}')
            print(f'Response: {r.text}')
            return None
        try:
            return r.json()
        except Exception as e:
            print(e)
            return None

    def request_post(self, url, params=None, data=None, headers=None):
        """送出 POST 請求，取得回傳 JSON 資料

        :param url: 請求網址
        :param params: 傳遞參數資料
        :param data: 傳遞 data 資料
        :param headers: 傳遞 headers 資料
        :return data: requests 回應資料
        """
        # 合併 headers
        request_headers = {
            **self.base_headers,
            'content-type': 'application/json',
            **(headers or {})
        }
        
        r = requests.post(url, params=params, data=data, headers=request_headers)
        if r.status_code != requests.codes.ok:
            print(f'網頁載入發生問題：{url}')
            print(f'Status code: {r.status_code}')
            print(f'Response: {r.text}')
            return None
        try:
            data = r.json()
        except Exception as e:
            print(e)
            return None
        return data

    def search_restaurants(self, keyword, limit=48, offset=0):
        """搜尋餐廳"""
        url = 'https://tw.fd-api.com/vendors-gateway/api/v1/pandora/search'
        params = {
            'query': keyword,
            'longitude': self.longitude,
            'latitude': self.latitude,
            'configuration': 'undefined',
            'vertical': 'restaurants',
            'search_vertical': 'restaurants',
            'include_component_types': 'vendors',
            'include_fields': 'feed',
            'language_id': '6',
            'opening_type': 'delivery',
            'platform': 'web',
            'language_code': 'zh',
            'customer_type': 'regular',
            'limit': limit,
            'offset': offset,
            'dynamic_pricing': 0,
            'brand': 'foodpanda',
            'country_code': 'tw',
            'use_free_delivery_label': 'false'
        }
        
        headers = {
            'accept': 'application/json',
            'x-disco-client-id': 'web'
        }
        
        data = self.request_get(url=url, params=params, headers=headers)
        if not data:
            print('搜尋餐廳失敗')
            return []

        try:
            response = {
                'status_code': data.get('status_code'),
                'message': data.get('message'),
                'data': {
                    'available_count': data['data'].get('available_count'),
                    'returned_count': data['data'].get('returned_count'),
                    'items': data['data'].get('items', []),
                    'aggregations': data['data'].get('aggregations', {})
                }
            }
            return response
        except Exception as e:
            print(f'資料格式有誤：{e}')
            return []

    def get_nearby_restaurants(
            self, way='外送', sort='', cuisine='', food_characteristic='',
            budgets='', has_discount=False, limit='', offset=''):
        """取得附近所有餐廳
        :param way: 取餐方式(外送、外帶自取、生鮮雜貨)
        :param sort: 餐廳排序(rating_desc、delivery_time_asc、distance_asc)
        :param cuisine: 料理種類
        :param food_characteristic: 特色
        :param budgets: 預算
        :param has_discount: 是否有折扣
        :return restaurants: 附近所有餐廳結果
        """
        url = 'https://disco.deliveryhero.io/listing/api/v1/pandora/vendors'
        query = {
            'longitude': self.longitude,
            'latitude': self.latitude,
            'language_id': 6,
            'include': 'characteristics',
            'dynamic_pricing': 0,
            'configuration': 'Variant1',
            'country': 'tw',
            'budgets': budgets,
            'cuisine': cuisine,
            'sort': sort,
            'food_characteristic': food_characteristic,
            'use_free_delivery_label': False,
            'vertical': 'restaurants',
            'limit': limit,
            'offset': offset,
            'customer_type': 'regular'
        }
        headers = {
            'x-disco-client-id': 'web',
        }
        # 取餐方式
        if way == '外送':
            query['vertical'] = 'restaurants'
        elif way == '外帶自取':
            query['vertical'] = 'restaurants'
            query['opening_type'] = 'pickup'
        else:
            query['vertical'] = 'shop'
        # 是否有折扣
        if has_discount:
            query['has_discount'] = 1

        curl_command = f"curl -X GET '{url}' \\\n"
        for key, value in query.items():
            curl_command += f"    -d '{key}={value}' \\\n"
        for key, value in headers.items():
            curl_command += f"    -H '{key}: {value}' \\\n"

        data = self.request_get(url=url, params=query, headers=headers)
        if not data:
            print('取得附近所有餐廳失敗')
            return []

        try:
            restaurants = data['data']['items']
            status_code = data['status_code']
            message = data['message']
            response = {
                "data": restaurants,
                "status_code": status_code,
                "message": message,
            }
        except Exception as e:
            print(f'資料格式有誤：{e}')
            return []
        return response

    def get_recommendation_restaurants(self, way='外送'):
        """取得分類推薦的餐廳

        :param way: 取餐方式(外送、外帶自取、生鮮雜貨)
        :return restaurants: 分類推薦結果
        """
        url = 'https://disco.deliveryhero.io/core/api/v1/swimlanes'
        query = {
            'longitude': self.longitude,
            'latitude': self.latitude,
            'brand': 'foodpanda',
            'language_code': 'zh',
            'language_id': 6,
            'country_code': 'tw',
            'dynamic_pricing': 0,
            'use_free_delivery_label': False,
            'customer_type': 'regular'
        }
        # 取餐方式
        if way == '外送':
            query['config'] = 'Original'
            query['vertical_type'] = 'restaurants'
            query['opening_type'] = 'delivery'
        elif way == '外帶自取':
            query['config'] = 'control'
            query['vertical_type'] = 'restaurants'
            query['opening_type'] = 'pickup'
        else:
            query['config'] = 'shops-variant'
            query['vertical_type'] = 'shop,darkstores'
            query['opening_type'] = 'delivery'

        data = self.request_get(url=url, params=query)
        if not data:
            print('取得分類推薦的餐廳失敗')
            return []

        try:
            recommendations = data['data']['items']
        except Exception as e:
            print(f'資料格式有誤：{e}')
            return []
        return recommendations

    def get_info_menu(self, restaurant_code):
        """取得餐廳基本資料與菜單

        :param restaurant_code: 餐廳代碼
        :return info_menu: 餐廳基本資料與菜單
        """
        url = f'https://tw.fd-api.com/api/v5/vendors/{restaurant_code}'
        query = {
            'include': 'menus',
            'language_id': '6',
            'dynamic_pricing': '0',
            'opening_type': 'delivery',
            'longitude': self.longitude,  # 非必要(影響顯示距離)
            'latitude': self.latitude
        }
        data = self.request_get(url=url, params=query)
        if (not data) or ('data' not in data):
            print('取得餐廳菜單失敗')
            return {}
        info_menu = data['data']
        return info_menu


if __name__ == '__main__':
    foodpanda_spider = FoodPandaSpider('121.555', '25.0495')
    # 取得分類推薦的餐廳
    recommendations = foodpanda_spider.get_recommendation_restaurants()
    print(recommendations[0]['headline'])
    for recommendation in recommendations[:2]:
        if recommendation['headline'] != '在家吃遍全世界':
            print(recommendation['vendors'])
