from typing import List, Optional
from models.favorite import Favorite, db
from datetime import datetime
import pytz

tw_tz = pytz.timezone('Asia/Taipei')

class FavoriteDAO:
    @staticmethod
    def get_all_favorites() -> List[Favorite]:
        """獲取所有最愛"""
        return Favorite.query.all()
    
    @staticmethod
    def get_user_favorites(user_id: int) -> List[Favorite]:
        """獲取用戶的所有最愛"""
        return Favorite.query.filter_by(user_id=user_id).all()
    
    @staticmethod
    def get_favorite_by_id(favorite_id: int) -> Optional[Favorite]:
        """根據ID獲取最愛"""
        return Favorite.query.get(favorite_id)
    
    @staticmethod
    def create_favorite(favorite_data: dict) -> Favorite:
        """創建最愛"""
        favorite = Favorite(**favorite_data)
        db.session.add(favorite)
        db.session.commit()
        return favorite
    
    @staticmethod
    def delete_favorite(favorite_id: int) -> bool:
        """刪除最愛"""
        favorite = Favorite.query.get(favorite_id)
        if favorite:
            db.session.delete(favorite)
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def check_exists(user_id: int, store_id: int) -> bool:
        """檢查是否已收藏"""
        return Favorite.query.filter_by(
            user_id=user_id,
            store_id=store_id
        ).first() is not None 