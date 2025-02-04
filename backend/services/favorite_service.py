from typing import List, Optional
from models.favorite import Favorite
from models.store import Store
from models.user import User
from dao.favorite_dao import FavoriteDAO
import logging

logger = logging.getLogger(__name__)

class FavoriteService:
    def __init__(self):
        self.dao = FavoriteDAO()
    
    def get_all_favorites(self) -> List[Favorite]:
        """獲取所有最愛"""
        return self.dao.get_all_favorites()
    
    def get_user_favorites(self, user_id: int) -> List[Favorite]:
        """獲取用戶的所有最愛"""
        try:
            return self.dao.get_user_favorites(user_id)
        except Exception as e:
            logger.error(f"獲取用戶最愛列表錯誤: {str(e)}", exc_info=True)
            raise
    
    def create_favorite(self, user_id: int, store_id: int) -> Favorite:
        """創建最愛"""
        try:
            # 檢查店家是否存在
            store = Store.query.get(store_id)
            if not store:
                raise ValueError('店家不存在')
                
            # 檢查是否已收藏
            if self.dao.check_exists(user_id, store_id):
                raise ValueError('已收藏此店家')
                
            # 獲取用戶資訊
            user = User.query.get(user_id)
            if not user:
                raise ValueError('用戶不存在')
            
            favorite_data = {
                'user_id': user_id,
                'store_id': store_id,
                'store_name': store.name,
                'store_image': store.hero_image,
                'username': user.username
            }
            
            return self.dao.create_favorite(favorite_data)
        except Exception as e:
            logger.error(f"創建收藏錯誤: {str(e)}", exc_info=True)
            raise
    
    def delete_favorite(self, favorite_id: int, user_id: int) -> bool:
        """刪除最愛"""
        try:
            # 獲取收藏記錄
            favorite = self.dao.get_favorite_by_id(favorite_id)
            if not favorite:
                raise ValueError('收藏不存在')
                
            # 檢查是否為當前用戶的收藏
            logger.info(f"檢查權限: favorite.user_id={favorite.user_id}, user_id={user_id}")
            if str(favorite.user_id) != str(user_id):  # 轉換為字符串比較
                raise ValueError('無權限刪除此收藏')
                
            return self.dao.delete_favorite(favorite_id)
        except Exception as e:
            logger.error(f"刪除最愛錯誤: {str(e)}", exc_info=True)
            raise 