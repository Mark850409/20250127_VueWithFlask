from sklearn.model_selection import train_test_split
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics import mean_squared_error, mean_absolute_error, confusion_matrix, accuracy_score, precision_score, \
    recall_score, f1_score, classification_report
import numpy as np
from sqlalchemy import create_engine
from flask import Flask, request, abort
import json
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (MessageEvent, TextMessage, TextSendMessage, FollowEvent, UnfollowEvent,
                            LocationMessage, CarouselTemplate, CarouselColumn, PostbackAction, MessageAction, URIAction,
                            TemplateSendMessage)
from config import setting
import random
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from scipy.stats import pearsonr
from sklearn.metrics.pairwise import euclidean_distances, manhattan_distances
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity as cosine_similarity_metric

# 你的Google Places API金鑰
api_key = setting.api_key

app = Flask(__name__)

# 設置您的Channel Access Token和Channel Secret
ACCESS_TOKEN = setting.ACCESS_TOKEN
SECRET = setting.SECRET

line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(SECRET)

# ===========================================================
# 測試資料集
# ===========================================================
# # 生成10000家店家的名稱
# restaurant_names = [f'店家{i}' for i in range(1, 10001)]
#
# # 生成10000個隨機亂數作為店家的ID
# restaurant_ids = random.sample(range(10000, 99999), 10000)
#
# # 生成100個使用者對10000家店家的評分資料
# ratings_data = {
#     'user_id': [random.randint(1, 1000) for _ in range(10000)],
#     'restaurant_name': restaurant_names,
#     'restaurant_id': restaurant_ids,
#     'rating': [random.randint(1, 5) for _ in range(10000)],
#     'city': ['台北市'] * 10000
# }

# # 生成100個使用者對10000家店家的評分資料
# ratings_data = {
#     'user_id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
#     'restaurant_name': ['可不可熟成紅茶 (台北通化店)', '好了啦紅茶冰 (饒河八德店)', '水巷茶弄 (南京三民店)',
#                         '清心福全 (信義永吉店)', 'COMEBUY (台北市府店)', 'TEATOP 第一味 (台北通化店)',
#                         '北投紅茶 (大安店)', '嘉義紅茶 (台北饒河店)', '富士堂-日本鮮奶茶飲', '果霸茶 (台北通化店)'],
#     'restaurant_id': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
#     'rating': [1, 2, 3, 1, 5, 1, 4, 5, 1, 3],
#     'city': ['台北市'] * 10
# }
#
# # # 生成店家的地理位置和網址資料
# restaurants_data = {
#     'restaurant_id': [101, 102, 103, 104, 105, 106, 107, 108, 109, 110],
#     'latitude': [round(random.uniform(25.02, 25.05), 4) for _ in range(10)],
#     'longitude': [round(random.uniform(121.55, 121.58), 4) for _ in range(10)],
#     'name': ['可不可熟成紅茶 (台北通化店)', '好了啦紅茶冰 (饒河八德店)', '水巷茶弄 (南京三民店)',
#                         '清心福全 (信義永吉店)', 'COMEBUY (台北市府店)', 'TEATOP 第一味 (台北通化店)',
#                         '北投紅茶 (大安店)', '嘉義紅茶 (台北饒河店)', '富士堂-日本鮮奶茶飲', '果霸茶 (台北通化店)'],
#     'redirection_url': ['http://google.com'] * 10,
#     'navigation_url': ['http://google.com'] * 10
# }

