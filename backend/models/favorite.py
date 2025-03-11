from models.database import db
from datetime import datetime
import pytz

tw_tz = pytz.timezone('Asia/Taipei')

class Favorite(db.Model):
    """最愛模型"""
    __tablename__ = 'favorites'
    __table_args__ = (
        db.Index('ix_favorite_created_at', 'created_at'),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
    store_name = db.Column(db.String(100), nullable=False)
    store_image = db.Column(db.String(255), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(50), nullable=True)
    city_CN = db.Column(db.String(50), nullable=True)
    customer_phone = db.Column(db.String(20), nullable=True)
    description = db.Column(db.Text, nullable=True)
    is_new_until = db.Column(db.String(100), nullable=True)
    redirection_url = db.Column(db.String(255), nullable=True)
    navigation_url = db.Column(db.String(500), nullable=True)
    rating = db.Column(db.Float, nullable=True, default=0)
    review_number = db.Column(db.Integer, nullable=True, default=0)
    username = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(tw_tz))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(tw_tz), onupdate=lambda: datetime.now(tw_tz))

    # 關聯
    user = db.relationship('User', backref='favorites')
    store = db.relationship('Store', backref='favorites')

    def to_dict(self):
        """轉換為字典"""
        # 檢查是否為 Row 對象（來自 with_entities 查詢）
        if hasattr(self, '_fields'):
            return {
                'id': self.id,
                'user_id': self.user_id,
                'store_id': self.store_id,
                'store_name': self.store_name,
                'store_image': self.store_image,
                'address': self.address,
                'city': self.city,
                'city_CN': self.city_CN,
                'customer_phone': self.customer_phone,
                'description': self.description,
                'is_new_until': self.is_new_until,
                'redirection_url': self.redirection_url,
                'navigation_url': self.navigation_url,
                'rating': self.rating,
                'review_number': self.review_number,
                'username': self.username,
                'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
            }
        # 一般對象
        return {
            'id': self.id,
            'user_id': self.user_id,
            'store_id': self.store_id,
            'store_name': self.store.name,
            'store_image': self.store.hero_image,
            'address': self.address,
            'city': self.city,
            'city_CN': self.city_CN,
            'customer_phone': self.customer_phone,
            'description': self.description,
            'is_new_until': self.is_new_until,
            'redirection_url': self.redirection_url,
            'navigation_url': self.navigation_url,
            'rating': self.rating,
            'review_number': self.review_number,
            'username': self.user.username,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        } 