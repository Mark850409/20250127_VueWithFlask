from typing import List, Optional
from models.langflow import Langflow, db
from models.monitor import LangflowMonitor
from models.database import db
from sqlalchemy import text

class LangflowDAO:
    @staticmethod
    def create_langflow(data: dict) -> Langflow:
        """創建 Langflow 記錄"""
        langflow = Langflow(**data)
        db.session.add(langflow)
        db.session.commit()
        return langflow
    
    @staticmethod
    def get_by_flow_id(flow_id: str) -> Optional[Langflow]:
        """根據 flow_id 獲取記錄"""
        return Langflow.query.filter_by(
            flow_id=flow_id,
            status='active'
        ).first()
    
    @staticmethod
    def get_by_flow_id_and_name(flow_id: str, file_name: str) -> Optional[Langflow]:
        """根據 flow_id 和檔名獲取記錄"""
        return Langflow.query.filter(
            Langflow.flow_id == flow_id,
            Langflow.file_name == file_name,
            Langflow.status == 'active'
        ).first()
    
    @staticmethod
    def get_files_by_flow_id(flow_id: str) -> List[Langflow]:
        """獲取指定 flow_id 的所有檔案"""
        return Langflow.query.filter_by(
            flow_id=flow_id,
            status='active'
        ).all()
    
    @staticmethod
    def delete_langflow(langflow_id: int) -> bool:
        """刪除記錄（軟刪除）"""
        langflow = Langflow.query.get(langflow_id)
        if langflow:
            langflow.status = 'deleted'
            db.session.commit()
            return True
        return False

    def get_by_flow_id_and_file_id(self, flow_id: str, file_id: str) -> Optional[Langflow]:
        """根據 flow_id 和 file_id 獲取記錄"""
        return Langflow.query.filter(
            Langflow.flow_id == flow_id,
            Langflow.file_id == file_id,
            Langflow.status == 'active'
        ).first()

    @staticmethod
    def get_monitor_messages(flow_id: str, session_id: str = None, 
                            sender: str = None, sender_name: str = None,
                            order_by: str = 'timestamp') -> List[LangflowMonitor]:
        """獲取監控訊息"""
        query = LangflowMonitor.query.filter(
            LangflowMonitor.flow_id == flow_id
        )
        
        if session_id:
            query = query.filter(LangflowMonitor.session_id == session_id)
        if sender:
            query = query.filter(LangflowMonitor.sender == sender)
        if sender_name:
            query = query.filter(LangflowMonitor.sender_name == sender_name)
            
        # 處理排序
        if order_by == 'timestamp':
            query = query.order_by(LangflowMonitor.timestamp.desc())
        
        return query.all()

    @staticmethod
    def create_monitor_message(data: dict) -> LangflowMonitor:
        """創建監控訊息"""
        message = LangflowMonitor(**data)
        db.session.add(message)
        db.session.commit()
        return message

    def delete_messages_by_session(self, session_id: str) -> bool:
        """根據 session_id 刪除對話記錄
        
        Args:
            session_id: 對話 Session ID
            
        Returns:
            bool: 是否刪除成功
        """
        try:
            # 使用原生 SQL 執行刪除
            sql = text("""
                DELETE FROM langflow_messages 
                WHERE session_id = :session_id
            """)
            
            result = db.session.execute(sql, {'session_id': session_id})
            db.session.commit()
            
            # 檢查是否有刪除記錄
            return result.rowcount > 0
            
        except Exception as e:
            db.session.rollback()
            raise e 