from typing import List, Optional
from models.message import Message, db
from sqlalchemy import desc

class MessageDAO:
    @staticmethod
    def get_all_messages() -> List[Message]:
        """獲取所有評論"""
        return Message.query.order_by(desc(Message.created_at)).all()
    
    @staticmethod
    def get_user_messages(user_id: int) -> List[Message]:
        """獲取用戶的所有評論"""
        return Message.query.filter_by(user_id=user_id)\
            .order_by(desc(Message.created_at))\
            .all()
    
    @staticmethod
    def get_message(message_id: int) -> Optional[Message]:
        """獲取指定留言"""
        return Message.query.get(message_id)
    
    @staticmethod
    def create_message(message_data: dict) -> Message:
        """創建評論"""
        # 設置初始狀態為待審核
        message_data['status'] = 'pending'
        # 初始化回覆列表
        message_data['replies'] = []
        message = Message(**message_data)
        db.session.add(message)
        db.session.commit()
        return message
    
    @staticmethod
    def update_message(message_id: int, message_data: dict) -> Optional[Message]:
        """更新留言"""
        message = Message.query.get(message_id)
        if message:
            # 只更新允許的欄位
            allowed_fields = {'content', 'status', 'rating'}
            update_data = {k: v for k, v in message_data.items() if k in allowed_fields}
            for key, value in update_data.items():
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

    @staticmethod
    def add_reply(message_id: int, reply_data: dict) -> Message:
        """添加回覆"""
        message = Message.query.get(message_id)
        if message:
            if not message.replies:
                message.replies = []
            message.replies.append(reply_data)
            db.session.commit()
        return message

    @staticmethod
    def delete_reply(message_id: int, reply_id: int) -> Message:
        """刪除回覆"""
        message = Message.query.get(message_id)
        if message and message.replies:
            message.replies = [r for r in message.replies if r['id'] != reply_id]
            db.session.commit()
        return message 