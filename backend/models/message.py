from . import db
from datetime import datetime
import pytz

tw_tz = pytz.timezone('Asia/Taipei')

class Message(db.Model):
    """留言板模型"""
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'), nullable=False)
    store_name = db.Column(db.String(100),  nullable=False)
    store_image = db.Column(db.String(255),  nullable=False)
    content = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')
    replies = db.Column(db.JSON, default=list)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(tw_tz))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(tw_tz), onupdate=lambda: datetime.now(tw_tz))
    
    # 關聯
    user = db.relationship('User', backref='messages')
    store = db.relationship('Store', backref='messages')
    
    def to_dict(self):
        """轉換為字典"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user': self.user.username if self.user else '已刪除用戶',
            'store_id': self.store_id,
            'store_name': self.store_name,
            'store_image': self.store_image,
            'content': self.content,
            'rating': self.rating,
            'status': self.status,
            'replies': self.replies or [],
            'created_at': self.created_at.replace(tzinfo=pytz.UTC).astimezone(tw_tz).strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.replace(tzinfo=pytz.UTC).astimezone(tw_tz).strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        } 