# # 生成10000家店家的名稱和ID
# restaurant_names = [f'店家{i}' for i in range(1, 10001)]
# restaurant_ids = random.sample(range(10000, 99999), 10000)
#
# # 生成店家的地理位置和網址資料
# restaurants_data = {
#     'restaurant_id': restaurant_ids,
#     'latitude': [round(random.uniform(25.0, 25.1), 4) for _ in range(10000)],
#     'longitude': [round(random.uniform(121.5, 121.6), 4) for _ in range(10000)],
#     'name': restaurant_names,
#     'redirection_url': ['http://google.com'] * 10000,
#     'navigation_url': ['http://google.com'] * 10000
# }
#
# # 生成100個使用者ID
# user_ids = list(range(1, 101))
#
# # 生成評分資料
# ratings_data = {
#     'user_id': [],
#     'restaurant_name': [],
#     'restaurant_id': [],
#     'rating': [],
#     'city': []
# }
#
# for user_id in user_ids:
#     # 隨機選擇每位使用者評論的店家數量，假設為5至20家店家
#     idx = random.randint(0, 9)  # 隨機選擇店家資料的索引
#     ratings_data['user_id'].append(user_id)
#     ratings_data['restaurant_name'].append(restaurants_data['name'][idx])
#     ratings_data['restaurant_id'].append(restaurants_data['restaurant_id'][idx])
#     ratings_data['rating'].append(random.randint(1, 5))  # 隨機生成評分
#     ratings_data['city'].append('台北市')  # 假設都在台北市
#
# ratings_df = pd.DataFrame(ratings_data)
# print(ratings_df)
# restaurants_df = pd.DataFrame(restaurants_data)
# print(restaurants_df)
# # 資料集合併
# merged_df = pd.merge(ratings_df, restaurants_df, on='restaurant_id')
#
# # 建立餐廳矩陣
# user_restaurant_matrix = merged_df.pivot_table(index='user_id', columns='restaurant_id', values='rating').fillna(0)
#
# # 將資料集拆分為訓練集與測試集
# train_data, test_data = train_test_split(ratings_df, test_size=0.5, random_state=42)
#
# # 建立用户-餐廳矩陣，使用综合評分
# train_user_restaurant_matrix = ratings_df.pivot_table(index='user_id', columns='restaurant_id',
#                                                       values='rating').fillna(0)

# ===========================================================
# 從資料庫取得資料集
# ===========================================================

# 建立連線
connect_ibfo = setting.SQLALCHEMY_DATABASE_URI
engine = create_engine(connect_ibfo)

# 取得評分資料集
ratings_df = pd.read_sql('''select GMRW.id,GMRW.place_id,GMRW.restaurant_name,GMRW.rating,GMRW.composite_score,GMRW.user,RTL.city,RTL.city_CN,RTL.distance,RTL.review_number
from google_maps_review_with_selenium GMRW
JOIN restaurant_type_list  RTL ON  RTL.id=GMRW.id
where confidence>=0.7
''', con=engine)

# 建立user對應ID的表格，從1開始編號
unique_users = ratings_df['user'].unique()
user_to_id = {user: idx + 1 for idx, user in enumerate(unique_users)}

# 使用 user_to_id 替换 'user' 列中的值
ratings_df['user_id'] = ratings_df['user'].map(user_to_id)

# 取得餐廳資料集
restaurants_df = pd.read_sql(
    "SELECT * FROM ConvertNameToPlaceID WHERE navigation_url<>'No navigation found' and place_id is not null",
    con=engine)

# 取得筆數資料集
count_data = pd.read_sql(
    "SELECT count(*) as count from restaurant_type_list",
    con=engine)

count_df = pd.DataFrame(count_data)

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
city_url_to_id = {row['restaurant_id']: row['city'] for _, row in ratings_df.iterrows()}

# 資料集合併
merged_df = pd.merge(ratings_df, restaurants_df, on='restaurant_id')

# ===========================================================
# 情感分析+餐廳評分+距離使用+瀏覽次數(定義權重)
# ===========================================================
# 定義初始權重
base_rating_weight = 0.1
base_overall_sentiment_weight = 0.1
base_distance_weight = 0.4

# 正規化餐廳評分、距離、瀏覽量
scaler = MinMaxScaler()
ratings_df['normalized_rating'] = scaler.fit_transform(ratings_df[['rating']])
ratings_df['normalized_distance'] = scaler.fit_transform(ratings_df[['distance']])
ratings_df['normalized_review_number'] = scaler.fit_transform(ratings_df[['review_number']])

print(ratings_df['normalized_rating'])
print(ratings_df['normalized_distance'])
print(ratings_df['normalized_review_number'])

# 動態調整權重，使用指數函數或其他非線性函數
ratings_df['dynamic_rating_weight'] = np.exp(ratings_df['normalized_rating']) * base_rating_weight
ratings_df['dynamic_sentiment_weight'] = np.exp(ratings_df['sentiment_score']) * base_overall_sentiment_weight
ratings_df['dynamic_distance_weight'] = np.exp(-ratings_df['normalized_distance']) * base_distance_weight
ratings_df['dynamic_review_number_weight'] = np.exp(ratings_df['normalized_review_number'])

# 對瀏覽量權重進行正規化，確保不超過1
max_dynamic_review_number_weight = ratings_df['dynamic_review_number_weight'].max()
ratings_df['dynamic_review_number_weight'] = ratings_df['dynamic_review_number_weight'] / max_dynamic_review_number_weight

