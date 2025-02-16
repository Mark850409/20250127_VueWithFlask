import os
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mail import Mail
from models.database import db
from extensions import jwt
from services.googlemaps_service import GoogleMapsService
from config.config import GOOGLE_MAPS_API_KEY
from services.mail_service import mail

def init_app(app):
    """初始化應用配置"""
    # 初始化 JWT
    jwt.init_app(app)
    
    # JWT 錯誤處理
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return {'msg': '不合法的token，請重新輸入!!!'}, 401

    @jwt.unauthorized_loader
    def unauthorized_callback(error):
        return {'msg': '缺少正確的token驗證表頭，請重新輸入!!!'}, 401

    # 初始化數據庫
    db.init_app(app)
    with app.app_context():
        db.create_all()
        print("數據庫表已創建")

    # 配置 CORS
    setup_cors(app)
    
    # 配置上傳目錄
    setup_upload_folders(app)
    
    # 配置 Google Maps Service
    GoogleMapsService(GOOGLE_MAPS_API_KEY)

    # 初始化 Mail
    mail.init_app(app)

def setup_cors(app):
    """設置 CORS"""
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '').split(',')
    CORS(app, 
        resources={
            r"/*": {
                "origins": CORS_ORIGINS,
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
                "allow_headers": "*",
                "expose_headers": ["Content-Type", "Authorization"],
                "supports_credentials": True,
                "max_age": 3600
            }
        }
    )

def setup_upload_folders(app):
    """設置上傳目錄"""
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['AVATAR_FOLDER'] = os.path.join('uploads', 'avatars')
    app.config['STORE_FOLDER'] = os.path.join('uploads', 'stores')
    
    os.makedirs(app.config['AVATAR_FOLDER'], exist_ok=True)
    os.makedirs(app.config['STORE_FOLDER'], exist_ok=True) 