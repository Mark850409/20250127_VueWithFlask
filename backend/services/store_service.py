from typing import List, Optional
from models.store import Store
from dao.store_dao import StoreDAO

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
        # 驗證城市名稱格式
        if 'city' in store_data and not store_data['city'].endswith('市') and not store_data['city'].endswith('縣'):
            store_data['city'] = store_data['city'] + '市'
            
        return self.dao.create_store(store_data)
    
    def update_store(self, store_id: int, store_data: dict) -> Optional[Store]:
        """更新店家"""
        # 驗證城市名稱格式
        if 'city' in store_data and not store_data['city'].endswith('市') and not store_data['city'].endswith('縣'):
            store_data['city'] = store_data['city'] + '市'
            
        return self.dao.update_store(store_id, store_data)
    
    def delete_store(self, store_id: int) -> bool:
        """刪除店家"""
        return self.dao.delete_store(store_id)
    
    def view_store(self, store_id: int) -> bool:
        """瀏覽店家（增加瀏覽次數）"""
        return self.dao.increment_views(store_id) 