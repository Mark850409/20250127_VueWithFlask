import logging
from typing import List, Optional
from models.admin import Admin
from dao.admin_dao import AdminDAO

logger = logging.getLogger(__name__)

class AdminService:
    def __init__(self):
        self.dao = AdminDAO()
    
    def get_all_admins(self) -> List[Admin]:
        """獲取所有管理員"""
        try:
            return self.dao.get_all_admins()
        except Exception as e:
            logger.error(f"Service層獲取管理員列表錯誤: {str(e)}", exc_info=True)
            raise
    
    def get_admin(self, admin_id: int) -> Optional[Admin]:
        """獲取指定管理員"""
        return self.dao.get_admin_by_id(admin_id)
    
    def create_admin(self, admin_data: dict) -> Admin:
        """創建管理員"""
        # 檢查郵箱是否已存在
        if self.dao.get_admin_by_email(admin_data['email']):
            raise ValueError('郵箱已被使用')
        return self.dao.create_admin(admin_data)
    
    def update_admin(self, admin_id: int, admin_data: dict) -> Optional[Admin]:
        """更新管理員"""
        admin = self.dao.get_admin_by_id(admin_id)
        if not admin:
            raise ValueError('管理員不存在')
            
        # 如果更新郵箱，檢查是否已被使用
        if 'email' in admin_data and admin_data['email'] != admin.email:
            if self.dao.get_admin_by_email(admin_data['email']):
                raise ValueError('郵箱已被使用')
                
        return self.dao.update_admin(admin_id, admin_data)
    
    def delete_admin(self, admin_id: int) -> bool:
        """刪除管理員"""
        admin = self.dao.get_admin_by_id(admin_id)
        if not admin:
            raise ValueError('管理員不存在')
        if admin.role == 'super_admin':
            raise ValueError('無法刪除超級管理員')
            
        return self.dao.delete_admin(admin_id)
    
    def update_login_time(self, admin_id: int) -> bool:
        """更新登入時間"""
        return self.dao.update_login_time(admin_id) 