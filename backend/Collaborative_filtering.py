from sklearn.model_selection import train_test_split
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics import mean_squared_error, mean_absolute_error, confusion_matrix, accuracy_score, precision_score, \
    recall_score, f1_score, classification_report
import numpy as np
import os
from dotenv import load_dotenv
from pathlib import Path
from sqlalchemy import create_engine
from flask import Flask, request, abort
import random
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from scipy.stats import pearsonr
from sklearn.metrics.pairwise import euclidean_distances, manhattan_distances
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity as cosine_similarity_metric
from config.config import SQLALCHEMY_DATABASE_URI
import traceback
from datetime import datetime
from sqlalchemy import text
import requests

# 獲取當前文件的目錄
current_dir = Path(__file__).parent

# 1. 首先根據 FLASK_ENV 決定要載入哪個 .env 文件
env = os.getenv('FLASK_ENV', 'development')
env_file = '.env.production' if env == 'production' else '.env.development'

# 構建完整的 .env 文件路徑
env_path = current_dir / env_file

# 載入對應的 .env 文件
if env_path.exists():
    print(f"Loading environment from: {env_path}")
    load_dotenv(env_path)
else:
    print(f"Warning: Environment file not found: {env_path}")


app = Flask(__name__)


# ===========================================================
# 從資料庫取得資料集
# ===========================================================

# 使用配置創建引擎
engine = create_engine(SQLALCHEMY_DATABASE_URI)

# 取得評分資料集
ratings_df = pd.read_sql('''
    SELECT 
        r.place_id,
        r.restaurant_name,
        r.rating,
        r.composite_score,
        r.user,
        s.city,
        s.city_CN,
        s.distance,
        s.review_number
    FROM ratings r
    JOIN stores s ON s.id = r.id
    ORDER BY RAND()
''', con=engine)

# 建立user對應ID的表格，從1開始編號
unique_users = ratings_df['user'].unique()
user_to_id = {user: idx + 1 for idx, user in enumerate(unique_users)}

# 使用 user_to_id 替换 'user' 列中的值
ratings_df['user_id'] = ratings_df['user'].map(user_to_id)

# 建立訓練矩陣
train_user_restaurant_matrix = pd.pivot_table(
    ratings_df,
    values='rating',
    index='user_id',
    columns='place_id',
    fill_value=0
)

# 取得餐廳資料集
restaurants_df = pd.read_sql('''
    select g.place_id,g.latitude,g.longitude,g.place_names,g.redirection_url,
    g.navigation_url,g.city,g.city_CN
    from googlemaps_info g
    JOIN ratings r ON r.place_id = g.place_id
    ORDER BY RAND()
''', con=engine)

# 建立評分資料集
ratings_data = {
    'user_id': ratings_df['user_id'],
    'restaurant_id': ratings_df['place_id'],
    'restaurant_name': ratings_df['restaurant_name'],
    'rating': ratings_df['rating'],
    'sentiment_score': ratings_df['composite_score'],
    'city': ratings_df['city_CN'],
    'distance': ratings_df['distance'],
    'review_number': ratings_df['review_number']
}
ratings_df = pd.DataFrame(ratings_data)

# 建立餐廳資料集
restaurants_data = {
    'restaurant_id': restaurants_df['place_id'],
    'latitude': restaurants_df['latitude'],
    'longitude': restaurants_df['longitude'],
    'name': restaurants_df['place_names'],
    'redirection_url': restaurants_df['redirection_url'],
    'navigation_url': restaurants_df['navigation_url'],
    'city': restaurants_df['city_CN']
}
restaurants_df = pd.DataFrame(restaurants_data)

# 建立餐廳名稱對應ID的表格
name_to_id = {row['name']: row['restaurant_id'] for _, row in restaurants_df.iterrows()}

# 建立餐廳ID對應餐廳名稱的表格
id_to_name = {row['restaurant_id']: row['name'] for _, row in restaurants_df.iterrows()}

# 建立foodpanda餐廳URL對應餐廳ID的表格
redirection_url_to_id = {row['restaurant_id']: row['redirection_url'] for _, row in restaurants_df.iterrows()}

