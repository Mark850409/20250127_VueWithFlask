from typing import List, Optional
from dao.log_dao import LogDAO
from models.log import Log
from models.user import User

class LogService:
    def __init__(self):
        self.dao = LogDAO()
    
    def get_all_logs(self) -> List[Log]:
        """獲取所有日誌"""
        return self.dao.get_all_logs()
    
    def get_log(self, log_id: int) -> Optional[Log]:
        """獲取指定日誌"""
        return self.dao.get_log_by_id(log_id)
    
    def create_log(self, log_data: dict) -> Log:
        """創建日誌"""
        # 檢查用戶是否存在
        if log_data.get('user_id'):
            user = User.query.get(log_data['user_id'])
            if not user:
                log_data['user_id'] = None
                
        return self.dao.create_log(log_data)
    
    def get_logs_by_user(self, user_id: int) -> List[Log]:
        """獲取指定用戶的所有日誌"""
        return self.dao.get_logs_by_user(user_id)
    
    def get_logs_by_action(self, action: str) -> List[Log]:
        """獲取指定操作類型的日誌"""
        return self.dao.get_logs_by_action(action) 