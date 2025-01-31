from flask_openapi3 import APIBlueprint, Tag
from services.log_service import LogService
from schemas.log_schema import *
from schemas.user_schema import UserPath
from models.user import User
from pydantic import BaseModel, Field

log_bp = APIBlueprint('logs', __name__, url_prefix='/api/logs')
log_tag = Tag(name='logs', description='系統日誌管理')

@log_bp.get('/', tags=[log_tag])
def get_logs():
    """獲取所有日誌
    
    Returns:
        200 (LogResponseSchema): 日誌列表
        500: 服務器錯誤
    """
    try:
        service = LogService()
        logs = service.get_all_logs()
        return {'logs': [log.to_dict() for log in logs]}
    except Exception as e:
        return {'message': f'獲取日誌失敗: {str(e)}'}, 500

@log_bp.post('/', tags=[log_tag])
def create_log(body: LogCreateSchema):
    """創建日誌
    
    Args:
        body (LogCreateSchema): 日誌數據
        
    Returns:
        201 (LogResponseSchema): 創建成功
        400: 用戶不存在/參數錯誤
        500: 服務器錯誤
        
    Example:
        {
            "user_id": 1,
            "action": "login",
            "description": "用戶登入系統",
            "ip_address": "127.0.0.1",
            "status": "success"
        }
    """
    try:
        service = LogService()
        
        # 檢查用戶是否存在
        if body.user_id:
            user = User.query.get(body.user_id)
            if not user:
                return {'message': '用戶不存在'}, 400
        
        log = service.create_log(body.dict())
        return log.to_dict(), 201
    except ValueError as e:
        return {'message': str(e)}, 400
    except Exception as e:
        return {'message': f'創建日誌失敗: {str(e)}'}, 500

@log_bp.get('/<int:log_id>', tags=[log_tag])
def get_log(path: LogPath):
    """獲取指定日誌
    
    Args:
        path (LogPath): 路徑參數
            log_id (int): 要查詢的日誌ID
            
    Returns:
        200 (LogResponseSchema): 查詢成功
        404: 日誌不存在
        500: 服務器錯誤
    """
    try:
        service = LogService()
        log = service.get_log(path.log_id)
        if not log:
            return {'message': '日誌不存在'}, 404
        return log.to_dict()
    except Exception as e:
        return {'message': f'獲取日誌失敗: {str(e)}'}, 500

@log_bp.get('/user/<int:user_id>', tags=[log_tag])
def get_user_logs(path: UserPath):
    """獲取指定用戶的所有日誌
    
    Args:
        path (UserPath): 路徑參數
            user_id (int): 要查詢的用戶ID
            
    Returns:
        200 (LogResponseSchema): 日誌列表
        404: 用戶不存在
        500: 服務器錯誤
    """
    try:
        service = LogService()
        
        # 檢查用戶是否存在
        user = User.query.get(path.user_id)
        if not user:
            return {'message': '用戶不存在'}, 404
            
        logs = service.get_logs_by_user(path.user_id)
        return {'logs': [log.to_dict() for log in logs]}
    except Exception as e:
        return {'message': f'獲取用戶日誌失敗: {str(e)}'}, 500 