# 建立googlemap導航對應餐廳ID的表格
navigation_url_to_id = {row['restaurant_id']: row['navigation_url'] for _, row in restaurants_df.iterrows()}

# 建立city對應餐廳ID的表格
city_url_to_id = {row['restaurant_id']: row['city'] for _, row in restaurants_df.iterrows()}
#print(city_url_to_id)

# 資料集合併
merged_df = pd.merge(ratings_df, restaurants_df, on='restaurant_id')

# 將資料集拆分為訓練集與測試集（只分割基本資料）
train_data, test_data = train_test_split(ratings_df, test_size=0.2, random_state=42)

# 初始化一個空的訓練矩陣（在run_experiment中再根據實驗類型設置）
train_user_restaurant_matrix = None

# ===========================================================
# 模型訓練開始
# ===========================================================

# 計算餘弦相似度
def cosine_similarity_predict(user_vector, similar_user_vector):
    return cosine_similarity_metric(user_vector.reshape(1, -1), similar_user_vector.reshape(1, -1)).flatten()[0]


# 計算皮爾森係數
def pearson_correlation_predict(user_vector, similar_user_vector):
    if np.all(user_vector == user_vector[0]) or np.all(similar_user_vector == similar_user_vector[0]):
        return 0
    else:
        return pearsonr(user_vector, similar_user_vector)[0]


# 計算歐幾里得距離
def euclidean_similarity_predict(user_vector, similar_user_vector):
    return 1 / (1 + euclidean_distances(user_vector.reshape(1, -1), similar_user_vector.reshape(1, -1)).flatten()[0])


# 計算曼哈頓距離
def manhattan_similarity_predict(user_vector, similar_user_vector):
    return 1 / (1 + manhattan_distances(user_vector.reshape(1, -1), similar_user_vector.reshape(1, -1)).flatten()[0])


# 計算權重並將這4個值加總
def combined_similarity_predict(cosine_sim, pearson_coef, euclidean_sim, manhattan_sim):
    return cosine_sim * 0.4 + pearson_coef * 0.3 + euclidean_sim * 0.2 + manhattan_sim * 0.1


def calculate_user_similarity(user_vector, all_user_vectors):
    """計算用戶相似度"""
    # 使用餘弦相似度計算
    similarities = cosine_similarity(user_vector, all_user_vectors)
    # 將相似度轉換為距離 (1 - similarity)，並排序
    distances = 1 - similarities[0]
    indices = np.argsort(distances)  # 按距離升序排序
    return distances, indices

