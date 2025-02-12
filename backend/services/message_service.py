from typing import List, Optional
from models.message import Message
from dao.message_dao import MessageDAO
from models.store import Store
from datetime import datetime

class MessageService:
    def __init__(self):
        self.dao = MessageDAO()
    
    def get_all_messages(self) -> List[dict]:
        """獲取所有評論"""
        messages = self.dao.get_all_messages()
        return [message.to_dict() for message in messages]
    
    def get_user_messages(self, user_id: int) -> List[Message]:
        """獲取用戶的所有留言"""
        return self.dao.get_user_messages(user_id)
    
    def get_message(self, message_id: int) -> Optional[Message]:
        """獲取指定留言"""
        return self.dao.get_message(message_id)
    
    def create_message(self, user_id: int, message_data: dict) -> Message:
        """創建評論"""
        message_data['user_id'] = user_id
        # 驗證店家是否存在
        store = Store.query.get(message_data['store_id'])
        if not store:
            raise ValueError('店家不存在')
        # 驗證評分範圍
        if not 0 <= message_data['rating'] <= 5:
            raise ValueError('評分必須在0-5之間')
        # 添加店家名稱和圖片
        message_data['store_name'] = store.name
        message_data['store_image'] = store.hero_image or ''
        return self.dao.create_message(message_data)
    
    def update_message(self, user_id: int, message_id: int, message_data: dict) -> Optional[Message]:
        """更新留言"""
        message = self.dao.get_message(message_id)
        if not message:
            raise ValueError('留言不存在')
        
        # 只有管理員可以更新狀態，一般用戶只能更新自己的留言內容和評分
        if 'status' in message_data:
            # TODO: 這裡應該加入管理員權限檢查
            pass
        elif message.user_id != user_id and not message_data.get('status'):
            raise ValueError('只能修改自己的留言')
        
        # 驗證評分範圍
        if 'rating' in message_data and not (0 <= message_data['rating'] <= 5):
            raise ValueError('評分必須在0-5之間')
        
        return self.dao.update_message(message_id, message_data)
    
    def delete_message(self, user_id: int, message_id: int) -> bool:
        """刪除留言"""
        message = self.dao.get_message(message_id)
        if not message:
            raise ValueError('留言不存在')
        if message.user_id != user_id:
            raise ValueError('只能刪除自己的留言')
            
        return self.dao.delete_message(message_id)

    def add_reply(self, message_id: int, reply_data: dict) -> Message:
        """添加回覆"""
        message = self.dao.get_message(message_id)
        if not message:
            raise ValueError('評論不存在')
        
        reply_data['id'] = len(message.replies) + 1 if message.replies else 1
        reply_data['create_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        return self.dao.add_reply(message_id, reply_data)

    def delete_reply(self, message_id: int, reply_id: int) -> Message:
        """刪除回覆"""
        message = self.dao.get_message(message_id)
        if not message:
            raise ValueError('評論不存在')
        
        return self.dao.delete_reply(message_id, reply_id) 