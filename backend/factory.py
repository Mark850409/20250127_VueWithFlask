from flask_openapi3 import OpenAPI
from flask import request, send_from_directory
from config.config import Config
from config.api_info import info, servers, security_schemes
from config.app_config import init_app
from controllers import (
    user_bp, git_bp, log_bp, menu_bp, store_bp, rating_bp,
    message_bp, admin_bp, favorite_bp, foodpanda_core_bp,
    foodpanda_vendors_bp, foodpanda_menu_bp, foodpanda_feed_bp,
    googlemaps_bp, system_bp, googlemaps_info_bp, dashboard_bp,
    recommend_bp
)


def create_app():
    """創建應用實例"""
    app = OpenAPI(__name__, info=info, servers=servers)
    
    # 載入配置
    app.config.from_object(Config)
    
    # 註冊所有藍圖
    blueprints = [
        user_bp, git_bp, log_bp, menu_bp, store_bp, rating_bp,
        message_bp, admin_bp, favorite_bp, foodpanda_core_bp,
        foodpanda_vendors_bp, foodpanda_menu_bp, foodpanda_feed_bp,
        googlemaps_bp, system_bp, googlemaps_info_bp, dashboard_bp,
        recommend_bp
    ]
    


    for blueprint in blueprints:
        app.register_api(blueprint)
    
    # 設置安全方案
    if 'components' not in app.api_doc:
        app.api_doc['components'] = {}
    app.api_doc['components']['securitySchemes'] = security_schemes
    app.api_doc['security'] = [{'Bearer': []}, {'ApiKeyAuth': []}]
    
    # 初始化應用
    init_app(app)
    
    # 添加靜態文件路由
    @app.route('/api/users/avatar/<path:filename>')
    def get_avatar(filename):
        return send_from_directory(app.config['AVATAR_FOLDER'], filename)

    @app.route('/api/stores/uploads/stores/<path:filename>')
    def get_store_image(filename):
        return send_from_directory(app.config['STORE_FOLDER'], filename)
    
    # CORS 預檢請求處理
    @app.after_request
    def after_request(response):
        origin = request.headers.get('Origin')
        response.headers.update({
            'Access-Control-Allow-Origin': origin,
            'Access-Control-Allow-Credentials': 'true',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Requested-With, Origin'
        })
        return response
    
    return app 