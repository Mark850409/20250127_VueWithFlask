from flask import Blueprint, jsonify
from flask_cors import CORS
from model.restaurant_type_list import restaurant_type_list
from extensions import db
from sqlalchemy.sql import text
import random
from sqlalchemy.orm.exc import NoResultFound
from utils.foodpandaAPI import FoodPandaSpider
from datetime import datetime, timedelta
from config.setting import COUNTRY_COUNT, TIMEOUT_SECONDS, COORDINATES, COUNTRY_RANGES, CITY_TRANSLATION
import re
from dao.drink_dao import DrinkDAO
from schemas.drink_schemas import ErrorResponse
from sqlalchemy.exc import SQLAlchemyError

# 註冊路由
restaurant_route = Blueprint('restaurant_route', __name__)

# 避免前端call api產生CORS問題，因此加入這一行
CORS(restaurant_route)

# 各餐廳縣市抓取筆數
COUNTRY_COUNT = COUNTRY_COUNT

# 定義超時時間（秒）
TIMEOUT_SECONDS = TIMEOUT_SECONDS  # 假設超過120秒就視為超時

# 縣市經緯度範圍
COUNTRY_RANGES = COUNTRY_RANGES

# 英文到中文的城市名稱對應
CITY_TRANSLATION = CITY_TRANSLATION


def generate_new_coordinates(county):
    """
    生成隨機經緯度，範圍限制在指定縣市內
    """
    range = COUNTRY_RANGES[county]
    latitude = random.uniform(range['lat_min'], range['lat_max'])
    longitude = random.uniform(range['lng_min'], range['lng_max'])
    return latitude, longitude


def normalize_address(address, city, name):
    """
    正規化地址，去除括號中的任意內容，並取出地址的前三個字作為 city_CN
    :param address: 原地址
    :return: 正規化後的地址和 city_CN
    """
    normalized_address = re.sub(r'\(.*?\)', '', address).strip()  # 去除括號及其中的內容，並去除左右空白
    city_CN = CITY_TRANSLATION.get(city, city)  # 轉換城市名稱為中文，若無對應則使用原名
    normalized_name = re.sub(r'\s*\(\s*(.*?)\s*\)\s*', r'(\1)', name).strip()  # 去除括號及其中的內容，並去除左右空白
    return normalized_address, city_CN, normalized_name


# 首頁進入點
@restaurant_route.route('/', methods=['GET'])
def InsertDrink():
    """
    將FoodPanda爬取的資料寫入飲料店管理資料庫
    """
    try:
        # 移除資料表
        db.session.execute(text("DROP TABLE IF EXISTS restaurant_type_list"))
        # 提交
        db.session.commit()
        # 重建資料表
        db.create_all()
        # 重設auto_increment
        db.session.execute(text("ALTER TABLE restaurant_type_list AUTO_INCREMENT = 1"))

        # 定義目前所在地經緯度
        coordinates = COORDINATES

        # 記錄每個縣市已抓取的筆數
        fetched_count = {county: 0 for county in coordinates}

        # 設定最大抓取時間為120秒
        max_fetch_time = timedelta(seconds=TIMEOUT_SECONDS)  # seconds

        print("===============================")

        for county, location in coordinates.items():
            start_time = datetime.now()
            print(f"開始時間: {start_time.strftime('%Y年%m月%d日 %H時%M分%S秒')}")

            while fetched_count[county] < COUNTRY_COUNT:
                current_time = datetime.now()
                print(f"目前時間: {current_time.strftime('%Y年%m月%d日 %H時%M分%S秒')}")
                latitude, longitude = location
                print(f"目前抓取的縣市: {county}, 筆數: {fetched_count[county]}")
                print(f"經緯度為: {latitude, longitude}")

                # 初始化並傳入經緯度
                foodpanda_spider = FoodPandaSpider(longitude, latitude)

                # 取得附近所有餐廳
                restaurants = foodpanda_spider.get_nearby_restaurants(
                    way='外送',
                    cuisine='181',
                    limit=COUNTRY_COUNT,
                )

                new_restaurants = []

                for restaurant in restaurants['data']:
                    try:
                        # 檢查餐廳是否已存在於資料庫中
                        db.session.query(restaurant_type_list).filter_by(name=restaurant['name']).one()
                    except NoResultFound:
                        # 若餐廳不存在，則新增到 new_restaurants 列表中
                        normalized_address, city_CN, normalized_name = normalize_address(restaurant['address'], county,
                                                                                         restaurant['name'])
                        restaurant['address'] = normalized_address
                        restaurant['city_CN'] = city_CN
                        restaurant['normalized_name'] = normalized_name
                        new_restaurants.append(restaurant)

                # 提取需要的字段並構建新字典
                for item in new_restaurants:
                    new_dinks = {
                        'name': item['name'],
                        'normalized_name': item['normalized_name'],
                        'address': item['address'],
                        'budget': item['budget'],
                        'city': item['city']['name'],
                        'city_CN': item['city_CN'],
                        'customer_phone': item['customer_phone'],
                        'description': item['description'],
                        'hero_image': item['hero_image'],
                        'hero_listing_image': item['hero_listing_image'],
                        'distance': item['distance'],
                        'is_new_until': item['is_new_until'],
                        'latitude': item['latitude'],
                        'longitude': item['longitude'],
                        'minimum_delivery_fee': item['minimum_delivery_fee'],
                        'minimum_delivery_time': item['minimum_delivery_time'],
                        'minimum_order_amount': item['minimum_order_amount'],
                        'minimum_pickup_time': item['minimum_pickup_time'],
                        'primary_cuisine_id': item['primary_cuisine_id'],
                        'rating': item['rating'],
                        'redirection_url': item['redirection_url'],
                        'review_number': item['review_number'],
                        'tag': item['tag']
                    }
                    # 寫入資料庫
                    DrinkDAO.create_drink(new_dinks)

                # 寫入資料庫並更新已抓取的筆數
                fetched_count[county] += len(new_restaurants)

                # 若抓取不到100筆，生成新的經緯度並重新抓取
                if fetched_count[county] < COUNTRY_COUNT:
                    latitude, longitude = generate_new_coordinates(county)
                    location = (latitude, longitude)
                    print(f"新的經緯度為: {location}")

                # 計算總執行時間
                total_time = datetime.now() - start_time
                print(f"目前總執行時間: {total_time}秒")
                print(f"時間限制為: {max_fetch_time}秒")
                print(f"還有幾秒: {max_fetch_time - total_time}結束，即將跳過{county} 的抓取")
                print("===============================")
                # 單獨判斷該市或縣是否繼續抓取
                if datetime.now() - start_time > max_fetch_time:
                    print(f"超過時間，跳過 {county} 的抓取")
                    break
    # 捕捉SQL錯誤訊息
    except SQLAlchemyError as e:
        db.session.rollback()
        error_msg = str(e)
        sql_statement = getattr(e, 'statement', None)
        return jsonify(ErrorResponse(error='Database error occurred.', sql_error_message=error_msg,
                                     sql_statement=sql_statement).dict()), 500
    # 捕捉其他錯誤訊息
    except Exception as e:
        return jsonify(ErrorResponse(message=str(e)).dict()), 500
