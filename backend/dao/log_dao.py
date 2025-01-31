from typing import List, Optional
from models.log import Log, db

class LogDAO:
    @staticmethod
    def get_all_logs() -> List[Log]:
        """獲取所有日誌"""
        return Log.query.order_by(Log.created_at.desc()).all()
    
    @staticmethod
    def get_log_by_id(log_id: int) -> Optional[Log]:
        """獲取指定日誌"""
        return Log.query.get(log_id)
    
    @staticmethod
    def create_log(log_data: dict) -> Log:
        """創建日誌"""
        log = Log(**log_data)
        db.session.add(log)
        db.session.commit()
        return log
    
    @staticmethod
    def get_logs_by_user(user_id: int) -> List[Log]:
        """獲取指定用戶的日誌"""
        return Log.query.filter_by(user_id=user_id).order_by(Log.created_at.desc()).all()
    
    @staticmethod
    def get_logs_by_action(action: str) -> List[Log]:
        """獲取指定操作類型的日誌"""
        return Log.query.filter_by(action=action).order_by(Log.created_at.desc()).all() 