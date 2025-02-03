from flask_openapi3 import APIBlueprint, Tag
from services.store_service import StoreService
from services.store_crawler_service import StoreCrawlerService
from flask_jwt_extended import jwt_required
from schemas.store_schema import *
import os
from werkzeug.utils import secure_filename
from flask import request, current_app
from datetime import datetime

store_bp = APIBlueprint('stores', __name__, url_prefix='/api/stores')
store_tag = Tag(name='stores', description='店家管理')

@store_bp.get('/', tags=[store_tag])
def get_stores():
    """獲取所有店家
    
    Returns:
        200 (StoreResponseSchema): 店家列表
        500: 服務器錯誤
    """
    try:
        service = StoreService()
        stores = service.get_all_stores()
        return {'stores': [store.to_dict() for store in stores]}
    except Exception as e:
        return {'message': f'獲取店家列表失敗: {str(e)}'}, 500

@store_bp.post('/', tags=[store_tag])
def create_store(body: StoreCreateSchema):
    """創建店家
    
    Args:
        body (StoreCreateSchema): 店家數據
        
    Returns:
        201 (StoreResponseSchema): 創建成功
        400: 參數錯誤
        500: 服務器錯誤
    """
    try:
        service = StoreService()
        store = service.create_store(body.dict())
        return store.to_dict(), 201
    except ValueError as e:
        return {'message': str(e)}, 400
    except Exception as e:
        return {'message': f'創建店家失敗: {str(e)}'}, 500

@store_bp.get('/<int:store_id>', tags=[store_tag])
def get_store(path: StorePath):
    """獲取指定店家
    
    Args:
        path (StorePath): 路徑參數
            store_id (int): 店家ID
            
    Returns:
        200 (StoreResponseSchema): 查詢成功
        404: 店家不存在
        500: 服務器錯誤
    """
    try:
        service = StoreService()
        store = service.get_store(path.store_id)
        if not store:
            return {'message': '店家不存在'}, 404
            
        # 增加瀏覽次數
        service.view_store(path.store_id)
        return store.to_dict()
    except Exception as e:
        return {'message': f'獲取店家失敗: {str(e)}'}, 500

@store_bp.put('/<int:store_id>', tags=[store_tag])
def update_store(path: StorePath, body: StoreUpdateSchema):
    """更新店家
    
    Args:
        path (StorePath): 路徑參數
            store_id (int): 店家ID
        body (StoreUpdateSchema): 更新數據
            
    Returns:
        200 (StoreResponseSchema): 更新成功
        404: 店家不存在
        500: 服務器錯誤
    """
    try:
        service = StoreService()
        store = service.get_store(path.store_id)
        if not store:
            return {'message': '店家不存在'}, 404
            
        store = service.update_store(path.store_id, body.dict(exclude_unset=True))
        return store.to_dict()
    except Exception as e:
        return {'message': f'更新店家失敗: {str(e)}'}, 500

@store_bp.delete('/<int:store_id>', tags=[store_tag])
def delete_store(path: StorePath):
    """刪除店家
    
    Args:
        path (StorePath): 路徑參數
            store_id (int): 店家ID
            
    Returns:
        204: 刪除成功
        404: 店家不存在
        500: 刪除失敗
        
    Example:
        DELETE /api/stores/1
    """
    try:
        service = StoreService()
        store = service.get_store(path.store_id)
        if not store:
            return {'message': '店家不存在'}, 404
            
        if service.delete_store(path.store_id):
            return '', 204
        return {'message': '刪除失敗'}, 500
    except Exception as e:
        return {'message': f'刪除店家失敗: {str(e)}'}, 500

