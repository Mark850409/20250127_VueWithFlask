from flask_openapi3 import Info, Server
from config.config import API_URL, FOODPANDA_RECOMMENDATION_URL, FOODPANDA_SERVICE_URL

# API 信息配置
info = Info(
    title='點餐推薦系統 API', 
    version='1.0.0', 
    description='點餐推薦系統系統的API文檔'
)

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
    ),
    Server(
        url='https://mylangflow0108.zeabur.app',
        description='Langflow 生產環境'
    )
]

# 安全配置
security_schemes = {
    'Bearer': {
        'type': 'http',
        'scheme': 'bearer',
        'bearerFormat': 'JWT',
        'description': '請輸入 JWT token，格式為：Bearer your-token-here'
    },
    'ApiKeyAuth': {
        "type": "apiKey",
        "name": "x-disco-client-id",
        "in": "header",
        "description": "Foodpanda API 需要的 client ID，請輸入: web"
    }
} 