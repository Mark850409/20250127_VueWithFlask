from typing import List, Optional
from models.store import Store
from dao.store_dao import StoreDAO
from schemas.store_schema import SortField, SortOrder
from sqlalchemy import desc, asc
import logging

logger = logging.getLogger(__name__)

class StoreService:
    def __init__(self):
        self.dao = StoreDAO()
    
    def get_all_stores(self) -> List[Store]:
        """獲取所有店家"""
        return self.dao.get_all_stores()
    
    def get_store(self, store_id: int) -> Optional[Store]:
        """獲取指定店家"""
        return self.dao.get_store_by_id(store_id)
    
    def get_stores_by_city(self, city: str) -> List[Store]:
        """獲取指定城市的店家"""
        return self.dao.get_stores_by_city(city)
    
    def create_store(self, store_data: dict) -> Store:
        """創建店家"""
        return self.dao.create_store(store_data)
    
    def update_store(self, store_id: int, store_data: dict) -> Optional[Store]:
        """更新店家信息"""
        try:
            store = self.dao.get_store_by_id(store_id)
            if not store:
                raise ValueError('店家不存在')
            
            # 直接傳遞 store_id 和 data 到 dao 層
            return self.dao.update_store(store_id, store_data)
        except Exception as e:
            raise Exception(f'更新店家失敗: {str(e)}')
    
    def delete_store(self, store_id: int) -> bool:
        """刪除店家"""
        return self.dao.delete_store(store_id)
    
    def view_store(self, store_id: int) -> bool:
        """瀏覽店家（增加瀏覽次數）"""
        try:
            store = self.dao.get_store_by_id(store_id)
            if not store:
                raise ValueError('店家不存在')
            return self.dao.increment_views(store_id)
        except Exception as e:
            raise Exception(f'瀏覽店家失敗: {str(e)}')
    
    def get_stores_with_params(
        self,
        limit: Optional[int] = None,
        sort_by: SortField = SortField.DEFAULT,
        order: SortOrder = SortOrder.DESC,
        city: Optional[str] = None
    ) -> List[Store]:
        """獲取排序後的店家列表"""
        try:
            query = Store.query

            if city:
                query = query.filter(Store.city_CN == city)

            # 根據排序參數設置排序
            if sort_by == SortField.RATING:
                query = query.order_by(desc(Store.rating) if order == SortOrder.DESC else asc(Store.rating))
            elif sort_by == SortField.REVIEW_NUMBER:
                query = query.order_by(desc(Store.review_number) if order == SortOrder.DESC else asc(Store.review_number))
            elif sort_by == SortField.DISTANCE:
                # 距離排序在前端處理，這裡返回未排序的結果
                pass
            elif sort_by == SortField.DEFAULT:
                query = query.order_by(desc(Store.rating))

            stores = query.limit(limit).all()
            return stores
        except Exception as e:
            logger.error(f"獲取店家列表失敗: {str(e)}")
            raise 