@store_bp.get('/city/<string:city>', tags=[store_tag])
def get_stores_by_city(path: CityPath):
    """獲取指定城市的店家
    
    Args:
        path (CityPath): 路徑參數
            city (str): 城市名稱，例如：台北、台中、高雄
            
    Returns:
        200 (StoreResponseSchema): 店家列表
            stores (List[Store]): 店家列表
        500: 服務器錯誤
    
    Example:
        GET /api/stores/city/台北
        
    Response Example:
        {
            "stores": [
                {
                    "id": 1,
                    "name": "春水堂",
                    "address": "台北市信義區信義路五段7號",
                    "city": "台北市",
                    "phone": "02-27201234",
                    "business_hours": "10:00-22:00",
                    "description": "台灣珍珠奶茶始祖",
                    "image_url": "https://example.com/store.jpg",
                    "status": "active",
                    "views": 100,
                    "avg_rating": 4.5,
                    "rating_count": 10,
                    "comment_count": 5,
                    "created_at": "2024-01-31 10:00:00",
                    "updated_at": "2024-01-31 10:00:00"
                }
            ]
        }
    """
    try:
        service = StoreService()
        stores = service.get_stores_by_city(path.city)
        return {'stores': [store.to_dict() for store in stores]}
    except Exception as e:
        return {'message': f'獲取店家列表失敗: {str(e)}'}, 500

@store_bp.get('/crawl', tags=[store_tag])
@jwt_required()
def crawl_stores():
    """爬取 Foodpanda 餐廳資料
    
    此端點會爬取 Foodpanda 上的飲料店資料並立即存入資料庫
    
    Returns:
        200 (StoreCrawlerResponse): 爬取成功
            message (str): 成功信息
            data (dict): 爬取統計數據
                total_fetched (int): 總抓取筆數
                fetched_by_city (dict): 各縣市抓取筆數
                total_duration_seconds (int): 總耗時(秒)
        500 (ErrorResponse): 服務器錯誤
            message (str): 錯誤信息
    
    Response Example:
        {
            "message": "資料抓取完成",
            "data": {
                "total_fetched": 100,
                "fetched_by_city": {
                    "台北市": 30,
                    "新北市": 25,
                    "桃園市": 45
                },
                "total_duration_seconds": 300
            }
        }
    
    Error Example:
        {
            "message": "爬取資料失敗: 連接超時"
        }
    """
    try:
        service = StoreCrawlerService()
        result = service.crawl_restaurants()
        return result
    except Exception as e:
        error_response = ErrorResponse(message=f'爬取資料失敗: {str(e)}')
        return error_response.dict(), 500

@store_bp.post(
    '/upload',
    tags=[store_tag],
    responses={
        "200": FileUploadResponse,
        "400": ErrorResponse,
        "500": ErrorResponse
    }
)
@jwt_required()
def upload_image(form: UploadFileForm):
    """
    上傳店家圖片


    responses:
      200:
        description: 上傳成功
        content:
          application/json:
            schema:
              type: object
              properties:
                url:
                  type: string
                message:
                  type: string
      400:
        description: 參數錯誤
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
      500:
        description: 服務器錯誤
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
    """
    try:
        print("接收到的文件:", request.files)  # 調試用
        if 'file' not in request.files:
            print("未找到文件字段，可用字段:", list(request.files.keys()))  # 調試用
            return {'message': '未找到上傳的圖片'}, 400
            
        file = request.files['file']
        if file.filename == '':
            return {'message': '未選擇圖片'}, 400
            
        if not file or not allowed_file(file.filename):
            return {'message': '不支援的圖片格式'}, 400
        
        # 生成安全的文件名
        filename = secure_filename(file.filename)
        # 添加時間戳避免重名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        
        # 確保上傳目錄存在
        upload_folder = os.path.join(current_app.root_path, 'uploads', 'stores')
        os.makedirs(upload_folder, exist_ok=True)
        
        # 打印完整的文件路徑
        file_path = os.path.join(upload_folder, filename)
        print("準備保存文件到:", file_path)  # 調試用
        
        # 保存文件
        file.save(file_path)
        
        # 返回可訪問的URL
        url = f"/uploads/stores/{filename}"
        print("返回的URL:", url)  # 調試用
        return {'url': url}
        
    except Exception as e:
        print(f"上傳過程中發生錯誤: {str(e)}")  # 調試用
        import traceback
        print("錯誤堆疊:", traceback.format_exc())  # 打印完整錯誤堆疊
        return {'message': f'圖片上傳失敗: {str(e)}'}, 500

def allowed_file(filename):
    """檢查文件類型是否允許"""
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS 