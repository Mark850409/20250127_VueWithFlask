import os
from datetime import timedelta
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

class Config:
    # 數據庫配置
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = os.environ.get('DB_PORT', '3306')
    DB_USER = os.environ.get('DB_USER', 'mark')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'mark850409')
    DB_NAME = os.environ.get('DB_NAME', 'restaurant')
    
    # 構建 MySQL 連線 URL
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
    
    # API 配置
    API_URL = os.environ.get('API_URL', 'http://localhost:5000')
    
    # 其他配置保持不變...
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_MAX_OVERFLOW = 20
    
    # JWT配置
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-secret-key')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    
    # 其他配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret')
    
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