from models.recommend_data import RecommendData
from models.database import db
from sqlalchemy import text
import pandas as pd
from config.config import SQLALCHEMY_DATABASE_URI
from sqlalchemy import create_engine

class RecommendDAO:
    def __init__(self):
        self.engine = create_engine(SQLALCHEMY_DATABASE_URI)
    
    def get_ratings_data(self):
        """獲取評分資料集"""
        return pd.read_sql('''
            select r.place_id,r.restaurant_name,r.rating,r.composite_score,
            r.user,s.city,s.city_CN,s.distance,s.review_number
            from ratings r
            JOIN stores s ON s.id=r.id
            where confidence>=0.7 or confidence<= -0.7
            ORDER BY RAND()
        ''', con=self.engine)
    
    def get_restaurants_data(self):
        """獲取餐廳資料集"""
        return pd.read_sql('''
            select g.place_id,g.latitude,g.longitude,g.place_names,g.redirection_url,
            g.navigation_url,g.city,g.city_CN
            from googlemaps_info g
            JOIN ratings r ON r.place_id = g.place_id
            WHERE g.place_id is not null
        ''', con=self.engine)
    
    def create_recommend_data(self, data):
        """創建推薦數據"""
        recommend_data = RecommendData(**data)
        db.session.add(recommend_data)
        db.session.commit()
        return recommend_data
    
    def get_recommend_data_by_user(self, user_id):
        """根據用戶ID獲取推薦數據"""
        return RecommendData.query.filter_by(user_id=user_id).all() 