from typing import List, Optional
from models.rating import Rating, db
from sqlalchemy import desc

class RatingDAO:
    @staticmethod
    def get_store_ratings(store_id: int) -> List[Rating]:
        """獲取店家的所有評分"""
        return Rating.query.filter_by(store_id=store_id).all()
    
    @staticmethod
    def get_user_ratings(user_id: int) -> List[Rating]:
        """獲取用戶的所有評分"""
        return Rating.query.filter(
            Rating.user_id == user_id,
            Rating.status == 'active'
        ).order_by(desc(Rating.created_at)).all()
    
    @staticmethod
    def get_rating(rating_id: int) -> Optional[Rating]:
        """獲取指定評分"""
        return Rating.query.get(rating_id)
    
    @staticmethod
    def get_user_store_rating(user_id: int, store_id: int) -> Optional[Rating]:
        """獲取用戶對指定店家的評分"""
        return Rating.query.filter(
            Rating.user_id == user_id,
            Rating.store_id == store_id
        ).first()
    
    @staticmethod
    def create_rating(rating_data: dict) -> Rating:
        """創建評分"""
        rating = Rating(**rating_data)
        db.session.add(rating)
        db.session.commit()
        return rating
    
    @staticmethod
    def update_rating(rating_id: int, rating_data: dict) -> Optional[Rating]:
        """更新評分"""
        rating = Rating.query.get(rating_id)
        if rating:
            for key, value in rating_data.items():
                setattr(rating, key, value)
            db.session.commit()
        return rating
    
    @staticmethod
    def delete_rating(rating_id: int) -> bool:
        """刪除評分（實際刪除）"""
        rating = Rating.query.get(rating_id)
        if rating:
            db.session.delete(rating)  # 實際從數據庫中刪除
            db.session.commit()
            return True
        return False 