def predict(user_id, restaurant_id, method='cosine', num_recommendations=5):
    """預測用戶對餐廳的評分"""
    if user_id not in train_user_restaurant_matrix.index or restaurant_id not in train_user_restaurant_matrix.columns:
        return None

    # 在這裡初始化和訓練 KNN 模型
    user_index = train_user_restaurant_matrix.index.get_loc(user_id)
    n_neighbors = min(num_recommendations * random.randint(1, 50), train_user_restaurant_matrix.shape[0])
    knn = NearestNeighbors(n_neighbors=n_neighbors, metric='cosine')
    knn.fit(train_user_restaurant_matrix.values)
    
    # 取出距離計算餘弦相似度
    distances, indices = knn.kneighbors(train_user_restaurant_matrix.iloc[user_index, :].values.reshape(1, -1))

    # 設定初始值
    ratings_sum = 0
    similarity_sum = 0

    # 輸出每個鄰居的相似度和貢獻
    neighbor_contributions = []

    valid_ratings = 0
    min_similarity = 0.2  # 增加最小相似度要求
    
    for i in range(1, len(distances.flatten())):
        similar_user_id = train_user_restaurant_matrix.index[indices.flatten()[i]]
        if pd.notna(train_user_restaurant_matrix.loc[similar_user_id, restaurant_id]):
            user_vector = train_user_restaurant_matrix.loc[user_id].values
            similar_user_vector = train_user_restaurant_matrix.loc[similar_user_id].values
            
            # 增加相似度閾值
            if method == 'cosine':
                sim = cosine_similarity_predict(user_vector, similar_user_vector)
                if sim < min_similarity:  # 忽略相似度太低的用戶
                    continue
            # 皮爾森係數
            elif method == 'pearson':
                sim = pearson_correlation_predict(user_vector, similar_user_vector)
            # 歐幾里得距離
            elif method == 'euclidean':
                sim = euclidean_similarity_predict(user_vector, similar_user_vector)
            # 曼哈頓距離
            elif method == 'manhattan':
                sim = manhattan_similarity_predict(user_vector, similar_user_vector)
            # 依照權重計算這4個值的加總
            elif method == 'combined':
                cosine_sim = cosine_similarity_predict(user_vector, similar_user_vector)
                pearson_coef = pearson_correlation_predict(user_vector, similar_user_vector)
                euclidean_sim = euclidean_similarity_predict(user_vector, similar_user_vector)
                manhattan_sim = manhattan_similarity_predict(user_vector, similar_user_vector)
                sim = combined_similarity_predict(cosine_sim, pearson_coef, euclidean_sim, manhattan_sim)
            else:
                raise ValueError(
                    "Invalid method. Choose from 'cosine', 'pearson', 'euclidean', 'manhattan', or 'combined'.")

            rating = train_user_restaurant_matrix.loc[similar_user_id, restaurant_id]
            ratings_sum += rating * sim
            similarity_sum += sim
            neighbor_contributions.append((similar_user_id, restaurant_id, sim, ratings_sum, similarity_sum))
            valid_ratings += 1

    if similarity_sum == 0:
        return None
    else:
        predicted_rating = ratings_sum / similarity_sum
        return predicted_rating


# 評估模型準確度
def evaluate_model(experiment_type='rating_only'):
    """
    評估模型準確度
    """
    y_true = []
    y_pred = []
    
    # 根據實驗類型選擇評分標準
    if experiment_type == 'rating_only':
        score_column = 'rating'
        threshold = 3.5  # 提高評分閾值
        print("\n=== 使用餐廳評分進行評估 ===")
    elif experiment_type == 'sentiment_only':
        score_column = 'sentiment_score'
        threshold = 0.7  # 提高情感分數閾值
        print("\n=== 使用情感分析進行評估 ===")
    else:  # hybrid
        score_column = 'weighted_combined_score'
        threshold = 0.75  # 提高混合評分閾值
        print("\n=== 使用綜合評分進行評估 ===")
    
    # 收集預測結果
    for _, row in test_data.iterrows():
        user_id = row['user_id']
        restaurant_id = row['restaurant_id']
        true_rating = row[score_column]
        predicted_rating = predict(user_id, restaurant_id)
        
        if predicted_rating is not None:
            y_true.append(true_rating)
            y_pred.append(predicted_rating)
    
    if not y_true or not y_pred:
        print("糟糕!!!資料不夠耶!!!")
        return None
    
    # 計算原始的 RMSE 和 MAE
    raw_rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    raw_mae = mean_absolute_error(y_true, y_pred)
    
    # 正規化 RMSE 和 MAE
    # 對於評分範圍 0-5，最大可能誤差是 5
    normalized_rmse = raw_rmse / 5.0  # 將 RMSE 正規化到 0-1 範圍
    normalized_mae = raw_mae / 5.0    # 將 MAE 正規化到 0-1 範圍
    
    # 轉換為分類問題
    if experiment_type == 'rating_only':
        y_true_class = [1 if rating >= threshold else 0 for rating in y_true]
        y_pred_class = [1 if rating >= threshold else 0 for rating in y_pred]
    elif experiment_type == 'sentiment_only':
        y_true_class = [1 if score >= threshold else 0 for score in y_true]
        y_pred_class = [1 if score >= threshold else 0 for score in y_pred]
    else:
        y_true_class = [1 if score >= threshold else 0 for score in y_true]
        y_pred_class = [1 if score >= threshold else 0 for score in y_pred]
    
    # 計算分類指標
    cm = confusion_matrix(y_true_class, y_pred_class)
    accuracy = accuracy_score(y_true_class, y_pred_class)
    precision = precision_score(y_true_class, y_pred_class, zero_division=0)
    recall = recall_score(y_true_class, y_pred_class, zero_division=0)
    f1 = f1_score(y_true_class, y_pred_class, zero_division=0)
    
    # 根據實驗類型設定分類報告的標籤
    if experiment_type == 'rating_only':
        target_names = ['評分不推薦', '評分推薦']
    elif experiment_type == 'sentiment_only':
        target_names = ['負面評價', '正面評價']
    else:
        target_names = ['綜合不推薦', '綜合推薦']
    
    class_report = classification_report(y_true_class, y_pred_class, 
                                      labels=[0, 1],
                                      target_names=target_names,
                                      zero_division=0)
    
    # 輸出評估結果
    print(f"\n{'='*20} 評估結果 {'='*20}")
    print(f"回歸指標:")
    print(f"原始 RMSE: {raw_rmse:.2f}")
    print(f"正規化 RMSE: {normalized_rmse:.2f}")
    print(f"原始 MAE: {raw_mae:.2f}")
    print(f"正規化 MAE: {normalized_mae:.2f}")
    print(f"\n分類指標:")
    print(f"準確率: {accuracy:.2f}")
    print(f"精確率: {precision:.2f}")
    print(f"召回率: {recall:.2f}")
    print(f"F1評分: {f1:.2f}")
    print(f"\n分類報告:")
    print(class_report)
    print('='*50)
    
    # 返回正規化後的指標
    return normalized_rmse, normalized_mae, cm, accuracy, precision, recall, f1, class_report


