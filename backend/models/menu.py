from datetime import datetime
from models.database import db
import pytz

# 設定台灣時區
tw_tz = pytz.timezone('Asia/Taipei')

class Menu(db.Model):
    __tablename__ = 'menus'
    
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('menus.id'), nullable=True)
    name = db.Column(db.String(50), nullable=False)    # 選單名稱
    path = db.Column(db.String(255))                   # 路由路徑
    component = db.Column(db.String(255))              # 組件路徑
    icon = db.Column(db.String(50))                    # 圖標
    sort_order = db.Column(db.Integer, default=0)      # 排序
    is_hidden = db.Column(db.Boolean, default=False)   # 是否隱藏
    status = db.Column(db.String(20), default='active')# 狀態
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'parent_id': self.parent_id,
            'name': self.name,
            'path': self.path,
            'component': self.component,
            'icon': self.icon,
            'sort_order': self.sort_order,
            'is_hidden': self.is_hidden,
            'status': self.status,
            'created_at': self.created_at.replace(tzinfo=pytz.UTC).astimezone(tw_tz).strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None,
            'updated_at': self.updated_at.replace(tzinfo=pytz.UTC).astimezone(tw_tz).strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
        } 