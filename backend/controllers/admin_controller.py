from flask_openapi3 import APIBlueprint, Tag
from services.admin_service import AdminService
from schemas.admin_schema import *
from flask_jwt_extended import jwt_required, get_jwt_identity
from pydantic import BaseModel, Field
import logging

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

admin_bp = APIBlueprint('admins', __name__, url_prefix='/api/admins')
admin_tag = Tag(name='admins', description='管理員管理')

@admin_bp.get('/', tags=[admin_tag])
@jwt_required()
def get_admins():
    """獲取所有管理員
    
    Returns:
        200: 
            admins (List[AdminResponseSchema]): 管理員列表
        401: 未登入
        500: 服務器錯誤
    """
    try:
        service = AdminService()
        admins = service.get_all_admins()
        return {'admins': [admin.to_dict() for admin in admins]}
    except Exception as e:
        logger.error(f"獲取管理員列表錯誤: {str(e)}", exc_info=True)
        return {'message': f'獲取管理員列表失敗: {str(e)}'}, 500

@admin_bp.post('/', tags=[admin_tag])
@jwt_required()
def create_admin(body: AdminCreateSchema):
    """創建管理員
    
    Args:
        body (AdminCreateSchema): 管理員數據
    
    Returns:
        201 (AdminResponseSchema): 創建成功
        400: 參數錯誤
        401: 未登入
        500: 服務器錯誤
    """
    try:
        service = AdminService()
        admin = service.create_admin(body.dict())
        return admin.to_dict(), 201
    except ValueError as e:
        return {'message': str(e)}, 400
    except Exception as e:
        print(f"創建管理員錯誤: {str(e)}")
        return {'message': '創建管理員失敗'}, 500

@admin_bp.put('/<int:admin_id>', tags=[admin_tag])
@jwt_required()
def update_admin(path: AdminPath, body: AdminUpdateSchema):
    """更新管理員
    
    Args:
        path (AdminPath): 路徑參數
        body (AdminUpdateSchema): 更新數據
    
    Returns:
        200 (AdminResponseSchema): 更新成功
        400: 參數錯誤
        401: 未登入
        404: 管理員不存在
        500: 服務器錯誤
    """
    try:
        service = AdminService()
        admin = service.update_admin(path.admin_id, body.dict(exclude_unset=True))
        if not admin:
            return {'message': '管理員不存在'}, 404
        return admin.to_dict()
    except ValueError as e:
        return {'message': str(e)}, 400
    except Exception as e:
        print(f"更新管理員錯誤: {str(e)}")
        return {'message': '更新管理員失敗'}, 500

@admin_bp.delete('/<int:admin_id>', tags=[admin_tag])
@jwt_required()
def delete_admin(path: AdminPath):
    """刪除管理員
    
    Args:
        path (AdminPath): 路徑參數
    
    Returns:
        204: 刪除成功
        400: 無法刪除超級管理員
        401: 未登入
        404: 管理員不存在
        500: 刪除失敗
    """
    try:
        service = AdminService()
        if service.delete_admin(path.admin_id):
            return '', 204
        return {'message': '管理員不存在'}, 404
    except ValueError as e:
        return {'message': str(e)}, 400
    except Exception as e:
        print(f"刪除管理員錯誤: {str(e)}")
        return {'message': '刪除管理員失敗'}, 500 