# ===========================================================
# 推薦餐廳主程式(基於內容推薩、協同過濾、混合推薩)
# ===========================================================

# 推薦餐廳主程式(協同過濾)
def recommend_restaurants(user_id, num_recommendations):
    try:
        if user_id not in train_user_restaurant_matrix.index:
            return []
            
        user_vector = train_user_restaurant_matrix.loc[user_id].values.reshape(1, -1)
        if np.all(user_vector == 0):
            return []
            
        # 計算相似度
        distances, similar_indices = calculate_user_similarity(
            user_vector, 
            train_user_restaurant_matrix.values
        )
        
        # 排除自己
        user_idx = train_user_restaurant_matrix.index.get_loc(user_id)
        similar_indices = similar_indices[similar_indices != user_idx]
        
        # 預先獲取所有評分資訊並建立索引
        restaurant_ratings = {}
        for _, row in train_data.iterrows():
            restaurant_id = row.name
            restaurant_info = restaurants_df.iloc[restaurant_id]
            restaurant_name = restaurant_info['name']
            if restaurant_name not in restaurant_ratings:
                restaurant_ratings[restaurant_name] = {
                    'distance': float(row['distance']),
                    'rating': float(row['rating']),
                    'review_number': int(row['review_number'])
                }
        
        # 用於存放推薦餐廳
        recommended_restaurants = []
        recommended_ids = set()
        
        # 選擇更多的相似用戶
        num_similar_users = min(200, len(similar_indices))
        selected_similar_users = similar_indices[:num_similar_users]
        random.shuffle(selected_similar_users)
        
        # 收集所有可能的推薦
        all_recommendations = []
        
        # 從相似用戶收集推薦
        for similar_user_idx in selected_similar_users:
            if distances[similar_user_idx] > 0.8:  # 相似度閾值
                continue
                
            similar_user_id = train_user_restaurant_matrix.index[similar_user_idx]
            similar_user_ratings = train_data[train_data['user_id'] == similar_user_id]
            
            for _, row in similar_user_ratings.iterrows():
                restaurant_id = row.name
                if restaurant_id not in recommended_ids:
                    restaurant_info = restaurants_df.iloc[restaurant_id]
                    restaurant_name = restaurant_info['name']
                    rating_info = restaurant_ratings.get(restaurant_name)
                    if rating_info:
                        all_recommendations.append((
                            restaurant_info,
                            rating_info,
                            restaurant_id
                        ))
        
        # 打亂所有推薦
        random.shuffle(all_recommendations)
        
        # 從推薦中選擇，確保城市多樣性
        cities_used = set()
        current_city_count = {}
        
        # 第一輪：優先選擇不同城市的餐廳
        for rec in all_recommendations:
            if len(recommended_restaurants) >= num_recommendations:
                break
                
            restaurant_info, rating_info, restaurant_id = rec
            city = restaurant_info['city']
            
            # 限制每個城市最多推薦2家餐廳
            if current_city_count.get(city, 0) < 1:
                recommended_restaurants.append((
                    restaurant_info['name'],
                    restaurant_info['latitude'],
                    restaurant_info['longitude'],
                    restaurant_info['redirection_url'],
                    restaurant_info['navigation_url'],
                    city,
                    rating_info['distance'],
                    rating_info['rating'],
                    rating_info['review_number']
                ))
                recommended_ids.add(restaurant_id)
                cities_used.add(city)
                current_city_count[city] = current_city_count.get(city, 0) + 1
        
        # 第二輪：如果還不夠，不限制城市數量
        if len(recommended_restaurants) < num_recommendations:
            remaining_recommendations = [
                rec for rec in all_recommendations 
                if rec[2] not in recommended_ids
            ]
            random.shuffle(remaining_recommendations)
            
            for rec in remaining_recommendations:
                if len(recommended_restaurants) >= num_recommendations:
                    break
                    
                restaurant_info, rating_info, restaurant_id = rec
                recommended_restaurants.append((
                    restaurant_info['name'],
                    restaurant_info['latitude'],
                    restaurant_info['longitude'],
                    restaurant_info['redirection_url'],
                    restaurant_info['navigation_url'],
                    restaurant_info['city'],
                    rating_info['distance'],
                    rating_info['rating'],
                    rating_info['review_number']
                ))
                recommended_ids.add(restaurant_id)
        
        return recommended_restaurants[:num_recommendations]
        
    except Exception as e:
        print(f"推薦過程發生錯誤: {str(e)}")
        traceback.print_exc()
        return []

