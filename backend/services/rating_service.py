from typing import List, Optional
from models.rating import Rating
from dao.rating_dao import RatingDAO
from dao.store_dao import StoreDAO
from models.database import db

class RatingService:
    def __init__(self):
        self.dao = RatingDAO()
        self.store_dao = StoreDAO()
    
    def get_store_ratings(self, place_id: str) -> List[Rating]:
        """獲取店家的所有評分"""
        return Rating.query.filter_by(place_id=place_id).all()
    
    def get_user_ratings(self, user_id: int) -> List[Rating]:
        """獲取用戶的所有評分"""
        return self.dao.get_user_ratings(user_id)
    
    def get_rating(self, rating_id: int) -> Optional[Rating]:
        """獲取指定評分"""
        return Rating.query.get(rating_id)
    
    def create_rating(self, rating_data: dict) -> Rating:
        """創建新評分
        
        Args:
            rating_data (dict): 評分數據，包含以下字段：
                place_id: str
                restaurant_name: str
                user: str
                rating: float
                text: Optional[str]
                english_texts: Optional[str]
                time: Optional[str]
                positive_prob: Optional[float]
                negative_prob: Optional[float]
                composite_score: Optional[float]
                confidence: Optional[float]
                keywords_scores: Optional[float]
                sentiment: Optional[str]
                hash: str
        
        Returns:
            Rating: 創建的評分對象
        """
        try:
            rating = Rating(**rating_data)
            db.session.add(rating)
            db.session.commit()
            return rating
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"創建評分失敗: {str(e)}")
    
    def update_rating(self, rating_id: int, rating_data: dict) -> Optional[Rating]:
        """更新評分"""
        rating = Rating.query.get(rating_id)
        if rating:
            try:
                for key, value in rating_data.items():
                    setattr(rating, key, value)
                db.session.commit()
                return rating
            except Exception as e:
                db.session.rollback()
                raise ValueError(f"更新評分失敗: {str(e)}")
        return None
    
    def delete_rating(self, rating_id: int) -> bool:
        """刪除評分"""
        rating = Rating.query.get(rating_id)
        if rating:
            try:
                db.session.delete(rating)
                db.session.commit()
                return True
            except Exception as e:
                db.session.rollback()
                raise ValueError(f"刪除評分失敗: {str(e)}")
        return False
    
    def get_all_ratings(self):
        """獲取所有評分"""
        return self.dao.get_all_ratings() 