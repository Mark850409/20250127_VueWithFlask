from flask_openapi3 import APIBlueprint, Tag
from schemas.langflow_schema import FolderPath, FolderCreate, FolderUpdate, FolderDownloadResponse
from services.langflow_folder_service import FolderService
import logging
from flask import Response
# 設定 logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
folder_tag = Tag(name='Langflow_folder', description='Langflow 專案相關操作')
folder_bp = APIBlueprint('folder', __name__, url_prefix='/api/v1/folders')

service = FolderService()

@folder_bp.get('/', tags=[folder_tag])
def read_folders():
    """讀取所有專案"""
    try:
        folders = service.get_all_folders()
        return folders
    except Exception as e:
        logger.error(f"讀取專案失敗: {str(e)}")
        return {'message': f"讀取專案失敗: {str(e)}"}, 400

@folder_bp.post('/', tags=[folder_tag])
def create_folder(body: FolderCreate):
    """建立專案"""
    try:
        # 將 pydantic 模型轉換為字典
        folder_data = {
            "name": body.name,
            "description": body.description,
            "components_list": body.components_list,
            "flows_list": body.flows_list
        }
        folder = service.create_folder(folder_data)
        return {'message': '建立成功', 'data': folder}
    except Exception as e:
        logger.error(f"建立專案失敗: {str(e)}")
        return {'message': str(e)}, 400

@folder_bp.get('/<folder_id>', tags=[folder_tag])
def read_folder(path: FolderPath):
    """讀取單一專案"""
    try:
        folder = service.get_folder(path.folder_id)
        if not folder:
            return {'message': '專案不存在'}, 404
        return folder
    except Exception as e:
        logger.error(f"讀取專案失敗: {str(e)}")
        return {'message': str(e)}, 400

@folder_bp.patch('/<folder_id>', tags=[folder_tag])
def update_folder(path: FolderPath, body: FolderUpdate):
    """更新專案"""
    try:
        # 將 pydantic 模型轉換為字典
        folder_data = {
            "name": body.name,
            "description": body.description,
            "parent_id": body.parent_id,
            "components": body.components,
            "flows": body.flows
        }
        folder = service.update_folder(path.folder_id, folder_data)
        if not folder:
            return {'message': '專案不存在'}, 404
        return folder
    except Exception as e:
        logger.error(f"更新專案失敗: {str(e)}")
        return {'message': str(e)}, 400

@folder_bp.delete('/<folder_id>', tags=[folder_tag])
def delete_folder(path: FolderPath):
    """刪除專案"""
    try:
        result = service.delete_folder(path.folder_id)
        return {'message': '刪除成功' if result else '刪除失敗'}
    except Exception as e:
        logger.error(f"刪除專案失敗: {str(e)}")
        return {'message': str(e)}, 400


@folder_bp.get(
    '/download/<folder_id>', 
    tags=[folder_tag],
    responses={
        200: FolderDownloadResponse,
        404: {"description": "專案不存在或無法生成 ZIP"},
        400: {"description": "下載失敗"}
    }
)
def download_folder(path: FolderPath):
    """下載單一專案下面的所有專案"""
    try:
        result = service.download_folder(path.folder_id)
        if not result:
            return {'message': '專案不存在或無法下載'}, 404

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
        logger.error(f"下載專案失敗: {str(e)}")
        return {'message': str(e)}, 400