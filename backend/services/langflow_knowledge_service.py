import os
from typing import List, Optional
from werkzeug.utils import secure_filename
from models.langflow import Langflow
from dao.langflow_dao import LangflowDAO
import logging
from urllib.parse import quote, unquote
from datetime import datetime
import unicodedata
import requests
from config.config import config
import zipfile
import io
from services.langflow_base_service import LangflowBaseService

# 設定 logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class LangflowService(LangflowBaseService):
    def __init__(self):
        super().__init__()
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
    
    def upload_file(self, flow_id: str, file_data: bytes, file_name: str) -> dict:
        """上傳檔案到 Langflow"""
        try:
            url = f"{self.base_url}/api/v1/files/upload/{flow_id}"
            files = {
                'file': (file_name, file_data)
            }
            response = requests.post(
                url, 
                files=files, 
                headers={'Authorization': self.config.LANGFLOW_API_KEY}
            )
            response.raise_for_status()
            return {'status': 'success', 'message': '上傳成功'}
        except requests.exceptions.RequestException as e:
            logger.error(f"上傳檔案失敗: {str(e)}")
            raise Exception(f"上傳檔案失敗: {str(e)}")
    
    def download_file(self, flow_id: str, file_name: str) -> dict:
        """下載 Langflow 檔案"""
        try:
            url = f"{self.base_url}/api/v1/files/download/{flow_id}/{file_name}"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return {
                'file_data': response.content,
                'file_name': file_name,
                'content_type': response.headers.get('Content-Type', 'application/octet-stream')
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"下載檔案失敗: {str(e)}")
            raise Exception(f"下載檔案失敗: {str(e)}")
    
    def list_files(self, flow_id: str) -> List[dict]:
        """列出 Langflow 檔案"""
        try:
            url = f"{self.base_url}/api/v1/files/list/{flow_id}"
            logger.info(f"列出檔案 URL: {url}")
            logger.info(f"Headers: {self.headers}")
            
            response = requests.get(url, headers=self.headers)
            logger.info(f"Response status: {response.status_code}")
            logger.info(f"Response content: {response.content}")
            
            response.raise_for_status()
            data = response.json()
            logger.info(f"Parsed JSON data: {data}")
            
            # 檢查回傳格式是否包含 'files' 鍵
            if isinstance(data, dict) and 'files' in data:
                return data['files']
            # 如果直接是列表
            elif isinstance(data, list):
                return data
            # 如果是其他格式，返回空列表
            else:
                logger.warning(f"Unexpected response format: {data}")
                return []
        except requests.exceptions.RequestException as e:
            logger.error(f"列出檔案失敗: {str(e)}")
            raise Exception(f"列出檔案失敗: {str(e)}")
    
    def delete_file(self, flow_id: str, file_name: str) -> dict:
        """刪除 Langflow 檔案"""
        try:
            url = f"{self.base_url}/api/v1/files/delete/{flow_id}/{file_name}"
            response = requests.delete(url, headers=self.headers)
            response.raise_for_status()
            return {'status': 'success', 'message': '刪除成功'}
        except requests.exceptions.RequestException as e:
            logger.error(f"刪除檔案失敗: {str(e)}")
            raise Exception(f"刪除檔案失敗: {str(e)}")
    
    def batch_download(self, flow_id: str, file_names: List[str]) -> tuple:
        """批次下載並打包檔案"""
        try:
            # 創建記憶體中的 ZIP 檔案
            memory_file = io.BytesIO()
            with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
                # 下載每個檔案並添加到 ZIP
                for file_name in file_names:
                    file_info = self.download_file(flow_id, file_name)
                    if file_info:
                        zf.writestr(file_name, file_info['file_data'])
            
            # 將指針移到開頭
            memory_file.seek(0)
            
            # 生成下載檔名
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            zip_filename = f'knowledge_files_{timestamp}.zip'
            
            return memory_file, zip_filename
            
        except Exception as e:
            logger.error(f"批次下載失敗: {str(e)}")
            raise Exception(f"批次下載失敗: {str(e)}")