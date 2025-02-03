from flask_cors import CORS
from flask_openapi3 import OpenAPI, Info, Server
from models.database import db
from controllers.user_controller import user_bp
from controllers.git_controller import git_bp
from controllers.log_controller import log_bp
from controllers.menu_controller import menu_bp
from controllers.store_controller import store_bp
from controllers.rating_controller import rating_bp
from controllers.message_controller import message_bp
from controllers.admin_controller import admin_bp
from controllers.favorite_controller import favorite_bp
from controllers.foodpanda_controller import (
    foodpanda_core_bp, 
    foodpanda_vendors_bp, 
    foodpanda_menu_bp, 
    foodpanda_feed_bp
)
from controllers.googlemaps_controller import googlemaps_bp
from config.config import config
from extensions import jwt
import os
from dotenv import load_dotenv
from services.googlemaps_service import GoogleMapsService
from controllers.restaurant_controller import restaurant_bp
from pathlib import Path

# 獲取當前文件的目錄
current_dir = Path(__file__).parent.parent

# 1. 首先根據 FLASK_ENV 決定要載入哪個 .env 文件
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

# 檢查並打印關鍵環境變數
required_env_vars = [
    'FOODPANDA_RECOMMENDATION_URL',
    'FOODPANDA_SERVICE_URL',
    'GOOGLE_MAPS_API_KEY',
    'DB_HOST',
    'DB_PORT',
    'DB_USER',
    'DB_PASSWORD',
    'DB_NAME',
    'CORS_ORIGINS',
    'JWT_SECRET_KEY',
    'API_URL',
    'PORT'
]


# 打印所有環境變數的狀態
print("\nEnvironment Variables Status:")
for var in required_env_vars:
    value = os.getenv(var)
    status = "✓ Found" if value else "✗ Missing"
    print(f"{var}: {status}")

# 檢查必要的環境變數
if not os.getenv('FOODPANDA_RECOMMENDATION_URL'):
    raise ValueError('Missing FOODPANDA_RECOMMENDATION_URL in environment variables')
if not os.getenv('FOODPANDA_SERVICE_URL'):
    raise ValueError('Missing FOODPANDA_SERVICE_URL in environment variables')

# 設置數據庫 URI
DB_HOST = os.getenv('DB_HOST', 'db')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_USER = os.getenv('DB_USER', 'mark')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'mark850409')
DB_NAME = os.getenv('DB_NAME', 'restaurant')

# 構建數據庫 URI
SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
os.environ['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

# API 信息配置
info = Info(title='點餐推薦系統 API', version='1.0.0', description='點餐推薦系統系統的API文檔')

# 從環境變量獲取 API URL
API_URL = os.getenv('API_URL', 'http://localhost:5000')
FOODPANDA_RECOMMENDATION_URL = os.getenv('FOODPANDA_RECOMMENDATION_URL')
FOODPANDA_SERVICE_URL = os.getenv('FOODPANDA_SERVICE_URL')

# 配置服務器
servers = [
    Server(url=API_URL, description="API 服務器"),
    Server(
        url=FOODPANDA_RECOMMENDATION_URL, 
        description='取得foodpanda推薦餐廳使用'
    ),
    Server(
        url=FOODPANDA_SERVICE_URL, 
        description='取得foodpanda菜單和搜尋使用'
    )
]

# 獲取 Google Maps API Key
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
if not GOOGLE_MAPS_API_KEY:
    raise ValueError('Missing GOOGLE_MAPS_API_KEY in environment variables')

# 創建應用實例
app = OpenAPI(
    __name__, 
    info=info, 
    servers=servers
)

# 載入配置
app.config.from_object(config[env])

# JWT 配置
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your-secret-key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 24 * 60 * 60
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_HEADER_NAME'] = 'Authorization'
app.config['JWT_HEADER_TYPE'] = 'Bearer'
app.config['JWT_IDENTITY_CLAIM'] = 'sub'
app.config['JWT_ERROR_MESSAGE_KEY'] = 'msg'

# 添加 Google Maps API Key 到應用配置
app.config['GOOGLE_MAPS_API_KEY'] = GOOGLE_MAPS_API_KEY

# 初始化 JWT
jwt.init_app(app)

# JWT 錯誤處理
@jwt.invalid_token_loader
def invalid_token_callback(error):
    return {'msg': '不合法的token，請重新輸入!!!'}, 401

@jwt.unauthorized_loader
def unauthorized_callback(error):
    return {'msg': '缺少正確的token驗證表頭，請重新輸入!!!'}, 401

# 初始化 SQLAlchemy
db.init_app(app)

# 從環境變數獲取 CORS origins
CORS_ORIGINS = os.getenv('CORS_ORIGINS', '').split(',')

# CORS配置
CORS(app, 
    resources={
        r"/*": {
            "origins": CORS_ORIGINS,  # 使用環境變數中的 origins
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization", "X-Requested-With"],
            "expose_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True,
            "max_age": 600,
            "send_wildcard": False
        }
    }
)

# 配置 Google Maps Service
googlemaps_service = GoogleMapsService(GOOGLE_MAPS_API_KEY)

# 註冊所有藍圖
app.register_api(user_bp)
app.register_api(git_bp)
app.register_api(log_bp)
app.register_api(menu_bp)
app.register_api(store_bp)
app.register_api(rating_bp)
app.register_api(message_bp)
app.register_api(admin_bp)
app.register_api(favorite_bp)
app.register_api(foodpanda_core_bp)
app.register_api(foodpanda_vendors_bp)
app.register_api(foodpanda_menu_bp)
app.register_api(foodpanda_feed_bp)
app.register_api(googlemaps_bp)
app.register_api(restaurant_bp)

# JWT 安全配置
security_scheme = {
    'type': 'http',
    'scheme': 'bearer',
    'bearerFormat': 'JWT',
    'description': '請輸入 JWT token，格式為：Bearer your-token-here'
}

# Foodpanda API Key 配置
api_key_scheme = {
    "type": "apiKey",
    "name": "x-disco-client-id",
    "in": "header",
    "description": "Foodpanda API 需要的 client ID，請輸入: web"
}

# 設置安全方案
if 'components' not in app.api_doc:
    app.api_doc['components'] = {}
if 'securitySchemes' not in app.api_doc['components']:
    app.api_doc['components']['securitySchemes'] = {}

# 註冊安全方案
app.api_doc['components']['securitySchemes'].update({
    'Bearer': security_scheme,
    'ApiKeyAuth': api_key_scheme
})

# 設置全局安全要求
app.api_doc['security'] = [
    {'Bearer': []},
    {'ApiKeyAuth': []}
]

# 創建所有表
with app.app_context():
    db.create_all()
    print("數據庫表已創建")

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=(env == 'development')) 