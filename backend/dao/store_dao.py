from typing import List, Optional
from models.store import Store, db
from sqlalchemy import desc

class StoreDAO:
    @staticmethod
    def get_all_stores() -> List[Store]:
        """獲取所有店家"""
        return Store.query.order_by(desc(Store.created_at)).all()
    
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
        store = Store.query.get(store_id)
        if store and store.status != 'deleted':
            for key, value in store_data.items():
                setattr(store, key, value)
            db.session.commit()
        return store
    
    @staticmethod
    def delete_store(store_id: int) -> bool:
        """刪除店家（實體刪除）"""
        store = Store.query.get(store_id)
        if store:
            db.session.delete(store)
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def increment_views(store_id: int) -> bool:
        """增加瀏覽次數"""
        store = Store.query.get(store_id)
        if store and store.status != 'deleted':
            store.views += 1
            db.session.commit()
            return True
        return False 