print(ratings_df[['dynamic_rating_weight', 'dynamic_sentiment_weight','dynamic_distance_weight','dynamic_review_number_weight']])
# 確保權重之和為1
total_weight = (
    ratings_df['dynamic_rating_weight'] +
    ratings_df['dynamic_sentiment_weight'] +
    ratings_df['dynamic_distance_weight'] +
    ratings_df['dynamic_review_number_weight']
)
ratings_df['dynamic_rating_weight'] /= total_weight
ratings_df['dynamic_sentiment_weight'] /= total_weight
ratings_df['dynamic_distance_weight'] /= total_weight
ratings_df['dynamic_review_number_weight'] /= total_weight

# 計算未正規化的綜合評分
ratings_df['unscaled_combined_score'] = (
    ratings_df['normalized_rating'] * ratings_df['dynamic_rating_weight'] +
    ratings_df['sentiment_score'] * ratings_df['dynamic_sentiment_weight'] +
    ratings_df['normalized_distance'] * ratings_df['dynamic_distance_weight'] +
    ratings_df['normalized_review_number'] * ratings_df['dynamic_review_number_weight']
)

# 正規化綜合評分，確保在0到1之間
scaler_combined = MinMaxScaler()
ratings_df['weighted_combined_score'] = scaler_combined.fit_transform(ratings_df[['unscaled_combined_score']])

# 將資料集拆分為訓練集與測試集
train_data, test_data = train_test_split(ratings_df, test_size=0.2, random_state=42)

# 建立用户-餐廳矩陣，使用综合評分
train_user_restaurant_matrix = ratings_df.pivot_table(index='user_id', columns='restaurant_id',
                                                     values='weighted_combined_score').fillna(0)

# ===========================================================
# 情感分析+餐廳評分+距離使用(定義權重)
# ===========================================================
# # 定義初始權重
# base_rating_weight = 0.2
# base_overall_sentiment_weight = 0.2
# base_distance_weight = 0.6
# # 正規化餐廳評分、距離
# scaler = MinMaxScaler()
# ratings_df['normalized_rating'] = scaler.fit_transform(ratings_df[['rating']])
# ratings_df['normalized_distance'] = scaler.fit_transform(ratings_df[['distance']])
#
# # 動態調整權重，使用指數函數或其他非線性函數
# ratings_df['dynamic_rating_weight'] = np.exp(ratings_df['normalized_rating']) * base_rating_weight
# ratings_df['dynamic_sentiment_weight'] = np.exp(ratings_df['sentiment_score']) * base_overall_sentiment_weight
# #ratings_df['dynamic_distance_weight'] = np.exp(ratings_df['normalized_distance']) * base_distance_weight
# ratings_df['dynamic_distance_weight'] = np.exp(-ratings_df['normalized_distance'])* base_distance_weight  # 反轉距離的正規化值
#
# # 確保權重之和為1
# total_weight = (
#     ratings_df['dynamic_rating_weight'] +
#     ratings_df['dynamic_sentiment_weight'] +
#     ratings_df['dynamic_distance_weight']
# )
# ratings_df['dynamic_rating_weight'] /= total_weight
# ratings_df['dynamic_sentiment_weight'] /= total_weight
# ratings_df['dynamic_distance_weight'] /= total_weight
#
# # 計算未正規化的綜合評分
# ratings_df['unscaled_combined_score'] = (
#     ratings_df['normalized_rating'] * ratings_df['dynamic_rating_weight'] +
#     ratings_df['sentiment_score'] * ratings_df['dynamic_sentiment_weight'] +
#     ratings_df['normalized_distance'] * ratings_df['dynamic_distance_weight']
# )
#
# # 正規化綜合評分，確保在0到1之間
# scaler_combined = MinMaxScaler()
# ratings_df['weighted_combined_score'] = scaler_combined.fit_transform(ratings_df[['unscaled_combined_score']])
#
# # 將資料集拆分為訓練集與測試集
# train_data, test_data = train_test_split(ratings_df, test_size=0.2, random_state=42)
#
# # 建立用户-餐廳矩陣，使用综合評分
# train_user_restaurant_matrix = ratings_df.pivot_table(index='user_id', columns='restaurant_id',
#                                                       values='weighted_combined_score').fillna(0)
# ===========================================================
# # 情感分析+餐廳評分(定義權重)
# ===========================================================

# 定義初始權重
base_rating_weight = 0.7
base_overall_sentiment_weight = 0.3

