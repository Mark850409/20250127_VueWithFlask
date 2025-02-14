from models.database import db
from datetime import datetime
import pytz

tw_tz = pytz.timezone('Asia/Taipei')

class Folder(db.Model):
    """資料夾模型"""
    __tablename__ = 'langflows_folders'
    
    id = db.Column(db.Integer, primary_key=True)
    folder_id = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    parent_id = db.Column(db.String(100))
    status = db.Column(db.String(20), default='active')  # active, deleted
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(tw_tz))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(tw_tz), onupdate=lambda: datetime.now(tw_tz))

    def to_dict(self):
        """轉換為字典"""
        return {
            'id': self.id,
            'folder_id': self.folder_id,
            'name': self.name,
            'description': self.description,
            'parent_id': self.parent_id,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        } 