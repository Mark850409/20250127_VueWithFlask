from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from utils.sqlfunctions import execute_query
from models import db
from sqlalchemy import create_engine
import re
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone, timedelta
import os
from dotenv import load_dotenv
import openai
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from dao.googlemaps_dao import GoogleMapsDAO
import emoji
from ollama import Client
import hashlib
import sys
from pathlib import Path
import json

# 添加專案根目錄到 Python 路徑
backend_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(backend_dir))

# 從專案根目錄導入 app
from app import app

# ----------------------------------------------------------------------------------------
# 參數定義
# ----------------------------------------------------------------------------------------

# 1. 首先根據 FLASK_ENV 決定要載入哪個 .env 文件
env = os.getenv('FLASK_ENV', 'development')
if env == 'production':
    load_dotenv('.env.production')
else:
    load_dotenv('.env.development')

# 設置數據庫 URI
DB_HOST = os.getenv('DB_HOST', 'db')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_USER = os.getenv('DB_USER', 'mark')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'mark850409')
DB_NAME = os.getenv('DB_NAME', 'restaurant')

# 構建數據庫 URI
SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
os.environ['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

# 建立連線
engine = create_engine(SQLALCHEMY_DATABASE_URI)

# 設置 API 密鑰
gmaps_dao = GoogleMapsDAO(os.getenv('GOOGLE_MAPS_API_KEY'))

# 停用詞列表 - 將字串轉換為列表
stopwords_str = os.getenv('STOPWORDS', '[]')
stopwords = eval(stopwords_str) if isinstance(stopwords_str, str) else stopwords_str

# 最大線呈數
max_workers = int(os.getenv('MAX_WORKERS', '20'))

# 每次抓取的評論筆數
comment_count = int(os.getenv('COMMENT_COUNT', '20'))

# 關鍵詞權重 - 將字串轉換為字典
keywords_weights_str = os.getenv('KEYWORDS_WEIGHTS', '{}')
keywords_weights = eval(keywords_weights_str) if isinstance(keywords_weights_str, str) else keywords_weights_str

# 設定 OpenAI API 金鑰
openai.api_key = os.getenv('OPENAI_API_KEY')

# 確保已下載VADER字典
nltk.download('vader_lexicon')

# 初始化VADER情感分析器
sid = SentimentIntensityAnalyzer()

# ----------------------------------------------------------------------------------------
# 文本清理
# ----------------------------------------------------------------------------------------

# 去除括號內的空白
def remove_space_around_brackets(name):
    return re.sub(r'\s*\(\s*(.*?)\s*\)\s*', r'(\1)', name).strip()


# 文本清理
async def clean_text(text):
    # 移除所有換行符和空白字符
    text = re.sub(r'\s+', '', text)
    # 移除句子開頭和結尾的標點符號
    text = re.sub(r'^[^\w\s]+|[^\w\s]+$', '', text)
    # 定義要保留的標點符號
    keep_punctuation = '，！'
    # 移除除了保留標點以外的所有標點符號
    text = re.sub(f'[^\w\s{keep_punctuation}]', '', text)
    # 移除表情符號
    text = emoji.replace_emoji(text, '')
    return text


def clean_text2(text):
    # Remove emojis
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               "]+", flags=re.UNICODE)
    text = emoji_pattern.sub(r'', text)

    # Remove newlines
    text = text.replace('\n', ' ').replace('\r', '')

    # Remove leading and trailing punctuation
    text = text.strip('.,!?;:()[]{}""''')

    return text.strip()


# ----------------------------------------------------------------------------------------
# 翻譯函數
# ----------------------------------------------------------------------------------------

