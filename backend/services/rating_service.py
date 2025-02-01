from typing import List, Optional
from models.rating import Rating
from dao.rating_dao import RatingDAO
from dao.store_dao import StoreDAO

class RatingService:
    def __init__(self):
        self.dao = RatingDAO()
        self.store_dao = StoreDAO()
    
    def get_store_ratings(self, store_id: int) -> List[Rating]:
        """獲取店家的所有評分"""
        return self.dao.get_store_ratings(store_id)
    
    def get_user_ratings(self, user_id: int) -> List[Rating]:
        """獲取用戶的所有評分"""
        return self.dao.get_user_ratings(user_id)
    
    def get_rating(self, rating_id: int) -> Optional[Rating]:
        """獲取指定評分"""
        return self.dao.get_rating(rating_id)
    
    def create_rating(self, user_id: int, rating_data: dict) -> Rating:
        """創建評分"""
        # 檢查店家是否存在
        store = self.store_dao.get_store_by_id(rating_data['store_id'])
        if not store:
            raise ValueError(f'店家不存在 (ID: {rating_data["store_id"]})')
        
        # 檢查用戶是否已經評分過此店家
        existing_rating = self.dao.get_user_store_rating(user_id, rating_data['store_id'])
        if existing_rating:
            raise ValueError('您已經評分過此店家')
        
        # 添加用戶ID和其他必要欄位
        rating_data['user_id'] = user_id
        rating_data['status'] = 'active'  # 如果需要的話
        
        return self.dao.create_rating(rating_data)
    
    def update_rating(self, user_id: int, rating_id: int, rating_data: dict) -> Optional[Rating]:
        """更新評分"""
        # 檢查評分是否存在且屬於該用戶
        rating = self.dao.get_rating(rating_id)
        if not rating:
            raise ValueError('評分不存在或已被刪除')
        if rating.user_id != user_id:
            raise ValueError('只能修改自己的評分')

        return self.dao.update_rating(rating_id, rating_data)
    
    def delete_rating(self, user_id: int, rating_id: int) -> bool:
        """刪除評分"""
        # 檢查評分是否存在且屬於該用戶
        rating = self.dao.get_rating(rating_id)
        if not rating:
            raise ValueError('評分不存在或已被刪除')
        if rating.user_id != user_id:
            raise ValueError('只能刪除自己的評分')

        return self.dao.delete_rating(rating_id) 