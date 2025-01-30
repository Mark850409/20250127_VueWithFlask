from flask_cors import CORS
from flask_openapi3 import OpenAPI, Info
from models.user import User, db
from controllers.user_controller import user_bp
from controllers.git_controller import git_bp
from config.config import Config

info = Info(title='後台管理系統 API', version='1.0.0', description='Git小助手與用戶管理系統的API文檔')
app = OpenAPI(__name__, info=info)

# 修改 CORS 配置
CORS(app, 
    resources={
        r"/*": {
            "origins": ["http://localhost:3000", "http://localhost:5173", 
                       "http://127.0.0.1:3000", "http://127.0.0.1:5173",
                       "http://localhost:8080", "http://127.0.0.1:8080"],  # 添加所有可能的前端地址
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization", "X-Requested-With"],
            "expose_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True,
            "max_age": 600,
            "send_wildcard": False
        }
    }
)

app.config.from_object(Config)

db.init_app(app)

with app.app_context():
    db.create_all()

# 註冊藍圖 - 移除 url_prefix，因為已經在路由中包含了
app.register_api(user_bp)
app.register_api(git_bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 