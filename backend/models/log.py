from datetime import datetime
from models.database import db
import pytz
from models.user import User

# 設定台灣時區
tw_tz = pytz.timezone('Asia/Taipei')

class Log(db.Model):
    __tablename__ = 'logs'
    __table_args__ = (
        db.Index('ix_log_created_at', 'created_at'),
    )
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # 改為可為空
    action = db.Column(db.String(50), nullable=False)  # 操作類型
    description = db.Column(db.Text, nullable=False)   # 操作描述
    ip_address = db.Column(db.String(50))             # IP地址
    status = db.Column(db.String(20))                 # 狀態
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(tw_tz))
    
    # 添加關聯
    user = db.relationship('User', backref='logs')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'username': self.user.username if self.user else None,
            'action': self.action,
            'description': self.description,
            'ip_address': self.ip_address,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        } 