from flask_openapi3 import APIBlueprint, Tag
from flask import jsonify, current_app
from services.googlemaps_service import GoogleMapsService
from schemas.googlemaps_schema import *
import logging

logger = logging.getLogger(__name__)
googlemaps_tag = Tag(name='googlemaps', description='Google Maps API')

# 創建藍圖
googlemaps_bp = APIBlueprint('googlemaps', __name__, url_prefix='/api/v1/maps')

@googlemaps_bp.get(
    '/places/find',
    tags=[googlemaps_tag],
    responses={"200": PlaceResponse, "400": ErrorResponse, "500": ErrorResponse}
)
def find_place(query: PlaceQuery):
    """
    搜尋地點
    
    根據輸入文字搜尋地點，返回地點ID
    """
    try:
        service = GoogleMapsService(current_app.config['GOOGLE_MAPS_API_KEY'])
        result = service.find_place(query.input)
        return jsonify(result)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"搜尋地點失敗: {str(e)}")
        return jsonify({'error': '服務器錯誤'}), 500

@googlemaps_bp.get(
    '/places/details',
    tags=[googlemaps_tag],
    responses={"200": PlaceDetailsResponse, "400": ErrorResponse, "500": ErrorResponse}
)
def get_place_details(query: PlaceDetailsQuery):
    """
    獲取地點詳細資訊
    
    根據地點ID獲取詳細資訊，包括評論
    """
    try:
        service = GoogleMapsService(current_app.config['GOOGLE_MAPS_API_KEY'])
        result = service.get_place_details(
            query.place_id,
            query.language
        )
        return jsonify(result)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"獲取地點詳細資訊失敗: {str(e)}")
        return jsonify({'error': '服務器錯誤'}), 500

@googlemaps_bp.get(
    '/places/nearby',
    tags=[googlemaps_tag],
    responses={"200": NearbySearchResponse, "400": ErrorResponse, "500": ErrorResponse}
)
def search_nearby(query: NearbySearchQuery):
    """
    搜尋附近地點
    
    根據經緯度搜尋指定半徑內的地點
    """
    try:
        service = GoogleMapsService(current_app.config['GOOGLE_MAPS_API_KEY'])
        result = service.search_nearby(
            latitude=query.latitude,
            longitude=query.longitude,
            radius=query.radius,
            place_type=query.place_type,
            keyword=query.keyword
        )
        return jsonify(result)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"搜尋附近地點失敗: {str(e)}")
        return jsonify({'error': '服務器錯誤'}), 500

@googlemaps_bp.get(
    '/navigation',
    tags=[googlemaps_tag],
    responses={"200": NavigationResponse, "400": ErrorResponse, "500": ErrorResponse}
)
def get_navigation(query: NavigationQuery):
    """
    獲取導航 URL
    
    根據起點和終點地址生成 Google Maps 導航 URL
    """
    try:
        service = GoogleMapsService(current_app.config['GOOGLE_MAPS_API_KEY'])
        result = service.get_navigation_url(
            start_address=query.start_address,
            end_address=query.end_address,
            mode=query.mode,
            avoid=query.avoid
        )
        return jsonify(result)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"獲取導航 URL 失敗: {str(e)}")
        return jsonify({'error': '服務器錯誤'}), 500

@googlemaps_bp.get(
    '/distance-matrix',
    tags=[googlemaps_tag],
    responses={"200": DistanceMatrixResponse, "400": ErrorResponse, "500": ErrorResponse}
)
def get_distance_matrix(query: DistanceMatrixQuery):
    """
    獲取距離矩陣
    
    計算多個起點到多個終點的距離和時間
    """
    try:
        service = GoogleMapsService(current_app.config['GOOGLE_MAPS_API_KEY'])
        result = service.get_distance_matrix(
            origins=query.origins,
            destinations=query.destinations,
            mode=query.mode
        )
        return jsonify(result)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"獲取距離矩陣失敗: {str(e)}")
        return jsonify({'error': '服務器錯誤'}), 500

@googlemaps_bp.get(
    '/geocode/reverse',
    tags=[googlemaps_tag],
    responses={"200": ReverseGeocodeResponse, "400": ErrorResponse, "500": ErrorResponse}
)
def reverse_geocode(query: ReverseGeocodeQuery):
    """
    將經緯度轉換為地址
    
    Args:
        query (ReverseGeocodeQuery): 包含經緯度的查詢參數
    
    Returns:
        200: 成功獲取地址
        400: 參數錯誤
        500: 服務器錯誤
    """
    try:
        service = GoogleMapsService(current_app.config['GOOGLE_MAPS_API_KEY'])
        result = service.reverse_geocode(
            latitude=query.latitude,
            longitude=query.longitude,
            language=query.language
        )
        return jsonify(result)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        logger.error(f"地理編碼失敗: {str(e)}")
        return jsonify({'error': '服務器錯誤'}), 500 