# 定義翻譯函數(ollama API版本)
def translate_to_english(texts):
    """使用 Ollama API 將中文翻譯成英文"""
    client = Client(host=os.getenv('OLLAMA_API_HOST'))
    translations = []

    for text in texts:
        try:
            if not text or text.isspace():  # 檢查空文本
                translations.append("")
                continue
                
            response = client.chat(
                model=os.getenv('OLLAMA_MODEL'),
                messages=[
                    {
                        "role": "system",
                        "content": os.getenv('OLLAMA_SYSTEM_PROMPT')
                    },
                    {
                        "role": "user",
                        "content": text
                    }
                ]
            )
            
            # 解析回應
            translation = response["message"]["content"].strip()
            
            # 檢查翻譯結果
            if not translation or translation.isspace():
                translations.append(text)  # 如果翻譯為空，保留原文
            else:
                translations.append(translation)
                
            print(f"原文: {text}")
            print(f"翻譯: {translation}")
            print("-" * 50)
            
        except Exception as e:
            print(f"翻譯出錯: {str(e)}")
            translations.append(text)  # 出錯時保留原文
            
    return translations

# ----------------------------------------------------------------------------------------
# 加密函數
# ----------------------------------------------------------------------------------------

# 定義加密函數
def generate_hash(value):
    return hashlib.sha256(value.encode()).hexdigest()

