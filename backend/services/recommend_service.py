from dao.recommend_dao import RecommendDAO
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd
import random
import traceback

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
        ratings_data = {
            'user_id': self.ratings_df['user_id'],
            'place_id': self.ratings_df['place_id'],
            'restaurant_name': self.ratings_df['restaurant_name'],
            'rating': self.ratings_df['rating'],  # 使用用戶評分
            'composite_score': self.ratings_df['composite_score']
        }
        self.ratings_df = pd.DataFrame(ratings_data)

        # 建立餐廳資料集
        restaurants_data = {
            'place_id': self.restaurants_df['place_id'],
            'latitude': self.restaurants_df['latitude'],
            'longitude': self.restaurants_df['longitude'],
            'name': self.restaurants_df['place_names'],
            'redirection_url': self.restaurants_df['redirection_url'],
            'navigation_url': self.restaurants_df['navigation_url'],
            'city': self.restaurants_df['city'],
            'city_CN': self.restaurants_df['city_CN'],
            'hero_image': self.restaurants_df['hero_image'],
            'hero_listing_image': self.restaurants_df['hero_listing_image'],
            'tag': self.restaurants_df['tag'],
            'is_new_until': self.restaurants_df['is_new_until'],
            'review_number': self.restaurants_df['review_number'],
            'distance': self.restaurants_df['distance'],
            'rating': self.restaurants_df['rating'],
            'description': self.restaurants_df['description']
        }
        self.restaurants_df = pd.DataFrame(restaurants_data)
        
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
        """獲取混合推薦結果"""
        try:
            if user_id not in self.train_user_restaurant_matrix.index:
                print(f"{user_id}這筆資料在矩陣內找不到，要不換一筆試試?")
                return []
            
            # 返回混合推薦結果
            return self._hybrid_recommendations(user_id, num_recommendations)
            
        except Exception as e:
            print(f"獲取混合推薦過程發生錯誤: {str(e)}")
            traceback.print_exc()
            return []

    def get_collaborative_recommendations(self, user_id, num_recommendations=5):
        """獲取協同過濾推薦結果"""
        try:
            if user_id not in self.train_user_restaurant_matrix.index:
                print(f"{user_id}這筆資料在矩陣內找不到，要不換一筆試試?")
                return []
            
            # 返回混合推薦結果
            return self._collaborative_recommendations(user_id, num_recommendations)
            
        except Exception as e:
            print(f"獲取協同過濾推薦過程發生錯誤: {str(e)}")
            traceback.print_exc()
            return []

    def get_content_recommendations(self, user_id, num_recommendations=5):
        """獲取內容推薦結果"""
        try:
            if user_id not in self.train_user_restaurant_matrix.index:
                print(f"{user_id}這筆資料在矩陣內找不到，要不換一筆試試?")
                return []
            
            # 返回混合推薦結果
            return self._content_recommendations(user_id, num_recommendations)
            
        except Exception as e:
            print(f"獲取內容推薦過程發生錯誤: {str(e)}")
            traceback.print_exc()
            return []

    def _collaborative_recommendations(self, user_id, num_recommendations):
        """協同過濾推薦 - 使用純評分"""
        try:
            if user_id not in self.train_user_restaurant_matrix.index:
                return []
            
            user_vector = self.train_user_restaurant_matrix.loc[user_id].values.reshape(1, -1)
            if np.all(user_vector == 0):
                return []
                
            # 修改：使用純評分進行排序
            self.train_data['weighted_combined_score'] = self.train_data['rating']
            
            # 重新建立評分矩陣
            self.train_user_restaurant_matrix = self.train_data.pivot_table(
                index='user_id',
                columns='place_id',
                values='weighted_combined_score'
            ).fillna(0)
            
            # 計算相似度
            distances, similar_indices = self.calculate_user_similarity(
                user_vector, 
                self.train_user_restaurant_matrix.values
            )
            
            # 排除自己
            user_idx = self.train_user_restaurant_matrix.index.get_loc(user_id)
            similar_indices = similar_indices[similar_indices != user_idx]
            
            # 選擇更多的相似用戶
            num_similar_users = min(500, len(similar_indices))
            selected_similar_users = similar_indices[:num_similar_users]
            random.shuffle(selected_similar_users)
            
            # 收集所有可能的推薦
            all_recommendations = []
            recommended_ids = set()
            processed_cities = set()
            
            # 從相似用戶收集推薦
            for similar_user_idx in selected_similar_users:
                if distances[similar_user_idx] > 0.8:  # 相似度閾值
                    continue
                    
                similar_user_id = self.train_user_restaurant_matrix.index[similar_user_idx]
                similar_user_ratings = self.train_data[self.train_data['user_id'] == similar_user_id]
                
                for _, row in similar_user_ratings.iterrows():
                    restaurant_id = row['place_id']
                    if restaurant_id not in recommended_ids:
                        # 使用 place_id 查找餐廳資訊
                        restaurant_info = self.restaurants_df[
                            self.restaurants_df['place_id'] == restaurant_id
                        ].iloc[0] if not self.restaurants_df[
                            self.restaurants_df['place_id'] == restaurant_id
                        ].empty else None
                        
                        if restaurant_info is not None:
                            all_recommendations.append((
                                restaurant_info,
                                restaurant_id
                            ))
            
            # 打亂所有推薦
            random.shuffle(all_recommendations)
            
            # 用於存放推薦結果
            recommended_restaurants = []
            
            # 第一輪：優先選擇不同城市的餐廳
            for rec in all_recommendations:
                if len(recommended_restaurants) >= num_recommendations:
                    break
                    
                restaurant_info, restaurant_id = rec
                city = restaurant_info['city']
                
                # 限制每個城市最多推薦1家餐廳
                if city not in processed_cities:
                    recommended_restaurants.append({
                        'name': restaurant_info['name'],
                        'latitude': float(restaurant_info['latitude']),
                        'longitude': float(restaurant_info['longitude']),
                        'redirection_url': restaurant_info['redirection_url'],
                        'navigation_url': restaurant_info['navigation_url'],
                        'city': city,
                        'city_CN': restaurant_info['city_CN'],
                        'distance': float(restaurant_info['distance']),
                        'rating': float(restaurant_info['rating']),
                        'review_number': int(restaurant_info['review_number']),
                        'hero_image': restaurant_info['hero_image'],
                        'hero_listing_image': restaurant_info['hero_listing_image'],
                        'tag': restaurant_info['tag'],
                        'is_new_until': restaurant_info['is_new_until'],
                        'description': restaurant_info['description']
                    })
                    recommended_ids.add(restaurant_id)
                    processed_cities.add(city)
            
            # 第二輪：如果還不夠，不限制城市數量
            if len(recommended_restaurants) < num_recommendations:
                remaining_recommendations = [
                    rec for rec in all_recommendations 
                    if rec[1] not in recommended_ids
                ]
                random.shuffle(remaining_recommendations)
                
                for rec in remaining_recommendations:
                    if len(recommended_restaurants) >= num_recommendations:
                        break
                        
                    restaurant_info, restaurant_id = rec
                    recommended_restaurants.append({
                        'name': restaurant_info['name'],
                        'latitude': float(restaurant_info['latitude']),
                        'longitude': float(restaurant_info['longitude']),
                        'redirection_url': restaurant_info['redirection_url'],
                        'navigation_url': restaurant_info['navigation_url'],
                        'city': restaurant_info['city'],
                        'city_CN': restaurant_info['city_CN'],
                        'distance': float(restaurant_info['distance']),
                        'rating': float(restaurant_info['rating']),
                        'review_number': int(restaurant_info['review_number']),
                        'hero_image': restaurant_info['hero_image'],
                        'hero_listing_image': restaurant_info['hero_listing_image'],
                        'tag': restaurant_info['tag'],
                        'is_new_until': restaurant_info['is_new_until'],
                        'description': restaurant_info['description']
                    })
                    recommended_ids.add(restaurant_id)
            
            return recommended_restaurants[:num_recommendations]
            
        except Exception as e:
            print(f"協同過濾推薦過程發生錯誤: {str(e)}")
            traceback.print_exc()
            return []

    def _content_recommendations(self, user_id, num_recommendations):
        """內容推薦 - 使用純情感分數"""
        try:
            if user_id not in self.train_user_restaurant_matrix.index:
                return []
            
            # 獲取用戶向量並檢查是否有評分
            user_vector = self.train_user_restaurant_matrix.loc[user_id].values.reshape(1, -1)
            if np.all(user_vector == 0):
                return []
            
            # 修改：使用純情感分數進行排序
            self.train_data['weighted_combined_score'] = self.train_data['composite_score']
            
            # 重新建立評分矩陣
            self.train_user_restaurant_matrix = self.train_data.pivot_table(
                index='user_id',
                columns='place_id',
                values='weighted_combined_score'
            ).fillna(0)
            
            # 獲取用戶的歷史評分
            user_ratings = self.train_data[self.train_data['user_id'] == user_id]
            rated_restaurants = set(user_ratings.index)
            
            # 預先過濾有評分資訊的餐廳
            valid_restaurants = []
            for idx, restaurant in self.restaurants_df.iterrows():
                if idx not in rated_restaurants:
                    valid_restaurants.append(idx)
            
            # 隨機選擇有效的餐廳索引
            num_random_restaurants = min(100, len(valid_restaurants))
            if num_random_restaurants == 0:
                return []
            
            random_indices = random.sample(valid_restaurants, num_random_restaurants)
            
            # 收集所有可能的推薦
            all_recommendations = []
            recommended_ids = set()
            processed_cities = set()
            
            # 第一輪：嘗試找到不同城市的推薦
            for idx in random_indices:
                if len(recommended_ids) >= num_recommendations * 2:  # 收集更多候選
                    break
                    
                restaurant_info = self.restaurants_df.iloc[idx]
                city = restaurant_info['city']
                
                # 確保城市不重複且未處理過
                if city not in processed_cities:
                    all_recommendations.append((
                        restaurant_info,
                        idx
                    ))
                    recommended_ids.add(idx)
                    processed_cities.add(city)
            
            # 打亂所有推薦
            random.shuffle(all_recommendations)
            
            # 用於存放推薦結果
            recommended_restaurants = []
            processed_cities.clear()  # 重置已處理城市集合
            
            # 第一輪：優先選擇不同城市的餐廳
            for rec in all_recommendations:
                if len(recommended_restaurants) >= num_recommendations:
                    break
                    
                restaurant_info, restaurant_id = rec
                city = restaurant_info['city']
                
                # 限制每個城市最多推薦1家餐廳
                if city not in processed_cities:
                    recommended_restaurants.append({
                        'name': restaurant_info['name'],
                        'latitude': float(restaurant_info['latitude']),
                        'longitude': float(restaurant_info['longitude']),
                        'redirection_url': restaurant_info['redirection_url'],
                        'navigation_url': restaurant_info['navigation_url'],
                        'city': city,
                        'city_CN': restaurant_info['city_CN'],
                        'distance': float(restaurant_info['distance']),
                        'rating': float(restaurant_info['rating']),
                        'review_number': int(restaurant_info['review_number']),
                        'hero_image': restaurant_info['hero_image'],
                        'hero_listing_image': restaurant_info['hero_listing_image'],
                        'tag': restaurant_info['tag'],
                        'is_new_until': restaurant_info['is_new_until'],
                        'description': restaurant_info['description']
                    })
                    processed_cities.add(city)
            
            # 如果推薦數量不足，從其他城市隨機補充
            while len(recommended_restaurants) < num_recommendations:
                # 獲取未處理的城市
                remaining_cities = list(set(self.restaurants_df['city'].unique()) - processed_cities)
                
                # 如果沒有未處理的城市，則重新使用所有城市
                if not remaining_cities:
                    remaining_cities = list(self.restaurants_df['city'].unique())
                    processed_cities.clear()  # 重置已處理城市集合
                
                # 隨機選擇一個城市
                city = random.choice(remaining_cities)
                
                # 獲取該城市所有有效的餐廳
                city_restaurants = []
                for idx in valid_restaurants:
                    restaurant = self.restaurants_df.iloc[idx]
                    if restaurant['city'] == city and idx not in recommended_ids:
                        city_restaurants.append(restaurant)
                
                if city_restaurants:
                    restaurant_info = random.choice(city_restaurants)
                    recommended_restaurants.append({
                        'name': restaurant_info['name'],
                        'latitude': float(restaurant_info['latitude']),
                        'longitude': float(restaurant_info['longitude']),
                        'redirection_url': restaurant_info['redirection_url'],
                        'navigation_url': restaurant_info['navigation_url'],
                        'city': city,
                        'city_CN': restaurant_info['city_CN'],
                        'distance': float(restaurant_info['distance']),
                        'rating': float(restaurant_info['rating']),
                        'review_number': int(restaurant_info['review_number']),
                        'hero_image': restaurant_info['hero_image'],
                        'hero_listing_image': restaurant_info['hero_listing_image'],
                        'tag': restaurant_info['tag'],
                        'is_new_until': restaurant_info['is_new_until'],
                        'description': restaurant_info['description']
                    })
                    processed_cities.add(city)
            
            return recommended_restaurants[:num_recommendations]
            
        except Exception as e:
            print(f"內容推薦過程發生錯誤: {str(e)}")
            traceback.print_exc()
            return []
    
    def _hybrid_recommendations(self, user_id, num_recommendations):
        """混合推薦 - 使用加權評分"""
        try:
            # 標準化評分和情感分數
            scaler = MinMaxScaler()
            self.train_data['normalized_rating'] = scaler.fit_transform(
                self.train_data[['rating']].values
            )
            self.train_data['normalized_sentiment'] = scaler.fit_transform(
                self.train_data[['composite_score']].values
            )
            
            # 計算加權分數 (70% 評分 + 30% 情感)
            self.train_data['weighted_combined_score'] = (
                0.7 * self.train_data['normalized_rating'] +
                0.3 * self.train_data['normalized_sentiment']
            )
            
            # 重新建立評分矩陣
            self.train_user_restaurant_matrix = self.train_data.pivot_table(
                index='user_id',
                columns='place_id',
                values='weighted_combined_score'
            ).fillna(0)
            
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
            seen_restaurants = set()
            
            for rec in all_recommendations:
                restaurant_name = rec['name']
                if restaurant_name not in seen_restaurants:
                    city = rec['city']
                    # 確保每個城市推薦的餐廳不超過指定數量
                    if city_count.get(city, 0) < 2:
                        recommendation = {
                            'name': rec['name'],
                            'latitude': rec['latitude'],
                            'longitude': rec['longitude'],
                            'redirection_url': rec['redirection_url'],
                            'navigation_url': rec['navigation_url'],
                            'city': city,
                            'city_CN': rec['city_CN'],
                            'distance': rec['distance'],
                            'rating': rec['rating'],
                            'review_number': rec['review_number'],
                            'hero_image': rec['hero_image'],
                            'hero_listing_image': rec['hero_listing_image'],
                            'tag': rec['tag'],
                            'is_new_until': rec['is_new_until'],
                            'description': rec['description']
                        }
                        unique_recommendations.append(recommendation)
                        city_count[city] = city_count.get(city, 0) + 1
                        seen_restaurants.add(restaurant_name)
            
            if len(unique_recommendations) > num_recommendations:
                unique_recommendations = random.sample(unique_recommendations, num_recommendations)
            
            return unique_recommendations[:num_recommendations]
            
        except Exception as e:
            print(f"混合推薦過程發生錯誤: {str(e)}")
            traceback.print_exc()
            return []

    def calculate_user_similarity(self, user_vector, matrix):
        """計算用戶相似度"""
        try:
            # 計算餐廳評分的餘弦相似度
            similarities = cosine_similarity(user_vector, matrix)[0]
            
            # 根據相似度排序並返回索引
            similar_indices = np.argsort(similarities)[::-1]
            
            return similarities, similar_indices
            
        except Exception as e:
            print(f"計算用戶相似度時發生錯誤: {str(e)}")
            traceback.print_exc()
            return [], []