# 正規化餐廳評分、情感分數
scaler = MinMaxScaler()
ratings_df['normalized_rating'] = scaler.fit_transform(ratings_df[['rating']])
ratings_df['normalized_sentiment_score'] = scaler.fit_transform(ratings_df[['sentiment_score']])

# 動態調整權重，使用指數函數或其他非線性函數
ratings_df['dynamic_rating_weight'] = np.exp(ratings_df['normalized_rating']) * base_rating_weight
ratings_df['dynamic_sentiment_weight'] = np.exp(
    ratings_df['normalized_sentiment_score']) * base_overall_sentiment_weight

# 確保權重之和為1
total_weight = ratings_df['dynamic_rating_weight'] + ratings_df['dynamic_sentiment_weight']
ratings_df['dynamic_rating_weight'] /= total_weight
ratings_df['dynamic_sentiment_weight'] /= total_weight

# 打印或存儲動態權重
print(ratings_df[['dynamic_rating_weight', 'dynamic_sentiment_weight']])

# 計算未正規化的綜合評分
ratings_df['unscaled_combined_score'] = (
        ratings_df['normalized_rating'] * ratings_df['dynamic_rating_weight'] +
        ratings_df['sentiment_score'] * ratings_df['dynamic_sentiment_weight']
)

# 正規化綜合評分，確保在0到1之間
scaler_combined = MinMaxScaler()
ratings_df['weighted_combined_score'] = scaler_combined.fit_transform(ratings_df[['unscaled_combined_score']])

# 將資料集拆分為訓練集與測試集
train_data, test_data = train_test_split(ratings_df, test_size=0.2, random_state=42)

# 建立用户-餐廳矩陣，使用综合評分
train_user_restaurant_matrix = ratings_df.pivot_table(index='user_id', columns='restaurant_id',
                                                      values='weighted_combined_score').fillna(0)


# ===========================================================
# 模型訓練開始
# ===========================================================

# 訓練KNN模型
knn = NearestNeighbors(metric='cosine', algorithm='brute')
knn.fit(train_user_restaurant_matrix.values)


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


def predict(user_id, restaurant_id, method='cosine'):
    if user_id not in train_user_restaurant_matrix.index or restaurant_id not in train_user_restaurant_matrix.columns:
        return None

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

    # 透過不同方式計算相似度
    for i in range(1, len(distances.flatten())):
        similar_user_id = train_user_restaurant_matrix.index[indices.flatten()[i]]
        if pd.notna(train_user_restaurant_matrix.loc[similar_user_id, restaurant_id]):
            user_vector = train_user_restaurant_matrix.loc[user_id].values
            similar_user_vector = train_user_restaurant_matrix.loc[similar_user_id].values
            # 餘弦相似度
            if method == 'cosine':
                sim = cosine_similarity_predict(user_vector, similar_user_vector)
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

    if similarity_sum == 0:
        return None
    else:
        predicted_rating = ratings_sum / similarity_sum
        print("=============================")
        print(f"模型預測分數為: {predicted_rating}")
        print(f"加權評分為: {ratings_sum}")
        print(f"相似度總分為: {similarity_sum}")
        print("=============================")
        # print("鄰居的相似度和加權評分貢獻為:")
        # for neighbor in neighbor_contributions:
        #     print(
        #         f"使用者: {neighbor[0]}, 餐廳: {neighbor[1]},相似度預測評分: {neighbor[2]}, 加權評分: {neighbor[3]}, 相似度總分: {neighbor[4]}")
        # print("=============================")
        return predicted_rating


# 評估模型準確度
def evaluate_model():
    y_true = []
    y_pred = []

    for _, row in test_data.iterrows():
        user_id = row['user_id']
        restaurant_id = row['restaurant_id']
        true_rating = row['weighted_combined_score']
        predicted_rating = predict(user_id, restaurant_id)  # 使用 predict_function 來預測評分
        if predicted_rating is not None:
            y_true.append(true_rating)
            y_pred.append(predicted_rating)
            # print(f"評分預測 {predicted_rating}已加入!!!")
        else:
            print(f"未能預測 {user_id} 和 {restaurant_id} 的評分，可能由於資料不足或未知的組合。")
    # 檢查 y_true 和 y_pred 是否為空
    if not y_true or not y_pred:
        print("糟糕!!!資料不夠耶!!!")
        return None

    # 計算RMSE和MAE
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mae = mean_absolute_error(y_true, y_pred)

    # 設定評分閾值轉換
    threshold = 0.5  # 使用平均值作為評分閾值

    # 轉換為分類問題
    y_true_class = [1 if rating >= threshold else 0 for rating in y_true]
    y_pred_class = [1 if rating >= threshold else 0 for rating in y_pred]

    # 計算混淆矩陣及其他指標
    cm = confusion_matrix(y_true_class, y_pred_class)
    accuracy = accuracy_score(y_true_class, y_pred_class)
    precision = precision_score(y_true_class, y_pred_class, zero_division=0)
    recall = recall_score(y_true_class, y_pred_class, zero_division=0)
    f1 = f1_score(y_true_class, y_pred_class, zero_division=0)
    class_report = classification_report(y_true_class, y_pred_class, zero_division=0)

    return rmse, mae, cm, accuracy, precision, recall, f1, class_report


