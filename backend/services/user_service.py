from typing import List, Optional
from models.user import User
from dao.user_dao import UserDAO
from utils.password_util import hash_password
import bcrypt

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

    def register(self, user_data: dict) -> Optional[User]:
        """用戶註冊"""
        # 檢查郵箱是否已存在
        if self.dao.get_user_by_email(user_data['email']):
            raise ValueError('此郵箱已被註冊')

        # 檢查用戶名是否已存在
        if self.dao.get_user_by_username(user_data['username']):
            raise ValueError('此用戶名已被使用')

        # 密碼加密
        password = user_data['password'].encode('utf-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password, salt)
        user_data['password'] = hashed.decode('utf-8')

        return self.dao.create_user(user_data)

    def login(self, login_data: dict) -> Optional[User]:
        """用戶登入"""
        user = self.dao.get_user_by_email(login_data['email'])
        if not user:
            return None

        # 驗證密碼
        password = login_data['password'].encode('utf-8')
        if bcrypt.checkpw(password, user.password.encode('utf-8')):
            return user
        return None 