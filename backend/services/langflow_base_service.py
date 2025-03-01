from config.config import config
import os
import logging

logger = logging.getLogger(__name__)

class LangflowBaseService:
    def __init__(self):
        try:
            # 從環境變數獲取當前環境，預設為 development
            env = os.getenv('FLASK_ENV', 'development')
            self.config = config[env]()
            
            # 檢查並設置 base_url
            if not hasattr(self.config, 'LANGFLOW_API_BASE_URL'):
                raise ValueError("LANGFLOW_API_BASE_URL not found in config")
                
            if self.config.LANGFLOW_API_BASE_URL is None:
                raise ValueError("LANGFLOW_API_BASE_URL cannot be None")
                
            if not isinstance(self.config.LANGFLOW_API_BASE_URL, str):
                raise ValueError(f"LANGFLOW_API_BASE_URL must be a string, got {type(self.config.LANGFLOW_API_BASE_URL)}")
            
            self.base_url = str(self.config.LANGFLOW_API_BASE_URL)
            if self.base_url.endswith('/'):
                self.base_url = self.base_url[:-1]
            
            # 檢查並設置 API key
            if not hasattr(self.config, 'LANGFLOW_API_KEY'):
                raise ValueError("LANGFLOW_API_KEY not found in config")
                
            if self.config.LANGFLOW_API_KEY is None:
                raise ValueError("LANGFLOW_API_KEY cannot be None")
            
            # 設置 headers
            self.headers = {
                'Authorization': str(self.config.LANGFLOW_API_KEY),
                'Content-Type': 'application/json'
            }
            
            logger.info(f"LangflowBaseService initialized with base_url: {self.base_url}")
            
        except Exception as e:
            logger.error(f"Failed to initialize LangflowBaseService: {str(e)}")
            logger.error(f"Current config: {vars(self.config) if hasattr(self, 'config') else 'No config'}")
            raise 