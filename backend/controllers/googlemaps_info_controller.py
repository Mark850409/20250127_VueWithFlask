from flask_openapi3 import APIBlueprint, Tag
from services.googlemaps_info_service import GoogleMapsInfoService
from schemas.googlemaps_info_schema import *
from utils.sqlfunctions import execute_query
from models.database import db

googlemaps_info_bp = APIBlueprint('googlemaps_info', __name__, url_prefix='/api/googlemaps-info')
googlemaps_info_tag = Tag(name='googlemaps_info', description='Google Maps 資訊管理')

@googlemaps_info_bp.post(
    '/process',
    tags=[googlemaps_info_tag],
    responses={
        200: ProcessSuccessResponse,
        500: ProcessErrorResponse
    }
)
def process_stores():
    """
    處理店家資料並獲取 Google Maps 資訊
    
    此 API 會:
    1. 從資料庫獲取所有店家資料
    2. 使用 Google Maps API 獲取每個店家的 Place ID
    3. 生成每個店家的導航連結
    4. 將新資料保存到資料庫和 CSV 檔案
    
    Returns:
        200 (ProcessSuccessResponse):
            success: bool - 是否成功
            message: str - 處理結果訊息
            total_processed: int - 總處理筆數
            new_records: int - 新增筆數
            
        500 (ProcessErrorResponse):
            success: bool - 失敗
            message: str - 錯誤訊息
            error: str - 詳細錯誤資訊
    """
    try:
        # 查詢店家資料
        sql_query = """
            SELECT id, normalized_name, latitude, longitude, address, city, city_CN, redirection_url 
            FROM stores;
        """
        store_data = execute_query(db.session, sql_query)
        
        # 處理資料
        service = GoogleMapsInfoService()
        result = service.process_store_data(store_data)
        
        if result['success']:
            return ProcessSuccessResponse(
                success=True,
                message=result['message'],
                total_processed=result['total_processed'],
                new_records=result['new_records']
            ).dict(), 200
        else:
            return ProcessErrorResponse(
                success=False,
                message=result['message'],
                error=result.get('error', '未知錯誤')
            ).dict(), 500
            
    except Exception as e:
        return ProcessErrorResponse(
            success=False,
            message='處理資料失敗',
            error=str(e)
        ).dict(), 500 