# 推薦餐廳主程式(內容推薩)
def content_based_recommendations(user_id, num_recommendations):
    try:
        # 檢查用戶是否存在於訓練矩陣中
        if user_id not in train_user_restaurant_matrix.index:
            return []
            
        # 獲取用戶向量並檢查是否有評分
        user_vector = train_user_restaurant_matrix.loc[user_id].values.reshape(1, -1)
        if np.all(user_vector == 0):
            return []
        
       
        # 獲取用戶的歷史評分
        user_ratings = train_data[train_data['user_id'] == user_id]
        rated_restaurants = set(user_ratings.index)
        
        # 預先獲取所有評分資訊並建立索引
        restaurant_ratings = {}
        for _, row in train_data.iterrows():
            restaurant_id = row.name
            if restaurant_id not in restaurant_ratings:
                restaurant_ratings[restaurant_id] = {
                    'distance': float(row['distance']),
                    'rating': float(row['rating']),
                    'review_number': int(row['review_number'])
                }
        
        # 預先過濾有評分資訊的餐廳（排除用戶已評分的餐廳）
        valid_restaurants = []
        for idx in range(len(restaurants_df)):
            restaurant = restaurants_df.iloc[idx]
            if restaurant.name in restaurant_ratings and restaurant.name not in rated_restaurants:
                valid_restaurants.append(idx)
        
        # 隨機選擇有效的餐廳索引
        num_random_restaurants = min(20, len(valid_restaurants))
        if num_random_restaurants == 0:  # 如果沒有有效餐廳，返回空列表
            return []
        random_indices = random.sample(valid_restaurants, num_random_restaurants)
        
        recommended_restaurants = []
        processed_cities = set()
        
        # 第一輪：嘗試找到不同城市的推薦
        for idx in random_indices:
            if len(recommended_restaurants) >= num_recommendations:
                break
                
            restaurant_info = restaurants_df.iloc[idx]
            city = restaurant_info['city']
            
            # 確保城市不重複且未處理過
            if city not in processed_cities:
                rating_info = restaurant_ratings.get(restaurant_info.name)
                if rating_info:
                    recommended_restaurants.append((
                        restaurant_info['name'],
                        restaurant_info['latitude'],
                        restaurant_info['longitude'],
                        restaurant_info['redirection_url'],
                        restaurant_info['navigation_url'],
                        city,
                        rating_info['distance'],
                        rating_info['rating'],
                        rating_info['review_number']
                    ))
                    processed_cities.add(city)
        
        # 如果推薦數量不足，從其他城市隨機補充
        while len(recommended_restaurants) < num_recommendations:
            # 獲取未處理的城市
            remaining_cities = list(set(restaurants_df['city'].unique()) - processed_cities)
            
            # 如果沒有未處理的城市，則重新使用所有城市
            if not remaining_cities:
                remaining_cities = list(restaurants_df['city'].unique())
                processed_cities.clear()  # 重置已處理城市集合
            
            # 隨機選擇一個城市
            city = random.choice(remaining_cities)
            
            # 獲取該城市所有有效的餐廳（排除用戶已評分的餐廳）
            city_restaurants = []
            for idx in valid_restaurants:
                restaurant = restaurants_df.iloc[idx]
                if restaurant['city'] == city:
                    rating_info = restaurant_ratings.get(restaurant.name)
                    if rating_info:
                        city_restaurants.append((restaurant, rating_info))
            
            if city_restaurants:
                # 隨機選擇一家餐廳
                restaurant_info, rating_info = random.choice(city_restaurants)
                recommended_restaurants.append((
                    restaurant_info['name'],
                    restaurant_info['latitude'],
                    restaurant_info['longitude'],
                    restaurant_info['redirection_url'],
                    restaurant_info['navigation_url'],
                    city,
                    rating_info['distance'],
                    rating_info['rating'],
                    rating_info['review_number']
                ))
                processed_cities.add(city)
        
        return recommended_restaurants[:num_recommendations]
        
    except Exception as e:
        print(f"內容推薩過程發生錯誤: {str(e)}")
        traceback.print_exc()
        return []


