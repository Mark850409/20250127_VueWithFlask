from dao.banner_dao import BannerDAO
from schemas.banner_schema import (
    BannerSchema, BannerCreateBody, 
    BannerUpdateBody, BannerResponse, 
    BannerListResponse
)

class BannerService:
    def __init__(self):
        self.banner_dao = BannerDAO()

    def _convert_to_schema(self, banner) -> dict:
        """將 Banner 模型轉換為 schema 字典"""
        schema_fields = {
            'id': banner.id,
            'banner_type': banner.banner_type,
            'title': banner.title,
            'subtitle': banner.subtitle,
            'description': banner.description,
            'image_url': banner.image_url,
            'alt': banner.alt,
            'sort_order': banner.sort_order,
            'is_active': banner.is_active,
            'created_at': banner.created_at,
            'updated_at': banner.updated_at
        }
        return schema_fields

    def get_all_banners(self):
        banners = self.banner_dao.get_all_banners()
        banner_list = [
            BannerSchema.model_validate(self._convert_to_schema(banner))
            for banner in banners
        ]
        return BannerListResponse(data=banner_list).model_dump()

    def get_active_banners(self):
        banners = self.banner_dao.get_active_banners()
        banner_list = [
            BannerSchema.model_validate(self._convert_to_schema(banner))
            for banner in banners
        ]
        return BannerListResponse(data=banner_list).model_dump()

    def get_banner(self, banner_id):
        banner = self.banner_dao.get_banner_by_id(banner_id)
        if banner:
            return BannerResponse(
                data=BannerSchema.model_validate(self._convert_to_schema(banner))
            ).model_dump()
        return None

    def create_banner(self, banner_data: BannerCreateBody):
        # 先驗證並轉換輸入數據
        validated_data = banner_data.model_dump(exclude_unset=True)
        # 確保必要字段都存在
        if 'sort_order' not in validated_data:
            validated_data['sort_order'] = 0
        if 'is_active' not in validated_data:
            validated_data['is_active'] = True
        
        # 創建 banner
        banner = self.banner_dao.create_banner(validated_data)
        
        return BannerResponse(
            data=BannerSchema.model_validate(self._convert_to_schema(banner))
        ).model_dump()

    def update_banner(self, banner_id: int, banner_data: BannerUpdateBody):
        # 只更新非 None 的字段
        update_data = banner_data.model_dump(exclude_unset=True, exclude_none=True)
        banner = self.banner_dao.update_banner(banner_id, update_data)
        if banner:
            return BannerResponse(
                data=BannerSchema.model_validate(self._convert_to_schema(banner))
            ).model_dump()
        return None

    def delete_banner(self, banner_id: int):
        return self.banner_dao.delete_banner(banner_id)

    def get_banners_by_type(self, banner_type: str):
        """
        獲取指定類型的輪播圖
        只返回已啟用的輪播圖
        
        Args:
            banner_type: 輪播圖類型，可以是以下之一：
                - home: 首頁
                - feature: 特色功能
                - learning: 學習中心
                - pricing: 定價方案
                - food: 尋找美食
                - footer: 頁腳
                - login: 登入
                - admin: 後台
        """
        if banner_type == 'admin':
            # 如果是 admin，獲取所有包含 admin 的輪播圖
            banners = self.banner_dao.get_banners_by_pattern('admin%', active_only=True)
        else:
            # 其他類型維持原有邏輯
            banners = self.banner_dao.get_banners_by_type(banner_type, active_only=True)
        
        banner_list = [
            BannerSchema.model_validate(self._convert_to_schema(banner))
            for banner in banners
        ]
        return BannerListResponse(data=banner_list).model_dump()

    VALID_BANNER_TYPES = {
        'home',
        'feature', 
        'learning',
        'pricing',
        'food',
        'footer',
        'login',
        'forgot-password',
        'admin'
    } 