# ===========================================================
# 推薦餐廳主程式(基於內容推薦、協同過濾、混合推薦)
# ===========================================================

# 推薦餐廳主程式(協同過濾)
def recommend_restaurants(user_id, num_recommendations):
    # print(f"相似用戶名稱為: {train_user_restaurant_matrix.index}")
    if user_id not in train_user_restaurant_matrix.index:
        print(f"{user_id}這筆資料在矩陣內找不到，要不換一筆試試?")
        return []
    else:
        user_index = train_user_restaurant_matrix.index.get_loc(user_id)

        db_count = int(count_df['count'].iloc[0])

        print(f"餐廳資料集的筆數是: {db_count}\n")

        # 設定較大的 n_neighbors 值以擴大潛在推薦範圍
        n_neighbors = min(num_recommendations * random.randint(1, 5), len(train_user_restaurant_matrix))

        # 取出距離計算餘弦相似度
        distances, indices = knn.kneighbors(train_user_restaurant_matrix.iloc[user_index, :].values.reshape(1, -1),
                                            n_neighbors=n_neighbors)

        # 取出相似度最高的前5個使用者的索引和距離
        top_5_indices = indices.flatten()[1:6]  # 排除自己，取出前5個相似用戶的索引
        top_5_distances = distances.flatten()[1:6]  # 取出前5個相似用戶的距離

        print(f"與{user_id}相似度最高的前5個使用者及其距離是：\n")

        for idx, (user_idx, distance) in enumerate(zip(top_5_indices, top_5_distances), 1):
            similar_user_id = train_user_restaurant_matrix.index[user_idx]
            print(f"{idx}. 使用者ID: {similar_user_id}, 相似度距離: {distance:.2f}")

            # 取出相似用戶的評分資料
            similar_user_ratings = train_data[train_data['user_id'] == similar_user_id]
            printed_restaurant_ids = set()  # 用於跟踪已打印的餐廳ID

            for _, row in similar_user_ratings.iterrows():
                restaurant_id = row['restaurant_id']
                if restaurant_id not in printed_restaurant_ids:
                    print(
                        f"======================================\n餐廳ID: {row['restaurant_id']}\n評分: {row['rating']}\n餐廳名稱: {row['restaurant_name']}\n所在城市: {row['city']}\n======================================")
                    printed_restaurant_ids.add(restaurant_id)

        # 隨機選擇部分鄰居的索引
        random_neighbors = random.sample(range(1, len(distances.flatten())),
                                         min(num_recommendations * 1, len(distances.flatten()) - 1))

        # 用於存放餐廳
        recommended_restaurants = []

        # 用於追蹤已推薦的餐廳ID
        recommended_ids = set()

        # 用於存放城市數量
        city_count = {}

        for i in random_neighbors:
            similar_user_id = train_user_restaurant_matrix.index[indices.flatten()[i]]
            similar_user_ratings = train_data[train_data['user_id'] == similar_user_id]

            for _, row in similar_user_ratings.iterrows():
                restaurant_id = row['restaurant_id']
                if restaurant_id not in recommended_ids:
                    # 取得經緯度
                    restaurant_location = restaurants_df[restaurants_df['restaurant_id'] == restaurant_id]
                    # 若經緯度為空就跳過
                    if restaurant_location.empty:
                        continue
                    # 取得相關資訊
                    restaurant_name = id_to_name.get(restaurant_id)
                    redirection_urls = redirection_url_to_id.get(restaurant_id)
                    navigation_urls = navigation_url_to_id.get(restaurant_id)
                    city = city_url_to_id.get(restaurant_id)
                    # 確保每個城市推薦的餐廳不超過指定數量
                    if city_count.get(city, 0) <= 1:
                        recommended_restaurants.append((restaurant_name, restaurant_location['latitude'].values[0],
                                                        restaurant_location['longitude'].values[0], redirection_urls,
                                                        navigation_urls, city))
                        recommended_ids.add(restaurant_id)
                        city_count[city] = city_count.get(city, 0) + 1
                    # 如果推薦餐廳已滿，跳出內層循環
                    if len(recommended_restaurants) >= num_recommendations:
                        break
            # 如果推薦餐廳已滿，跳出外層循環
            if len(recommended_restaurants) >= num_recommendations:
                break
        # 增加隨機性，從推薦列表中隨機選擇指定數量的餐廳
        if len(recommended_restaurants) > num_recommendations:
            recommended_restaurants = random.sample(recommended_restaurants, num_recommendations)
        else:
            recommended_restaurants = recommended_restaurants[:num_recommendations]
    # 返回最近的num_recommendations家餐廳的名稱和經緯度
    return recommended_restaurants