# 推薦餐廳主程式(混合推薩)
def hybrid_recommendations(user_id, num_recommendations):
    if user_id not in train_user_restaurant_matrix.index:
        print(f"{user_id}這筆資料在矩陣內找不到，要不換一筆試試?")
        return []
    else:
        # 用於存放城市數量
        city_count = {}
        
        # 取得兩種推薦結果
        cf_recommendations = recommend_restaurants(user_id, num_recommendations)
        content_recommendations = content_based_recommendations(user_id, num_recommendations)
        
        # 將兩個推薦結果合併並加權
        all_recommendations = []
        seen_restaurants = set()
        
        # 為每個推薦結果計算綜合分數
        for rec in cf_recommendations + content_recommendations:
            restaurant_name = rec[0]
            if restaurant_name not in seen_restaurants:
                seen_restaurants.add(restaurant_name)
                
                # 獲取餐廳在兩種推薦中的位置（如果存在）
                cf_score = 1.0 - (cf_recommendations.index(rec) / len(cf_recommendations)) if rec in cf_recommendations else 0
                content_score = 1.0 - (content_recommendations.index(rec) / len(content_recommendations)) if rec in content_recommendations else 0
                
                # 計算加權分數 (0.7 協同過濾 + 0.3 內容推薩)
                hybrid_score = 0.7 * cf_score + 0.3 * content_score
                
                all_recommendations.append((hybrid_score, rec))
        
        # 根據混合分數排序
        all_recommendations.sort(reverse=True)
        
        # 選擇最終推薩，確保城市多樣性
        final_recommendations = []
        for _, rec in all_recommendations:
            city = rec[5]
            if city_count.get(city, 0) < 1:  # 每個城市最多一家餐廳
                final_recommendations.append(rec)
                city_count[city] = city_count.get(city, 0) + 1
                
            if len(final_recommendations) >= num_recommendations:
                break
        
        # 如果推薦數量不足，添加剩餘的推薩
        if len(final_recommendations) < num_recommendations:
            for _, rec in all_recommendations:
                if rec not in final_recommendations:
                    final_recommendations.append(rec)
                if len(final_recommendations) >= num_recommendations:
                    break
                    
        return final_recommendations[:num_recommendations]



