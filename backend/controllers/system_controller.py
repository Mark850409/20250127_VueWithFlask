from flask_openapi3 import APIBlueprint, Tag
from services.system_service import SystemService
from schemas.system_schema import ClientIPResponse, ErrorResponse
from flask import request

system_bp = APIBlueprint('system', __name__, url_prefix='/api')
system_tag = Tag(name='system', description='系統相關操作')

@system_bp.get(
    '/client-ip',
    tags=[system_tag],
    responses={
        200: ClientIPResponse,
        500: ErrorResponse
    }
)
def get_client_ip():
    """獲取客戶端 IP 地址
    
    此 API 用於獲取發送請求的客戶端 IP 地址。
    會優先檢查 X-Forwarded-For 請求頭，如果不存在則使用 remote_addr。
    
    Returns:
        200: 成功獲取 IP 地址
            ip (str): 客戶端 IP 地址
        500: 服務器錯誤
            message (str): 錯誤信息
    """
    try:
        service = SystemService()
        ip = service.get_client_ip(request.headers, request.remote_addr)
        return ClientIPResponse(ip=ip).dict()
    except Exception as e:
        return ErrorResponse(message=str(e)).dict(), 500 