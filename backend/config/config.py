import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta

# 獲取當前文件的目錄
current_dir = Path(__file__).parent.parent

# 檢查要載入的配置文件路徑
env_development = current_dir / '.env.development'
env_production = current_dir / '.env.production'

# 先檢查系統環境變數
env = os.getenv('FLASK_ENV')
print(f"系統環境變數 FLASK_ENV: {env}")

# 根據環境載入對應的配置文件
if env and env.strip() == 'production':  # 確保移除空白並檢查非空值
    env_path = env_production
    print("使用生產環境配置")
else:
    env_path = env_development
    print("使用開發環境配置")

print(f"嘗試載入配置文件: {env_path}")

if env_path.exists():
    print(f"載入的路徑是: {env_path}")
    load_dotenv(env_path, override=True)
else:
    print(f"Warning: 環境檔案未找到: {env_path}")
    print("使用系統環境變數")

# 重新獲取環境變數（確保配置文件已載入）
env = os.getenv('FLASK_ENV')
# 調試輸出
print(f"環境變數值: '{env}'")
print(f"環境變數長度: {len(env) if env else 0}")
print(f"環境變數類型: {type(env)}")

if env not in ['development', 'production']:
    env = 'development'
    os.environ['FLASK_ENV'] = env

print(f"目前配置的環境是: {env}")

# 檢查 Google Maps API Key
if not os.getenv('GOOGLE_MAPS_API_KEY'):
    raise ValueError('Missing GOOGLE_MAPS_API_KEY in environment variables')

# 定義 Foodpanda API URLs
FOODPANDA_RECOMMENDATION_URL = "https://disco.deliveryhero.io"
FOODPANDA_SERVICE_URL = "https://tw.fd-api.com"

# 資料庫配置
DB_CONFIG = {
    'HOST': os.getenv('DB_HOST', 'host.docker.internal'),
    'PORT': os.getenv('DB_PORT', '3307'),
    'USER': os.getenv('DB_USER', 'mark'),
    'PASSWORD': os.getenv('DB_PASSWORD', 'mark850409'),
    'NAME': os.getenv('DB_NAME', 'restaurant')
}

# 構建數據庫 URI
SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_CONFIG["USER"]}:{DB_CONFIG["PASSWORD"]}@{DB_CONFIG["HOST"]}:{DB_CONFIG["PORT"]}/{DB_CONFIG["NAME"]}'

# API URLs
API_URL = os.getenv('API_URL', 'http://localhost:5000')

# PORT
PORT = os.getenv('PORT', 5000)

# Flask配置
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev')

    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 資料庫連接池配置
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 20,
        'pool_recycle': 1800,
        'pool_pre_ping': True,
        'pool_timeout': 60,
        'max_overflow': 10,
        'connect_args': {
            'charset': 'utf8mb4'
        }
    }

    # 設置 SQLAlchemy 的其他選項
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False
    SQLALCHEMY_ENGINE_OPTIONS['echo'] = False
    SQLALCHEMY_POOL_RECYCLE = 1800
    SQLALCHEMY_POOL_TIMEOUT = 60
    SQLALCHEMY_MAX_OVERFLOW = 10

    # API 配置
    API_URL = API_URL
    FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:5173')

    # 資料夾 API 路徑
    FOLDER_API_PATH = os.getenv('FOLDER_API_PATH')

    # Langflow API 配置
    LANGFLOW_API_BASE_URL = os.getenv('LANGFLOW_API_BASE_URL')
    LANGFLOW_API_KEY = os.getenv('LANGFLOW_API_KEY')
    LANGFLOW_AUTH_TOKEN = os.getenv('LANGFLOW_AUTH_TOKEN')

    # 獲取 Google Maps API Key
    GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
    
    # 獲取 Foodpanda API Key
    FOODPANDA_RECOMMENDATION_URL = os.getenv('FOODPANDA_RECOMMENDATION_URL')
    FOODPANDA_SERVICE_URL = os.getenv('FOODPANDA_SERVICE_URL')

    # JWT配置
    JWT_SECRET_KEY = 'your-default-secret-key-here-123456789'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
    JWT_IDENTITY_CLAIM = 'sub'
    JWT_ERROR_MESSAGE_KEY = 'msg'
    
    # 日誌配置
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # CORS配置
    CORS_ORIGINS = [
        'http://localhost:3000',
        'http://localhost:5173',
        'http://127.0.0.1:3000',
        'http://127.0.0.1:5173'
    ]

    # 郵件配置
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'true').lower() == 'true'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
    
    # 重設密碼 token 配置
    RESET_TOKEN_EXPIRE_TYPE = os.getenv('RESET_TOKEN_EXPIRE_TYPE', 'minutes')
    RESET_TOKEN_EXPIRE_VALUE = int(os.getenv('RESET_TOKEN_EXPIRE_VALUE', 10))

class DevelopmentConfig(Config):
    """開發環境配置"""
    DEBUG = True
    # 重設密碼 token 配置
    RESET_TOKEN_EXPIRE_TYPE = os.getenv('RESET_TOKEN_EXPIRE_TYPE', 'minutes')
    RESET_TOKEN_EXPIRE_VALUE = int(os.getenv('RESET_TOKEN_EXPIRE_VALUE', 10))
    
class ProductionConfig(Config):
    DEBUG = False
    # 重設密碼 token 配置
    RESET_TOKEN_EXPIRE_TYPE = os.getenv('RESET_TOKEN_EXPIRE_TYPE', 'hours')
    RESET_TOKEN_EXPIRE_VALUE = int(os.getenv('RESET_TOKEN_EXPIRE_VALUE', 1))

# 根據環境變量選擇配置
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
}

# 載入並導出選擇的配置
selected_config = config[env]
print(f"使用配置: {selected_config.__name__}")
selected_config 