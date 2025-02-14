from flask_openapi3 import APIBlueprint, Tag
from schemas.langflow_schema import FolderPath, FolderCreate, FolderUpdate, FolderDownloadResponse
from services.folder_service import FolderService
from flask import send_file, jsonify, make_response
import logging
from datetime import datetime
import os
import uuid
import json
from flask import Response
import requests
# 設定 logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
folder_tag = Tag(name='Langflow_folder', description='Langflow 資料夾相關操作')
folder_bp = APIBlueprint('folder', __name__, url_prefix='/api/v1/folders')

service = FolderService()

@folder_bp.get('/', tags=[folder_tag])
def read_folders():
    """讀取所有資料夾"""
    try:
        folders = service.get_all_folders()
        return {'folders': [f.to_dict() for f in folders]}
    except Exception as e:
        logger.error(f"讀取資料夾失敗: {str(e)}")
        return {'message': str(e)}, 400

@folder_bp.post('/', tags=[folder_tag])
def create_folder(body: FolderCreate):
    """建立資料夾"""
    try:
        folder = service.create_folder(body.dict())
        return {'message': '建立成功', 'data': folder.to_dict()}
    except Exception as e:
        logger.error(f"建立資料夾失敗: {str(e)}")
        return {'message': str(e)}, 400

@folder_bp.get('/<folder_id>', tags=[folder_tag])
def read_folder(path: FolderPath):
    """讀取單一資料夾"""
    try:
        folder = service.get_folder(path.folder_id)
        if not folder:
            return {'message': '資料夾不存在'}, 404
        return folder.to_dict()
    except Exception as e:
        logger.error(f"讀取資料夾失敗: {str(e)}")
        return {'message': str(e)}, 400

@folder_bp.patch('/<folder_id>', tags=[folder_tag])
def update_folder(path: FolderPath, body: FolderUpdate):
    """更新資料夾"""
    try:
        folder = service.update_folder(path.folder_id, body.dict(exclude_unset=True))
        if not folder:
            return {'message': '資料夾不存在'}, 404
        return {'message': '更新成功', 'data': folder.to_dict()}
    except Exception as e:
        logger.error(f"更新資料夾失敗: {str(e)}")
        return {'message': str(e)}, 400

@folder_bp.delete('/<folder_id>', tags=[folder_tag])
def delete_folder(path: FolderPath):
    """刪除資料夾"""
    try:
        result = service.delete_folder(path.folder_id)
        return {'message': '刪除成功' if result else '刪除失敗'}
    except Exception as e:
        logger.error(f"刪除資料夾失敗: {str(e)}")
        return {'message': str(e)}, 400


@folder_bp.get(
    '/download/<folder_id>', 
    tags=[folder_tag],
    responses={
        200: FolderDownloadResponse,
        404: {"description": "資料夾不存在或無法生成 ZIP"},
        400: {"description": "下載失敗"}
    }
)
def download_folder(path: FolderPath):
    """下載資料夾"""
    try:
        result = service.download_folder(path.folder_id)
        if not result:
            return {'message': '資料夾不存在或無法下載'}, 404

        zip_data, filename = result

        # 建立 Flask Response
        return Response(
            response=zip_data,
            mimetype='application/zip',
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )

    except Exception as e:
        logger.error(f"下載資料夾失敗: {str(e)}")
        return {'message': str(e)}, 400