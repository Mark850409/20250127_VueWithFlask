from typing import List, Optional
from models.message import Message
from dao.message_dao import MessageDAO

class MessageService:
    def __init__(self):
        self.dao = MessageDAO()
    
    def get_all_messages(self) -> List[Message]:
        """獲取所有留言"""
        return self.dao.get_all_messages()
    
    def get_user_messages(self, user_id: int) -> List[Message]:
        """獲取用戶的所有留言"""
        return self.dao.get_user_messages(user_id)
    
    def get_message(self, message_id: int) -> Optional[Message]:
        """獲取指定留言"""
        return self.dao.get_message(message_id)
    
    def create_message(self, user_id: int, message_data: dict) -> Message:
        """創建留言"""
        message_data['user_id'] = user_id
        return self.dao.create_message(message_data)
    
    def update_message(self, user_id: int, message_id: int, message_data: dict) -> Optional[Message]:
        """更新留言"""
        message = self.dao.get_message(message_id)
        if not message:
            raise ValueError('留言不存在')
        if message.user_id != user_id:
            raise ValueError('只能修改自己的留言')
            
        return self.dao.update_message(message_id, message_data)
    
    def delete_message(self, user_id: int, message_id: int) -> bool:
        """刪除留言"""
        message = self.dao.get_message(message_id)
        if not message:
            raise ValueError('留言不存在')
        if message.user_id != user_id:
            raise ValueError('只能刪除自己的留言')
            
        return self.dao.delete_message(message_id) 