# ----------------------------------------------------------------------------------------
# 爬蟲函數
# ----------------------------------------------------------------------------------------
def get_place_review_with_selenium(my_restaurant_name, rest_id, comment_count):
    options = webdriver.ChromeOptions()
    # 背景執行
    options.add_argument('--headless')

    # 視窗最大化
    options.add_argument("start-maximized")

    # 休息1秒
    time.sleep(1)

    browser = webdriver.Chrome(options=options)

    # 基本url
    url = 'https://www.google.com.tw/maps/@25.0328862,121.5491486,17z?entry=ttu'

    # 取得url
    browser.get(url)

    # 錯誤訊息清單
    error_list = []
    id = 0

    # 記錄開始時間
    start_time = datetime.now()
    print(f"開始時間: {start_time.strftime('%Y年%m月%d日 %H時%M分%S秒')}")
    print("===============================")

    try:
        # ----------------------------------------------------------------------------------------
        # python selenium 爬蟲程式碼
        # ----------------------------------------------------------------------------------------

        # 清空搜尋框文字
        WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='searchboxinput']"))).clear()

        # 定位到搜尋框並傳入文字
        WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='searchboxinput']"))).send_keys(my_restaurant_name)

        # 休息1秒
        time.sleep(1)

        # 定位到查詢按鈕
        WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='searchbox-searchbutton']"))).click()

        # 休息1秒
        time.sleep(5)

        # 取得html網頁元素
        soup = BeautifulSoup(browser.page_source, 'html.parser')

        # 定位到每家餐廳的標題
        place_name_element = soup.find('h1', {'class': 'DUwDvf lfPIob'})

        if not place_name_element:
            print(f"找不到店家: {my_restaurant_name}")
            error_list.append((my_restaurant_name, "找不到店家"))
            # 检查文件是否存在或为空
            write_header = not os.path.isfile('csv/error_log.csv') or os.stat('csv/error_log.csv').st_size == 0
            # 将出错店家信息写入CSV文件
            if error_list:
                error_df = pd.DataFrame(error_list, columns=['店家名稱', '錯誤訊息'])
                if write_header:
                    error_df.to_csv('csv/error_log.csv', index=False, encoding='utf-8-sig', mode='w', header=True)
                else:
                    error_df.to_csv('csv/error_log.csv', index=False, encoding='utf-8-sig', mode='a', header=False)
            return

        # 休息1秒
        time.sleep(1)

        # 定位到評論頁籤並點擊
        WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                                        "//*[@id='QA0Szd']/div/div/div[1]/div[2]/div/div[1]/div/div/div[3]/div/div/button[2]/div[2]"))).click()

        # 取得店家評論數量
        review_count_element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH,
                                            "//*[@id='QA0Szd']/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div[2]/div/div[2]/div[3]")))
        review_count_text = review_count_element.text.strip()
        review_count = int(re.search(r'\d+', review_count_text).group()) if review_count_text else 0

        # 如果評論數小於要求的最小評論數，抓取所有現有的評論
        if review_count < comment_count:
            print("===============================")
            print(
                f"店家 {my_restaurant_name} 的評論數 {review_count} 小於您要求的最小評論數，筆數為{comment_count}，將抓取所有現有的評論")
            required_reviews = review_count
        else:
            print("===============================")
            print(f"抓取所有評論筆數為: {comment_count}")
            required_reviews = comment_count

        # 評論數的起始值
        tmp = browser.find_elements(By.XPATH, "//div[@class='jftiEf fontBodyMedium ']")

        # ----------------------------------------------------------------------------------------
        # 取得評論
        # ----------------------------------------------------------------------------------------

        # 初始化列表
        users = []
        ratings = []
        comments = []
        times = []
        batch_size = 10  # 每10筆評論處理一次
        processed_count = 0  # 已處理的評論數量

        # 評論總數
        while len(tmp) < int(required_reviews):
            browser.execute_script('''
                const body = document.querySelector(`
                    div.m6QErb.DxyBCb.kA9KIf.dS8AEf`);
    
                body.scrollTo(0, body.scrollHeight);
            ''')

            time.sleep(0.5)

            tmp = browser.find_elements(By.XPATH, "//div[@class='jftiEf fontBodyMedium ']")

            # 抓取資料及欄位定義
            for review in tmp[processed_count:]:  # 只處理新的評論
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

                    users.append(user)
                    ratings.append(rating)
                    comments.append(text)
                    times.append(timestamp)
                    processed_count += 1

                    # 取得place_id
                    place_id = gmaps_dao.find_place(my_restaurant_name)

                    print(f"抓取所有google place id: {place_id}")

                    # 當收集到10筆評論時進行處理
                    if len(comments) % batch_size == 0:
                        # 建立當前批次的 DataFrame
                        df = pd.DataFrame({
                            'place_id': [place_id] * batch_size,
                            'restaurant_name': [my_restaurant_name] * batch_size,
                            'user': users[-batch_size:],
                            'rating': ratings[-batch_size:],
                            'text': comments[-batch_size:],
                            'time': times[-batch_size:]
                        })

                        # 翻譯文本
                        english_texts = translate_to_english(comments[-batch_size:])
                        df['english_texts'] = english_texts

                        # 情感分析
                        result = analyze_sentiment_with_NLTK(english_texts)
                        analysis_df = pd.DataFrame(result,
                            columns=['positive_prob', 'negative_prob', 'composite_score', 'confidence', 'sentiment'])

                        df['positive_prob'] = analysis_df['positive_prob'].round(2)
                        df['negative_prob'] = analysis_df['negative_prob'].round(2)
                        df['composite_score'] = analysis_df['composite_score'].round(2)
                        df['confidence'] = analysis_df['confidence'].round(2)
                        df['sentiment'] = analysis_df['sentiment']

                        # 關鍵詞分析
                        tokenized_comments = tokenize_and_clean_comments(comments[-batch_size:], stopwords)
                        vectorizer = TfidfVectorizer()
                        tfidf_matrix = vectorizer.fit_transform(tokenized_comments)
                        feature_names = vectorizer.get_feature_names_out()
                        tfidf_scores = tfidf_matrix.toarray()
                        keywords_scores = calculate_score(tfidf_scores, feature_names, keywords_weights, 1)
                        df['keywords_scores'] = keywords_scores
                        df['keywords_scores'] = df['keywords_scores'].round(2)

                        # 生成哈希值
                        df['hash'] = df.apply(
                            lambda x: generate_hash(f"{x['restaurant_name']}_{x['user']}_{x['text']}_{x['time']}"),
                            axis=1
                        )

                        # 檢查並過濾重複評論
                        existing_hashes_query = 'SELECT hash FROM google_maps_review_with_selenium_ollama'
                        existing_hashes = pd.read_sql(existing_hashes_query, con=engine)
                        new_data_df = df[~df['hash'].isin(existing_hashes['hash'])]

                        if not new_data_df.empty:
                            # 寫入CSV
                            new_data_df.to_csv(
                                'backend/csv/google_maps_review_with_selenium_ollama.csv',
                                mode='a',
                                header=False,
                                index=False,
                                encoding='utf-8-sig'
                            )
                            # 寫入資料庫
                            new_data_df.to_sql(
                                'google_maps_review_with_selenium_ollama',
                                engine,
                                if_exists='append',
                                index=False
                            )
                            print(f"成功新增 {len(new_data_df)} 筆評論")

                except Exception as e:
                    print(f"處理評論時出錯: {str(e)}")
                    continue

            if processed_count >= required_reviews:
                break

        # 處理剩餘的評論
        if len(comments) % batch_size > 0:
            remaining = len(comments) % batch_size
            remaining_start = len(comments) - remaining

            # 取得place_id
            place_id = gmaps_dao.find_place(my_restaurant_name)

            print(f"抓取所有google place id: {place_id}")
            
            # 建立剩餘評論的 DataFrame
            df = pd.DataFrame({
                'place_id': [place_id] * remaining,
                'restaurant_name': [my_restaurant_name] * remaining,
                'user': users[remaining_start:],
                'rating': ratings[remaining_start:],
                'text': comments[remaining_start:],
                'time': times[remaining_start:]
            })

            # 翻譯文本
            english_texts = translate_to_english(comments[remaining_start:])
            df['english_texts'] = english_texts

            # 情感分析
            result = analyze_sentiment_with_NLTK(english_texts)
            analysis_df = pd.DataFrame(result,
                columns=['positive_prob', 'negative_prob', 'composite_score', 'confidence', 'sentiment'])

            df['positive_prob'] = analysis_df['positive_prob'].round(2)
            df['negative_prob'] = analysis_df['negative_prob'].round(2)
            df['composite_score'] = analysis_df['composite_score'].round(2)
            df['confidence'] = analysis_df['confidence'].round(2)
            df['sentiment'] = analysis_df['sentiment']

            # 關鍵詞分析
            tokenized_comments = tokenize_and_clean_comments(comments[remaining_start:], stopwords)
            vectorizer = TfidfVectorizer()
            tfidf_matrix = vectorizer.fit_transform(tokenized_comments)
            feature_names = vectorizer.get_feature_names_out()
            tfidf_scores = tfidf_matrix.toarray()
            keywords_scores = calculate_score(tfidf_scores, feature_names, keywords_weights, 1)
            df['keywords_scores'] = keywords_scores
            df['keywords_scores'] = df['keywords_scores'].round(2)

            # 生成哈希值
            df['hash'] = df.apply(
                lambda x: generate_hash(f"{x['restaurant_name']}_{x['user']}_{x['text']}_{x['time']}"),
                axis=1
            )

            # 檢查並過濾重複評論
            existing_hashes_query = 'SELECT hash FROM google_maps_review_with_selenium_ollama'
            existing_hashes = pd.read_sql(existing_hashes_query, con=engine)
            new_data_df = df[~df['hash'].isin(existing_hashes['hash'])]

            if not new_data_df.empty:
                # 寫入CSV
                new_data_df.to_csv(
                    'backend/csv/google_maps_review_with_selenium_ollama.csv',
                    mode='a',
                    header=False,
                    index=False,
                    encoding='utf-8-sig'
                )
                # 寫入資料庫
                new_data_df.to_sql(
                    'google_maps_review_with_selenium_ollama',
                    engine,
                    if_exists='append',
                    index=False
                )
                print(f"成功新增剩餘的 {len(new_data_df)} 筆評論")

    except Exception as e:
        print(f"處理店家 {my_restaurant_name} 時出錯: {str(e)}")
        error_df = pd.DataFrame([(my_restaurant_name, str(e))], columns=['店家名稱', '錯誤訊息'])
        error_df.to_csv(
            'backend/csv/error_log.csv',
            mode='a',
            header=False,
            index=False,
            encoding='utf-8-sig'
        )
    finally:
        browser.quit()

    # 記錄結束時間
    end_time = datetime.now()
    print(f"結束時間: {end_time.strftime('%Y年%m月%d日 %H時%M分%S秒')}")

    # 計算總執行時間
    total_time = end_time - start_time
    print(f"總執行時間: {total_time}秒")


