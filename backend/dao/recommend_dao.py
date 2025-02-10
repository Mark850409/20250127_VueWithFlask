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
                r.user
            FROM ratings r
            ORDER BY RAND()
        ''', con=self.engine)
    
    def get_restaurants_data(self):
        """獲取餐廳資料集"""
        return pd.read_sql('''
            SELECT 
                g.place_id,
                g.latitude,
                g.longitude,
                g.place_names,
                g.redirection_url,
                g.navigation_url,
                g.city,
                g.city_CN,
                s.hero_image,
                s.hero_listing_image,
                s.tag,
                s.is_new_until,
                s.review_number,
                s.distance,
                s.rating,
                s.description
            FROM googlemaps_info g
            JOIN stores s ON s.id = g.id
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