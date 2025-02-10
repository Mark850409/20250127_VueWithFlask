import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta

# 載入環境變數
load_dotenv()

# 獲取當前文件的目錄
current_dir = Path(__file__).parent.parent

# 根據 FLASK_ENV 決定要載入哪個 .env 文件
env = os.getenv('FLASK_ENV', 'development')
env_file = '.env.production' if env == 'production' else '.env.development'

# 構建完整的 .env 文件路徑
env_path = current_dir / env_file

# 載入對應的 .env 文件
if env_path.exists():
    print(f"Loading environment from: {env_path}")
    load_dotenv(env_path)
else:
    print(f"Warning: Environment file not found: {env_path}")

# 資料庫配置
DB_CONFIG = {
    'HOST': os.getenv('DB_HOST', 'db'),
    'PORT': os.getenv('DB_PORT', '3306'),
    'USER': os.getenv('DB_USER', 'mark'),
    'PASSWORD': os.getenv('DB_PASSWORD', 'mark850409'),
    'NAME': os.getenv('DB_NAME', 'restaurant')
}

# 構建數據庫 URI
SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_CONFIG["USER"]}:{DB_CONFIG["PASSWORD"]}@{DB_CONFIG["HOST"]}:{DB_CONFIG["PORT"]}/{DB_CONFIG["NAME"]}'

# 添加這些變數到 config.py
# API URLs
API_URL = os.getenv('API_URL', 'http://localhost:5000')
FOODPANDA_RECOMMENDATION_URL = os.getenv('FOODPANDA_RECOMMENDATION_URL')
FOODPANDA_SERVICE_URL = os.getenv('FOODPANDA_SERVICE_URL')

# Google Maps API Key
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
if not GOOGLE_MAPS_API_KEY:
    raise ValueError('Missing GOOGLE_MAPS_API_KEY in environment variables')

# 檢查必要的環境變數
if not FOODPANDA_RECOMMENDATION_URL:
    raise ValueError('Missing FOODPANDA_RECOMMENDATION_URL in environment variables')
if not FOODPANDA_SERVICE_URL:
    raise ValueError('Missing FOODPANDA_SERVICE_URL in environment variables')

# Flask配置
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev')
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # API 配置
    API_URL = API_URL

    # 獲取 Google Maps API Key
    GOOGLE_MAPS_API_KEY = GOOGLE_MAPS_API_KEY
    
    # 獲取 Foodpanda API Key
    FOODPANDA_RECOMMENDATION_URL = FOODPANDA_RECOMMENDATION_URL
    FOODPANDA_SERVICE_URL = FOODPANDA_SERVICE_URL

    # 其他配置保持不變...
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_MAX_OVERFLOW = 20
    
    # JWT配置
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', '86400')))
    
    # 日誌配置
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # CORS配置
    CORS_ORIGINS = [
        'http://localhost:3000',
        'http://localhost:5173',
        'http://127.0.0.1:3000',
        'http://127.0.0.1:5173'
    ]

class DevelopmentConfig(Config):
    DEBUG = True
    
class ProductionConfig(Config):
    DEBUG = False
    # 生產環境可以有不同的配置
    SQLALCHEMY_POOL_SIZE = 20
    SQLALCHEMY_MAX_OVERFLOW = 40

# 根據環境變量選擇配置
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
} 