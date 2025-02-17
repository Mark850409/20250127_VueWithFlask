from flask_openapi3 import APIBlueprint, Tag
from services.learning_service import LearningService
from schemas.learning_schema import *
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename
import os
import logging
from flask import request

logger = logging.getLogger(__name__)
learning_bp = APIBlueprint('learning', __name__, url_prefix='/api/v1/learning')
learning_tag = Tag(name='learning', description='學習中心管理')

@learning_bp.get('/', tags=[learning_tag])
def get_learning_sections():
    """獲取所有學習區塊
    
    Returns:
        200 (LearningResponseSchema): 學習區塊列表
        500: 服務器錯誤
    """
    try:
        service = LearningService()
        sections = service.get_all_sections()
        return {'sections': sections}
    except Exception as e:
        logger.error(f"獲取學習區塊失敗: {str(e)}")
        return {'message': str(e)}, 500

@learning_bp.post('/sections', tags=[learning_tag])
@jwt_required()
def create_section(body: SectionCreateSchema):
    """創建主標題區塊
    
    Args:
        body: 區塊數據
            title: 標題
            description: 描述
            sort_order: 排序順序
            
    Returns:
        201: 創建成功
        400: 參數錯誤
        500: 服務器錯誤
    """
    try:
        service = LearningService()
        section = service.create_section(body.dict())
        return section, 201
    except Exception as e:
        logger.error(f"創建學習區塊失敗: {str(e)}")
        return {'message': str(e)}, 500

@learning_bp.post('/subsections', tags=[learning_tag])
@jwt_required()
def create_subsection(body: SubsectionCreateSchema):
    """創建次標題區塊
    
    Args:
        body: 子區塊數據
            section_id: 主區塊ID
            title: 標題
            content: 內容
            images: 圖片列表
            sort_order: 排序順序
            
    Returns:
        201: 創建成功
        400: 參數錯誤
        404: 主區塊不存在
        500: 服務器錯誤
    """
    try:
        service = LearningService()
        subsection = service.create_subsection(body.dict())
        return subsection, 201
    except ValueError as e:
        return {'message': str(e)}, 400
    except Exception as e:
        logger.error(f"創建子區塊失敗: {str(e)}")
        return {'message': str(e)}, 500

@learning_bp.put('/sections/<int:section_id>', tags=[learning_tag])
@jwt_required()
def update_section(path: SectionPath, body: SectionUpdateSchema):
    """更新主標題區塊
    
    Args:
        section_id: 區塊ID
        body: 更新數據
            title: 標題
            description: 描述
            sort_order: 排序順序
            
    Returns:
        200: 更新成功
        404: 區塊不存在
        500: 服務器錯誤
    """
    try:
        service = LearningService()
        section = service.update_section(path.section_id, body.dict())
        return section
    except Exception as e:
        logger.error(f"更新區塊失敗: {str(e)}")
        return {'message': str(e)}, 500

@learning_bp.put('/subsections/<int:subsection_id>', tags=[learning_tag])
@jwt_required()
def update_subsection(path: SubsectionPath, body: SubsectionUpdateSchema):
    """更新次標題區塊
    
    Args:
        subsection_id: 子區塊ID
        body: 更新數據
            title: 標題
            content: 內容
            images: 圖片列表
            sort_order: 排序順序
            
    Returns:
        200: 更新成功
        404: 子區塊不存在
        500: 服務器錯誤
    """
    try:
        service = LearningService()
        subsection = service.update_subsection(path.subsection_id, body.dict())
        return subsection
    except Exception as e:
        logger.error(f"更新子區塊失敗: {str(e)}")
        return {'message': str(e)}, 500

@learning_bp.delete('/sections/<int:section_id>', tags=[learning_tag])
@jwt_required()
def delete_section(path: SectionPath):
    """刪除主標題區塊
    
    Args:
        section_id: 區塊ID
        
    Returns:
        204: 刪除成功
        404: 區塊不存在
        500: 服務器錯誤
    """
    try:
        service = LearningService()
        service.delete_section(path.section_id)
        return '', 204
    except Exception as e:
        logger.error(f"刪除區塊失敗: {str(e)}")
        return {'message': str(e)}, 500

@learning_bp.delete('/subsections/<int:subsection_id>', tags=[learning_tag])
@jwt_required()
def delete_subsection(path: SubsectionPath):
    """刪除次標題區塊
    
    Args:
        subsection_id: 子區塊ID
        
    Returns:
        204: 刪除成功
        404: 子區塊不存在
        500: 服務器錯誤
    """
    try:
        service = LearningService()
        service.delete_subsection(path.subsection_id)
        return '', 204
    except Exception as e:
        logger.error(f"刪除子區塊失敗: {str(e)}")
        return {'message': str(e)}, 500

@learning_bp.post(
    '/images',
    tags=[learning_tag],
    responses={
        200: FileUploadResponse,
        400: ErrorResponse,
        500: ErrorResponse
    }
)
@jwt_required()
def upload_image(form: UploadFileForm):
    """上傳圖片
    
    使用 multipart/form-data 格式上傳圖片文件
    
    Request Body:
        file (file): 圖片文件 (支援 jpg、png、gif、webp 格式，最大 5MB)
    
    Returns:
        200 (FileUploadResponse):
            url (str): 圖片URL
            message (str): 成功信息
        400 (ErrorResponse): 文件格式錯誤
        500 (ErrorResponse): 上傳失敗
    """
    try:
        if not form.file:
            return ErrorResponse(message='未上傳文件').dict(), 400
            
        service = LearningService()
        image_url = service.upload_image(form.file)
        
        return FileUploadResponse(
            url=image_url,
            message='圖片上傳成功'
        ).dict()
        
    except ValueError as e:
        return ErrorResponse(message=str(e)).dict(), 400
    except Exception as e:
        logger.error(f"上傳圖片失敗: {str(e)}")
        return ErrorResponse(message=f'上傳圖片失敗: {str(e)}').dict(), 500 