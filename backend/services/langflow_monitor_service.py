import logging
import requests
from typing import List
from config.config import config
from services.langflow_base_service import LangflowBaseService

# 設定 logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class LangflowMonitorService(LangflowBaseService):
    def __init__(self):
        super().__init__()
        logger.info(f"LangflowMonitorService initialized with base_url: {self.base_url}")
        logger.info(f"Headers: {self.headers}")
        
    def get_monitor_messages(self, flow_id: str, session_id: str = None,
                           sender: str = None, sender_name: str = None,
                           order_by: str = 'timestamp') -> List[dict]:
        """獲取監控訊息
        
        Args:
            flow_id: Flow ID
            session_id: Session ID (可選)
            sender: 發送者 (可選)
            sender_name: 發送者名稱 (可選)
            order_by: 排序欄位 (預設: timestamp)
            
        Returns:
            List[dict]: 監控訊息列表
        """
        try:
            # 構建查詢參數
            params = {
                'flow_id': flow_id,
                'session_id': session_id,
                'sender': sender,
                'sender_name': sender_name,
                'order_by': order_by
            }
            # 移除 None 值的參數
            params = {k: v for k, v in params.items() if v is not None}
            
            # 構建完整的 URL
            url = f"{self.base_url}/api/v1/monitor/messages"
            logger.info(f"Making request to: {url}")
            logger.info(f"Using headers: {self.headers}")
            logger.info(f"Using params: {params}")
            
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"Response content: {data}")
            
            # 確保返回的是列表
            if isinstance(data, list):
                return data
            elif isinstance(data, dict) and 'messages' in data:
                return data['messages']
            else:
                logger.warning(f"Unexpected response format: {data}")
                return []
                
        except requests.exceptions.RequestException as e:
            logger.error(f"獲取監控訊息失敗: {str(e)}")
            raise Exception(f"獲取監控訊息失敗: {str(e)}")
            
    def delete_messages_by_session(self, session_id: str) -> dict:
        """刪除指定 session 的對話記錄"""
        try:
            # 使用 self.base_url 而不是硬編碼的 URL
            url = f"{self.base_url}/api/v1/monitor/messages/session/{session_id}"
                                  
            response = requests.delete(url, headers=self.headers)
            
            # 加入響應內容的日誌
            logger.info(f"Response status code: {response.status_code}")
            logger.info(f"Response content: {response.text}")
            
            # 加入更詳細的錯誤處理
            if response.status_code == 404:
                return {
                    'success': False,
                    'message': '找不到指定的對話記錄'
                }
            elif response.status_code == 401:
                return {
                    'success': False,
                    'message': '未授權的請求'
                }
            
            response.raise_for_status()
            
            return {
                'success': True,
                'message': '成功刪除對話記錄'
            }
                
        except requests.exceptions.RequestException as e:
            logger.error(f"刪除對話記錄失敗: {str(e)}")
            raise Exception(f"刪除對話記錄失敗: {str(e)}")