from typing import List, Optional
from models.user import User
from dao.user_dao import UserDAO
from utils.password_util import hash_password

class UserService:
    def __init__(self):
        self.dao = UserDAO()
    
    def get_all_users(self) -> List[User]:
        """獲取所有用戶"""
        return self.dao.get_all_users()
    
    def get_user(self, user_id: int) -> Optional[User]:
        """獲取指定用戶"""
        return self.dao.get_user_by_id(user_id)
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """根據用戶名獲取用戶"""
        return self.dao.get_user_by_username(username)
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """根據郵箱獲取用戶"""
        return self.dao.get_user_by_email(email)
    
    def create_user(self, user_data: dict) -> User:
        """創建用戶"""
        if 'password' in user_data:
            user_data['password'] = hash_password(user_data['password'])
        return self.dao.create_user(user_data)
    
    def update_user(self, user_id: int, user_data: dict) -> Optional[User]:
        """更新用戶"""
        if 'password' in user_data:
            user_data['password'] = hash_password(user_data['password'])
        return self.dao.update_user(user_id, user_data)
    
    def delete_user(self, user_id: int) -> bool:
        """刪除用戶"""
        return self.dao.delete_user(user_id) 