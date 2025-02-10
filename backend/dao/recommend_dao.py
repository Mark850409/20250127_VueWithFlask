from models.recommend_data import RecommendData, db
from models.database import db
from sqlalchemy import text
import pandas as pd
from config.config import SQLALCHEMY_DATABASE_URI
from sqlalchemy import create_engine
from typing import Dict, Any

class RecommendDAO:
    def __init__(self):
        self.engine = create_engine(SQLALCHEMY_DATABASE_URI)
    
    def get_ratings_data(self):
        """獲取評分資料集"""
        return pd.read_sql('''
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
        ''', con=self.engine)
    
    def get_restaurants_data(self):
        """獲取餐廳資料集"""
        return pd.read_sql('''
            select g.place_id,g.latitude,g.longitude,g.place_names as name,g.redirection_url,
            g.navigation_url,g.city,g.city_CN
            from googlemaps_info g
            JOIN ratings r ON r.place_id = g.place_id
            ORDER BY RAND()
        ''', con=self.engine)
    
    def create_recommend_data(self, data: Dict[str, Any]) -> bool:
        """創建推薦數據"""
        try:
            recommend = RecommendData(**data)
            db.session.add(recommend)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print(f"保存推薦數據失敗: {str(e)}")
            return False
    
    def get_recommend_data_by_user(self, user_id):
        """根據用戶ID獲取推薦數據"""
        return RecommendData.query.filter_by(user_id=user_id).all() 