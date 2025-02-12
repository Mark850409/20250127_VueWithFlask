from typing import List, Optional
from models.favorite import Favorite
from models.store import Store
from models.user import User
from models.googlemaps_info import GoogleMapsInfo
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
            # 先檢查店家是否存在
            store = Store.query.get(store_id)
            if not store:
                raise ValueError('店家不存在')
            
            # 檢查是否已經收藏
            existing = self.dao.check_exists(user_id, store_id)
            if existing:
                raise ValueError('已經收藏過此店家')
            
            # 獲取用戶資訊
            user = User.query.get(user_id)
            if not user:
                raise ValueError('用戶不存在')
            
            # 獲取 Google Maps 資訊
            maps_info = GoogleMapsInfo.query.filter_by(id=store_id).first()
            navigation_url = maps_info.navigation_url if maps_info else None
            
            # 創建收藏資料
            favorite_data = {
                'user_id': user_id,
                'store_id': store_id,
                'store_name': store.name,
                'store_image': store.hero_image,
                'address': store.address,
                'city': store.city,
                'city_CN': store.city_CN,
                'customer_phone': store.customer_phone,
                'description': store.description,
                'is_new_until': store.is_new_until,
                'redirection_url': store.redirection_url,
                'navigation_url': navigation_url,
                'rating': store.rating,
                'review_number': store.review_number,
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
    
    def check_favorite_status(self, user_id: int, store_id: int) -> dict:
        """檢查最愛狀態"""
        try:
            logger.info(f"[Service] 開始檢查最愛狀態: user_id={user_id}, store_id={store_id}")
            favorite = self.dao.check_exists(user_id, store_id)
            
            if favorite:
                logger.info(f"[Service] 找到收藏記錄: id={favorite.id}, store_id={favorite.store_id}")
                return {
                    'is_favorite': True,
                    'favorite_id': favorite.id
                }
                
            logger.info(f"[Service] 未找到收藏記錄: user_id={user_id}, store_id={store_id}")
            return {
                'is_favorite': False,
                'favorite_id': None
            }
        except Exception as e:
            logger.error(f"檢查最愛狀態錯誤: {str(e)}", exc_info=True)
            raise 