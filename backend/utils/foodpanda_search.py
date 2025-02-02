import json
import requests
from urllib.parse import urlencode

# 基本 URL
base_url = 'https://tw.fd-api.com/vendors-gateway/api/v1/pandora/search'

# 請求參數
params = {
    'query': '星巴克',
    'longitude': 120.3025185,  # 經度
    'latitude': 22.639473,  # 緯度,
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
    'limit': 48,  # 一次最多顯示幾筆(預設 48 筆)
    'offset': 0,  # 偏移值，想要獲取更多資料時使用
    'dynamic_pricing': 0,
    'brand': 'foodpanda',
    'country_code': 'tw',
    'use_free_delivery_label': 'false'
}

# Headers
headers = {
    'accept': 'application/json',
    'x-disco-client-id': 'web'
}

# 發送 GET 請求
r = requests.get(
    url=base_url,
    params=params,
    headers=headers
)

if r.status_code == requests.codes.ok:
    data = r.json()
    
    # 取得基本資訊
    status_code = data.get('status_code')
    message = data.get('message')
    available_count = data['data'].get('available_count')
    returned_count = data['data'].get('returned_count')
    
    print(f"狀態碼: {status_code}")
    print(f"訊息: {message}")
    print(f"可用餐廳數量: {available_count}")
    print(f"返回餐廳數量: {returned_count}")
    print("\n=== 餐廳列表 ===")
    
    # 取得餐廳列表
    restaurants = data['data']['items']
    for i, restaurant in enumerate(restaurants, 1):
        print(f"\n{i}. 餐廳資訊:")
        print(f"ID: {restaurant.get('id')}")
        print(f"代碼: {restaurant.get('code')}")
        print(f"名稱: {restaurant.get('name')}")
        print(f"地址: {restaurant.get('address')}")
        print(f"接受指示: {restaurant.get('accepts_instructions')}")
        
        # 如果需要更多資訊，可以繼續添加
        if 'rating' in restaurant:
            print(f"評分: {restaurant['rating']}")
        if 'minimum_order_amount' in restaurant:
            print(f"最低訂單金額: {restaurant['minimum_order_amount']}")
        if 'delivery_fee' in restaurant:
            print(f"外送費: {restaurant['delivery_fee']}")
    
    # 取得分類資訊
    if 'aggregations' in data['data']:
        print("\n=== 分類統計 ===")
        aggregations = data['data']['aggregations']
        if 'cuisines' in aggregations:
            print("\n料理類型:")
            for cuisine in aggregations['cuisines']:
                print(f"{cuisine['title']}: {cuisine['count']}家")
else:
    print('請求失敗')
    print(f'Status code: {r.status_code}')
    print(f'Response: {r.text}')