# 取得googlemaps評論
def google_maps_review_processing():
    """處理 Google Maps 評論"""
    with app.app_context():
        try:
            # 建立 CSV 目錄（如果不存在）
            os.makedirs('backend/csv', exist_ok=True)
            
            # 檢查並建立錯誤日誌 CSV
            error_log_path = 'backend/csv/error_log.csv'
            if not os.path.exists(error_log_path):
                pd.DataFrame(columns=['店家名稱', '錯誤訊息']).to_csv(
                    error_log_path, index=False, encoding='utf-8-sig'
                )
                
            # 檢查並建立評論資料 CSV
            reviews_csv_path = 'backend/csv/google_maps_review_with_selenium_ollama.csv'
            if not os.path.exists(reviews_csv_path):
                # 建立空的 CSV 檔案，包含所有必要欄位
                empty_df = pd.DataFrame(columns=[
                    'place_id', 'restaurant_name', 'user', 'rating', 'text',
                    'english_texts', 'time', 'positive_prob', 'negative_prob',
                    'composite_score', 'confidence', 'keywords_scores', 'sentiment',
                    'hash'
                ])
                empty_df.to_csv(reviews_csv_path, index=False, encoding='utf-8-sig')

            # 使用 SQL 語法查詢所有餐廳
            sql_query = "SELECT id, normalized_name FROM restaurant_type_list"
            get_restaurants_name = execute_query(db.session, sql_query)

            # 收集店家名稱和ID
            restaurant_data = [(row.normalized_name, row.id) for row in get_restaurants_name]

            # 使用 ThreadPoolExecutor 進行平行處理
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = []
                for name, rest_id in restaurant_data:
                    futures.append(executor.submit(
                        get_place_review_with_selenium, name, rest_id, comment_count
                    ))
                for future in as_completed(futures):
                    try:
                        result = future.result()
                    except Exception as e:
                        print(f"Error occurred: {e}")

        except Exception as e:
            print(f"處理評論時發生錯誤: {str(e)}")


