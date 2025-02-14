import os
from typing import List, Optional
from werkzeug.utils import secure_filename
from models.langflow import Langflow
from dao.langflow_dao import LangflowDAO
import logging
from urllib.parse import quote, unquote
from datetime import datetime
import unicodedata

logger = logging.getLogger(__name__)

class LangflowService:
    def __init__(self):
        self.dao = LangflowDAO()
    
    def normalize_filename(self, filename: str) -> str:
        """正規化檔名，保留中文字元"""
        # 將檔名分成名稱和副檔名
        name, ext = os.path.splitext(filename)
        # 正規化 Unicode 字元
        normalized = unicodedata.normalize('NFKC', name)
        # 移除不安全的字元，但保留中文
        safe_name = ''.join(c for c in normalized if c.isalnum() or c.isspace() or c in '-_()[]{}中文')
        # 重新組合檔名
        return f"{safe_name}{ext}"
    
    def upload_file(self, flow_id: str, file) -> Langflow:
        """上傳檔案"""
        try:
            # 處理原始檔名
            original_filename = file.filename
            
            # 生成檔案 ID
            file_id = datetime.now().strftime('%Y%m%d%H%M%S')
            
            # 建立儲存路徑
            _, ext = os.path.splitext(original_filename)
            storage_filename = f"{file_id}{ext}"
            cache_dir = os.path.join(os.path.expanduser('~'), '.cache', 'langflow', flow_id)
            file_path = os.path.join(cache_dir, storage_filename)
            
            # 確保目錄存在
            os.makedirs(cache_dir, exist_ok=True)
            
            # 保存檔案
            content = file.read()
            with open(file_path, 'wb') as f:
                f.write(content)
            
            # 創建記錄
            data = {
                'flow_id': flow_id,
                'file_id': file_id,
                'file_name': original_filename,
                'file_path': file_path
            }
            return self.dao.create_langflow(data)
        except Exception as e:
            logger.error(f"上傳檔案失敗: {str(e)}")
            raise
    
    def download_file_by_id(self, flow_id: str, file_id: str) -> Optional[dict]:
        """根據 ID 下載檔案"""
        try:
            langflow = self.dao.get_by_flow_id_and_file_id(flow_id, file_id)
            
            if not langflow or langflow.status != 'active':
                raise ValueError('檔案不存在')
            
            if not os.path.exists(langflow.file_path):
                raise ValueError('檔案已被刪除')
            
            return {
                'file_path': langflow.file_path,
                'file_name': langflow.file_name
            }
        except Exception as e:
            logger.error(f"下載檔案失敗: {str(e)}")
            raise
    
    def list_files(self, flow_id: str) -> List[Langflow]:
        """列出檔案"""
        try:
            return self.dao.get_files_by_flow_id(flow_id)
        except Exception as e:
            logger.error(f"列出檔案失敗: {str(e)}")
            raise
    
    def delete_file(self, flow_id: str, file_name: str) -> bool:
        """刪除檔案"""
        try:
            langflow = self.dao.get_by_flow_id_and_name(flow_id, file_name)
            if not langflow:
                raise ValueError('檔案不存在')
                
            # 刪除實體檔案
            if os.path.exists(langflow.file_path):
                os.remove(langflow.file_path)
                
            return self.dao.delete_langflow(langflow.id)
        except Exception as e:
            logger.error(f"刪除檔案失敗: {str(e)}")
            raise
    
    def get_monitor_messages(self, flow_id: str, session_id: str = None,
                            sender: str = None, sender_name: str = None,
                            order_by: str = 'timestamp') -> List[dict]:
        """獲取監控訊息"""
        try:
            messages = self.dao.get_monitor_messages(
                flow_id=flow_id,
                session_id=session_id,
                sender=sender,
                sender_name=sender_name,
                order_by=order_by
            )
            return [msg.to_dict() for msg in messages]
        except Exception as e:
            logger.error(f"獲取監控訊息失敗: {str(e)}")
            raise
    
    def create_monitor_message(self, data: dict) -> dict:
        """創建監控訊息"""
        try:
            message = self.dao.create_monitor_message(data)
            return message.to_dict()
        except Exception as e:
            logger.error(f"創建監控訊息失敗: {str(e)}")
            raise 