from typing import List, Optional, Dict
from dao.folder_dao import FolderDAO
import logging
import uuid
import os
import zipfile
from datetime import datetime
import requests
from config.config import config
import io

# 設定 logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class FolderService:
    def __init__(self):
        self.dao = FolderDAO()
        self.config = config['development']()
    
    def get_all_folders(self) -> List[dict]:
        """獲取所有資料夾"""
        try:
            return self.dao.get_all_folders()
        except Exception as e:
            logger.error(f"獲取資料夾失敗: {str(e)}")
            raise
    
    def create_folder(self, data: dict) -> dict:
        """建立資料夾"""
        try:
            # 生成唯一 ID
            folder_id = str(uuid.uuid4())
            data['folder_id'] = folder_id
            
            # 檢查父資料夾是否存在
            if data.get('parent_id'):
                parent = self.dao.get_by_folder_id(data['parent_id'])
                if not parent:
                    raise ValueError('父資料夾不存在')
            
            return self.dao.create_folder(data)
        except Exception as e:
            logger.error(f"建立資料夾失敗: {str(e)}")
            raise
    
    def get_folder(self, folder_id: str) -> Optional[dict]:
        """獲取單一資料夾"""
        try:
            return self.dao.get_by_folder_id(folder_id)
        except Exception as e:
            logger.error(f"獲取資料夾失敗: {str(e)}")
            raise
    
    def update_folder(self, folder_id: str, data: dict) -> Optional[dict]:
        """更新資料夾"""
        try:
            # 檢查資料夾是否存在
            folder = self.dao.get_by_folder_id(folder_id)
            if not folder:
                return None
            
            # 檢查父資料夾是否存在
            if data.get('parent_id'):
                parent = self.dao.get_by_folder_id(data['parent_id'])
                if not parent:
                    raise ValueError('父資料夾不存在')
                # 檢查是否形成循環引用
                if folder_id == data['parent_id']:
                    raise ValueError('不能將資料夾設為自己的父資料夾')
            
            return self.dao.update_folder(folder_id, data)
        except Exception as e:
            logger.error(f"更新資料夾失敗: {str(e)}")
            raise

    def download_folder(self, folder_id: str) -> Optional[tuple[bytes, str]]:
        """下載資料夾
        Returns:
            Optional[tuple[bytes, str]]: (ZIP 內容, 檔案名稱) 或 None
        """
        try:
            # 呼叫外部 API
            logger.info(f"Downloading folder from: {self.config.LANGFLOW_API_BASE_URL}")
            url = f"{self.config.LANGFLOW_API_BASE_URL}/download/{folder_id}"
            logger.info(f"Downloading folder from: {url}")

            response = requests.get(
                url,
                headers={'Accept': 'application/zip'},
                timeout=10,
                stream=True  # 啟用串流下載
            )

            # 確保回應有效
            if response.status_code != 200:
                logger.error(f"下載失敗: {response.status_code}")
                return None
            
            # 確保下載的檔案是 ZIP 格式
            content_type = response.headers.get("Content-Type", "")
            logger.info(f"下載的 content-type: {content_type}")
            if "application/zip" not in content_type and "application/x-zip-compressed" not in content_type:
                logger.error("下載的內容不是 ZIP 檔案")
                return None

            logger.info(f"下載的 response: {response}")
            
            # 讀取 ZIP 檔案內容
            zip_data = response.content

            # 記錄下載成功
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{folder_id}.zip"
            logger.info(f"下載成功: {timestamp}_{filename} ({len(zip_data)} bytes)")

            return zip_data, filename

        except Exception as e:
            logger.error(f"下載資料夾失敗: {str(e)}")
            return None

