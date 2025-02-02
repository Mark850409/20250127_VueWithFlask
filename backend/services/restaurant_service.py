from dao.restaurant_dao import RestaurantDAO
from utils.foodpandaAPI import FoodPandaSpider
from datetime import datetime, timedelta
import os
import json
import ast
import random
import re
import logging

logger = logging.getLogger(__name__)

class RestaurantService:
    def __init__(self):
        # 從環境變量讀取配置
        self.country_count = int(os.getenv('COUNTRY_COUNT', 100))
        self.timeout_seconds = int(os.getenv('TIMEOUT_SECONDS', 120))
        
        # 讀取並解析 COORDINATES
        coordinates_str = os.getenv('COORDINATES', '{}')
        try:
            self.coordinates = json.loads(coordinates_str)
        except Exception as e:
            logger.error(f"解析 COORDINATES 失敗: {str(e)}")
            self.coordinates = {}

        # 讀取並解析 COUNTRY_RANGES
        ranges_str = os.getenv('COUNTRY_RANGES', '{}')
        try:
            self.country_ranges = json.loads(ranges_str)
        except Exception as e:
            logger.error(f"解析 COUNTRY_RANGES 失敗: {str(e)}")
            self.country_ranges = {}

        # 讀取並解析 CITY_TRANSLATION
        translation_str = os.getenv('CITY_TRANSLATION', '{}')
        try:
            self.city_translation = json.loads(translation_str)
        except Exception as e:
            logger.error(f"解析 CITY_TRANSLATION 失敗: {str(e)}")
            self.city_translation = {}

        self.dao = RestaurantDAO()

    def generate_new_coordinates(self, county):
        """生成隨機經緯度"""
        range = self.country_ranges[county]
        latitude = random.uniform(range['lat_min'], range['lat_max'])
        longitude = random.uniform(range['lng_min'], range['lng_max'])
        return latitude, longitude

    def normalize_address(self, address, city, name):
        """正規化地址"""
        normalized_address = re.sub(r'\(.*?\)', '', address).strip()
        city_CN = self.city_translation.get(city, city)
        normalized_name = re.sub(r'\s*\(\s*(.*?)\s*\)\s*', r'(\1)', name).strip()
        return normalized_address, city_CN, normalized_name

    def crawl_restaurants(self):
        """爬取餐廳資料"""
        try:
            total_start_time = datetime.now()
            logger.info(f"開始爬取全台飲料店資料 - {total_start_time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # 重置資料表
            self.dao.reset_table()

            # 記錄每個縣市已抓取的筆數
            fetched_count = {county: 0 for county in self.coordinates}
            
            for county, location in self.coordinates.items():
                county_start_time = datetime.now()
                logger.info(f"\n{'='*50}")
                logger.info(f"開始抓取 {county} 的資料 - {county_start_time.strftime('%Y-%m-%d %H:%M:%S')}")
                logger.info(f"目標筆數: {self.country_count}")

                while fetched_count[county] < self.country_count:
                    current_time = datetime.now()
                    time_elapsed = (current_time - county_start_time).seconds
                    time_remaining = self.timeout_seconds - time_elapsed
                    
                    logger.info(f"\n目前進度:")
                    logger.info(f"- 縣市: {county}")
                    logger.info(f"- 已抓取: {fetched_count[county]} 筆")
                    logger.info(f"- 剩餘時間: {time_remaining} 秒")
                    logger.info(f"- 當前座標: ({location[0]:.6f}, {location[1]:.6f})")

                    latitude, longitude = location
                    spider = FoodPandaSpider(longitude, latitude)
                    restaurants = spider.get_nearby_restaurants(
                        way='外送',
                        cuisine='181',
                        limit=self.country_count
                    )

                    # 處理每個餐廳資料
                    for restaurant in restaurants['data']:
                        if not self.dao.find_by_name(restaurant['name']):
                            normalized_address, city_CN, normalized_name = self.normalize_address(
                                restaurant['address'], 
                                county,
                                restaurant['name']
                            )
                            
                            # 處理 is_new_until 日期時間格式
                            is_new_until = restaurant.get('is_new_until')
                            if is_new_until and is_new_until.strip():  # 確保不是空字符串
                                try:
                                    # 處理不同的日期時間格式
                                    if 'T' in is_new_until:
                                        # 處理 ISO 格式 (2020-04-24T00:00:00Z)
                                        is_new_until = is_new_until.replace('T', ' ').replace('Z', '')
                                        is_new_until = datetime.strptime(is_new_until, '%Y-%m-%d %H:%M:%S')
                                    else:
                                        # 處理普通格式 (2020-04-24 00:00:00)
                                        is_new_until = datetime.strptime(is_new_until, '%Y-%m-%d %H:%M:%S')
                                except Exception as e:
                                    logger.warning(f"日期轉換失敗 ({is_new_until}): {str(e)}")
                                    is_new_until = None
                            else:
                                is_new_until = None  # 如果是空值，直接設為 None
                            
                            # 準備資料
                            restaurant_data = {
                                'name': restaurant['name'],
                                'normalized_name': normalized_name,
                                'address': normalized_address,
                                'budget': restaurant.get('budget'),
                                'city': restaurant['city']['name'],
                                'city_CN': city_CN,
                                'customer_phone': restaurant.get('customer_phone'),
                                'description': restaurant.get('description'),
                                'hero_image': restaurant.get('hero_image'),
                                'hero_listing_image': restaurant.get('hero_listing_image'),
                                'distance': restaurant.get('distance'),
                                'is_new_until': is_new_until,  # 使用轉換後的日期時間
                                'latitude': restaurant.get('latitude'),
                                'longitude': restaurant.get('longitude'),
                                'minimum_delivery_fee': restaurant.get('minimum_delivery_fee'),
                                'minimum_delivery_time': restaurant.get('minimum_delivery_time'),
                                'minimum_order_amount': restaurant.get('minimum_order_amount'),
                                'minimum_pickup_time': restaurant.get('minimum_pickup_time'),
                                'primary_cuisine_id': restaurant.get('primary_cuisine_id'),
                                'rating': restaurant.get('rating'),
                                'redirection_url': restaurant.get('redirection_url'),
                                'review_number': restaurant.get('review_number'),
                                'tag': restaurant.get('tag')
                            }
                            
                            # 創建記錄
                            self.dao.create_restaurant(restaurant_data)
                            fetched_count[county] += 1
                            if fetched_count[county] % 10 == 0:  # 每10筆記錄一次進度
                                logger.info(f"- {county} 已抓取: {fetched_count[county]} 筆")

                    # 檢查是否超時
                    if datetime.now() - county_start_time > timedelta(seconds=self.timeout_seconds):
                        logger.warning(f"\n{county} 抓取超時 ({self.timeout_seconds}秒)")
                        logger.warning(f"已抓取 {fetched_count[county]} 筆，準備切換到下一個縣市")
                        break

                    # 如果還沒抓夠，生成新的座標
                    if fetched_count[county] < self.country_count:
                        latitude, longitude = self.generate_new_coordinates(county)
                        location = (latitude, longitude)
                        logger.info(f"生成新座標: ({latitude:.6f}, {longitude:.6f})")

                county_end_time = datetime.now()
                county_duration = (county_end_time - county_start_time).seconds
                logger.info(f"\n完成 {county} 資料抓取:")
                logger.info(f"- 總計: {fetched_count[county]} 筆")
                logger.info(f"- 耗時: {county_duration} 秒")
                logger.info(f"{'='*50}\n")

            total_end_time = datetime.now()
            total_duration = (total_end_time - total_start_time).seconds
            logger.info(f"\n全台資料抓取完成:")
            logger.info(f"- 總筆數: {sum(fetched_count.values())} 筆")
            logger.info(f"- 總耗時: {total_duration} 秒")
            logger.info(f"- 開始時間: {total_start_time.strftime('%Y-%m-%d %H:%M:%S')}")
            logger.info(f"- 結束時間: {total_end_time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            return {
                "message": "資料抓取完成",
                "data": {
                    "total_fetched": sum(fetched_count.values()),
                    "fetched_by_city": fetched_count,
                    "total_duration_seconds": total_duration
                }
            }
                
        except Exception as e:
            logger.error(f"抓取資料時發生錯誤: {str(e)}")
            raise 