from typing import List, Optional
from models.store import Store, db
from sqlalchemy import desc
from datetime import datetime

class StoreDAO:
    @staticmethod
    def get_all_stores() -> List[Store]:
        """獲取所有店家"""
        return Store.query.all()
    
    @staticmethod
    def get_store_by_id(store_id: int) -> Optional[Store]:
        """根據ID獲取店家"""
        return Store.query.get(store_id)
    
    @staticmethod
    def get_stores_by_city(city: str) -> List[Store]:
        """根據城市獲取店家"""
        return Store.query.filter(Store.city == city).order_by(desc(Store.created_at)).all()
    
    @staticmethod
    def create_store(store_data: dict) -> Store:
        """創建店家"""
        store = Store(**store_data)
        db.session.add(store)
        db.session.commit()
        return store
    
    @staticmethod
    def update_store(store_id: int, store_data: dict) -> Optional[Store]:
        """更新店家"""
        try:
            store = Store.query.get(store_id)
            if store:
                # 更新每個提供的欄位
                for key, value in store_data.items():
                    if hasattr(store, key):  # 確保欄位存在
                        setattr(store, key, value)
                
                store.updated_at = datetime.utcnow()
                db.session.commit()
                db.session.refresh(store)
                return store
            return None
        except Exception as e:
            db.session.rollback()
            raise Exception(f'更新店家失敗: {str(e)}')
    
    @staticmethod
    def delete_store(store_id: int) -> bool:
        """刪除店家"""
        store = Store.query.get(store_id)
        if store:
            db.session.delete(store)
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def increment_views(store_id: int) -> bool:
        """增加瀏覽次數"""
        try:
            store = Store.query.get(store_id)
            if store:
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            raise Exception(f'更新瀏覽次數失敗: {str(e)}') 