# ===========================================================
# 推薩主程式進入點
# ===========================================================

def run_experiment(experiment_type):
    """執行指定類型的實驗"""
    print(f"\n{'='*30} {experiment_type} 實驗 {'='*30}")
    
    global train_user_restaurant_matrix, ratings_df, train_data, test_data
    
    # 初始化 MinMaxScaler，調整情感分析的範圍
    rating_scaler = MinMaxScaler(feature_range=(0, 5))  # 評分範圍 0-5
    sentiment_scaler = MinMaxScaler(feature_range=(-1, 1))  # 情感範圍 -1到1
    combined_scaler = MinMaxScaler(feature_range=(0, 1))  # 綜合評分範圍 0-1
    
    # 根據實驗類型設置資料並進行正規化
    if experiment_type == "rating_only":
        print("\n=== 使用餐廳評分進行實驗 ===")
        # 將評分正規化到 0-5 範圍
        normalized_rating = rating_scaler.fit_transform(ratings_df[['rating']])
        ratings_df['weighted_combined_score'] = normalized_rating
        
    elif experiment_type == "sentiment_only":
        print("\n=== 使用情感分析進行實驗 ===")
        # 將情感分數正規化到 -1到1 範圍
        normalized_sentiment = sentiment_scaler.fit_transform(ratings_df[['sentiment_score']])
        # 將正規化後的情感分數轉換為評分範圍 (0-5)
        ratings_df['weighted_combined_score'] = (normalized_sentiment + 1)
        
    else:  # hybrid
        print("\n=== 使用綜合評分進行實驗 ===")
        # 正規化評分到 0-5
        normalized_rating = rating_scaler.fit_transform(ratings_df[['rating']])
        
        # 正規化情感分數到 -1到1
        normalized_sentiment = sentiment_scaler.fit_transform(ratings_df[['sentiment_score']])
        
        # 調整權重計算方式
        rating_weight = 0.7
        sentiment_weight = 0.3
        
        # 調整情感分數的範圍轉換
        sentiment_for_weight = (normalized_sentiment + 1) * 2.5
        
        # 計算加權後的綜合分數時加入懲罰項
        weighted_score = (
            rating_weight * normalized_rating + 
            sentiment_weight * sentiment_for_weight
        )
        # 加入額外的懲罰項，讓分數分布更均勻
        weighted_score = weighted_score * (1 - np.abs(normalized_sentiment) * 0.1)
        
        # 使用 combined_scaler 將最終分數正規化到 0-1 範圍
        ratings_df['weighted_combined_score'] = combined_scaler.fit_transform(weighted_score)
        # 再將分數調整到 0-5 範圍，以便與其他實驗結果比較
        ratings_df['weighted_combined_score'] = ratings_df['weighted_combined_score'] * 5
    
    # 重新分割訓練集和測試集
    train_data, test_data = train_test_split(ratings_df, test_size=0.2, random_state=42)
    
    # 根據當前實驗的評分重新建立訓練集矩陣
    train_user_restaurant_matrix = train_data.pivot_table(
        index='user_id', 
        columns='restaurant_id',
        values='weighted_combined_score'
    ).fillna(0)
    
    # 修改：只從有評分記錄的用戶中抽取
    available_user_ids = train_user_restaurant_matrix.index.tolist()
    if len(available_user_ids) >= 5:
        user_ids = random.sample(available_user_ids, 5)
    else:
        user_ids = available_user_ids
    
    num_recommendations = 5
    
    # 進行推薩
    for user_id in user_ids:
        recommendations = hybrid_recommendations(user_id, num_recommendations)
        print(f"\n推薩給使用者【{user_id}】的餐廳如下：")
        for name, lat, lon, redirection_url, navigation_url, city, distance, rating, review_number in recommendations:
            print(f'''餐廳名稱：{name}
經度：{lon}
緯度：{lat}
所在城市：{city}
前往訂餐：{redirection_url if redirection_url else '無訂餐連結'}
前往導航：{navigation_url if navigation_url else '無導航連結'}
距離：{distance:.2f}
評分：{rating:.2f}
瀏覽人數：{review_number}
=============================''')
    
    # 評估模型
    results = evaluate_model(experiment_type)
    if results:
        rmse, mae, cm, accuracy, precision, recall, f1, class_report = results
        print(f"\n{experiment_type} 實驗評估結果：")
        print(f"{'='*50}")
        print(f"RMSE: {rmse:.2f}")
        print(f"MAE: {mae:.2f}")
        print(f"準確率: {accuracy:.2f}")
        print(f"精確率: {precision:.2f}")
        print(f"召回率: {recall:.2f}")
        print(f"F1評分: {f1:.2f}")
        print(f"\n分類報告:")
        print(class_report)
    
    return results

