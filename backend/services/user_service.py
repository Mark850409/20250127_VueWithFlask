from typing import List, Optional
from models.user import User
from dao.user_dao import UserDAO
from utils.password_util import hash_password
import bcrypt
import logging
from services.mail_service import MailService
from flask import current_app

logger = logging.getLogger(__name__)

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
    
    def update_user(self, user_id: int, data: dict):
        """更新用戶信息"""
        try:
            user = self.dao.get_user_by_id(user_id)
            if not user:
                raise ValueError('用戶不存在')
            
            # 直接傳遞 user_id 和 data 到 dao 層
            return self.dao.update_user(user_id, data)
        except Exception as e:
            raise Exception(f'更新用戶失敗: {str(e)}')
    
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

    def update_avatar(self, user_id: int, avatar_file) -> str:
        """更新用戶頭像"""
        try:
            # 驗證文件類型
            if not avatar_file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                raise ValueError('只支援 PNG、JPG 格式的圖片')
            
            # 驗證文件大小 (2MB)
            if len(avatar_file.read()) > 2 * 1024 * 1024:
                avatar_file.seek(0)  # 重置文件指針
                raise ValueError('圖片大小不能超過 2MB')
            
            avatar_file.seek(0)  # 重置文件指針
            return self.dao.update_avatar(user_id, avatar_file)
            
        except Exception as e:
            logger.error(f"更新頭像服務錯誤: {str(e)}", exc_info=True)
            raise 

    def request_password_reset(self, email: str) -> bool:
        """請求重設密碼"""
        try:
            user = self.dao.get_user_by_email(email)
            if not user:
                raise ValueError('找不到此 email 的用戶')

            # 生成重設密碼 token
            token = self.dao.create_reset_token(user)

            # 發送重設密碼郵件
            MailService.send_reset_password_email(user, token)

            return True
        except Exception as e:
            logger.error(f"請求重設密碼錯誤: {str(e)}")
            raise

    def reset_password(self, token: str, new_password: str) -> bool:
        """重設密碼"""
        try:
            # 驗證 token
            user = self.dao.verify_reset_token(token)
            if not user:
                raise ValueError('無效的重設密碼連結或已過期')

            # 檢查新密碼是否與歷史密碼重複
            if not user.check_password_history(new_password):
                raise ValueError('新密碼不能與最近5次使用過的密碼相同')

            # 密碼加密
            password = new_password.encode('utf-8')
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(password, salt)
            new_password = hashed.decode('utf-8')

            # 更新密碼
            return self.dao.reset_password(user, new_password)
        except Exception as e:
            logger.error(f"重設密碼錯誤: {str(e)}")
            raise 

    def verify_reset_token(self, token: str) -> bool:
        """驗證重設密碼 token"""
        try:
            user = self.dao.verify_reset_token(token)
            return user is not None
        except Exception as e:
            logger.error(f"驗證重設密碼 token 錯誤: {str(e)}")
            raise 