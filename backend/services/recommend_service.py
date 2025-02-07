from dao.recommend_dao import RecommendDAO
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
import random

class RecommendService:
    def __init__(self):
        self.recommend_dao = RecommendDAO()
        self.train_user_restaurant_matrix = None
        self.init_data()
    
    def init_data(self):
        """初始化數據"""
        self.ratings_df = self.recommend_dao.get_ratings_data()
        self.restaurants_df = self.recommend_dao.get_restaurants_data()
        self._prepare_data()
    
    def _prepare_data(self):
        """準備數據"""
        # 建立user對應ID的表格
        unique_users = self.ratings_df['user'].unique()
        print(unique_users)
        self.user_to_id = {user: idx + 1 for idx, user in enumerate(unique_users)}
        print(self.user_to_id)
        self.ratings_df['user_id'] = self.ratings_df['user'].map(self.user_to_id)
        
        # 準備評分數據
        self.train_data, self.test_data = train_test_split(self.ratings_df, test_size=0.2, random_state=42)
        
        # 初始化評分矩陣
        self._init_matrix()
    
    def _init_matrix(self):
        """初始化評分矩陣"""
        try:
            # 標準化評分
            scaler = MinMaxScaler()
            self.train_data['normalized_rating'] = scaler.fit_transform(
                self.train_data[['rating']].values
            )
            
            # 計算情感分數
            self.train_data['normalized_sentiment'] = scaler.fit_transform(
                self.train_data[['composite_score']].values
            )
            
            # 計算加權分數
            self.train_data['weighted_combined_score'] = (
                0.7 * self.train_data['normalized_rating'] +
                0.3 * self.train_data['normalized_sentiment']
            )
            
            # 建立用戶-餐廳矩陣
            self.train_user_restaurant_matrix = self.train_data.pivot_table(
                index='user_id',
                columns='place_id',
                values='weighted_combined_score'
            ).fillna(0)
            
        except Exception as e:
            print(f"初始化評分矩陣時發生錯誤: {str(e)}")
            self.train_user_restaurant_matrix = pd.DataFrame()

    def get_recommendations(self, user_id, num_recommendations=5):
        """獲取推薦結果"""
        try:
            if user_id not in self.train_user_restaurant_matrix.index:
                print(f"{user_id}這筆資料在矩陣內找不到，要不換一筆試試?")
                return []
            
            # 直接返回混合推薦結果
            return self._hybrid_recommendations(user_id, num_recommendations)
            
        except Exception as e:
            print(f"推薦過程發生錯誤: {str(e)}")
            return []

    def _collaborative_recommendations(self, user_id, num_recommendations):
        """協同過濾推薦"""
        recommendations = []
        recommended_ids = set()
        processed_cities = set()
        
        # 計算用戶相似度
        user_vector = self.train_user_restaurant_matrix.loc[user_id].values.reshape(1, -1)
        user_similarities = cosine_similarity(
            user_vector,
            self.train_user_restaurant_matrix.values
        )[0]
        
        similar_indices = user_similarities.argsort()[::-1]
        
        # 從相似用戶中獲取推薦
        for similar_user_idx in similar_indices[:30]:
            if len(recommendations) >= num_recommendations:
                break
            
            similar_user_id = self.train_user_restaurant_matrix.index[similar_user_idx]
            similar_user_ratings = self.train_data[self.train_data['user_id'] == similar_user_id]
            
            for _, row in similar_user_ratings.iterrows():
                restaurant_id = row['place_id']
                if restaurant_id not in recommended_ids:
                    restaurant_info = self.restaurants_df[
                        self.restaurants_df['place_id'] == restaurant_id
                    ]
                    if not restaurant_info.empty:
                        city = restaurant_info['city'].values[0]
                        if city not in processed_cities:
                            recommendations.append((
                                restaurant_info['place_names'].values[0],
                                float(restaurant_info['latitude'].values[0]),
                                float(restaurant_info['longitude'].values[0]),
                                restaurant_info['redirection_url'].values[0],
                                restaurant_info['navigation_url'].values[0],
                                city,
                                float(row['distance']),
                                float(row['rating']),
                                int(row['review_number'])
                            ))
                            recommended_ids.add(restaurant_id)
                            processed_cities.add(city)
                            
                            if len(recommendations) >= num_recommendations:
                                break
        
        return recommendations

    def _content_recommendations(self, user_id, num_recommendations):
        """內容基礎推薦"""
        recommendations = []
        recommended_ids = set()
        processed_cities = set()
        
        # 預先獲取並整理所有餐廳的評分信息
        restaurant_ratings = {}
        for _, row in self.train_data.iterrows():
            restaurant_id = row['place_id']
            if restaurant_id not in restaurant_ratings:
                restaurant_ratings[restaurant_id] = {
                    'distance': float(row['distance']),
                    'rating': float(row['rating']),
                    'review_number': int(row['review_number'])
                }
        
        # 隨機打亂所有餐廳並按城市分組
        all_restaurants = self.restaurants_df.sample(frac=1).to_dict('records')
        city_restaurants = {}
        for restaurant in all_restaurants:
            city = restaurant['city']
            if city not in city_restaurants:
                city_restaurants[city] = []
            city_restaurants[city].append(restaurant)
        
        # 第一輪：從不同城市選擇餐廳
        cities = list(city_restaurants.keys())
        random.shuffle(cities)
        
        for city in cities:
            if len(recommendations) >= num_recommendations:
                break
            
            if city not in processed_cities:
                available_restaurants = [
                    r for r in city_restaurants[city]
                    if r['place_id'] not in recommended_ids
                ]
                
                if available_restaurants:
                    restaurant = random.choice(available_restaurants)
                    restaurant_id = restaurant['place_id']
                    rating_info = restaurant_ratings.get(restaurant_id)
                    
                    if rating_info:
                        recommendations.append((
                            restaurant['place_names'],
                            float(restaurant['latitude']),
                            float(restaurant['longitude']),
                            restaurant['redirection_url'],
                            restaurant['navigation_url'],
                            city,
                            rating_info['distance'],
                            rating_info['rating'],
                            rating_info['review_number']
                        ))
                        recommended_ids.add(restaurant_id)
                        processed_cities.add(city)
        
        # 第二輪：如果還不夠，從未推薦的餐廳中隨機補充
        while len(recommendations) < num_recommendations:
            random_idx = random.randint(0, len(self.restaurants_df) - 1)
            restaurant_info = self.restaurants_df.iloc[random_idx]
            city = restaurant_info['city']
            
            # 如果這個城市還沒被推薦過
            if city not in processed_cities:
                try:
                    recommendations.append((
                        restaurant_info['place_names'],
                        float(restaurant_info['latitude']),
                        float(restaurant_info['longitude']),
                        restaurant_info['redirection_url'],
                        restaurant_info['navigation_url'],
                        city,
                        float(row['distance']),
                        float(row['rating']),
                        int(row['review_number'])
                    ))
                    processed_cities.add(city)
                except (IndexError, KeyError):
                    continue
        
        return recommendations[:num_recommendations]

    def _hybrid_recommendations(self, user_id, num_recommendations):
        """混合推薦"""
        if user_id not in self.train_user_restaurant_matrix.index:
            print(f"{user_id}這筆資料在矩陣內找不到，要不換一筆試試?")
            return []
        else:
            # 用於存放城市數量
            city_count = {}
            
            # 取得協同過濾推薦餐廳
            cf_recommendations = self._collaborative_recommendations(user_id, num_recommendations)
            # 取得內容推薦餐廳
            content_recommendations = self._content_recommendations(user_id, num_recommendations)
            # 混合推薦餐廳結果
            all_recommendations = cf_recommendations + content_recommendations
            # 存放唯一的推薦結果
            unique_recommendations = []
            seen = set()
            
            for rec in all_recommendations:
                # 沒有推薦過的餐廳才進行推薦
                if rec not in seen:
                    # 取得所有城市
                    city = rec[5]  # 元組中的第6個元素是城市
                    # 確保每個城市推薦的餐廳不超過指定數量
                    if city_count.get(city, 0) < 1:
                        # 將元組轉換為字典格式
                        recommendation_dict = {
                            'name': rec[0],
                            'latitude': rec[1],
                            'longitude': rec[2],
                            'redirection_url': rec[3],
                            'navigation_url': rec[4],
                            'city': rec[5],
                            'distance': rec[6],
                            'rating': rec[7],
                            'review_number': rec[8]
                        }
                        unique_recommendations.append(recommendation_dict)
                        city_count[city] = city_count.get(city, 0) + 1
                    seen.add(rec)
            
            if len(unique_recommendations) > num_recommendations:
                unique_recommendations = random.sample(unique_recommendations, num_recommendations)
            
            return unique_recommendations[:num_recommendations]

    def create_recommend_data(self, data):
        """創建推薦數據"""
        return self.recommend_dao.create_recommend_data(data)