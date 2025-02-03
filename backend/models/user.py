from datetime import datetime
from models.database import db
import pytz

# 設定台灣時區
tw_tz = pytz.timezone('Asia/Taipei')

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    avatar = db.Column(db.String(255))
    status = db.Column(db.String(20), default='Enabled')  # Enabled/Disabled
    register_time = db.Column(db.DateTime, default=datetime.utcnow)
    update_time = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'avatar': self.avatar,
            'status': self.status,
            'register_time': self.register_time.replace(tzinfo=pytz.UTC).astimezone(tw_tz).strftime('%Y-%m-%d %H:%M:%S') if self.register_time else None,
            'update_time': self.update_time.replace(tzinfo=pytz.UTC).astimezone(tw_tz).strftime('%Y-%m-%d %H:%M:%S') if self.update_time else None
        } 