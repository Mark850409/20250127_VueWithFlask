from flask_cors import CORS
from flask_openapi3 import OpenAPI, Info, Server
from models.database import db
from models.user import User
from models.log import Log
from models.menu import Menu
from controllers.user_controller import user_bp
from controllers.git_controller import git_bp
from controllers.log_controller import log_bp
from controllers.menu_controller import menu_bp
from config.config import config
import os
from dotenv import load_dotenv

# 1. 首先根據 FLASK_ENV 決定要載入哪個 .env 文件
env = os.getenv('FLASK_ENV', 'development')
if env == 'production':
    load_dotenv('.env.production')
else:
    load_dotenv('.env.development')

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

# 配置服務器
servers = [
    Server(url=API_URL, description="API 服務器"),
]

# 創建應用實例
app = OpenAPI(__name__, info=info, servers=servers)

# 載入配置
app.config.from_object(config[env])

# 初始化 SQLAlchemy
db.init_app(app)

# CORS配置
CORS(app, 
    resources={
        r"/*": {
            "origins": ["http://localhost:3000", "http://localhost:5173", 
                       "http://127.0.0.1:3000", "http://127.0.0.1:5173",
                       "http://localhost:8080", "http://127.0.0.1:8080"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization", "X-Requested-With"],
            "expose_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True,
            "max_age": 600,
            "send_wildcard": False
        }
    }
)

# 註冊所有藍圖（確保在 db.init_app 之後）
app.register_api(user_bp)
app.register_api(git_bp)
app.register_api(log_bp)
app.register_api(menu_bp)

# 創建所有表（確保在註冊藍圖之後）
with app.app_context():
    db.create_all()
    print("數據庫表已創建")

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=(env == 'development')) 