# 計算情感分析(NLTK)
def analyze_sentiment_with_NLTK(texts):
    results = []
    # 遍歷並分析每個文本
    for idx, text in enumerate(texts, 1):
        # 分析文本情感
        scores = sid.polarity_scores(text)

        # 提取情感分析結果並取小數點後兩位
        pos_score = round(scores['pos'], 2)
        neg_score = round(scores['neg'], 2)
        neu_score = round(scores['neu'], 2)
        compound_score = round(scores['compound'], 2)

        # 判斷情感類別
        if compound_score >= 0.05:
            sentiment = '正向情感'
        elif compound_score <= -0.05:
            sentiment = '負向情感'
        else:
            sentiment = '中性情感'

        # 將結果添加到列表
        results.append([pos_score, neg_score, neu_score, compound_score, sentiment])

    return results


# 設定未定義關鍵詞的預設權重
default_weight = 1


# 計算每個評論的總評分
def calculate_score(tfidf_scores, feature_names, keywords_weights, default_weight):
    # 確保 keywords_weights 是字典類型
    if isinstance(keywords_weights, str):
        keywords_weights = eval(keywords_weights)
    
    total_scores = []
    for row in tfidf_scores:
        score = 0
        for i, word_score in enumerate(row):
            word = feature_names[i]
            weight = keywords_weights.get(word, default_weight)
            score += word_score * weight
        total_scores.append(score)
    return total_scores


# 使用 jieba 進行斷詞，並過濾掉停用詞
def tokenize_and_clean_comments(comments, stopwords):
    # 確保 stopwords 是列表類型
    if isinstance(stopwords, str):
        stopwords = eval(stopwords)
    return [" ".join(jieba.cut(comment)) for comment in comments if comment not in stopwords]


# ----------------------------------------------------------------------------------------
# 程式進入點
# ----------------------------------------------------------------------------------------
if __name__ == "__main__":
    google_maps_review_processing()
