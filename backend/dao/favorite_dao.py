from typing import List, Optional
from models.favorite import Favorite, db
from models.store import Store
from models.user import User
from datetime import datetime
import pytz
import logging

logger = logging.getLogger(__name__)
tw_tz = pytz.timezone('Asia/Taipei')

class FavoriteDAO:
    @staticmethod
    def get_all_favorites() -> List[Favorite]:
        """獲取所有最愛"""
        return Favorite.query.all()
    
    @staticmethod
    def get_user_favorites(user_id: int) -> List[Favorite]:
        """獲取用戶的所有最愛"""
        try:
            return (Favorite.query
                .filter_by(user_id=user_id)
                .order_by(Favorite.created_at.desc())
                .all())
        except Exception as e:
            logger.error(f"獲取用戶最愛列表錯誤: {str(e)}", exc_info=True)
            raise
    
    @staticmethod
    def get_favorite_by_id(favorite_id: int) -> Optional[Favorite]:
        """根據ID獲取最愛"""
        return Favorite.query.get(favorite_id)
    
    @staticmethod
    def create_favorite(favorite_data: dict) -> Favorite:
        """創建最愛"""
        try:
            favorite = Favorite(
                user_id=favorite_data['user_id'],
                store_id=favorite_data['store_id'],
                store_name=favorite_data['store_name'],
                store_image=favorite_data['store_image'],
                username=favorite_data['username']
            )
            db.session.add(favorite)
            db.session.commit()
            return favorite
        except Exception as e:
            db.session.rollback()
            logger.error(f"創建收藏錯誤: {str(e)}", exc_info=True)
            raise
    
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
        try:
            logger.info(f"檢查收藏: user_id={user_id}, store_id={store_id}")
            #print(f"檢查收藏: user_id={user_id}, store_id={store_id}")
            
            # 使用 query 和 filter_by 進行查詢
            result = Favorite.query.filter_by(
                user_id=user_id,
                store_id=store_id
            ).order_by(Favorite.created_at.desc()).first()
            
            if not result:
                # 如果找不到，嘗試查詢所有該用戶的收藏並打印出來
                all_favorites = Favorite.query.filter_by(
                    user_id=user_id
                ).order_by(Favorite.created_at.desc()).all()
                #print(f"該用戶所有收藏: {[(f.id, f.store_id, f.store_name) for f in all_favorites]}")

                # 再次確認 store_id 的類型和值
                #print(f"輸入的 store_id 類型: {type(store_id)}, 值: {store_id}")
                for fav in all_favorites:
                    print(f"資料庫中的 store_id 類型: {type(fav.store_id)}, 值: {fav.store_id}")

            logger.info(f"檢查結果: {result}")
            #print(f"檢查結果: {result}")
            db.session.commit()
            return result
        except Exception as e:
            db.session.rollback()
            logger.error(f"檢查收藏存在錯誤: {str(e)}", exc_info=True)
            raise 