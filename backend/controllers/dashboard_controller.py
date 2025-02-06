from flask_openapi3 import APIBlueprint, Tag
from services.dashboard_service import DashboardService
from schemas.dashboard_schema import DashboardStatsResponse
from flask_jwt_extended import jwt_required, get_jwt_identity
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)
dashboard_bp = APIBlueprint('dashboard', __name__, url_prefix='/api/dashboard')
dashboard_tag = Tag(name='dashboard', description='儀表板數據')

# 定義空的請求模型（因為GET請求不需要請求體）
class EmptyRequest(BaseModel):
    pass

@dashboard_bp.get(
    '/stats/',  # 添加結尾斜線以匹配前端請求
    tags=[dashboard_tag],
    summary='獲取儀表板統計數據',
    description='獲取系統整體統計數據，包括用戶數、店家數、評論數等',
    responses={
        "200": DashboardStatsResponse,
        "401": {"description": "未授權訪問"},
        "500": {"description": "服務器錯誤"}
    },
    security=[{"Bearer": []}]
)
@jwt_required()
def get_dashboard_stats(query: EmptyRequest):
    """獲取儀表板統計數據
    
    Returns:
        200: 成功返回統計數據
        401: 未授權訪問
        500: 服務器錯誤
    """
    try:
        service = DashboardService()
        return service.get_stats()
    except Exception as e:
        logger.error(f"獲取儀表板數據失敗: {str(e)}")
        return {'error': '服務器錯誤'}, 500 