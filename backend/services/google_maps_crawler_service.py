from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime
import time
import pandas as pd
import re
from models.database import db
from models.rating import Rating
from utils.text_analysis import (
    translate_to_english,
    analyze_sentiment_with_NLTK,
    tokenize_and_clean_comments,
    calculate_score,
    generate_hash
)
from sklearn.feature_extraction.text import TfidfVectorizer
from dao.googlemaps_dao import GoogleMapsDAO
import os
import logging
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed
from models.store import Store  # 導入 Store 模型
from flask import current_app

# 設置日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('crawler.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class GoogleMapsCrawlerService:
    def __init__(self):
        self.stopwords = eval(os.getenv('STOPWORDS', '[]'))
        self.keywords_weights = eval(os.getenv('KEYWORDS_WEIGHTS', '{}'))
        self.gmaps_dao = GoogleMapsDAO(os.getenv('GOOGLE_MAPS_API_KEY'))
        self.batch_size = 5  # 設定批次大小

    def save_reviews_batch(self, reviews_data: List[Dict]) -> None:
        """批次保存評論到資料庫"""
        from flask import current_app
        
        try:
            with current_app.app_context():
                ratings = []
                for review in reviews_data:
                    rating = Rating(
                        place_id=review['place_id'],
                        restaurant_name=review['restaurant_name'],
                        user=review['user'],
                        rating=review['rating'],
                        text=review['text'],
                        english_texts=review['english_texts'],
                        time=review['time'],
                        positive_prob=review['positive_prob'],
                        negative_prob=review['negative_prob'],
                        composite_score=review['composite_score'],
                        confidence=review['confidence'],
                        keywords_scores=review['keywords_scores'],
                        sentiment=review['sentiment'],
                        hash=review['hash']
                    )
                    ratings.append(rating)

                db.session.bulk_save_objects(ratings)
                db.session.commit()
                logger.info(f"成功批次保存 {len(ratings)} 筆評論")
                
        except Exception as e:
            db.session.rollback()
            logger.error(f"批次保存評論失敗: {str(e)}")
            raise

    def crawl_restaurant_reviews(self, restaurant_name: str, comment_count: int = 10) -> dict:
        """爬取指定餐廳的 Google Maps 評論
        
        Args:
            restaurant_name (str): 餐廳名稱
            comment_count (int): 要爬取的評論數量，默認為10
            
        Returns:
            dict: 包含爬取結果的字典
                success (bool): 是否成功
                message (str): 結果訊息
                data (list): 評論數據列表
                error (str, optional): 錯誤訊息
        """
        with current_app.app_context():
            logger.info(f"開始爬取餐廳 '{restaurant_name}' 的評論")
            try:
                # 先使用 GoogleMapsDAO 獲取 place_id
                try:
                    place_id = self.gmaps_dao.find_place(restaurant_name)
                    logger.info(f"成功獲取 place_id: {place_id}")
                except ValueError as e:
                    logger.warning(f"無法獲取 place_id: {str(e)}")
                    place_id = ''

                options = webdriver.ChromeOptions()
                options.add_argument('--headless')
                options.add_argument("start-maximized")
                
                browser = webdriver.Chrome(options=options)
                url = 'https://www.google.com.tw/maps/@25.0328862,121.5491486,17z?entry=ttu'
                browser.get(url)
                logger.info(f"已打開 Google Maps 頁面")
                
                # 搜尋餐廳
                search_box = WebDriverWait(browser, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[@id='searchboxinput']"))
                )
                search_box.clear()
                search_box.send_keys(restaurant_name)
                logger.info(f"已輸入餐廳名稱: {restaurant_name}")
                
                # 點擊搜尋
                WebDriverWait(browser, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[@id='searchbox-searchbutton']"))
                ).click()
                logger.info("已點擊搜尋按鈕")
                
                time.sleep(5)
                
                # 檢查是否找到餐廳
                soup = BeautifulSoup(browser.page_source, 'html.parser')
                place_name_element = soup.find('h1', {'class': 'DUwDvf lfPIob'})
                
                if not place_name_element:
                    logger.warning(f"找不到餐廳: {restaurant_name}")
                    return {
                        'success': False,
                        'message': f'找不到餐廳: {restaurant_name}',
                        'data': []
                    }
                
                logger.info("已找到餐廳，準備爬取評論")
                
                # 點擊評論頁籤
                WebDriverWait(browser, 10).until(
                    EC.element_to_be_clickable((By.XPATH,
                        "//*[@id='QA0Szd']/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div/div/button[2]/div[2]"))
                ).click()
                
                # 取得評論數量
                review_count_element = WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.XPATH,
                        "//*[@id='QA0Szd']/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[2]/div/div[2]/div[3]"))
                )
                review_count_text = review_count_element.text.strip()
                total_reviews = int(re.search(r'\d+', review_count_text).group()) if review_count_text else 0
                
                required_reviews = min(comment_count, total_reviews)
                logger.info(f"預計爬取 {required_reviews} 筆評論")
                
                # 收集評論
                reviews_data = []
                current_batch = []
                processed_count = 0
                tmp = browser.find_elements(By.XPATH, "//div[@class='jftiEf fontBodyMedium ']")
                
                while len(tmp) < required_reviews:
                    browser.execute_script(
                        'const body = document.querySelector('
                        '"div.m6QErb.DxyBCb.kA9KIf.dS8AEf"); '
                        'body.scrollTo(0, body.scrollHeight);'
                    )
                    time.sleep(0.5)
                    tmp = browser.find_elements(By.XPATH, "//div[@class='jftiEf fontBodyMedium ']")
                
                # 處理評論
                for review in tmp[:required_reviews]:
                    try:
                        user = review.find_element(By.CLASS_NAME, 'd4r55').text.strip()
                        rating = review.find_element(By.CLASS_NAME, 'kvMYJc').get_attribute('aria-label')
                        rating = int(re.search(r'\d+', rating).group()) if rating else 0
                        
                        try:
                            more = review.find_element(By.CLASS_NAME, 'w8nwRe.kyuRq')
                            browser.execute_script("arguments[0].click();", more)
                            time.sleep(1)
                        except:
                            pass
                        
                        text = review.find_element(By.CLASS_NAME, 'wiI7pd').text.strip()
                        timestamp = review.find_element(By.CLASS_NAME, 'rsqaWe').text.strip()
                        
                        logger.info(f"正在處理第 {processed_count + 1} 筆評論")
                        
                        # 翻譯和分析
                        english_text = translate_to_english([text])[0]
                        sentiment_result = analyze_sentiment_with_NLTK([english_text])[0]
                        
                        # 關鍵詞分析
                        tokenized_comment = tokenize_and_clean_comments([text], self.stopwords)
                        vectorizer = TfidfVectorizer()
                        tfidf_matrix = vectorizer.fit_transform(tokenized_comment)
                        feature_names = vectorizer.get_feature_names_out()
                        tfidf_scores = tfidf_matrix.toarray()
                        keywords_score = calculate_score(tfidf_scores, feature_names, self.keywords_weights, 1)[0]
                        
                        # 生成評論雜湊值
                        hash_value = generate_hash(f"{restaurant_name}_{user}_{text}_{timestamp}")
                        
                        # 修改 review_data 字典，使用獲取到的 place_id
                        review_data = {
                            'place_id': place_id,  # 使用 GoogleMapsDAO 獲取的 place_id
                            'restaurant_name': restaurant_name,
                            'user': user,
                            'rating': rating,
                            'text': text,
                            'english_texts': english_text,
                            'time': timestamp,
                            'positive_prob': round(sentiment_result[0], 2),
                            'negative_prob': round(sentiment_result[1], 2),
                            'composite_score': round(sentiment_result[2], 2),
                            'confidence': round(sentiment_result[3], 2),
                            'keywords_scores': round(keywords_score, 2),
                            'sentiment': sentiment_result[4],
                            'hash': hash_value
                        }
                        
                        reviews_data.append(review_data)
                        current_batch.append(review_data)
                        processed_count += 1
                        
                        # 每收集到一定數量的評論就批次寫入資料庫
                        if len(current_batch) >= self.batch_size:
                            logger.info(f"準備批次寫入 {len(current_batch)} 筆評論")
                            self.save_reviews_batch(current_batch)
                            current_batch = []
                        
                    except Exception as e:
                        logger.error(f"處理評論時出錯: {str(e)}")
                        continue
                
                # 處理剩餘的評論
                if current_batch:
                    logger.info(f"準備寫入最後 {len(current_batch)} 筆評論")
                    self.save_reviews_batch(current_batch)
                
                logger.info(f"爬取完成，共處理 {len(reviews_data)} 筆評論")
                return {
                    'success': True,
                    'message': f'成功爬取 {len(reviews_data)} 筆評論',
                    'data': reviews_data
                }
                
            except Exception as e:
                logger.error(f"爬取評論失敗: {str(e)}")
                return {
                    'success': False,
                    'message': f'爬取評論失敗',
                    'error': str(e),
                    'data': []
                }
                
            finally:
                browser.quit()
                logger.info("瀏覽器已關閉")

    def process_all_restaurants(self, comment_count: int = 10) -> dict:
        """批次處理所有餐廳的評論"""
        logger.info("開始批次處理所有餐廳評論")
        try:
            # 獲取應用實例
            from flask import current_app
            app = current_app._get_current_object()  # 獲取實際的應用實例
            
            # 使用應用上下文查詢餐廳
            with app.app_context():
                # 使用 SQLAlchemy ORM 查詢所有餐廳
                restaurants = db.session.query(Store).all()
                
                # 將查詢結果轉換為字典列表
                restaurants_data = [
                    {
                        'id': restaurant.id,
                        'normalized_name': restaurant.normalized_name
                    }
                    for restaurant in restaurants
                ]
            
            total_restaurants = len(restaurants_data)
            logger.info(f"找到 {total_restaurants} 家餐廳待處理")
            
            processed_count = 0
            total_reviews = 0
            failed_restaurants = []
            current_batch = []  # 用於批次寫入資料庫
            
            # 建立 CSV 檔案（如果不存在）
            reviews_csv_path = 'backend/csv/ratings.csv'
            if not os.path.exists(os.path.dirname(reviews_csv_path)):
                os.makedirs(os.path.dirname(reviews_csv_path))
            
            if not os.path.exists(reviews_csv_path):
                empty_df = pd.DataFrame(columns=[
                    'place_id', 'restaurant_name', 'user', 'rating', 'text',
                    'english_texts', 'time', 'positive_prob', 'negative_prob',
                    'composite_score', 'confidence', 'keywords_scores', 'sentiment',
                    'hash'
                ])
                empty_df.to_csv(reviews_csv_path, index=False, encoding='utf-8-sig')
                logger.info(f"已創建評論 CSV 文件: {reviews_csv_path}")

            def process_restaurant(restaurant_name: str, comment_count: int) -> dict:
                """在應用上下文中處理單個餐廳"""
                with app.app_context():
                    return self.crawl_restaurant_reviews(restaurant_name, comment_count)
            
            # 使用 ThreadPoolExecutor 進行平行處理
            with ThreadPoolExecutor(max_workers=int(os.getenv('MAX_WORKERS', '20'))) as executor:
                future_to_restaurant = {
                    executor.submit(
                        process_restaurant,  # 使用新的包裝函數
                        restaurant['normalized_name'],
                        comment_count
                    ): restaurant for restaurant in restaurants_data
                }
                
                for future in as_completed(future_to_restaurant):
                    restaurant = future_to_restaurant[future]
                    try:
                        with app.app_context():  # 在處理結果時也使用應用上下文
                            result = future.result()
                            processed_count += 1
                            
                            if result['success']:
                                reviews = result['data']
                                total_reviews += len(reviews)
                                
                                # 將評論加入批次
                                current_batch.extend(reviews)
                                
                                # 每達到批次大小就寫入資料庫
                                if len(current_batch) >= self.batch_size:
                                    logger.info(f"準備批次寫入 {len(current_batch)} 筆評論到資料庫")
                                    self.save_reviews_batch(current_batch)
                                    current_batch = []
                                
                                # 將評論寫入 CSV
                                df = pd.DataFrame(reviews)
                                df.to_csv(
                                    reviews_csv_path,
                                    mode='a',
                                    header=False,
                                    index=False,
                                    encoding='utf-8-sig'
                                )
                                
                                logger.info(
                                    f"已處理 {processed_count}/{total_restaurants} - "
                                    f"餐廳: {restaurant['normalized_name']}, "
                                    f"評論數: {len(reviews)}"
                                )
                            else:
                                failed_restaurants.append({
                                    'id': restaurant['id'],
                                    'name': restaurant['normalized_name'],
                                    'error': result.get('error', '未知錯誤')
                                })
                                logger.warning(
                                    f"處理失敗 {processed_count}/{total_restaurants} - "
                                    f"餐廳: {restaurant['normalized_name']}, "
                                    f"錯誤: {result.get('error', '未知錯誤')}"
                                )
                                
                    except Exception as e:
                        failed_restaurants.append({
                            'id': restaurant['id'],
                            'name': restaurant['normalized_name'],
                            'error': str(e)
                        })
                        logger.error(
                            f"處理異常 {processed_count}/{total_restaurants} - "
                            f"餐廳: {restaurant['normalized_name']}, "
                            f"錯誤: {str(e)}"
                        )
            
            # 處理剩餘的評論
            with app.app_context():
                if current_batch:
                    logger.info(f"準備寫入最後 {len(current_batch)} 筆評論到資料庫")
                    self.save_reviews_batch(current_batch)
            
            success_count = total_restaurants - len(failed_restaurants)
            logger.info(
                f"批次處理完成，成功: {success_count}/{total_restaurants}, "
                f"總評論數: {total_reviews}"
            )
            
            return {
                'success': True,
                'message': f'批次處理完成，成功處理 {success_count}/{total_restaurants} 家餐廳',
                'total_restaurants': total_restaurants,
                'total_reviews': total_reviews,
                'failed_restaurants': failed_restaurants
            }
            
        except Exception as e:
            logger.error(f"批次處理失敗: {str(e)}")
            return {
                'success': False,
                'message': f'批次處理失敗: {str(e)}',
                'total_restaurants': 0,
                'total_reviews': 0,
                'failed_restaurants': []
            } 