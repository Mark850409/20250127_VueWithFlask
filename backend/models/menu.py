from datetime import datetime
from models.database import db
import pytz
from typing import Optional

# 設定台灣時區
tw_tz = pytz.timezone('Asia/Taipei')

class Menu(db.Model):
    __tablename__ = 'menus'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('menus.id'), nullable=True)
    name = db.Column(db.String(50), nullable=False, comment='選單名稱')
    path = db.Column(db.String(100), nullable=True, comment='路由路徑')
    icon = db.Column(db.String(50), nullable=True, comment='圖標名稱')
    category = db.Column(db.String(50), nullable=True, comment='選單類別')
    description = db.Column(db.String(200), nullable=True, comment='選單描述')
    sort_order = db.Column(db.Integer, default=0, comment='排序順序')
    status = db.Column(db.String(20), default='active', comment='狀態')
    created_at = db.Column(db.DateTime, default=datetime.now, comment='創建時間')
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='更新時間')

    # 關聯子選單
    children = db.relationship('Menu', 
                             backref=db.backref('parent', remote_side=[id]),
                             lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'parent_id': self.parent_id,
            'name': self.name,
            'path': self.path,
            'icon': self.icon,
            'category': self.category,
            'description': self.description,
            'sort_order': self.sort_order,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        }

    def update_sort_order(self, new_order: int):
        """更新排序值"""
        self.sort_order = new_order
        db.session.add(self)

    @classmethod
    def reorder_siblings(cls, category: str, parent_id: Optional[int] = None):
        """重新排序同級選單"""
        siblings = cls.query.filter_by(
            category=category,
            parent_id=parent_id
        ).order_by(cls.sort_order.asc()).all()
        
        for index, menu in enumerate(siblings):
            menu.sort_order = index
            db.session.add(menu) 