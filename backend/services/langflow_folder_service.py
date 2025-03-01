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
from services.langflow_base_service import LangflowBaseService

# 設定 logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class FolderService(LangflowBaseService):
    def __init__(self):
        super().__init__()
    
    def get_all_folders(self) -> List[dict]:
        """獲取所有專案"""
        try:
            url = f"{self.base_url}/api/v1/folders/"
            logger.info(f"Making request to: {url}")
            logger.info(f"Using headers: {self.headers}")
            
            response = requests.get(url)
            
            logger.info(f"Response status: {response.status_code}")
            logger.info(f"Response headers: {response.headers}")
            
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"Successfully parsed JSON response: {str(data)[:200]}")
            return data
            
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP Error: {e.response.status_code}")
            logger.error(f"Response content: {e.response.text}")
            raise Exception(f"HTTP 錯誤: {e.response.status_code}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {str(e)}")
            raise Exception("API 請求失敗") from e
        except Exception as e:
            logger.error(f"獲取專案失敗: {str(e)}")
            raise
    
    def create_folder(self, data: dict) -> dict:
        """建立專案"""
        try:
            url = f"{self.base_url}/api/v1/folders/"
            logger.info(f"Creating folder with data: {data}")
            response = requests.post(url, headers=self.headers, json=data)
            logger.info(f"Response status: {response.status_code}")
            logger.info(f"Response content: {response.text}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"建立專案失敗: {str(e)}")
            raise
    
    def get_folder(self, folder_id: str) -> Optional[dict]:
        """獲取單一專案"""
        try:
            url = f"{self.base_url}/api/v1/folders/{folder_id}"
            logger.info(f"Getting folder from: {url}")
            response = requests.get(url, headers=self.headers)
            logger.info(f"Response status: {response.status_code}")
            logger.info(f"Response headers: {response.headers}")
            response.raise_for_status()
            data = response.json()
            logger.info(f"Successfully parsed JSON response: {str(data)[:200]}")
            return data
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP Error: {e.response.status_code}")
            logger.error(f"Response content: {e.response.text}")
            if e.response.status_code == 404:
                return None
            raise
        except Exception as e:
            logger.error(f"獲取專案失敗: {str(e)}")
            raise
    
    def update_folder(self, folder_id: str, data: dict) -> Optional[dict]:
        """更新專案"""
        try:
            url = f"{self.base_url}/api/v1/folders/{folder_id}"
            logger.info(f"Updating folder with data: {data}")
            response = requests.patch(url, headers=self.headers, json=data)
            logger.info(f"Response status: {response.status_code}")
            logger.info(f"Response content: {response.text}")
            response.raise_for_status()
            data = response.json()
            logger.info(f"Successfully parsed JSON response: {str(data)[:200]}")
            return data
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP Error: {e.response.status_code}")
            logger.error(f"Response content: {e.response.text}")
            if e.response.status_code == 404:
                return None
            raise
        except Exception as e:
            logger.error(f"更新專案失敗: {str(e)}")
            raise

    def download_folder(self, folder_id: str) -> Optional[tuple[bytes, str]]:
        """下載單一專案下面的所有專案"""
        try:
            # 呼叫外部 API
            logger.info(f"Downloading folder from: {self.config.LANGFLOW_API_BASE_URL}")
            url = f"{self.base_url}/api/v1/folders/download/{folder_id}"
            logger.info(f"Downloading folder from: {url}")

            response = requests.get(
                url,
                headers={'Accept': 'application/zip'},
                timeout=10,
                stream=True
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
            logger.error(f"下載專案失敗: {str(e)}")
            return None

    def delete_folder(self, folder_id: str) -> bool:
        """刪除專案"""
        try:
            url = f"{self.base_url}/api/v1/folders/{folder_id}"
            logger.info(f"Deleting folder from: {url}")
            
            response = requests.delete(url, headers=self.headers)
            logger.info(f"Response status: {response.status_code}")
            
            # 檢查回應狀態碼
            if response.status_code == 204:
                logger.info("專案刪除成功")
                return True
                
            response.raise_for_status()
            return True
            
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP Error: {e.response.status_code}")
            logger.error(f"Response content: {e.response.text}")
            if e.response.status_code == 404:
                logger.warning("專案不存在")
                return False
            raise
        except Exception as e:
            logger.error(f"刪除專案失敗: {str(e)}")
            raise

