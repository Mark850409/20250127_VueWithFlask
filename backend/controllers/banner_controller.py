from flask import jsonify
from flask_openapi3 import APIBlueprint, Tag
from flask_jwt_extended import jwt_required
from services.banner_service import BannerService
from schemas.banner_schema import (
    BannerPath, BannerResponse, 
    BannerListResponse, BannerCreateBody, 
    BannerUpdateBody, MessageResponse, BannerTypeParam
)

banner_bp = APIBlueprint('banner', __name__, url_prefix='/api/v1')
banner_service = BannerService()
banner_tag = Tag(name='Banner', description='輪播圖管理相關API')

@banner_bp.get(
    '/banners',
    tags=[banner_tag],
    responses={
        "200": BannerListResponse,
    }
)
def get_banners():
    """獲取所有啟用的輪播圖"""
    banners = banner_service.get_active_banners()
    return jsonify(banners)

@banner_bp.get(
    '/admin/banners',
    tags=[banner_tag],
    responses={
        "200": BannerListResponse,
        "401": MessageResponse
    }
)
@jwt_required()
def get_all_banners():
    """管理員獲取所有輪播圖"""
    banners = banner_service.get_all_banners()
    return jsonify(banners)

@banner_bp.post(
    '/admin/banners',
    tags=[banner_tag],
    responses={
        "201": BannerResponse,
        "400": MessageResponse,
        "401": MessageResponse
    }
)
@jwt_required()
def create_banner(body: BannerCreateBody):
    """創建新的輪播圖"""
    banner = banner_service.create_banner(body)
    return jsonify(banner), 201

@banner_bp.put(
    '/admin/banners/<int:banner_id>',
    tags=[banner_tag],
    responses={
        "200": BannerResponse,
        "400": MessageResponse,
        "401": MessageResponse,
        "404": MessageResponse
    }
)
@jwt_required()
def update_banner(path: BannerPath, body: BannerUpdateBody):
    """更新輪播圖"""
    banner = banner_service.update_banner(path.banner_id, body)
    if banner:
        return jsonify(banner)
    return jsonify({'message': 'Banner not found'}), 404

@banner_bp.delete(
    '/admin/banners/<int:banner_id>',
    tags=[banner_tag],
    responses={
        "200": MessageResponse,
        "401": MessageResponse,
        "404": MessageResponse
    }
)
@jwt_required()
def delete_banner(path: BannerPath):
    """刪除輪播圖"""
    success = banner_service.delete_banner(path.banner_id)
    if success:
        return jsonify({'message': 'Banner deleted successfully'})
    return jsonify({'message': 'Banner not found'}), 404

@banner_bp.get(
    '/banners/<string:banner_type>',
    tags=[banner_tag],
    responses={
        "200": BannerListResponse,
        "400": MessageResponse
    }
)
def get_banners_by_type(path: BannerTypeParam):
    """獲取指定類型的輪播圖（只返回已啟用的）
    
    Args:
        banner_type: 輪播圖類型 (home/features/learning/pricing)
    """
    try:
        banners = banner_service.get_banners_by_type(path.banner_type)
        return jsonify(banners)
    except ValueError as e:
        return jsonify({
            'message': f'Invalid banner type. Must be one of: home, features, learning, pricing'
        }), 400 