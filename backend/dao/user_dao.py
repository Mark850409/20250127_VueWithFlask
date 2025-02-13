from typing import List, Optional
from models.user import User, db
from datetime import datetime, timedelta
import os
from werkzeug.utils import secure_filename
from pathlib import Path
import logging
from flask import current_app
import pytz
logger = logging.getLogger(__name__)

# 獲取當前文件的目錄
CURRENT_DIR = Path(__file__).parent.parent
UPLOAD_FOLDER = 'uploads/avatars'
UPLOAD_PATH = CURRENT_DIR / UPLOAD_FOLDER

class UserDAO:
    @staticmethod
    def get_all_users() -> List[User]:
        """獲取所有用戶"""
        return User.query.all()
    
    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[User]:
        """根據ID獲取用戶"""
        return User.query.get(user_id)
    
    @staticmethod
    def get_user_by_username(username: str) -> Optional[User]:
        """根據用戶名獲取用戶"""
        return User.query.filter_by(username=username).first()
    
    @staticmethod
    def get_user_by_email(email: str) -> Optional[User]:
        """根據郵箱獲取用戶"""
        return User.query.filter_by(email=email).first()
    
    @staticmethod
    def create_user(user_data: dict) -> User:
        """創建用戶"""
        user = User(**user_data)
        db.session.add(user)
        db.session.commit()
        return user
    
    @staticmethod
    def update_user(user_id: int, user_data: dict) -> Optional[User]:
        """更新用戶"""
        try:
            user = User.query.get(user_id)
            if user:
                for key, value in user_data.items():
                    setattr(user, key, value)
                user.update_time = datetime.utcnow()
                db.session.commit()
                db.session.refresh(user)
                return user
            return None
        except Exception as e:
            db.session.rollback()
            raise Exception(f'更新用戶失敗: {str(e)}')
    
    @staticmethod
    def delete_user(user_id: int) -> bool:
        """刪除用戶"""
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False

    @staticmethod
    def update_avatar(user_id: int, avatar_file) -> str:
        """更新用戶頭像
        
        Args:
            user_id: 用戶ID
            avatar_file: 上傳的文件對象
        
        Returns:
            str: 頭像URL
        """
        try:
            # 獲取用戶
            user = User.query.get(user_id)
            if not user:
                raise ValueError('用戶不存在')

            # 生成安全的文件名
            filename = secure_filename(avatar_file.filename)
            # 添加時間戳避免重名
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{user_id}_{timestamp}_{filename}"
            
            # 確保上傳目錄存在
            if not UPLOAD_PATH.exists():
                UPLOAD_PATH.mkdir(parents=True, exist_ok=True)
            
            # 保存文件
            file_path = UPLOAD_PATH / filename
            avatar_file.save(file_path)
            
            # 更新用戶頭像URL
            avatar_url = f'/uploads/avatars/{filename}'
            user.avatar = avatar_url
            db.session.commit()
            
            return avatar_url
            
        except Exception as e:
            db.session.rollback()
            logger.error(f"更新頭像錯誤: {str(e)}", exc_info=True)
            raise 

    @staticmethod
    def create_reset_token(user: User) -> str:
        """創建重設密碼 token"""
        try:
            token = user.generate_reset_token()
            db.session.commit()
            return token
        except Exception as e:
            db.session.rollback()
            logger.error(f"創建重設密碼 token 錯誤: {str(e)}")
            raise

    @staticmethod
    def verify_reset_token(token: str) -> Optional[User]:
        """驗證重設密碼 token"""
        try:
            user = User.query.filter_by(reset_password_token=token).first()
            if not user:
                logger.info(f"找不到對應的 token: {token}")
                return None
            
            # 檢查 token 是否過期
            now = datetime.utcnow()
            logger.info(f"當前時間(UTC): {now}")
            logger.info(f"Token 過期時間(UTC): {user.reset_password_expires}")
            
            # 如果現在時間超過過期時間，則 token 已過期
            if now > user.reset_password_expires:
                logger.info("Token 已過期")
                return None
            
            logger.info("Token 驗證成功")
            return user
            
        except Exception as e:
            logger.error(f"驗證重設密碼 token 錯誤: {str(e)}")
            raise

    @staticmethod
    def reset_password(user: User, new_password: str) -> bool:
        """重設密碼"""
        try:
            # 更新密碼歷史
            user.update_password_history(user.password)
            
            # 更新新密碼
            user.password = new_password
            user.reset_password_token = None
            user.reset_password_expires = None
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            logger.error(f"重設密碼錯誤: {str(e)}")
            raise 