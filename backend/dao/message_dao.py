from typing import List, Optional
from models.message import Message, db
from sqlalchemy import desc

class MessageDAO:
    @staticmethod
    def get_all_messages() -> List[Message]:
        """獲取所有留言"""
        return Message.query.order_by(desc(Message.created_at)).all()
    
    @staticmethod
    def get_user_messages(user_id: int) -> List[Message]:
        """獲取用戶的所有留言"""
        return Message.query.filter_by(user_id=user_id).order_by(desc(Message.created_at)).all()
    
    @staticmethod
    def get_message(message_id: int) -> Optional[Message]:
        """獲取指定留言"""
        return Message.query.get(message_id)
    
    @staticmethod
    def create_message(message_data: dict) -> Message:
        """創建留言"""
        message = Message(**message_data)
        db.session.add(message)
        db.session.commit()
        return message
    
    @staticmethod
    def update_message(message_id: int, message_data: dict) -> Optional[Message]:
        """更新留言"""
        message = Message.query.get(message_id)
        if message:
            for key, value in message_data.items():
                setattr(message, key, value)
            db.session.commit()
        return message
    
    @staticmethod
    def delete_message(message_id: int) -> bool:
        """刪除留言（實際刪除）"""
        message = Message.query.get(message_id)
        if message:
            db.session.delete(message)
            db.session.commit()
            return True
        return False 