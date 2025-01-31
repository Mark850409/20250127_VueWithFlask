from typing import List, Optional
from models.user import User, db

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
        user = User.query.get(user_id)
        if user:
            for key, value in user_data.items():
                setattr(user, key, value)
            db.session.commit()
        return user
    
    @staticmethod
    def delete_user(user_id: int) -> bool:
        """刪除用戶"""
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False 