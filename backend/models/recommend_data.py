from models.database import db
from datetime import datetime

class RecommendData(db.Model):
    __tablename__ = 'recommend_data'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float, default=0)
    distance = db.Column(db.Float, default=0)
    review_number = db.Column(db.Integer, default=0)
    sentiment_score = db.Column(db.Float, default=0)
    weighted_score = db.Column(db.Float, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'rating': self.rating,
            'distance': self.distance,
            'review_number': self.review_number,
            'sentiment_score': self.sentiment_score,
            'weighted_score': self.weighted_score,
            'created_at': self.created_at
        } 