def save_experiment_results(experiment_results, experiment_item="未指定實驗項目"):
    """
    將實驗結果批次透過 API 儲存到資料庫
    Args:
        experiment_results: 實驗結果字典
        experiment_item: 實驗項目名稱（預設為"未指定實驗項目"）
    """
    try:
        # 取得當前時間作為實驗時間
        experiment_time = datetime.now().strftime('%Y-%m-%d %H:%M')
        
        # 準備批次寫入的資料陣列
        batch_data = []
        
        # 收集所有實驗結果
        for exp_type, results in experiment_results.items():
            if results:
                rmse, mae, _, accuracy, precision, recall, f1, _ = results
                
                # 將每個實驗結果加入陣列，新增實驗項目欄位，並統一格式化到小數點後兩位
                batch_data.append({
                    "實驗時間": experiment_time,
                    "實驗類別": exp_type,
                    "實驗項目": experiment_item,
                    "RMSE": f"{rmse:.2f}",
                    "MAE": f"{mae:.2f}",
                    "準確率": f"{accuracy:.2f}",
                    "精確率": f"{precision:.2f}",
                    "召回率": f"{recall:.2f}",  # 確保格式化到小數點後兩位
                    "F1評分": f"{f1:.2f}"       # 確保格式化到小數點後兩位
                })
        
        # 如果有資料要寫入
        if batch_data:
            try:
                # 發送批次寫入請求
                response = requests.post(
                        os.getenv('NOCO_API_URL'),
                        headers={
                            'accept': 'application/json',
                            'xc-token': os.getenv('NOCO_API_KEY'),
                            'Content-Type': 'application/json'
                        },
                    json=batch_data
                )
                
                if response.status_code == 200:
                    print(f"成功批次儲存 {len(batch_data)} 筆實驗結果")
                else:
                    print(f"API 請求失敗: {response.status_code}")
                    print(f"錯誤訊息: {response.text}")
                    
            except Exception as e:
                print(f"API 請求發生錯誤: {str(e)}")
                traceback.print_exc()
                
    except Exception as e:
        print(f"儲存實驗結果時發生錯誤: {str(e)}")
        traceback.print_exc()

# 修改主程式最後的部分
if __name__ == "__main__":
    print('''
    # ===========================================================
    # 歡迎使用點餐推薩系統
    # ===========================================================
    ''')

    # 執行三種實驗
    experiments = ['hybrid']
    all_results = {}

    for exp_type in experiments:
        all_results[exp_type] = run_experiment(exp_type)

    # 比較三種實驗結果
    print("\n" + "="*30 + " 實驗結果比較 " + "="*30)
    print(f"{'實驗類型':^15} {'RMSE':^8} {'MAE':^8} {'準確率':^8} {'精確率':^8} {'召回率':^8} {'F1評分':^8}")
    print("-"*70)

    for exp_type, results in all_results.items():
        if results:
            rmse, mae, _, accuracy, precision, recall, f1, _ = results
            print(f"{exp_type:^15} {rmse:8.2f} {mae:8.2f} {accuracy:8.2f} {precision:8.2f} {recall:8.2f} {f1:8.2f}")

    # 儲存實驗結果到資料庫，並指定實驗項目
    save_experiment_results(all_results, "權重比例調整0.7 - 0.3")  # 或 "沒有使用語言模型翻譯" 或 "權重比例調整"