# 推薦餐廳主程式(內容推薦)
def content_based_recommendations(user_id, num_recommendations):
    # 計算餐廳之間內容相似性
    content_similarities = cosine_similarity(train_user_restaurant_matrix)

    # 隨機選擇10間使用者可能感興趣的餐廳
    num_random_restaurants = 10
    random_restaurant_indices = random.sample(range(len(restaurants_df)), num_random_restaurants)

    # 用於存放城市數量
    city_count = {}

    # 根據隨機選擇的餐廳，找到相似度高的餐廳
    similar_restaurants = []
    for idx in random_restaurant_indices:
        restaurant_similarities = content_similarities[idx]
        top_indices = restaurant_similarities.argsort()[::-1][:num_recommendations]
        for top_idx in top_indices:
            # 超過索引值範圍就跳過
            if top_idx >= len(restaurants_df):
                continue
            restaurant_id = restaurants_df.iloc[top_idx]['restaurant_id']
            # 如果餐廳ID不在原先的推薦列表且餐廳列表的數量小於指定推薦數量，才放到列表進行推薦，否則就不推薦
            if restaurant_id not in similar_restaurants and len(similar_restaurants) < num_recommendations:
                similar_restaurants.append(restaurant_id)
        # 如果餐廳列表大於推薦數量，就跳過
        if len(similar_restaurants) >= num_recommendations:
            break

    # 根據餐廳ID和相關訊息放入推薦列表
    recommended_restaurants = []

    for restaurant_id in similar_restaurants:
        restaurant_info = restaurants_df[restaurants_df['restaurant_id'] == restaurant_id]
        rating_info = ratings_df[ratings_df['restaurant_id'] == restaurant_id]
        if not restaurant_info.empty and not rating_info.empty:
            city = rating_info['city'].values[0]
            # 確保每個城市推薦的餐廳不超過指定數量
            if city_count.get(city, 0) < 1:
                recommended_restaurants.append((
                    restaurant_info['name'].values[0],
                    restaurant_info['latitude'].values[0],
                    restaurant_info['longitude'].values[0],
                    restaurant_info['redirection_url'].values[0],
                    restaurant_info['navigation_url'].values[0],
                    city
                ))
                city_count[city] = city_count.get(city, 0) + 1

    # 如果推薦餐廳不足 num_recommendations，隨機補足，並確保城市不重複
    while len(recommended_restaurants) < num_recommendations:
        random_idx = np.random.randint(len(restaurants_df))
        restaurant_id = restaurants_df.iloc[random_idx]['restaurant_id']
        restaurant_info = restaurants_df[restaurants_df['restaurant_id'] == restaurant_id]
        rating_info = ratings_df[ratings_df['restaurant_id'] == restaurant_id]
        # 確保restaurant_info和rating_info不為空
        if not restaurant_info.empty and not rating_info.empty:
            city = rating_info['city'].values[0]
            # 確保每個城市推薦的餐廳不超過指定數量
            if city_count.get(city, 0) < 1:
                recommended_restaurants.append((
                    restaurant_info['name'].values[0],
                    restaurant_info['latitude'].values[0],
                    restaurant_info['longitude'].values[0],
                    restaurant_info['redirection_url'].values[0],
                    restaurant_info['navigation_url'].values[0],
                    city
                ))
                city_count[city] = city_count.get(city, 0) + 1
    # 回傳指定推薦的餐廳數量
    return recommended_restaurants[:num_recommendations]


