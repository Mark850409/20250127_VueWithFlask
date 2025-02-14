from flask_openapi3 import APIBlueprint, Tag
from schemas.langflow_schema import *
from services.langflow_service import LangflowService
from flask import send_file, current_app
import logging
from urllib.parse import unquote, quote
import os
import mimetypes
import base64
from datetime import datetime

logger = logging.getLogger(__name__)
langflow_tag = Tag(name='Langflow_knowledge', description='Langflow 知識庫相關操作')
langflow_bp = APIBlueprint('langflow', __name__, url_prefix='/api/v1/files')

service = LangflowService()

@langflow_bp.post('/upload/<flow_id>', tags=[langflow_tag])
def upload_file(path: LangflowUploadPath, form: LangflowUpload):
    """上傳檔案"""
    try:
        result = service.upload_file(path.flow_id, form.file)
        return {'message': '上傳成功', 'data': result.to_dict()}
    except Exception as e:
        logger.error(f"上傳檔案失敗: {str(e)}")
        return {'message': str(e)}, 400

@langflow_bp.get('/download/<flow_id>/<file_name>', tags=[langflow_tag])
def download_file(path: LangflowPath):
    """下載檔案"""
    try:
        # URL decode 檔名
        decoded_file_name = unquote(path.file_name)
        file_info = service.download_file(path.flow_id, decoded_file_name)
        
        if not file_info:
            return {'message': '檔案不存在'}, 404
            
        file_path = file_info['file_path']
        original_name = file_info['file_name']
        
        # 設置正確的 MIME 類型
        mime_type = mimetypes.guess_type(original_name)[0] or 'application/octet-stream'
        
        # 對中文檔名進行 URL 編碼
        encoded_filename = quote(original_name)
        
        response = send_file(
            file_path,
            as_attachment=True,
            download_name=encoded_filename,  # 使用編碼後的檔名
            mimetype=mime_type
        )
        
        # 設置 Content-Disposition 標頭
        response.headers.set(
            'Content-Disposition',
            "attachment; filename*=utf-8''{}".format(encoded_filename)
        )
        
        # 添加必要的 CORS 標頭
        response.headers.set('Access-Control-Allow-Origin', '*')
        response.headers.set('Access-Control-Expose-Headers', 'Content-Disposition')
        
        return response
        
    except Exception as e:
        logger.error(f"下載檔案失敗: {str(e)}")
        return {'message': str(e)}, 400

@langflow_bp.get('/list/<flow_id>', tags=[langflow_tag])
def list_files(path: LangflowQuery):
    """列出檔案"""
    try:
        files = service.list_files(path.flow_id)
        return {'files': [f.to_dict() for f in files]}
    except Exception as e:
        logger.error(f"列出檔案失敗: {str(e)}")
        return {'message': str(e)}, 400

@langflow_bp.delete('/delete/<flow_id>/<file_name>', tags=[langflow_tag])
def delete_file(path: LangflowPath):
    """刪除檔案"""
    try:
        result = service.delete_file(path.flow_id, path.file_name)
        return {'message': '刪除成功' if result else '刪除失敗'}
    except Exception as e:
        logger.error(f"刪除檔案失敗: {str(e)}")
        return {'message': str(e)}, 400 