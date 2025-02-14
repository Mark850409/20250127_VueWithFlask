from models.database import db
from datetime import datetime
import pytz

tw_tz = pytz.timezone('Asia/Taipei')

class LangflowMonitor(db.Model):
    """Langflow 監控模型"""
    __tablename__ = 'langflows_moniter'
    
    id = db.Column(db.Integer, primary_key=True)
    flow_id = db.Column(db.String(100), nullable=False)
    session_id = db.Column(db.String(100), nullable=False)
    sender = db.Column(db.String(50), nullable=False)  # user, assistant
    sender_name = db.Column(db.String(100))
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(tw_tz))

    def to_dict(self):
        """轉換為字典"""
        return {
            'id': self.id,
            'flow_id': self.flow_id,
            'session_id': self.session_id,
            'sender': self.sender,
            'sender_name': self.sender_name,
            'message': self.message,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        } 