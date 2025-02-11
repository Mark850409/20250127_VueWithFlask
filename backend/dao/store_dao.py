from typing import List, Optional
from models.store import Store, db
from sqlalchemy import desc, asc
from datetime import datetime
from schemas.store_schema import SortField, SortOrder

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
    
    @staticmethod
    def get_stores_with_params(
        limit: Optional[int] = None,
        sort_by: SortField = SortField.DEFAULT,
        order: SortOrder = SortOrder.DESC,
        city: Optional[str] = None
    ) -> List[Store]:
        """獲取排序後的店家列表"""
        query = Store.query

        # 添加城市過濾
        if city:
            query = query.filter(
                # 同時匹配中文或英文城市名
                (Store.city_CN == city) | (Store.city == city)
            )

        # 根據排序欄位和方向進行排序
        if sort_by != SortField.DEFAULT:
            # 使用 review_number 替代 views
            sort_column = getattr(Store, sort_by.value)
            if order == SortOrder.DESC:
                query = query.order_by(desc(sort_column))
            else:
                query = query.order_by(asc(sort_column))
        else:
            query = query.order_by(desc(Store.created_at))

        # 限制返回筆數
        if limit:
            query = query.limit(limit)

        return query.all()

    def get_stores_with_params(self, limit=None, sort_by=None, order='desc', city=None):
        """根據參數獲取店家列表"""
        query = self.db.session.query(Store)
        
        if city:
            query = query.filter(Store.city_CN == city)
            
        if sort_by:
            if sort_by == 'rating':
                query = query.order_by(desc(Store.rating) if order == 'desc' else asc(Store.rating))
            elif sort_by == 'review_number':
                query = query.order_by(desc(Store.review_number) if order == 'desc' else asc(Store.review_number))
            elif sort_by == 'distance':
                # 距離排序在前端處理
                pass
            
        if limit:
            query = query.limit(limit)
            
        return query.all() 