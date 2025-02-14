from flask_openapi3 import APIBlueprint, Tag
from schemas.langflow_schema import *
from services.langflow_service import LangflowService
from flask import send_file, request
import logging
from urllib.parse import unquote, quote
import os
import mimetypes
import base64
from datetime import datetime
import io


logger = logging.getLogger(__name__)
langflow_tag = Tag(name='Langflow_knowledge', description='Langflow 知識庫相關操作')
langflow_bp = APIBlueprint('langflow', __name__, url_prefix='/api/v1/files')

service = LangflowService()

@langflow_bp.post('/upload/<flow_id>', tags=[langflow_tag])
def upload_file(path: LangflowUploadPath, form: LangflowUpload):
    """上傳檔案"""
    try:
        if not form.file:
            return {'message': '未選擇檔案'}, 400
            
        file = form.file
        result = service.upload_file(
            flow_id=path.flow_id,
            file_data=file.read(),
            file_name=file.filename
        )
        return result
    except Exception as e:
        logger.error(f"上傳檔案失敗: {str(e)}")
        return {'message': str(e)}, 400

@langflow_bp.get('/download/<flow_id>/<file_name>', tags=[langflow_tag])
def download_file(path: LangflowPath):
    """下載檔案"""
    try:
        decoded_file_name = unquote(path.file_name)
        file_info = service.download_file(path.flow_id, decoded_file_name)
        
        if not file_info:
            return {'message': '檔案不存在'}, 404
            
        response = send_file(
            io.BytesIO(file_info['file_data']),
            mimetype=file_info['content_type'],
            as_attachment=True,
            download_name=file_info['file_name']
        )
        
        response.headers.set('Access-Control-Allow-Origin', '*')
        response.headers.set('Access-Control-Expose-Headers', 'Content-Disposition')
        
        return response
    except Exception as e:
        logger.error(f"下載檔案失敗: {str(e)}")
        return {'message': str(e)}, 400

@langflow_bp.post('/batch-download', tags=[langflow_tag])
def batch_download():
    """批次下載檔案"""
    try:
        # 從請求中獲取 flow_id 和檔案列表
        data = request.get_json()
        flow_id = data.get('flowId')
        file_names = data.get('fileNames', [])
        
        if not flow_id or not file_names:
            return {'message': '參數錯誤'}, 400
        
        # 呼叫 service 層的批次下載方法
        memory_file, zip_filename = service.batch_download(flow_id, file_names)
        
        return send_file(
            memory_file,
            mimetype='application/zip',
            as_attachment=True,
            download_name=zip_filename
        )
    except Exception as e:
        logger.error(f"批次下載失敗: {str(e)}")
        return {'message': str(e)}, 400

@langflow_bp.get('/list/<flow_id>', tags=[langflow_tag])
def list_files(path: LangflowQuery):
    """列出檔案"""
    try:
        files = service.list_files(path.flow_id)
        return {'status': 'success', 'files': files}
    except Exception as e:
        logger.error(f"列出檔案失敗: {str(e)}")
        return {'message': str(e)}, 400

@langflow_bp.delete('/delete/<flow_id>/<file_name>', tags=[langflow_tag])
def delete_file(path: LangflowPath):
    """刪除檔案"""
    try:
        decoded_file_name = unquote(path.file_name)
        result = service.delete_file(path.flow_id, decoded_file_name)
        return result
    except Exception as e:
        logger.error(f"刪除檔案失敗: {str(e)}")
        return {'message': str(e)}, 400 