from models.database import db
from datetime import datetime
import pytz

tw_tz = pytz.timezone('Asia/Taipei')

class Langflow(db.Model):
    """Langflow 模型"""
    __tablename__ = 'langflows_files_upload'
    
    id = db.Column(db.Integer, primary_key=True)
    flow_id = db.Column(db.String(100), nullable=False, unique=True)
    file_name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(20), default='active')  # active, deleted
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(tw_tz))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(tw_tz), onupdate=lambda: datetime.now(tw_tz))

    def to_dict(self):
        """轉換為字典"""
        return {
            'id': self.id,
            'flow_id': self.flow_id,
            'file_name': self.file_name,
            'file_path': self.file_path,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        } 