from models.banner import Banner
from models.database import db

class BannerDAO:
    @staticmethod
    def get_all_banners():
        return Banner.query.order_by(Banner.sort_order).all()
    
    @staticmethod
    def get_active_banners():
        return Banner.query.filter_by(is_active=True).order_by(Banner.sort_order).all()
    
    @staticmethod
    def get_banner_by_id(banner_id):
        return Banner.query.get(banner_id)
    
    @staticmethod
    def create_banner(banner_data):
        banner = Banner(**banner_data)
        db.session.add(banner)
        db.session.commit()
        return banner
    
    @staticmethod
    def update_banner(banner_id, banner_data):
        banner = Banner.query.get(banner_id)
        if banner:
            for key, value in banner_data.items():
                setattr(banner, key, value)
            db.session.commit()
        return banner
    
    @staticmethod
    def delete_banner(banner_id):
        banner = Banner.query.get(banner_id)
        if banner:
            db.session.delete(banner)
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def get_banners_by_type(banner_type: str, active_only: bool = True):
        query = Banner.query.filter_by(banner_type=banner_type)
        if active_only:
            query = query.filter_by(is_active=True)
        return query.order_by(Banner.sort_order).all()
    
    @staticmethod
    def get_banners_by_pattern(pattern: str, active_only: bool = False):
        """
        使用 LIKE 查詢獲取匹配模式的輪播圖
        
        Args:
            pattern: SQL LIKE 模式
            active_only: 是否只返回啟用的輪播圖
        """
        query = Banner.query.filter(Banner.banner_type.like(pattern))
        
        if active_only:
            query = query.filter(Banner.is_active == True)
            
        return query.order_by(Banner.sort_order).all() 