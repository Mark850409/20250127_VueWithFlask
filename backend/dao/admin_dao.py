import logging
from typing import List, Optional
from models.admin import Admin, db
from werkzeug.security import generate_password_hash
from datetime import datetime
import pytz

logger = logging.getLogger(__name__)
tw_tz = pytz.timezone('Asia/Taipei')

class AdminDAO:
    @staticmethod
    def get_all_admins() -> List[Admin]:
        """獲取所有管理員"""
        try:
            return Admin.query.all()
        except Exception as e:
            logger.error(f"DAO層獲取管理員列表錯誤: {str(e)}", exc_info=True)
            raise
    
    @staticmethod
    def get_admin_by_id(admin_id: int) -> Optional[Admin]:
        """根據ID獲取管理員"""
        return Admin.query.get(admin_id)
    
    @staticmethod
    def get_admin_by_email(email: str) -> Optional[Admin]:
        """根據郵箱獲取管理員"""
        return Admin.query.filter_by(email=email).first()
    
    @staticmethod
    def create_admin(admin_data: dict) -> Admin:
        """創建管理員"""
        # 加密密碼
        admin_data['password'] = generate_password_hash(admin_data['password'])
        admin = Admin(**admin_data)
        db.session.add(admin)
        db.session.commit()
        return admin
    
    @staticmethod
    def update_admin(admin_id: int, admin_data: dict) -> Optional[Admin]:
        """更新管理員"""
        admin = Admin.query.get(admin_id)
        if admin:
            # 如果有密碼更新，需要加密
            if 'password' in admin_data and admin_data['password']:
                admin_data['password'] = generate_password_hash(admin_data['password'])
            
            for key, value in admin_data.items():
                setattr(admin, key, value)
            db.session.commit()
        return admin
    
    @staticmethod
    def delete_admin(admin_id: int) -> bool:
        """刪除管理員"""
        admin = Admin.query.get(admin_id)
        if admin:
            db.session.delete(admin)
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def update_login_time(admin_id: int) -> bool:
        """更新登入時間"""
        admin = Admin.query.get(admin_id)
        if admin:
            admin.last_login = datetime.now(tw_tz)
            db.session.commit()
            return True
        return False 