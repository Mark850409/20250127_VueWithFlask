from flask_openapi3 import APIBlueprint, Tag
from services.dashboard_service import DashboardService
from schemas.dashboard_schema import (
    DashboardStatsResponse, BasicStatsResponse, TopShopsResponse,
    LatestReviewsResponse, SystemLogsResponse, ActivityDataResponse
)
from flask_jwt_extended import jwt_required, get_jwt_identity
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)
dashboard_bp = APIBlueprint('dashboard', __name__, url_prefix='/api/dashboard')
dashboard_tag = Tag(name='dashboard', description='儀表板數據')

# 定義空的請求模型
class EmptyRequest(BaseModel):
    pass

@dashboard_bp.get(
    '/stats/',
    tags=[dashboard_tag],
    summary='獲取完整儀表板統計數據',
    description='獲取系統所有統計數據（向後兼容）',
    responses={"200": DashboardStatsResponse},
    security=[{"Bearer": []}]
)
@jwt_required()
def get_dashboard_stats(query: EmptyRequest):
    try:
        service = DashboardService()
        return service.get_stats()
    except Exception as e:
        logger.error(f"獲取儀表板數據失敗: {str(e)}")
        return {'error': '服務器錯誤'}, 500

@dashboard_bp.get(
    '/basic-stats/',
    tags=[dashboard_tag],
    summary='獲取基本統計數據',
    description='獲取用戶數、店家數等基本統計數據',
    responses={"200": BasicStatsResponse},
    security=[{"Bearer": []}]
)
@jwt_required()
def get_basic_stats(query: EmptyRequest):
    try:
        service = DashboardService()
        return service.get_basic_stats()
    except Exception as e:
        logger.error(f"獲取基本統計數據失敗: {str(e)}")
        return {'error': '服務器錯誤'}, 500

@dashboard_bp.get(
    '/top-shops/',
    tags=[dashboard_tag],
    summary='獲取熱門店家',
    description='獲取評分最高的店家列表',
    responses={"200": TopShopsResponse},
    security=[{"Bearer": []}]
)
@jwt_required()
def get_top_shops(query: EmptyRequest):
    try:
        service = DashboardService()
        return service.get_top_shops()
    except Exception as e:
        logger.error(f"獲取熱門店家失敗: {str(e)}")
        return {'error': '服務器錯誤'}, 500

@dashboard_bp.get(
    '/latest-reviews/',
    tags=[dashboard_tag],
    summary='獲取最新評論',
    description='獲取最新的用戶評論列表',
    responses={"200": LatestReviewsResponse},
    security=[{"Bearer": []}]
)
@jwt_required()
def get_latest_reviews(query: EmptyRequest):
    try:
        service = DashboardService()
        return service.get_latest_reviews()
    except Exception as e:
        logger.error(f"獲取最新評論失敗: {str(e)}")
        return {'error': '服務器錯誤'}, 500

@dashboard_bp.get(
    '/system-logs/',
    tags=[dashboard_tag],
    summary='獲取系統日誌',
    description='獲取最新的系統操作日誌',
    responses={"200": SystemLogsResponse},
    security=[{"Bearer": []}]
)
@jwt_required()
def get_system_logs(query: EmptyRequest):
    try:
        service = DashboardService()
        return service.get_system_logs()
    except Exception as e:
        logger.error(f"獲取系統日誌失敗: {str(e)}")
        return {'error': '服務器錯誤'}, 500

@dashboard_bp.get(
    '/activity-data/',
    tags=[dashboard_tag],
    summary='獲取活動數據',
    description='獲取用戶活躍度統計數據',
    responses={"200": ActivityDataResponse},
    security=[{"Bearer": []}]
)
@jwt_required()
def get_activity_data(query: EmptyRequest):
    try:
        service = DashboardService()
        return service.get_activity_data()
    except Exception as e:
        logger.error(f"獲取活動數據失敗: {str(e)}")
        return {'error': '服務器錯誤'}, 500 