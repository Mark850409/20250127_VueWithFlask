from models.database import db
from datetime import datetime

class Bot(db.Model):
    __tablename__ = 'bots'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)  # 快速問答標題
    sort_order = db.Column(db.Integer, default=0)  # 排序順序
    icon = db.Column(db.String(100), nullable=True)  # 圖示
    is_active = db.Column(db.Boolean, default=True)
    is_default = db.Column(db.Boolean, default=False)  # 是否為預設訊息
    message = db.Column(db.Text, nullable=True)  # 預設訊息內容
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'sort_order': self.sort_order,
            'icon': self.icon,
            'is_active': self.is_active,
            'is_default': self.is_default,
            'message': self.message,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        } 