# 推薦餐廳主程式(混合推薦)
def hybrid_recommendations(user_id, num_recommendations):
    if user_id not in train_user_restaurant_matrix.index:
        print(f"{user_id}這筆資料在矩陣內找不到，要不換一筆試試?")
        return []
    else:
        # 用於存放城市數量
        city_count = {}
        # 取得協同過濾推薦餐廳
        cf_recommendations = recommend_restaurants(user_id, num_recommendations)
        # 取得內容推薦餐廳
        content_recommendations = content_based_recommendations(user_id, num_recommendations)
        # 將兩個推薦結果合併
        all_recommendations = cf_recommendations + content_recommendations
        # 存放唯一的推薦結果
        unique_recommendations = []
        seen = set()
        for rec in all_recommendations:
            # 沒有推薦過的餐廳才進行推薦
            if rec not in seen:
                # 取得所有城市
                city = rec[5]
                # 確保每個城市推薦的餐廳不超過指定數量
                if city_count.get(city, 0) < 1:
                    unique_recommendations.append(rec)
                    city_count[city] = city_count.get(city, 0) + 1
                seen.add(rec)

        if len(unique_recommendations) > num_recommendations:
            unique_recommendations = random.sample(unique_recommendations, num_recommendations)

    return unique_recommendations[:num_recommendations]


# ===========================================================
# LINE API串接
# ===========================================================

# 處理LINE訊息
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


user_states = {}  # 初始化使用者狀態字典


# 處理文字訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text.strip()
    user_id = event.source.user_id
    profile = line_bot_api.get_profile(user_id)
    user_name = profile.display_name

    if text.lower() == 'help' or text in ['使用須知', '使用說明', '提示', '提示文字']:
        message = TextSendMessage(
            text=f"您好：{user_name}\n感謝您加入好友😘\n歡迎使用點餐推薦機器人😎！\n🍽️ 下列為使用教學(總共為兩個步驟)：\n1.請輸入您的 user_id 來獲取餐廳推薦，例如：1\n2.️ ️您想要推薦幾家餐廳？請輸入數字，例如：3\n備註：user_id範圍在1~1039，請輸入在這範圍當中的任意數字!!!"
        )
        line_bot_api.reply_message(event.reply_token, message)
        return

    if user_id in user_states:
        if user_states[user_id]['step'] == 'ask_for_count':
            try:
                num_recommendations = int(text)

                if num_recommendations > 10 or num_recommendations < 1:
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text='🚫最多只能推薦10家餐廳，最少推薦1家餐廳，請重新輸入！')
                    )
                    return  # 在這裡加上 return，終止後續程式碼執行
                else:
                    user_states[user_id]['num_recommendations'] = num_recommendations
                    user_states[user_id]['step'] = 'done'
                    # 取得推薦的餐廳
                    recommendations = recommend_restaurants(user_states[user_id]['user_id'], num_recommendations)
                    if recommendations:
                        carousel_data = []
                        for name, lat, lon, redirection_urls, navigation_urls in recommendations:
                            carousel_data.append(
                                {
                                    'thumbnail_image_url': 'https://firebasestorage.googleapis.com/v0/b/mlimage-64f65.appspot.com/o/cake.jpg?alt=media&token=f9081587-8b75-4074-b1dc-4f98410397c1',
                                    # 替換成有效的圖片URL
                                    'title': name,
                                    'text': f"經度：{lon}，緯度：{lat}",
                                    'actions': [
                                        {'type': 'uri', 'label': '點我導覽至googlemaps', 'uri': navigation_urls},
                                        {'type': 'uri', 'label': '點我導覽至foodpanda', 'uri': redirection_urls},
                                        {'type': 'message', 'label': '使用說明',
                                         'text': '使用說明'}
                                    ]
                                }
                            )

                        columns = []
                        for item in carousel_data:
                            actions = []
                            for action in item['actions']:
                                if action['type'] == 'uri':
                                    actions.append(URIAction(label=action['label'], uri=action['uri']))
                                elif action['type'] == 'postback':
                                    actions.append(PostbackAction(label=action['label'], data=action['data'],
                                                                  text=action.get('text', None)))
                                elif action['type'] == 'message':
                                    actions.append(MessageAction(label=action['label'], text=action['text']))

                            column = CarouselColumn(
                                thumbnail_image_url=item['thumbnail_image_url'],
                                title=item['title'],
                                text=item['text'],
                                actions=actions
                            )
                            columns.append(column)

                        carousel_template = CarouselTemplate(columns=columns)
                        template_message = TemplateSendMessage(
                            alt_text='推薦餐廳',
                            template=carousel_template
                        )
                        line_bot_api.reply_message(event.reply_token, template_message)
                    else:
                        message = TextSendMessage(text="找不到相關餐廳推薦資料。")
                        line_bot_api.reply_message(event.reply_token, message)

                # 清除用户状态
                del user_states[user_id]

            except ValueError:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text="🚫請輸入有效的數字！")
                )
        return

    try:
        user_id_input = int(text)
        if (user_id_input < 1 or user_id_input > 1039):
            line_bot_api.push_message(user_id, TextSendMessage(text='🚫您輸入的user不存在，請重新輸入!!!'))
        else:
            user_states[user_id] = {
                'step': 'ask_for_count',
                'user_id': user_id_input
            }
            message = TextSendMessage(
                text="🍽️ 您想要推薦幾家餐廳？請輸入數字，例如：3"
            )
            line_bot_api.reply_message(event.reply_token, message)
    except ValueError:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="🚫 請輸入有效的 user_id！例如：1")
        )


