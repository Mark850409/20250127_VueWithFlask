from typing import List, Optional
from models.user import User, db

class UserDAO:
    @staticmethod
    def get_all_users() -> List[User]:
        return User.query.all()
    
    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[User]:
        return User.query.get(user_id)
    
    @staticmethod
    def create_user(user_data: dict) -> User:
        user = User(**user_data)
        db.session.add(user)
        db.session.commit()
        return user
    
    @staticmethod
    def update_user(user_id: int, user_data: dict) -> Optional[User]:
        user = User.query.get(user_id)
        if user:
            for key, value in user_data.items():
                setattr(user, key, value)
            db.session.commit()
        return user
    
    @staticmethod
    def delete_user(user_id: int) -> bool:
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False 