# LINE WEBHOOK串接進入點
@app.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)  # 取得收到的訊息內容
    signature = request.headers['X-Line-Signature']  # 加入回傳的 headers
    try:
        handler.handle(body, signature)  # 綁定訊息回傳的相關資訊
        json_data = json.loads(body)  # json 格式化訊息內容
        tk = json_data['events'][0]['replyToken']  # 取得回傳訊息的 Token
        event_type = json_data['events'][0]['type']  # 取得事件類型
    except InvalidSignatureError:
        abort(400)
    except Exception as e:
        print(f"Error: {e}")  # 印出錯誤訊息
        print(body)  # 印出收到的內容

    return 'OK'  # 驗證 Webhook 使用，不能省略


# 處理加入好友事件
@handler.add(FollowEvent)
def handle_follow(event):
    user_id = event.source.user_id
    profile = line_bot_api.get_profile(user_id)
    user_name = profile.display_name

    # 新用戶會看到的訊息
    welcome_message = f"您好：{user_name}\n感謝您加入好友😘\n歡迎使用點餐推薦機器人😎！\n🍽️ 下列為使用教學(總共為兩個步驟)：\n1.請輸入您的 user_id 來獲取餐廳推薦，例如：1\n2.️ ️您想要推薦幾家餐廳？請輸入數字，例如：3\n備註：user_id範圍在1~1039，請輸入在這範圍當中的任意數字!!!"
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=welcome_message)
    )


# 處理封鎖和重新加入好友事件
@handler.add(UnfollowEvent)
def handle_unfollow(event):
    user_id = event.source.user_id
    profile = line_bot_api.get_profile(user_id)
    user_name = profile.display_name

    # 新用戶會看到的訊息
    welcome_message = f"歡迎加入, {user_name}！🍽️ 請輸入您的 user_id 來獲取餐廳推薦，例如：1"
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=welcome_message)
    )


# 處理地點訊息事件
@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    location = event.message  # 取得地點訊息
    reply = f"地點名稱：{location.title}\n地址：{location.address}\n緯度：{location.latitude}\n經度：{location.longitude}"
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply)
    )


# ===========================================================
# 推薦主程式進入點
# ===========================================================

# 使用隨機亂數抽取餐廳資料集裡任5個數字當user_id
user_ids = random.sample(range(1, int(count_df['count'].iloc[0])), 1)
num_recommendations = 5
print(f'''
# ===========================================================
# 歡迎使用點餐推薦系統
# ===========================================================
''')
for user_id in user_ids:
    recommendations = hybrid_recommendations(user_id, num_recommendations)
    print(f"推薦給使用者【{user_id}】的餐廳如下：\n")
    for name, lat, lon, redirection_url, navigation_url, city in recommendations:
        print(f"餐廳名稱：{name}\n經度：{lon}\n緯度：{lat}\n所在城市：{city}")
        print("=============================")
# 評估模型準確度
results = evaluate_model()
if results:
    rmse, mae, cm, accuracy, precision, recall, f1, class_report = results
    print(f"RMSE:{rmse:.2f}")
    print(f"MAE:{mae:.2f}")
    print("=============================")
    print(f"準確率:{accuracy:.2f}")
    print(f"精確率:{precision:.2f}")
    print(f"召回率:{recall:.2f}")
    print(f"F1評分:{f1:.2f}")
    print("=============================")
    print("報表:\n", class_report)

# ===========================================================
# LINE主程式進入點
# ===========================================================
# if __name__ == "__main__":
#     warnings.filterwarnings("ignore", category=LineBotSdkDeprecatedIn30)
#     app.run(debug=True, host='0.0.0.0', port=5000)
